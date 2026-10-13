"""f2d iş 4 davranış kapısı: kapi4 + Desktop'un 8 görevi × A/B (16 claude -p). A canlı SessionStart, B yamalı kopya.
İki kolda da --disallowedTools Edit Write NotebookEdit. Koşu başına kapi5_<no>_<kol>.json (varsa atlanır → kaldığı yerden sürer).
  python kapi5.py            (arka.py ile)      python kapi5.py sina   (ayrıştırıcı öz-sınaması)"""
import json, os, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BURA = Path(__file__).parent
sys.path.insert(0, str(BURA))
from kapi4 import KOK, EV, PLUGINLER, is4, ram

GOREV = [
    "Bu repoda yeni bir landing sayfası bölümü (hero + özellik ızgarası) tasarlayacağız. Hangi tasarım araçlarını hangi sırayla kullanacağını belirle ve ilk adımın planını çıkar; kod yazma.",
    "tools/secim/dizin_uret.py içindeki dosyalar() fonksiyonu için kabulsüz ajanın zip'e girmediğini doğrulayan yeni bir test senaryosu tasarla; önce hangi test yaklaşımını izleyeceğini söyle, testi yalnız metin olarak öner.",
    "tools/tests altında bir testin aralıklı (flaky) düştüğünü varsay: kök nedeni bulmak için izleyeceğin adımları uygula, hipotezlerini sırala; dosya değiştirme.",
    "Supabase'de kullanıcıya özel 'notlar' tablosu için RLS politikaları ve migration SQL'i öner; yalnız metin.",
    "main ile kol/token8 arasındaki farkı commit öncesi incele: riskli değişiklikleri ve eksik testleri listele.",
    ".kos/kopru/ altındaki en büyük 3 .log dosyasını bul ve her birinde en sık geçen 5 hata/uyarı kalıbını özetle.",
    "Son 300 commit'i tarayıp hangi görev ailelerinin (KALITE, VIDEO, TOKEN, BLENDER…) kaç commit aldığını tablo yap.",
    "graphify-out/graph.json'dan en çok bağlantıya sahip 10 düğümü çıkar.",
]
YASAK = ["--disallowedTools", "Edit", "Write", "NotebookEdit"]


def ayristir(stdout):
    """stream-json → araç sırası (Skill adı / Read yolu ile), araç sonucu bayt toplamı, son yanıt."""
    araclar, sonuc_kr, j = [], 0, {}
    for s in stdout.splitlines():
        try:
            o = json.loads(s)
        except ValueError:
            continue
        icerik = (o.get("message") or {}).get("content") if isinstance(o.get("message"), dict) else None
        if o.get("type") == "assistant" and isinstance(icerik, list):
            for c in icerik:
                if c.get("type") == "tool_use":
                    g = c.get("input") or {}
                    araclar.append(c["name"] + (f":{g['skill']}" if "skill" in g else f":{g['file_path']}" if "file_path" in g else ""))
        if o.get("type") == "user" and isinstance(icerik, list):
            sonuc_kr += sum(len(json.dumps(c.get("content"), ensure_ascii=False)) for c in icerik if c.get("type") == "tool_result")
        if o.get("type") == "result":
            j = {k: o.get(k) for k in ("num_turns", "is_error", "result")}
    ctx = sum("ctx_" in a for a in araclar)
    veri = sum(a.split(":")[0] in ("Bash", "Read", "Grep", "Glob") or "ctx_" in a for a in araclar)
    return {"araclar": araclar, "ctx_payi": f"{ctx}/{veri}", "arac_sonuc_kr": sonuc_kr, **j}


def kos(no, kol, ek, esik):
    yol = BURA / f"kapi5_{no}_{kol}.json"
    if yol.exists():
        return f"{no}{kol} var"
    if ram() >= esik:
        return f"{no}{kol} RAM>={esik} atlandı"
    env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_API_KEY")}  # api-kredi.kapali
    cmd = ["claude", "-p", GOREV[no - 1], "--output-format", "stream-json", "--verbose", "--max-turns", "25"] + YASAK + ek
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, cwd=KOK, timeout=1200)
    yol.write_text(json.dumps({"no": no, "kol": kol, "rc": r.returncode, **ayristir(r.stdout)}, ensure_ascii=False, indent=1), encoding="utf8")
    return f"{no}{kol} rc={r.returncode}"


def main():
    tmp = Path(tempfile.mkdtemp(prefix="token8-kapi5-"))
    dizinler = []
    for goreli in PLUGINLER.values():
        hedef = tmp / ".claude" / goreli
        shutil.copytree(EV / goreli, hedef, ignore=shutil.ignore_patterns(".git"))
        dizinler += ["--plugin-dir", str(hedef)]
    assert is4.main(["uygula"], tmp / ".claude") == 0
    kollar = {"A": [], "B": dizinler + ["--settings", json.dumps({"enabledPlugins": {k: False for k in PLUGINLER}})]}
    with ThreadPoolExecutor(2) as h:  # aynı görevin A ve B'si eşzamanlı: ilk yuva <%88, ek <%86
        for no in range(1, len(GOREV) + 1):
            for f in [h.submit(kos, no, "A", kollar["A"], 88), h.submit(kos, no, "B", kollar["B"], 86)]:
                print(f.result(), flush=True)
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    if sys.argv[1:] == ["sina"]:
        ornek = "\n".join(json.dumps(o) for o in [
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Skill", "input": {"skill": "departman-frontend"}},
                                                          {"type": "tool_use", "name": "mcp__x__ctx_execute", "input": {}}]}},
            {"type": "user", "message": {"content": [{"type": "tool_result", "content": "abc"}]}},
            {"type": "result", "num_turns": 3, "is_error": False, "result": "son"}]) + "\nbozuk"
        a = ayristir(ornek)
        assert a["araclar"] == ["Skill:departman-frontend", "mcp__x__ctx_execute"] and a["ctx_payi"] == "1/1", a
        assert a["arac_sonuc_kr"] == 5 and a["result"] == "son", a
        sys.exit(print("sina tamam"))
    sys.exit(main())
