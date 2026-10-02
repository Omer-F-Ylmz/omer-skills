"""TOKEN-2 K3 kapı koşusu: sabit istem (tools/ altında 10 Read) → claude -p → worker kuyruğu boşalana dek bekle.
Kullanım: python kapi.py <etiket>   (istem ilk koşuda olcum/token-2-istem.txt'e yazılır, ikincide aynen okunur)"""
import datetime, json, pathlib, shutil, subprocess, sys, time, urllib.request

KOK = pathlib.Path(r"C:\Projeler\omer-skills")
etiket = sys.argv[1]
istem_yolu = KOK / "olcum" / "token-2-istem.txt"
simdi = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
if not istem_yolu.exists():
    haric = {"token_olc.py", "cmem_yama.py"}
    dosyalar = sorted(p.relative_to(KOK).as_posix() for p in (KOK / "tools").rglob("*.py")
                      if 17_000 <= p.stat().st_size <= 120_000 and p.name not in haric and "test" not in p.name)[:10]
    assert len(dosyalar) == 10, dosyalar
    istem_yolu.write_text(
        "Salt-okuma ölçüm görevi. Aşağıdaki 10 dosyanın her birini sırayla Read aracıyla bir kez, ek parametre "
        "vermeden oku. Başka araç kullanma, dosyaları yorumlama; sonunda yalnız 'bitti' yaz.\n"
        + "\n".join(dosyalar) + "\n", encoding="utf-8")
istem = istem_yolu.read_text(encoding="utf-8")


def durum():
    try:
        return json.load(urllib.request.urlopen("http://localhost:37777/api/processing-status", timeout=5))
    except Exception as e:  # noqa: BLE001
        return {"hata": str(e)}


k = {"etiket": etiket, "t0": simdi()}
r = subprocess.run([shutil.which("claude"), "-p", istem, "--model", "sonnet", "--max-turns", "15",
                    "--max-budget-usd", "1.5", "--output-format", "json"],
                   cwd=KOK, capture_output=True, text=True, encoding="utf-8", timeout=900)
k["t1"] = simdi()
try:
    j = json.loads(r.stdout)
    k.update(session_id=j.get("session_id"), cost=j.get("total_cost_usd"), num_turns=j.get("num_turns"),
             sonuc=str(j.get("result"))[:80])
except Exception:  # noqa: BLE001
    k.update(rc=r.returncode, stdout=r.stdout[-300:], stderr=r.stderr[-300:])
bas = time.time()
for _ in range(10):  # TOKEN-2b tarifi: aralık ≥30 sn, en fazla 10 yoklama
    time.sleep(40)
    d = durum()
    if d.get("queueDepth") == 0 and not d.get("isProcessing"):
        break
k.update(t2=simdi(), bekleme_sn=round(time.time() - bas), son_durum=durum())
(KOK / "olcum" / f"token-2-kapi-{etiket}.json").write_text(json.dumps(k, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps(k, ensure_ascii=False))
