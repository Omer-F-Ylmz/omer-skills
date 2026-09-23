"""15b kural kapısı: T0 → bekleyen + ONAY · kural-onay tek yazıcı · model adı olgu · bizde kurulum durumu. Ağsız; Jev sahte `gonder`."""
import ast
import hashlib
import json
import os
import re
from pathlib import Path

import pytest

from video import ogren as og
from video import uygula as uy
from video.cli import main

from test_ogren import OJev, ipucu
from test_uygula import UKos, calis, kayit, kok  # noqa: F401 (kok fixture)
from test_video import VID, ortam  # noqa: F401 (ortam fixture)


def omer(ortam):
    return Path(ortam["VIDEO_KURALLAR"].split(os.pathsep)[1])


def hash_(y):
    return hashlib.sha256(y.read_bytes()).hexdigest()


def test_t0_bekleyen_dosyasi_yazar_kural_dosyasi_degismez(ortam, kok, capsys):
    once = hash_(omer(ortam))
    y = ipucu(kok, "neden-ver", kural="İsteğin nedenini de yaz", gerekce="model amacı bilince daha iyi karar verir")
    assert calis(ortam, [y], UKos(), OJev()) == 0
    assert hash_(omer(ortam)) == once
    b = (kok / "docs" / "kurulumlar" / "bekleyen" / "kural-neden-ver.md").read_text(encoding="utf-8")
    assert "İsteğin nedenini de yaz" in b and "model amacı" in b and VID in b and "çift/çelişki: yok" in b
    assert "ONAY kural neden-ver" in capsys.readouterr().out
    assert kayit(kok)[-1]["katman"] == "T0" and "ONAY kural neden-ver" in kayit(kok)[-1]["karar"]


def test_kural_onay_ekler_cifti_eklemez_lf_korunur(ortam, kok, capsys):
    y = ipucu(kok, "neden-ver", kural="İsteğin nedenini de yaz")
    assert calis(ortam, [y], UKos(), OJev()) == 0
    assert main(["kural-onay", "neden-ver"], env=ortam) == 0
    ham = omer(ortam).read_bytes()
    assert b"\r\n" not in ham and ham.decode("utf-8").splitlines()[-1] == f"3. İsteğin nedenini de yaz (video {VID}, 15b)"
    assert not (kok / "docs" / "kurulumlar" / "bekleyen" / "kural-neden-ver.md").exists()
    assert "madde eklendi" in kayit(kok)[-1]["karar"]
    assert calis(ortam, [y, "--yeniden"], UKos(), OJev()) == 0  # aynı öneri yeniden onaya gelirse çift
    once = hash_(omer(ortam))
    assert main(["kural-onay", "neden-ver"], env=ortam) == 0
    assert hash_(omer(ortam)) == once and "ÇİFT" in capsys.readouterr().out


def test_kural_onay_kopru_altizinde_yok():
    k = json.loads((uy.KOK / "tools" / "cc-kopru" / "kopru.json").read_text(encoding="utf-8"))
    assert "kural-onay" not in k["izinli"]["video"]["altIzin"]


def test_kural_dosyasina_tek_yazan_kural_ekle():
    yazan, cagiran = set(), set()
    for p in Path(uy.__file__).parent.glob("*.py"):
        for f in ast.walk(ast.parse(p.read_text(encoding="utf-8"))):
            if not isinstance(f, ast.FunctionDef):
                continue
            src = ast.unparse(f)
            if "omer-kurallar" in src and re.search(r"\.write_(bytes|text)\(|\bopen\(", src):
                yazan.add(f.name)
            if any(isinstance(n, ast.Call) and "kural_ekle" in (getattr(n.func, "id", None), getattr(n.func, "attr", None)) for n in ast.walk(f)):
                cagiran.add(f.name)
    assert yazan == {"kural_ekle"} and cagiran == {"kural_onay"}


@pytest.mark.parametrize("model", ["Fable", "Opus"])
def test_model_adi_gecen_ipucu_jeve_sorulmadan_olgu(ortam, kok, model):
    once = hash_(omer(ortam))
    y = ipucu(kok, "muhakeme", kural=f"{model} muhakemesini açıklatmak gereksiz", zaman="7:42")
    jev = OJev(tur="kural")
    assert calis(ortam, [y], UKos(), jev) == 0
    assert hash_(omer(ortam)) == once and kayit(kok)[-1]["yargi"] == "ÖĞREN"
    assert not any(q.get("instructions") == og.TUR_SORU for g in jev.istek for q in g["questions"].values())
    assert not (kok / "docs" / "kurulumlar" / "bekleyen").exists()


def test_bizde_katalogda_olmayan_ad_settingsten(ortam, kok):
    cl = Path(ortam["VIDEO_EV"]) / ".claude"
    for ad in ("katalogda", "synced/x/gizli"):
        (cl / "skills" / ad).mkdir(parents=True)
        (cl / "skills" / ad / "SKILL.md").write_text(f"---\nname: {ad}\ndescription: d\n---\n", encoding="utf-8")
    (cl / "plugins").mkdir(parents=True)
    (cl / "plugins" / "installed_plugins.json").write_text(json.dumps({"plugins": {"kapali@m": [{}]}}), encoding="utf-8")
    (cl / "settings.json").write_text(json.dumps({"enabledPlugins": {"kapali@m": False, "hayalet@m": False},
                                                  "skillOverrides": {"anthropic-skills:gizli": "off", "yoksun": "off"}}), encoding="utf-8")
    beklenen = {"katalogda": "kurulu-açık", "kapali": "kurulu-kapalı", "gizli": "kurulu-kapalı", "hayalet": "yok", "yoksun": "yok", "hic": "yok"}
    yollar = [uy.Path(ipucu(kok, ad)) for ad in beklenen]
    assert main(["bizde", *map(str, yollar)], env=ortam, gonder=OJev()) == 0
    for (ad, dur), y in zip(beklenen.items(), yollar):
        satir = re.search(r"^- kurulum: (.*)$", uy.tr.bolum(y.read_text(encoding="utf-8"), "Bizde durum"), re.M)
        assert satir and satir[1].split(" ")[0] == dur, (ad, satir and satir[1])
