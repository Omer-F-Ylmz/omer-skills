"""MCP-HAFIF-2 ayrı onay: köprü ajan oturumlarına (sunucu.mjs claude -p spawn) DISABLE_AUTOUPDATER=1 + CLAUDE_MEM_INTERNAL=1.
Kapsam yalnız ajan -p alt süreçleri: etkileşimli CC ve Desktop otomatik güncellemeye devam eder (eklenti/CLI güncel kalır),
bu yüzden ayrı zamanlı güncelleme gerekmez; elle: `claude update` / `claude plugin marketplace update`. Hiçbir şey kaldırılmaz.
ÖLÇÜM (d5, 8 claude -p, docs/kutuphane/olcum/mcp-hafif-2-envab-d5{a,b,c}.tsv): girdi jetonu fark yok (±%1, gürültü);
eklenti temp_git klonu iki kolda da 0 — klon sanılan git fetch Serena MCP'nin uvx git+ başlatması, env'den bağımsız.
CLAUDE_MEM_INTERNAL ajan oturumlarını claude-mem'e yazdırmaz (sonraki oturumların bağlamı azalır) → ÖNERİ: UYGULAMA.
python onay/mcp_hafif_2_env.py --kuru | uygula | --geri   (uygula/--geri sonrası köprü yeniden başlatılınca etkin)"""
import shutil
import sys
from pathlib import Path

SUNUCU = Path("C:/Projeler/omer-skills/tools/cc-kopru/sunucu.mjs")
YEDEK = SUNUCU.with_name("sunucu.mjs.mh2-yedek")
CAPA = '    let ortam = AYAR.ajanJevAnahtari ? cocukOrtam("jev", AYAR) : process.env;\n'
EK = '    ortam = { ...ortam, DISABLE_AUTOUPDATER: "1", CLAUDE_MEM_INTERNAL: "1" };  // MCP-HAFIF-2 onay\n'


def yama(metin):
    if EK in metin:
        return metin
    if metin.count(CAPA) != 1:
        raise SystemExit("çapa satırı bulunamadı/birden çok — sunucu.mjs değişmiş, elle bak")
    return metin.replace(CAPA, CAPA + EK)


def main(kip):
    metin = SUNUCU.read_bytes().decode("utf-8")
    print(f"sunucu.mjs ajan env yaması: {'VAR' if EK in metin else 'YOK'} · yedek: {'VAR' if YEDEK.exists() else 'YOK'}")
    if kip == "--kuru":
        return print("PLAN (uygula): yedek -> sunucu.mjs.mh2-yedek, çapadan sonra 1 satır ekle. ÖNERİ: UYGULAMA (ölçümde kazanç yok).")
    if kip == "--geri":
        if not YEDEK.exists():
            return print("yedek yok, geri alınacak bir şey yok")
        shutil.copyfile(YEDEK, SUNUCU)
        return print("geri alındı (köprü yeniden başlatılınca etkin)")
    if kip == "uygula":
        if EK in metin:
            return print("zaten uygulanmış")
        yeni = yama(metin)
        shutil.copyfile(SUNUCU, YEDEK)
        SUNUCU.write_bytes(yeni.encode("utf-8"))  # bayt olarak: CRLF/LF korunur
        return print("uygulandı (köprü yeniden başlatılınca etkin)")
    raise SystemExit(f"bilinmeyen kip: {kip}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "--kuru")
