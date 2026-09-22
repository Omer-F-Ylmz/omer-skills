import { APIConnectionError, APIError, APITimeoutError, APIUserAbortError, TypeSafeClient } from "@typesafe-ai/sdk";

// Sınırlar docs.typesafe.ai/api ve /models'tan (Jev 1.13).
export const MODELLER = ["jev-latest", "jev-1.13"] as const;
const SECENEK_UST = 255;
const SEVIYE_ALT = 2;
const SEVIYE_UST = 10;
const TOPLAM_TOKEN = 64_000;
const STATE_ARTI_SORU_TOKEN = 32_000;
const CAGRI_MS = 30_000;
export const TOPLU_UST = 200;
const ESZAMANLI = 8;

export type Tip = "noul" | "choice" | "score";
export type Soru = { type: Tip; instructions: unknown; criteria?: unknown };
export type State = string | Record<string, unknown> | unknown[];
type Env = Record<string, string | undefined>;
export type Bagimlilik = { env?: Env; fetch?: typeof globalThis.fetch; retry?: Record<string, number> };

export class JevHata extends Error {
  constructor(public error_type: string, message: string, public status?: number) {
    super(message);
  }
  toJSON() {
    return { error_type: this.error_type, message: this.message, ...(this.status ? { status: this.status } : {}) };
  }
}

export function backendSec(env: Env = process.env) {
  if (env.TYPESAFE_API_KEY) return { ad: "TYPESAFE", baseURL: "https://api.typesafe.ai", apiKey: env.TYPESAFE_API_KEY };
  if (env.OPENROUTER_API_KEY) return { ad: "OPENROUTER", baseURL: "https://openrouter.ai/api", apiKey: env.OPENROUTER_API_KEY };
  throw new JevHata("no_key", "TYPESAFE_API_KEY ya da OPENROUTER_API_KEY ortamda yok");
}

export const modeller = () => [
  { id: "jev-latest", openrouter: "~typesafe/jev-latest", not: "en yeni Jev (alias)" },
  { id: "jev-1.13", openrouter: "typesafe/jev-1.13", not: "sabit sürüm" },
];

// ponytail: tokenizer yok, UTF-8 bayt/4 kaba tahmin; kesin sınır sunucunun 422'si.
const token = (x: unknown) => Math.ceil(Buffer.byteLength(typeof x === "string" ? x : JSON.stringify(x) ?? "") / 4);
const bos = (x: unknown) => x == null || x === "" || (typeof x === "object" && Object.keys(x as object).length === 0);
const gecersiz = (m: string) => new JevHata("validation", m);

export function dogrula(state: State, questions: Record<string, Soru>) {
  const adlar = Object.keys(questions ?? {});
  if (adlar.length === 0) throw gecersiz("questions boş");
  for (const ad of adlar) {
    const q = questions[ad];
    if (bos(q?.instructions)) throw gecersiz(`${ad}: instructions zorunlu`);
    if (q.type === "noul") {
      if (q.criteria != null && Object.keys(q.criteria as object).some((k) => k !== "true" && k !== "false"))
        throw gecersiz(`${ad}: noul criteria yalnız true/false`);
    } else if (q.type === "choice") {
      if (q.criteria == null || typeof q.criteria !== "object" || Array.isArray(q.criteria)) throw gecersiz(`${ad}: choice criteria seçenek haritası olmalı`);
      const n = Object.keys(q.criteria).length;
      if (n < 1 || n > SECENEK_UST) throw gecersiz(`${ad}: choice 1-${SECENEK_UST} seçenek (gelen ${n})`);
    } else if (q.type === "score") {
      if (!Array.isArray(q.criteria) || q.criteria.length < SEVIYE_ALT || q.criteria.length > SEVIYE_UST)
        throw gecersiz(`${ad}: score criteria ${SEVIYE_ALT}-${SEVIYE_UST} seviyelik dizi olmalı`);
    } else throw gecersiz(`${ad}: type noul|choice|score olmalı`);
  }
  const s = token(state);
  const sorular = adlar.map((a) => token(questions[a]));
  if (s + Math.max(...sorular) > STATE_ARTI_SORU_TOKEN)
    throw new JevHata("context_length", `state + en uzun soru ~${s + Math.max(...sorular)} token > ${STATE_ARTI_SORU_TOKEN}`);
  const toplam = s + sorular.reduce((a, b) => a + b, 0);
  if (toplam > TOPLAM_TOKEN) throw new JevHata("context_length", `toplam ~${toplam} token > ${TOPLAM_TOKEN}`);
}

function modelSec(model?: string) {
  const m = model ?? "jev-latest";
  if (!(MODELLER as readonly string[]).includes(m)) throw new JevHata("invalid_model", `model yalnız ${MODELLER.join(" | ")}`);
  return m;
}

const TUR: Record<number, string> = { 400: "bad_request", 401: "auth", 403: "permission", 404: "not_found", 408: "timeout", 422: "validation", 429: "rate_limit", 529: "overloaded" };

// Hata metnine yalnız sağlayıcının message/error_type'ı girer; gövdenin geri kalanı (girdi yankısı) ve başlıklar asla.
function cevir(e: unknown, apiKey: string): JevHata {
  if (e instanceof JevHata) return e;
  if (e instanceof APITimeoutError || e instanceof APIUserAbortError) return new JevHata("timeout", `çağrı ${CAGRI_MS / 1000} sn içinde bitmedi`);
  if (e instanceof APIConnectionError) return new JevHata("connection", "sağlayıcıya bağlanılamadı");
  if (e instanceof APIError) {
    const b = (e.body ?? {}) as Record<string, unknown>;
    const ic = (b.error ?? {}) as Record<string, unknown>;
    const ham = [b.message, ic.message, typeof b.detail === "string" ? b.detail : undefined, typeof b.error === "string" ? b.error : undefined].find((x) => typeof x === "string") as string | undefined;
    const tur = [b.error_type, ic.type, ic.code].find((x) => typeof x === "string") as string | undefined;
    const temiz = (ham ?? "").split(apiKey).join("***").replace(/bearer\s+\S+/gi, "***").slice(0, 300);
    return new JevHata(tur ?? TUR[e.status] ?? (e.status >= 500 ? "server" : "api"), `sağlayıcı ${e.status}${temiz ? `: ${temiz}` : ""}`, e.status);
  }
  return new JevHata("internal", "beklenmeyen hata");
}

function istemci(d: Bagimlilik) {
  const b = backendSec(d.env);
  const client = new TypeSafeClient({
    apiKey: b.apiKey,
    baseURL: b.baseURL,
    logLevel: "off",
    timeout: CAGRI_MS,
    retry: { maxRetries: 2, respectRetryAfter: true, maxRetryAfterMs: CAGRI_MS, ...d.retry },
    ...(d.fetch ? { fetch: d.fetch } : {}),
  });
  return { client, apiKey: b.apiKey };
}

type Istek = { state: State; questions: Record<string, Soru>; model?: string };

async function cagir(c: ReturnType<typeof istemci>, state: State, questions: Record<string, Soru>, model: string) {
  const t0 = performance.now();
  try {
    dogrula(state, questions);
    const r = (await c.client.systemOne({ model, state, questions } as never, { signal: AbortSignal.timeout(CAGRI_MS) })) as unknown as {
      model: string;
      answers: Record<string, unknown>;
      usage: Record<string, number>;
    };
    return { answers: r.answers, usage: r.usage, model: r.model, sure_ms: Math.round(performance.now() - t0) };
  } catch (e) {
    throw cevir(e, c.apiKey);
  }
}

export async function degerlendir({ state, questions, model }: Istek, d: Bagimlilik = {}) {
  const m = modelSec(model);
  return cagir(istemci(d), state, questions, m);
}

export async function toplu({ states, questions, model }: { states: State[]; questions: Record<string, Soru>; model?: string }, d: Bagimlilik = {}) {
  const m = modelSec(model);
  if (!Array.isArray(states) || states.length === 0 || states.length > TOPLU_UST) throw gecersiz(`states 1-${TOPLU_UST} öğe olmalı`);
  dogrula("", questions);
  const c = istemci(d);
  const sonuc: unknown[] = new Array(states.length);
  let sira = 0;
  const isci = async () => {
    for (let i = sira++; i < states.length; i = sira++) {
      try {
        sonuc[i] = { index: i, ok: true, ...(await cagir(c, states[i], questions, m)) };
      } catch (e) {
        sonuc[i] = { index: i, ok: false, error: (e as JevHata).toJSON() };
      }
    }
  };
  await Promise.all(Array.from({ length: Math.min(ESZAMANLI, states.length) }, isci));
  return sonuc as ({ index: number; ok: true } | { index: number; ok: false; error: ReturnType<JevHata["toJSON"]> })[];
}
