"""TOKEN-2 K2: tools/cmem_yama.py — claude-mem tek atımlık compress çağrısına DISABLE_PROMPT_CACHING (1h yazma 2× → girdi 1×)."""
import shutil
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import cmem_yama as y  # noqa: E402

# 13.25.2 worker-service.cjs'ten: ana observer oturumu (ANA) ve tek atımlık compress çağrısı (TEK)
ANA = ('let q=yg({prompt:h,options:{...vg({source:"Observer",sessionDbId:r.sessionDbId,contentSessionId:r.contentSessionId,'
       'project:r.project,model:n,env:c,pathToClaudeCodeExecutable:s,abortController:o}),extraArgs:{"no-session-persistence":null}}});')
TEK = ('let l=yg({prompt:e,options:{...vg({source:"Observer",sessionDbId:r.sessionDbId,contentSessionId:r.contentSessionId,'
       'project:r.project,model:n,env:i,pathToClaudeCodeExecutable:s,abortController:o}),maxTurns:1}}),u="";')
ORNEK = '"use strict";\r\n' + ANA + "\r\n" + TEK + "\r\n"
YAMALI_TEK = TEK.replace("env:i,", 'env:{...i,DISABLE_PROMPT_CACHING:"1"},')
GERCEK = Path.home() / ".claude/plugins/cache/thedotmack/claude-mem/13.25.2/scripts/worker-service.cjs"


def ok(_):
    return True


def kur(tmp_path, metin=ORNEK, surum="13.25.2"):
    yol = tmp_path / surum / "scripts" / "worker-service.cjs"
    yol.parent.mkdir(parents=True)
    yol.write_bytes(metin.encode("utf-8"))
    return yol


def test_yalniz_tek_atimlik_cagriya_disable_eklenir(tmp_path):
    yol = kur(tmp_path)
    assert y.uygula(yol, denetle=ok) == "uygulandı"
    # ana observer oturumu (ANA) aynen kalır; CRLF dahil başka bayt değişmez
    assert yol.read_bytes() == ORNEK.replace(TEK, YAMALI_TEK).encode("utf-8")


def test_dolar_isaretli_minified_ad(tmp_path):
    # 13.31.0: vg → $g; JS tanımlayıcısında $ geçerli
    metin = ORNEK.replace("...vg(", "...$g(").replace("env:i,", "env:$i,")
    yol = kur(tmp_path, metin)
    assert y.uygula(yol, denetle=ok) == "uygulandı"
    assert y.uygula(yol, denetle=ok) == "yamalı: dokunulmadı"


def test_idempotent(tmp_path):
    yol = kur(tmp_path)
    y.uygula(yol, denetle=ok)
    b = yol.read_bytes()
    assert y.uygula(yol, denetle=ok).startswith("yamalı")
    assert yol.read_bytes() == b
    assert y.durum(b.decode("utf-8")) == "yamalı"


def test_guncelleme_sonrasi_yeni_surume_yeniden_uygulanir(tmp_path):
    """Plugin güncellemesi yeni sürüm dizini getirir, minified adlar değişir; betik en yeniyi bulup yine yamalar."""
    kur(tmp_path)
    kur(tmp_path, ORNEK, "13.9.1")
    yeni = ORNEK.replace("vg(", "Zw(").replace("yg(", "Kq(").replace("env:i,", "env:k,")
    yol = kur(tmp_path, yeni, "13.26.0")
    assert y.bul(tmp_path) == yol
    assert y.durum(yeni) == "yamasız"
    assert y.uygula(yol, denetle=ok) == "uygulandı"
    assert 'env:{...k,DISABLE_PROMPT_CACHING:"1"},' in yol.read_text(encoding="utf-8")


def test_geri_bayt_esit(tmp_path):
    yol = kur(tmp_path)
    y.uygula(yol, denetle=ok)
    assert y.geri(yol) == "geri alındı"
    assert yol.read_bytes() == ORNEK.encode("utf-8")
    assert y.geri(yol).startswith("zaten yamasız")


@pytest.mark.parametrize("metin", [ORNEK.replace(TEK, ""), ORNEK + TEK], ids=["capa-0", "capa-2"])
def test_capa_0_ya_da_2_DUR(tmp_path, metin):
    yol = kur(tmp_path, metin)
    with pytest.raises(SystemExit, match="DUR"):
        y.uygula(yol, denetle=ok)
    assert yol.read_bytes() == metin.encode("utf-8")


def test_node_check_kirik_ise_geri_alinir_DUR(tmp_path):
    yol = kur(tmp_path)
    with pytest.raises(SystemExit, match="DUR"):
        y.uygula(yol, denetle=lambda _: False)
    assert yol.read_bytes() == ORNEK.encode("utf-8")


@pytest.mark.skipif(not shutil.which("node"), reason="node yok")
def test_node_check(tmp_path):
    (tmp_path / "a.cjs").write_text("let a=1;", encoding="utf-8")
    (tmp_path / "b.cjs").write_text("let a=;", encoding="utf-8")
    assert y.node_check(tmp_path / "a.cjs") and not y.node_check(tmp_path / "b.cjs")


def test_kullanici_ayarina_sizmaz(tmp_path, monkeypatch, capsys):
    ev = tmp_path / "ev"
    ayar = ev / ".claude" / "settings.json"
    ayar.parent.mkdir(parents=True)
    ayar.write_text('{"promptCacheTtl": "1h"}', encoding="utf-8")
    monkeypatch.setattr(Path, "home", lambda: ev)
    monkeypatch.setattr(y, "node_check", ok)
    yol = kur(tmp_path)
    assert y.main(["--dosya", str(yol)]) == 0
    assert y.main(["--dosya", str(yol), "--kontrol"]) == 0
    assert capsys.readouterr().out.rstrip().endswith("yamalı")
    assert ayar.read_text(encoding="utf-8") == '{"promptCacheTtl": "1h"}'
    assert sorted(p.name for p in ev.rglob("*")) == [".claude", "settings.json"]
    assert sorted(p.name for p in yol.parent.iterdir()) == ["worker-service.cjs", "worker-service.cjs.token2-yedek"]


@pytest.mark.skipif(not GERCEK.is_file(), reason="claude-mem 13.25.2 kurulu değil")
def test_gercek_kurulumda_capa_tek():
    assert y.durum(GERCEK.read_bytes().decode("utf-8")) in ("yamasız", "yamalı")
