import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mod_yama as my  # noqa: E402

REG = "await $.command.register({ name: 'x', description: 'd' }).catch(() => {}) // keep"
UYGUN = f"""import x
export const register: Register = on => {{
  on('session.start', async ($, e, next) => {{
    const r = await next(e)
    {REG}
    return r
  }})

  on('ui.render', {{ component: 'AbovePrompt' }}, async ($, e, next) => {{
    const rest = await next(e) // what others draw
    return rest
  }})
}}
"""
PANE = UYGUN.replace("component: 'AbovePrompt'", "component: 'Pane', requestId: P").replace("async ($, e, next) => {\n    const rest = await next(e) // what others draw", "async ($, e) => {\n    const rest = 1")
ERKEN = UYGUN.replace("    const r = await next(e)\n", "    const r = await next(e)\n    if (!ok) return r\n")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def kur(tmp, icerik):
    mods = tmp / "mods"
    for ad, (metin, nl) in icerik.items():
        d = mods / ad / "hooks"
        d.mkdir(parents=True)
        (d / "register.tsx").write_bytes(metin.replace("\n", nl).encode())
    return mods


def kos(tmp, *a):
    return my.main([*a, "--mods-dir", str(tmp / "mods"), "--kayit", str(tmp / "k.json"), "--yedek", str(tmp / "yedek")])


def test_yamala_register_ui_render_icine_tasinir():
    y, neden = my.yamala(UYGUN)
    assert neden is None
    assert y.count("command.register") == 1
    assert y.index("let cmdRegistered = false") < y.index("export const register")
    assert y.index("cmdRegistered = true") > y.index("const rest = await next(e)")
    assert "void $.command.register({ name: 'x', description: 'd' }).catch(() => {})" in y
    assert y.index("command.register") > y.index("component: 'AbovePrompt'")


def test_yamala_kalip_tutmayan_atlanir():
    assert my.yamala(PANE)[0] is None
    assert my.yamala(ERKEN)[0] is None
    assert my.yamala(UYGUN.replace(REG, ""))[0] is None
    assert my.yamala(my.yamala(UYGUN)[0])[0] is None  # zaten yamalı


def test_uygula_geri_bayt_bayt_ayni(tmp_path):
    mods = kur(tmp_path, {"a": (UYGUN, "\r\n"), "b": (UYGUN, "\n"), "pane": (PANE, "\n")})
    once = {m: sha(mods / m / "hooks" / "register.tsx") for m in ("a", "b", "pane")}
    assert kos(tmp_path, "--uygula") == 0
    assert sha(mods / "a" / "hooks" / "register.tsx") != once["a"]
    assert b"\r\n" in (mods / "a" / "hooks" / "register.tsx").read_bytes()
    assert b"\r\n" not in (mods / "b" / "hooks" / "register.tsx").read_bytes()
    assert sha(mods / "pane" / "hooks" / "register.tsx") == once["pane"]
    assert set(json.loads((tmp_path / "k.json").read_text())) == {"a", "b"}
    assert kos(tmp_path, "--geri") == 0
    assert {m: sha(mods / m / "hooks" / "register.tsx") for m in once} == once


def test_uygula_ikinci_kez_degismez(tmp_path):
    mods = kur(tmp_path, {"a": (UYGUN, "\n")})
    kos(tmp_path, "--uygula")
    s = sha(mods / "a" / "hooks" / "register.tsx")
    kos(tmp_path, "--uygula")
    assert sha(mods / "a" / "hooks" / "register.tsx") == s


def test_guncellenmis_mod_geri_dokunmaz_uygula_yeniden_yamalar(tmp_path, capsys):
    mods = kur(tmp_path, {"a": (UYGUN, "\n")})
    kos(tmp_path, "--uygula")
    p = mods / "a" / "hooks" / "register.tsx"
    yeni = UYGUN + "// v2\n"
    p.write_bytes(yeni.encode())  # marketplace güncellemesi yamayı sildi
    capsys.readouterr()
    kos(tmp_path, "--durum")
    assert "güncellenmiş" in capsys.readouterr().out
    kos(tmp_path, "--geri")
    assert p.read_bytes() == yeni.encode()  # dokunulmadı
    kos(tmp_path, "--uygula")
    assert b"cmdRegistered" in p.read_bytes() and b"// v2" in p.read_bytes()
    kos(tmp_path, "--geri")
    assert p.read_bytes() == yeni.encode()  # yeni orijinal yedekten döndü
