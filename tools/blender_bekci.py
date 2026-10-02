"""BLENDER-ARAC-1 K5: Blender kod bekçisi — PreToolUse hook (mcp__blender__execute_blender_code[_for_cli]).

    python -S tools/blender_bekci.py < hook-girdisi.json

Statik AST taraması (<100 ms, ağ yok). Red: exit 2 + stderr'de tek satır "sebep → düzeltme".
Koruma, sınır değil: kararlı biri statik taramayı aşabilir; amaç kaza ve dikkatsizliği durdurmak.
"""
import ast
import json
import os
import sys

import blender_cli as bc

YASAK_MODUL = {"subprocess", "ctypes", "socket", "urllib", "requests", "http", "importlib"}
YASAK_UYE = {"os": {"remove", "unlink", "rmdir", "removedirs", "system", "popen"}, "shutil": {"rmtree", "move"}}
SUREC = {"system", "popen"}
DINAMIK = {"exec", "eval", "compile", "__import__", "globals", "vars", "__builtins__"}
IC_OZNITELIK = {"__builtins__", "__globals__", "__subclasses__", "__code__", "__dict__", "__bases__", "__mro__"}
GIZLI = DINAMIK | YASAK_UYE["os"] | YASAK_UYE["shutil"]
DUZELT = {
    "modul": "bpy.data / bpy.ops ile yap; dış süreç ya da ağ işini CC tarafında ayrı araçla yap",
    "silme": "dosya silme/taşımayı CC'de elle yap; sahne verisi için bpy.data.<koleksiyon>.remove kullan",
    "dinamik": "kodu doğrudan yaz; exec/eval/compile/__import__/getattr ile gizleme yok",
    "yol": "sabit string ya da // göreli yol yaz (Desktop\\<Proje>\\ altında)",
    "render": "önce scene.render.filepath'i bu kodda sabit string ya da // göreli yol olarak ata",
    "kopya": "diskte kopya için yalnız bpy.ops.wm.save_as_mainfile(filepath=..., copy=True)",
}
YOL_DISI = "yol Desktop\\<Proje>\\ dışında ya da çözülemedi"


def _red(sebep, tur):
    return f"blender-bekçi: {sebep} → {DUZELT[tur]}"


def _ad(d):
    parca = []
    while isinstance(d, ast.Attribute):
        parca.append(d.attr)
        d = d.value
    if isinstance(d, ast.Name):
        parca.append(d.id)
    return ".".join(reversed(parca))


def _yol_tamam(d):
    """Sabit string (// göreli ya da Desktop\\<Proje>\\ altı mutlak) ya da bpy.path.abspath("//...")."""
    if isinstance(d, ast.Call) and _ad(d.func) == "bpy.path.abspath" and d.args:
        d = d.args[0]
    if not (isinstance(d, ast.Constant) and isinstance(d.value, str)):
        return False
    s = d.value
    return s.startswith("//") or (os.path.isabs(s) and bc.proje_ici(s))


def _kw(d, ad):
    return next((k.value for k in d.keywords if k.arg == ad), None)


def _yazma_kipi(d):
    kip = d.args[1] if len(d.args) > 1 else _kw(d, "mode")
    if kip is None:
        return False
    return not (isinstance(kip, ast.Constant) and isinstance(kip.value, str)) or any(c in kip.value for c in "wax+")


def _cagri(d, takma):
    ad = _ad(d.func)
    son = d.func.attr if isinstance(d.func, ast.Attribute) else ad
    if ad == "getattr" and len(d.args) >= 2:
        n = d.args[1]
        if not (isinstance(n, ast.Constant) and isinstance(n.value, str)) or n.value in GIZLI or n.value.startswith("__"):
            return _red("getattr ile gizli ad", "dinamik")
    if ad.endswith("libraries.write"):
        return _red("'bpy.data.libraries.write' Scene yazarken Blender 5.2.1'i çökertiyor", "kopya")
    kok = ad.split(".")[0]
    if kok in takma and "." in ad and son in YASAK_UYE[takma[kok]]:
        return _red(f"yasak çağrı '{takma[kok]}.{son}'", "modul" if son in SUREC else "silme")
    # ponytail: argümansız .unlink()/.rmdir() pathlib sayılır; bpy unlink hep argüman alır.
    if son in ("unlink", "rmdir") and not d.args:
        return _red(f"dosya silme '.{son}()'", "silme")
    if ad == "open" and _yazma_kipi(d) and not _yol_tamam(d.args[0] if d.args else _kw(d, "file")):
        return _red(f"open() yazma {YOL_DISI}", "yol")
    if son in ("write_text", "write_bytes"):
        taban = d.func.value
        hedef = taban.args[0] if isinstance(taban, ast.Call) and _ad(taban.func) in ("Path", "pathlib.Path") and taban.args else None
        if hedef is None or not _yol_tamam(hedef):
            return _red(f"'{son}' {YOL_DISI}", "yol")
    if "save" in son or "export" in ad:
        hedefler = [k.value for k in d.keywords if k.arg in ("filepath", "directory")]
        if son == "save_render" and d.args:
            hedefler.append(d.args[0])
        if not all(_yol_tamam(h) for h in hedefler):
            return _red(f"'{son}' {YOL_DISI}", "yol")
    return None


def denetle(kod):
    """Red sebebi (tek satır) ya da None."""
    try:
        agac = ast.parse(kod)
    except SyntaxError:
        return None  # ayrıştırılamayan kod Blender'da da çalışmaz
    takma, yol_atandi, render_yazar = {}, False, False
    for d in ast.walk(agac):
        if isinstance(d, ast.Import):
            for a in d.names:
                kok = a.name.split(".")[0]
                if kok in YASAK_MODUL:
                    return _red(f"yasak modül '{a.name}'", "modul")
                if kok in YASAK_UYE:
                    takma[a.asname or kok] = kok
        elif isinstance(d, ast.ImportFrom):
            kok = (d.module or "").split(".")[0]
            if kok in YASAK_MODUL:
                return _red(f"yasak modül '{d.module}'", "modul")
            for a in d.names:
                if kok in YASAK_UYE and (a.name == "*" or a.name in YASAK_UYE[kok]):
                    return _red(f"yasak ad '{kok}.{a.name}'", "modul" if a.name in SUREC else "silme")
        elif isinstance(d, ast.Name) and d.id in DINAMIK:
            return _red(f"dinamik çalıştırma '{d.id}'", "dinamik")
        elif isinstance(d, ast.Attribute) and d.attr in IC_OZNITELIK:
            return _red(f"iç öznitelik '{d.attr}'", "dinamik")
        elif isinstance(d, ast.Call):
            sebep = _cagri(d, takma)
            if sebep:
                return sebep
            if any(k.arg in ("write_still", "animation") and isinstance(k.value, ast.Constant) and k.value.value
                   for k in d.keywords):
                render_yazar = True
        elif isinstance(d, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            for t in d.targets if isinstance(d, ast.Assign) else [d.target]:
                if isinstance(t, ast.Attribute) and t.attr in ("filepath", "filepath_raw"):
                    if not _yol_tamam(d.value):
                        return _red(f"'.{t.attr}' ataması: {YOL_DISI}", "yol")
                    yol_atandi = True
    if render_yazar and not yol_atandi:
        return _red("render dosyaya yazıyor ama render.filepath bu kodda atanmadı", "render")
    return None


def main():
    try:
        kod = json.load(sys.stdin).get("tool_input", {}).get("code") or ""
    except ValueError:
        return 0
    sebep = denetle(kod)
    if sebep:
        print(sebep, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
