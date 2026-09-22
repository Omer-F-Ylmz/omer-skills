#!/usr/bin/env node
/**
 * KURULUM-11m-A K1 — Obsidian köprüsü başlatıcısı.
 *
 * Eski yol (`obsidian.cmd` -> mcp-remote) açılışta uca bağlanıyordu: Obsidian kapalıyken
 * `initialize` hiç dönmüyor, Desktop sunucuyu düşmüş sayıyor ve Obsidian sonradan
 * açılsa bile Desktop yeniden başlatılana kadar araç görünmüyordu.
 *
 * Bu sunucu açılışta HİÇ bağlanmaz. Eklenti HTTP+SSE konuşuyor, SDK 1.30'da
 * `SSEClientTransport` var — mcp-remote katmanına gerek yok.
 *   tools/list : canlı uçtan; uç kapalıysa son başarılı listenin önbelleğinden.
 *   tools/call : uç kapalıysa KAPALI_METIN döner (hata değil, yönerge).
 * Bağlantı her hatada düşürülür; bir sonraki çağrı yeniden dener — Desktop'ı yeniden
 * başlatmadan Obsidian açılır açılmaz ilk çağrı bağlanır.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const BURASI = path.dirname(fileURLToPath(import.meta.url));

/** 127.0.0.1 zorunlu: eklenti yalnız IPv4 dinler, "localhost" ::1'e çözülebilir (11g). */
export const UC = process.env.CC_KOPRU_OBSIDIAN_UC || "http://127.0.0.1:22360/sse";
export const SEMA_DOSYASI = process.env.CC_KOPRU_OBSIDIAN_SEMA
  || path.join(BURASI, "obsidian-semalar.json");
export const KAPALI_METIN = "Obsidian kapalı — aç ve tekrar dene";
/** Uç kapalıysa TCP reddi anında gelir; bu süre yalnız asılı kalan uç içindir. */
export const BAGLAN_MS = 8000;

export function semaOku(yol = SEMA_DOSYASI) {
  try {
    const x = JSON.parse(fs.readFileSync(yol, "utf8"));
    return Array.isArray(x) ? x : [];
  } catch { return []; }
}

export function semaYaz(araclar, yol = SEMA_DOSYASI) {
  try { fs.writeFileSync(yol, JSON.stringify(araclar, null, 2) + "\n", "utf8"); } catch { /* salt okunur */ }
}

let istemci = null;

export function baglantiDusur() {
  const c = istemci;
  istemci = null;
  if (c) Promise.resolve(c.close()).catch(() => { /* zaten kapalı */ });
}

/** Tek istemci paylaşılır; kapanan bağlantı kendini düşürür, sonraki çağrı yeniden kurar. */
export async function baglan({ uc = UC, zamanMs = BAGLAN_MS } = {}) {
  if (istemci) return istemci;
  const c = new Client({ name: "cc-kopru-obsidian", version: "0.1.0" });
  const tasima = new SSEClientTransport(new URL(uc));
  try {
    await c.connect(tasima, { timeout: zamanMs });
  } catch (e) {
    // Başarısız taşıma kapatılmazsa EventSource yeniden deneme zamanlayıcısı süreci
    // ayakta tutuyor (`node --test` hiç bitmiyordu).
    await Promise.resolve(tasima.close()).catch(() => { /* zaten kapalı */ });
    throw e;
  }
  c.onclose = () => { if (istemci === c) istemci = null; };
  istemci = c;
  return c;
}

/**
 * @returns {Promise<{araclar:object[], canli:boolean, hata?:string}>}
 * Hiçbir koşulda atmaz: `tools/list` Obsidian kapalıyken de yanıtlanmalı.
 */
export async function araclariGetir(secenek = {}) {
  try {
    const c = await baglan(secenek);
    const araclar = (await c.listTools()).tools || [];
    if (araclar.length) semaYaz(araclar, secenek.sema);
    return { araclar, canli: true };
  } catch (e) {
    baglantiDusur();
    return { araclar: semaOku(secenek.sema), canli: false, hata: String(e?.message || e) };
  }
}

export async function aracCagir(ad, arguman, secenek = {}) {
  try {
    const c = await baglan(secenek);
    return await c.callTool({ name: ad, arguments: arguman || {} });
  } catch (e) {
    // Atan her hata taşıma/protokol katmanındandır: aracın kendi hatası isError ile döner.
    baglantiDusur();
    return {
      content: [{ type: "text", text: `${KAPALI_METIN} (${secenek.uc || UC}: ${String(e?.message || e)})` }],
      isError: true,
    };
  }
}

/** Şemalar uçtan geldiği gibi yayınlanır; Zod'a çevirmek şemayı bozar (11l K1). */
async function ana() {
  const srv = new Server({ name: "obsidian", version: "0.1.0" }, { capabilities: { tools: {} } });
  srv.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: (await araclariGetir()).araclar }));
  srv.setRequestHandler(CallToolRequestSchema, (istek) =>
    aracCagir(istek.params.name, istek.params.arguments));
  await srv.connect(new StdioServerTransport());
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await ana();
}
