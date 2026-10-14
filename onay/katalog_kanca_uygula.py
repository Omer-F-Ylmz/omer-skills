"""KATALOG-KANCA-1 onay betiği — Desktop koşar (Ömer onayından sonra). CC: skills/yetenek-getir + tools/katalog_kanca.py +
katalog_ara.py → ~/.claude/skills/yetenek-getir; ~/.claude/settings.json hooks.UserPromptSubmit'e YALNIZ kanca girişi eklenir
(diğer hook/permissions değişmez, uygula sonrası denetlenir). Yedek ~/.claude/yedek/katalog-kanca-1/ (settings.json + eski skill).
claude.ai: dist/katalog-kanca/ altına yetenek-getir + 13 departman-* zip'i (zip_denetle'den geçer) + LISTE.md.

  python onay/katalog_kanca_uygula.py --kuru   # plan (varsayılan); hiçbir şey yazmaz
  python onay/katalog_kanca_uygula.py uygula   # yedekle + kur + giriş ekle + zip'le
  python onay/katalog_kanca_uygula.py --geri   # yalnız bu girişi sil, eski skill'i geri koy"""
import json, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import envanter_2_uygula as e2  # noqa: E402

KOK, AD = e2.KOK, e2.AD


def giris(ev):
    return {"type": "command", "command": f'python "{(ev / "skills" / AD / "katalog_kanca.py").as_posix()}"', "timeout": 5}


def ayar_oku(ayar):
    return json.loads(ayar.read_text(encoding="utf-8")) if ayar.exists() else {}


def ayar_yaz(ayar, j):
    ayar.write_text(json.dumps(j, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def girissiz(j, g):
    """j'nin kanca girişi çıkarılmış kopyası (boş kalan grup/olay da düşer)."""
    j = json.loads(json.dumps(j))
    ups = [dict(x, hooks=[h for h in x.get("hooks", []) if h != g]) for x in j.get("hooks", {}).get("UserPromptSubmit", [])]
    ups = [x for x in ups if x["hooks"]]
    if "UserPromptSubmit" in j.get("hooks", {}):
        if ups:
            j["hooks"]["UserPromptSubmit"] = ups
        else:
            del j["hooks"]["UserPromptSubmit"]
        if not j["hooks"]:
            del j["hooks"]
    return j


def main(argv=None, ev=Path.home() / ".claude", dist=KOK / "dist" / "katalog-kanca"):
    a = (argv if argv is not None else sys.argv[1:]) or ["--kuru"]
    ayar, hedef, yedek, g = ev / "settings.json", ev / "skills" / AD, ev / "yedek" / "katalog-kanca-1", giris(ev)
    j = ayar_oku(ayar)
    kurulu = any(g in x.get("hooks", []) for x in j.get("hooks", {}).get("UserPromptSubmit", []))
    if a[0] == "--geri":
        if not yedek.exists():
            print("yedek yok:", yedek); return 1
        if kurulu:
            ayar_yaz(ayar, girissiz(j, g))
        shutil.rmtree(hedef, ignore_errors=True)
        if (yedek / AD).exists():
            shutil.copytree(yedek / AD, hedef)
        shutil.rmtree(yedek)
        print("geri: giriş", "silindi" if kurulu else "zaten yoktu", "·", AD, "eski hale döndü" if hedef.exists() else "kaldırıldı"); return 0
    if a[0] != "uygula":
        print(f"KURU: {hedef} ← skills/{AD} + katalog_kanca.py + katalog_ara.py · mevcut {'var (yedeklenir)' if hedef.exists() else 'yok'}"
              f" · {ayar} UserPromptSubmit ← {g['command']} ({'zaten var' if kurulu else 'eklenecek'})"
              f" · zip {len(e2.kaynaklar())} → {dist}"); return 0
    if yedek.exists():
        sys.exit(f"yedek zaten var ({yedek}); önce --geri")
    yedek.mkdir(parents=True)
    if ayar.exists():
        shutil.copy2(ayar, yedek / "settings.json")
    if hedef.exists():
        shutil.copytree(hedef, yedek / AD); shutil.rmtree(hedef)
    shutil.copytree(KOK / "skills" / AD, hedef)
    for f in ("katalog_kanca.py", "katalog_ara.py"):
        shutil.copy2(KOK / "tools" / f, hedef / f)
    if not kurulu:
        yeni = json.loads(json.dumps(j))
        yeni.setdefault("hooks", {}).setdefault("UserPromptSubmit", []).append({"hooks": [g]})
        ayar_yaz(ayar, yeni)
        assert girissiz(ayar_oku(ayar), g) == girissiz(j, g), "settings.json'da kanca girişi dışında değişiklik"
    dist.mkdir(parents=True, exist_ok=True)
    liste = ["# KATALOG-KANCA-1 claude.ai zip'leri (Settings → Capabilities → Skills → yükle; aynı adlı eskisinin yerine)", ""]
    for d in e2.kaynaklar():
        zp, n = e2.zip_yaz(d, dist)
        sorun = e2.zip_denetle.denetle(zp)
        assert not sorun, f"{zp.name}: {sorun}"
        liste.append(f"- {zp.name} · {n} dosya · {zp.stat().st_size // 1024} KB")
    (dist / "LISTE.md").write_text("\n".join(liste) + "\n", encoding="utf-8")
    print("uygulandı:", hedef, "· UserPromptSubmit +1 giriş" if not kurulu else "· giriş zaten vardı", "· zip", len(liste) - 2, "→", dist,
          "· geri: --geri"); return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
