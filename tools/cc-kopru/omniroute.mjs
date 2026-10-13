// OMNIROUTE-1 (Ömer 13 Eki): haftalık plan limiti dolunca köprü ajanı yerel OmniRoute ile koşar.
// Saf işlevler; sunucu.mjs ajan aracı kullanır. Anahtar değeri döndürülür ama hiçbir yere yazılmaz.
import fs from "node:fs";

export const OMNI_URL = "http://127.0.0.1:20128";
export const OMNI_COMBO = "cc-yedek-dis"; // EK 06:21: Claude-dışı (openrouter gpt-6.1-sol > grok-4.7 > gemini-3.8-flash); eski cc-yedek Claude içeriyor, CLI silemiyor
export const OMNI_BAYRAK = "C:/Projeler/omer-skills/.kos/kopru/omniroute.ac";
export const SIRA = "C:/Projeler/omer-skills/.kos/kopru/SIRA.md";
// DEVAM-KURALI kalite kapısı; Claude dışı model DEVAM-KURALI'nı okumadan da görsün diye isteme eklenir.
export const OMNI_ISTEM = "[KOPRU_OMNIROUTE=1] Haftalık plan limiti: bu oturum OmniRoute ile koşuyor. Onay betiği `uygula`, "
  + "KABUL/kalite kararı ve ölçüm tabanı yazımı YOK — yalnız araştırma/indirme/etiketleme/taslak.";
const AYLAR = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"];

/** CC plan limiti metni → "haftalik" | "5saat" | null. Şablon (claude.exe 2.1.295): "You've hit your ${ad} · resets …";
 *  ad: five_hour "session limit", seven_day "weekly limit", seven_day_{opus,sonnet} "Opus/Sonnet limit", overage dahil "Fable limit".
 *  "You've used 90% of your …" uyarıdır, limit değil. Tür bilinmeyen "usage limit" 5 saatlik sayılır (geçiş yok, bekle). */
export function limitTuru(metin) {
  const s = String(metin || "");
  if (/You've hit your (weekly|Opus|Sonnet|Fable) limit/i.test(s)) return "haftalik";
  if (/You've hit your (session|usage) limit/i.test(s)) return "5saat";
  return null;
}

/** "resets 5am" / "resets Oct 14, 5am" / "resets Jan 2, 2027, 5:30pm" → Date (yerel saat); bulunamazsa null. */
export function sifirlanma(metin, simdi = new Date()) {
  const m = /resets\s+(?:([A-Za-z]{3})[a-z]*\s+(\d{1,2})(?:,\s*(\d{4}))?,?\s+)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)/i.exec(String(metin || ""));
  if (!m) return null;
  const saat = (Number(m[4]) % 12) + (m[6].toLowerCase() === "pm" ? 12 : 0);
  const t = new Date(simdi);
  t.setHours(saat, Number(m[5] || 0), 0, 0);
  if (m[1]) {
    const ay = AYLAR.indexOf(m[1].toLowerCase());
    if (ay < 0) return null;
    t.setMonth(ay, Number(m[2]));
    if (m[3]) t.setFullYear(Number(m[3]));
    else if (t <= simdi) t.setFullYear(t.getFullYear() + 1);
  } else if (t <= simdi) t.setDate(t.getDate() + 1);
  return t;
}

/** Bayrak var mı; içindeki bitiş geçtiyse bayrak silinir (plana dönüş). Bitişsiz (elle açılmış) bayrak kalıcıdır. */
export function omniAktif(yol = OMNI_BAYRAK, simdi = new Date()) {
  if (!fs.existsSync(yol)) return false;
  const b = /bitis:\s*(\S+)/.exec(fs.readFileSync(yol, "utf8"));
  if (b && Date.parse(b[1]) <= simdi.getTime()) { fs.rmSync(yol, { force: true }); return false; }
  return true;
}

// ponytail: sıfırlanma okunamazsa 6 saat; yanlışsa sonraki haftalık-limit yanıtı bayrağı yeniden açar (bir boşa çağrı).
export function bayrakYaz(yol = OMNI_BAYRAK, bitis = null, simdi = new Date()) {
  const b = bitis || new Date(simdi.getTime() + 6 * 3600e3);
  fs.writeFileSync(yol, `KÖPRÜ haftalık plan limiti ${simdi.toISOString()}\nbitis: ${b.toISOString()}\n`);
}

export function siraEkle(satir, yol = SIRA) {
  fs.appendFileSync(yol, `- ${satir}\n`);
}

/** Ajan çocuğunun env'i + ek argv. api-kredi kazanır (yalnız Ömer açar); omni yalnız tek başına uygulanır.
 *  d2 kök neden: ~/.claude/settings.json env.ANTHROPIC_BASE_URL (headroom vekili) süreç env'ini ezer → istek OmniRoute'a
 *  hiç gitmiyordu ("Not logged in"). --settings kullanıcı ayarının üstündedir (CC settings belgesi); anahtar argv'ye girmez. */
export function ajanOrtami(taban, { apiKredi, omni, oku }) {
  if (apiKredi) {
    const anahtar = oku("ANTHROPIC_API_KEY_AJAN");
    return anahtar ? { env: { ...taban, ANTHROPIC_API_KEY: anahtar }, sir: anahtar, arg: [] } : { env: taban, arg: [] };
  }
  if (!omni) return { env: taban, arg: [] };
  const anahtar = oku("OMNIROUTE_KEY");
  if (!anahtar) return { env: taban, eksik: "OMNIROUTE_KEY", arg: [] };
  // EK 06:21: Claude abonelik kimliği OmniRoute'a gitmez → OAuth env'i de çıkar (AUTH_TOKEN zaten önce gelir).
  const { ANTHROPIC_API_KEY: _at, CLAUDE_CODE_OAUTH_TOKEN: _ot, ...env } = taban;
  return {
    arg: ["--settings", JSON.stringify({ env: { ANTHROPIC_BASE_URL: OMNI_URL } })],
    env: {
      ...env,
      ANTHROPIC_BASE_URL: OMNI_URL,
      ANTHROPIC_AUTH_TOKEN: anahtar,
      ANTHROPIC_DEFAULT_OPUS_MODEL: OMNI_COMBO,
      ANTHROPIC_DEFAULT_SONNET_MODEL: OMNI_COMBO,
      ANTHROPIC_DEFAULT_HAIKU_MODEL: OMNI_COMBO,
      KOPRU_OMNIROUTE: "1",
    },
    sir: anahtar,
  };
}
