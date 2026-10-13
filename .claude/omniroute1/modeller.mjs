// OMNIROUTE-2: OmniRoute'taki ücretsiz modeller + sağlayıcı anahtarlarının VARLIĞI (değer basılmaz).
import { kullaniciEnv } from "../../tools/cc-kopru/kos.mjs";
const oku = (ad) => process.env[ad] || kullaniciEnv(ad);
const r = await fetch("http://127.0.0.1:20128/v1/models", { headers: { authorization: `Bearer ${oku("OMNIROUTE_KEY")}` } });
const ids = ((await r.json()).data || []).map((m) => m.id);
console.log(r.status, ids.length, ids.filter((i) => /free|cc-yedek/i.test(i)).slice(0, 25).join(" "));
for (const o of ["GEMINI_API_KEY", "GROQ_API_KEY", "OPENROUTER_API_KEY"]) console.log(o, !!oku(o));
