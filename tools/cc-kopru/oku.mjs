/**
 * KURULUM-11m-A K3 — köprünün `oku` aracı.
 *
 * claude-mem'in smart_* araçları bu kurulumda ÇALIŞMIYOR (CC'de de): tree-sitter CLI
 * PATH'te yok, `tree-sitter-cli` MODULE_NOT_FOUND, `~/.claude-mem/tree-sitter-libs`
 * hiç üretilmemiş — smart_search 170 dosyada 0 sembol, smart_outline/unfold
 * "Could not parse" veriyor. Onarım tree-sitter-cli + gramerler + C derleyici demek;
 * ayrı karar. Kaynak olarak projenin zaten ürettiği `graphify-out/graph.json` kullanılır.
 *
 * Düğümde `source_file` (köke göreli, / ayraçlı) ve `source_location` ("L44") var;
 * BİTİŞ satırı yok — sembol bir sonraki kardeşin başına kadar okunur.
 */
import fs from "node:fs";
import path from "node:path";

import { LOG_DIZIN, denyListesi, okumaDeny } from "./kos.mjs";

/** `aralik` tek çağrıda en fazla bu kadar satır döner. */
export const ARALIK_TAVAN = 400;

export const grafYolu = (kok) => path.join(kok, "graphify-out", "graph.json");

/**
 * Köprünün kendi log dizini `oku` için SALT-OKUMA kök: `kos()` tam çıktıyı oraya
 * yazıyor ama Temp izinli köklerin dışında, Desktop logu hiç açamıyordu (11m-A-FIX K3).
 * Çağıran yalnız mod=aralik'e izin verir; Read deny kapısı yine dosyaAc'ta çalışır.
 * @returns {string|null} LOG_DIZIN (yol onun altındaysa) ya da null
 */
export function logKoku(yol) {
  const k = path.resolve(LOG_DIZIN);
  const y = path.resolve(String(yol ?? ""));
  return y === k || y.startsWith(k + path.sep) ? k : null;
}

/** @returns {{id:string,ad:string,satir:number}[]} dosyanın düğümleri, satıra göre sıralı */
export function dosyaDugumleri(graf, gorelYol) {
  const hedef = gorelYol.toLowerCase();
  return (graf.nodes || [])
    .filter((n) => String(n.source_file || "").replace(/\\/g, "/").toLowerCase() === hedef)
    .map((n) => ({
      id: n.id,
      ad: String(n.label || n.id || "").replace(/\(\)$/, ""),
      satir: Number(String(n.source_location || "").replace(/^L/i, "")) || 0,
    }))
    .filter((n) => n.satir > 0)
    .sort((a, b) => a.satir - b.satir || a.ad.localeCompare(b.ad));
}

/**
 * Yol çözümü + Read deny kapısı. Kapı HER modda, dosya okunmadan önce çalışır.
 * @returns {{tam:string, gorel:string, satirlar:string[]}}
 */
export function dosyaAc(kok, dosya, deny = denyListesi()) {
  const tam = path.resolve(kok, dosya);
  okumaDeny(tam, deny, kok);
  if (!fs.existsSync(tam) || !fs.statSync(tam).isFile()) throw new Error(`dosya yok: ${dosya}`);
  return {
    tam,
    gorel: path.relative(kok, tam).replace(/\\/g, "/"),
    satirlar: fs.readFileSync(tam, "utf8").split(/\r?\n/),
  };
}

/**
 * Grafı yükler ve tazeliğini denetler. Dosya graftan yeniyse tahmin YAPILMAZ.
 * @returns {{nodes:object[]}}
 */
export function grafYukle(kok, dosyaTam) {
  const g = grafYolu(kok);
  if (!fs.existsSync(g)) {
    throw new Error(`graphify-out yok: ${g} — bu modu kullanmak için önce \`graphify .\` koşun `
      + "(ya da satır aralığı için mod=aralik kullanın)");
  }
  if (fs.statSync(dosyaTam).mtimeMs > fs.statSync(g).mtimeMs) {
    throw new Error("graph eski — graphify update .");
  }
  return JSON.parse(fs.readFileSync(g, "utf8"));
}

/** Dosyanın sembol iskeleti: ad + satır, gövde yok. */
export function iskelet(kok, dosya, deny) {
  const d = dosyaAc(kok, dosya, deny);
  const dugumler = dosyaDugumleri(grafYukle(kok, d.tam), d.gorel);
  if (!dugumler.length) return `${d.gorel} · ${d.satirlar.length} satır\n(grafta bu dosyanın sembolü yok)`;
  return `${d.gorel} · ${d.satirlar.length} satır · ${dugumler.length} sembol\n`
    + dugumler.map((n) => `L${n.satir}\t${n.ad}`).join("\n");
}

/** Tek sembolün satırları: kendi satırından bir sonraki kardeşin başına kadar. */
export function sembol(kok, dosya, ad, deny) {
  const d = dosyaAc(kok, dosya, deny);
  const dugumler = dosyaDugumleri(grafYukle(kok, d.tam), d.gorel);
  const aranan = String(ad).replace(/\(\)$/, "").toLowerCase();
  const i = dugumler.findIndex((n) => n.ad.toLowerCase() === aranan);
  if (i < 0) {
    return `'${ad}' ${d.gorel} içinde yok. Bilinen semboller: `
      + (dugumler.map((n) => n.ad).join(", ") || "(yok)");
  }
  const bas = dugumler[i].satir;
  // Bitiş satırı grafta yok: bir sonraki kardeşin başlangıcı sınırdır, son sembolde EOF.
  const bit = i + 1 < dugumler.length
    ? yorumsuzBitis(d.satirlar, bas, dugumler[i + 1].satir - 1)
    : d.satirlar.length;
  return govde(d, bas, bit, `${d.gorel} · ${dugumler[i].ad}`);
}

/**
 * Kardeşin doc-yorumu sembolün gövdesine sayılmasın (11m-A-FIX K4): bitişten geriye
 * boş satır, `//` satırı ve `/* *` bloğu atılır. Son sembolde çağrılmaz, EOF aynı kalır.
 */
function yorumsuzBitis(satirlar, bas, bit) {
  let b = bit;
  while (b > bas) {
    const s = String(satirlar[b - 1]).trim();
    if (!s || s.startsWith("//")) { b -= 1; continue; }
    if (s.endsWith("*/")) {
      let a = b;
      while (a > bas && !String(satirlar[a - 1]).trim().startsWith("/*")) a -= 1;
      if (String(satirlar[a - 1]).trim().startsWith("/*")) { b = a - 1; continue; }
    }
    break;
  }
  return b;
}

/** Grafsız satır aralığı. Tavan ARALIK_TAVAN satır. */
export function aralik(kok, dosya, bas, bit, deny) {
  const d = dosyaAc(kok, dosya, deny);
  const b = Math.max(1, Number(bas) || 1);
  const s = Math.min(Number(bit) || b + ARALIK_TAVAN - 1, b + ARALIK_TAVAN - 1, d.satirlar.length);
  return govde(d, b, s, d.gorel);
}

function govde(d, bas, bit, baslik) {
  const secili = d.satirlar.slice(bas - 1, bit);
  return `${baslik} · L${bas}-${bit} / ${d.satirlar.length}\n`
    + secili.map((s, i) => `${bas + i}\t${s}`).join("\n");
}

/** `oku` aracının tek girişi. Hata metni çağrıyı bozmaz, sebep olarak döner. */
export function oku({ kok, mod, dosya, ad, bas, bit, deny }) {
  if (mod === "iskelet") return iskelet(kok, dosya, deny);
  if (mod === "sembol") {
    if (!ad) throw new Error("mod=sembol için 'ad' zorunlu");
    return sembol(kok, dosya, ad, deny);
  }
  if (mod === "aralik") return aralik(kok, dosya, bas, bit, deny);
  throw new Error(`bilinmeyen mod: ${mod}`);
}
