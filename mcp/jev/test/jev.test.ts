import { afterEach, describe, expect, it, vi } from "vitest";
import { backendSec, degerlendir, dogrula, JevHata, modeller, toplu } from "../src/jev.js";

const ANAHTAR = "sk-or-v1-GIZLI0123456789abcdef";
const OR = { OPENROUTER_API_KEY: ANAHTAR };
const HIZLI = { backoffInitialMs: 1, backoffMaxMs: 2 };
const noulSoru = { acil: { type: "noul" as const, instructions: "Is this urgent?" } };
const tamam = { model: "typesafe/jev-1.13-20260917", answers: { acil: { type: "noul", noul: 0.9 } }, usage: { input_tokens: 10, output_tokens: 20 } };

const json = (govde: unknown, status = 200, baslik: Record<string, string> = {}) =>
  new Response(JSON.stringify(govde), { status, headers: { "content-type": "application/json", ...baslik } });

function sahte(...yanitlar: Response[]) {
  const cagrilar: { url: string; init: RequestInit }[] = [];
  const fetch = vi.fn(async (url: string | URL | Request, init?: RequestInit) => {
    cagrilar.push({ url: String(url), init: init ?? {} });
    return yanitlar.length > 1 ? yanitlar.shift()! : yanitlar[0].clone();
  });
  return { fetch: fetch as unknown as typeof globalThis.fetch, cagrilar };
}

async function hataAl(p: Promise<unknown>): Promise<JevHata> {
  try {
    await p;
  } catch (e) {
    return e as JevHata;
  }
  throw new Error("hata bekleniyordu");
}

describe("backend", () => {
  it("OpenRouter", () => expect(backendSec(OR).baseURL).toBe("https://openrouter.ai/api"));
  it("TypeSafe", () => expect(backendSec({ TYPESAFE_API_KEY: "x" }).baseURL).toBe("https://api.typesafe.ai"));
  it("ikisi de varsa TypeSafe", () => expect(backendSec({ TYPESAFE_API_KEY: "x", ...OR }).ad).toBe("TYPESAFE"));
  it("anahtar yoksa tipli hata", () => expect(() => backendSec({})).toThrow(JevHata));
  it("istek /v1/systemone'a Bearer ile gider", async () => {
    const s = sahte(json(tamam));
    await degerlendir({ state: "x", questions: noulSoru }, { env: OR, fetch: s.fetch });
    expect(s.cagrilar[0].url).toBe("https://openrouter.ai/api/v1/systemone");
    expect(new Headers(s.cagrilar[0].init.headers).get("authorization")).toBe(`Bearer ${ANAHTAR}`);
  });
});

describe("dogrulama (istek gitmez)", () => {
  const bos = sahte(json(tamam));
  const reddet = async (args: Parameters<typeof degerlendir>[0], tur: string) => {
    const h = await hataAl(degerlendir(args, { env: OR, fetch: bos.fetch }));
    expect(h).toBeInstanceOf(JevHata);
    expect(h.error_type).toBe(tur);
  };
  afterEach(() => expect(bos.fetch).not.toHaveBeenCalled());

  it("instructions zorunlu", () => reddet({ state: "x", questions: { a: { type: "noul", instructions: "" } } }, "validation"));
  it("bilinmeyen tip", () => reddet({ state: "x", questions: { a: { type: "yesno", instructions: "q" } as never } }, "validation"));
  it("soru yok", () => reddet({ state: "x", questions: {} }, "validation"));
  it("choice 256 secenek", () =>
    reddet({ state: "x", questions: { a: { type: "choice", instructions: "q", criteria: Object.fromEntries(Array.from({ length: 256 }, (_, i) => [`o${i}`, null])) } } }, "validation"));
  it("choice criteria yok", () => reddet({ state: "x", questions: { a: { type: "choice", instructions: "q" } } }, "validation"));
  it("score 1 seviye", () => reddet({ state: "x", questions: { a: { type: "score", instructions: "q", criteria: ["a"] } } }, "validation"));
  it("score 11 seviye", () => reddet({ state: "x", questions: { a: { type: "score", instructions: "q", criteria: Array.from({ length: 11 }, (_, i) => `l${i}`) } } }, "validation"));
  it("state+en uzun soru 32k asimi", () => reddet({ state: "a".repeat(130_000), questions: noulSoru }, "context_length"));
  it("toplam 64k asimi", () =>
    reddet({ state: "s", questions: Object.fromEntries(Array.from({ length: 3 }, (_, i) => [`q${i}`, { type: "noul" as const, instructions: "b".repeat(100_000) }])) }, "context_length"));
  it("model yalniz jev-latest/jev-1.13", () => reddet({ state: "x", questions: noulSoru, model: "gpt-4o" }, "invalid_model"));
  it("gecerli choice/score sinirlari gecer", () => {
    expect(() => dogrula("x", { a: { type: "choice", instructions: "q", criteria: Object.fromEntries(Array.from({ length: 255 }, (_, i) => [`o${i}`, null])) } })).not.toThrow();
    expect(() => dogrula("x", { a: { type: "score", instructions: "q", criteria: ["a", "b"] } })).not.toThrow();
  });
});

describe("model", () => {
  it("varsayilan jev-latest, cozulen model ve sure doner", async () => {
    const s = sahte(json(tamam));
    const r = await degerlendir({ state: "x", questions: noulSoru }, { env: OR, fetch: s.fetch });
    expect(JSON.parse(String(s.cagrilar[0].init.body)).model).toBe("jev-latest");
    expect(r.model).toBe("typesafe/jev-1.13-20260917");
    expect(r.usage.input_tokens).toBe(10);
    expect(r.answers.acil).toEqual({ type: "noul", noul: 0.9 });
    expect(typeof r.sure_ms).toBe("number");
  });
  it("jev-1.13 ciplak ad gider (OpenRouter eslemesi sunucuda)", async () => {
    const s = sahte(json(tamam));
    await degerlendir({ state: "x", questions: noulSoru, model: "jev-1.13" }, { env: OR, fetch: s.fetch });
    expect(JSON.parse(String(s.cagrilar[0].init.body)).model).toBe("jev-1.13");
  });
  it("jev_models sabit liste + OpenRouter eslemesi", () =>
    expect(modeller().map((m) => [m.id, m.openrouter])).toEqual([["jev-latest", "~typesafe/jev-latest"], ["jev-1.13", "typesafe/jev-1.13"]]));
});

describe("retry ve hatalar", () => {
  it("429 retry-after sonra basari", async () => {
    const s = sahte(json({ message: "slow down" }, 429, { "retry-after": "0" }), json(tamam));
    const r = await degerlendir({ state: "x", questions: noulSoru }, { env: OR, fetch: s.fetch, retry: HIZLI });
    expect(s.cagrilar.length).toBe(2);
    expect(r.answers.acil).toBeDefined();
  });
  it("529 en fazla 2 tekrar", async () => {
    const s = sahte(json({ message: "overloaded", error_type: "overloaded" }, 529));
    const h = await hataAl(degerlendir({ state: "x", questions: noulSoru }, { env: OR, fetch: s.fetch, retry: HIZLI }));
    expect(s.cagrilar.length).toBe(3);
    expect(h.error_type).toBe("overloaded");
    expect(h.status).toBe(529);
  });
  it("401 tekrar yok, tipli", async () => {
    const s = sahte(json({ message: `bad key ${ANAHTAR}` }, 401));
    const h = await hataAl(degerlendir({ state: "x", questions: noulSoru }, { env: OR, fetch: s.fetch, retry: HIZLI }));
    expect(s.cagrilar.length).toBe(1);
    expect(h.error_type).toBe("auth");
    expect(h.message).not.toContain(ANAHTAR);
    expect(h.message).not.toMatch(/bearer/i);
  });
  it("saglayici {message, error_type} okunur, girdi yankisi dusurulur", async () => {
    const s = sahte(json({ message: "questions.a.criteria invalid", error_type: "invalid_request", input: "GIZLI-GOVDE" }, 422));
    const h = await hataAl(degerlendir({ state: "GIZLI-GOVDE", questions: noulSoru }, { env: OR, fetch: s.fetch, retry: HIZLI }));
    expect(h.error_type).toBe("invalid_request");
    expect(h.message).toContain("questions.a.criteria invalid");
    expect(h.message).not.toContain("GIZLI-GOVDE");
  });
});

describe("toplu", () => {
  it("200 tavani", async () => {
    const h = await hataAl(toplu({ states: Array(201).fill("x"), questions: noulSoru }, { env: OR, fetch: sahte(json(tamam)).fetch }));
    expect(h.error_type).toBe("validation");
  });
  it("esz. en fazla 8, satir basina sonuc ya da hata", async () => {
    let aktif = 0;
    let tepe = 0;
    const fetch = (async (_u: unknown, init?: RequestInit) => {
      aktif++;
      tepe = Math.max(tepe, aktif);
      await new Promise((r) => setTimeout(r, 5));
      aktif--;
      const st = JSON.parse(String(init!.body)).state;
      return st === "kotu" ? json({ message: "bad" }, 400) : json(tamam);
    }) as typeof globalThis.fetch;
    const states = Array.from({ length: 20 }, (_, i) => (i === 3 ? "kotu" : `s${i}`));
    const r = await toplu({ states, questions: noulSoru }, { env: OR, fetch, retry: HIZLI });
    expect(tepe).toBeLessThanOrEqual(8);
    expect(r.length).toBe(20);
    expect(r[3]).toMatchObject({ index: 3, ok: false, error: { status: 400 } });
    expect(r[4]).toMatchObject({ index: 4, ok: true });
  });
});

describe("log yasagi", () => {
  it("govde ve anahtar hicbir cikisa yazilmaz (TYPESAFE_LOG_LEVEL=debug olsa bile)", async () => {
    const yakalanan: string[] = [];
    const yaz = (...a: unknown[]) => void yakalanan.push(a.map((x) => (typeof x === "string" ? x : JSON.stringify(x))).join(" "));
    const casuslar = (["log", "info", "warn", "error", "debug"] as const).map((m) => vi.spyOn(console, m).mockImplementation(yaz));
    const out = vi.spyOn(process.stdout, "write").mockImplementation((c) => (yaz(String(c)), true));
    const err = vi.spyOn(process.stderr, "write").mockImplementation((c) => (yaz(String(c)), true));
    process.env.TYPESAFE_LOG_LEVEL = "debug";
    try {
      await degerlendir({ state: "GIZLI-DURUM", questions: noulSoru }, { env: OR, fetch: sahte(json({ ...tamam, echo: "GIZLI-YANIT" })).fetch });
      await hataAl(degerlendir({ state: "GIZLI-DURUM", questions: noulSoru }, { env: OR, fetch: sahte(json({ message: "x" }, 500)).fetch, retry: HIZLI }));
    } finally {
      delete process.env.TYPESAFE_LOG_LEVEL;
      [...casuslar, out, err].forEach((c) => c.mockRestore());
    }
    const hepsi = yakalanan.join("\n");
    expect(hepsi).not.toContain("GIZLI-DURUM");
    expect(hepsi).not.toContain("GIZLI-YANIT");
    expect(hepsi).not.toContain(ANAHTAR);
  });
});
