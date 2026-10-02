"""TOKEN-3a tetik ölçümü: istem setini `claude -p` (stream-json, max-turns 2, plan modu) ile istemin
kendi klasöründe sırayla koşar; Skill çağrısını ve SKILL.md Read'ini yakalar, recall/precision hesaplar.

  python tools/tetik_olc.py olcum/tetik-seti.json olcum/token-3a-tetik.json --ham <dizin> [--sadece id,id] [--base-url-yok]
"""
import argparse
import json
import os
import socket
import subprocess
import sys
from collections import Counter
from pathlib import Path, PurePosixPath


HEADROOM = ("127.0.0.1", 6767)


def headroom_kayit():
    """Tek satır yönlendirme kaydı; ANTHROPIC_BASE_URL'in yalnız varlığı yazılır, değeri asla."""
    try:
        socket.create_connection(HEADROOM, timeout=0.5).close()
        acik = "açık"
    except OSError:
        acik = "kapalı"
    return (f"headroom: ANTHROPIC_BASE_URL={'tanımlı' if os.environ.get('ANTHROPIC_BASE_URL') else 'yok'}"
            f" · 127.0.0.1:6767={acik}")


def ad(s):
    return s.rsplit(":", 1)[-1]


def ayristir(satirlar):
    k = {"skiller": [], "skill_okuma": [], "skill_araci": False, "ilk_ctx": 0,
         "usd": 0.0, "son": None, "bozuk": 0}
    for s in satirlar:
        if not s.strip():
            continue
        try:
            o = json.loads(s)
        except ValueError:
            k["bozuk"] += 1
            continue
        if not isinstance(o, dict):
            continue
        tur = o.get("type")
        if tur == "system" and o.get("subtype") == "init":
            k["skill_araci"] = "Skill" in (o.get("tools") or [])
        elif tur == "assistant":
            m = o.get("message") or {}
            u = m.get("usage")
            if u and not k["ilk_ctx"]:
                k["ilk_ctx"] = sum(u.get(a) or 0 for a in
                                   ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
            for c in m.get("content") or []:
                if not isinstance(c, dict) or c.get("type") != "tool_use":
                    continue
                g = c.get("input") or {}
                if c.get("name") == "Skill":
                    k["skiller"].append(g.get("skill", ""))
                elif c.get("name") == "Read" and str(g.get("file_path", "")).replace("\\", "/").endswith("/SKILL.md"):
                    k["skill_okuma"].append(g["file_path"])
        elif tur == "result":
            k["son"] = o.get("subtype")
            k["usd"] = o.get("total_cost_usd") or 0.0
    return k


def tetiklenen(k):
    return ({ad(s) for s in k["skiller"] if s}
            | {PurePosixPath(p.replace("\\", "/")).parent.name for p in k["skill_okuma"]})


def degerlendir(istem, k):
    kabul = set(istem.get("kabul") or [])
    tet = tetiklenen(k)
    return {"id": istem["id"], "isabet": bool(tet & kabul) if kabul else None,
            "dogru": sorted(tet & kabul), "yanlis": sorted(tet - kabul),
            "skiller": k["skiller"], "okuma": k["skill_okuma"], "skill_araci": k["skill_araci"],
            "ilk_ctx": k["ilk_ctx"], "usd": k["usd"], "son": k["son"]}


def ozet(ds):
    poz = [d for d in ds if d["isabet"] is not None]
    neg = [d for d in ds if d["isabet"] is None]
    dogru = sum(len(d["dogru"]) for d in ds)
    yanlis = sum(len(d["yanlis"]) for d in ds)
    return {"n": len(ds),
            "recall": round(sum(d["isabet"] for d in poz) / len(poz), 3) if poz else None,
            "precision": round(dogru / (dogru + yanlis), 3) if dogru + yanlis else None,
            "negatif_temiz": f"{sum(not d['yanlis'] for d in neg)}/{len(neg)}",
            "yanlis_skill": dict(Counter(s for d in ds for s in d["yanlis"]).most_common()),
            "eksik": [d.get("id") for d in poz if not d["isabet"]],
            "ilk_ctx_ort": round(sum(d["ilk_ctx"] for d in ds) / len(ds)) if ds else 0,
            "usd_top": round(sum(d["usd"] for d in ds), 2)}


def kos(istem, ham, env=None, base_url=True, calistir=subprocess.run):
    env = dict(os.environ if env is None else env)
    if not base_url:
        env.pop("ANTHROPIC_BASE_URL", None)
    args = ["claude", "-p", istem["istem"], "--output-format", "stream-json", "--verbose",
            "--max-turns", "2", "--permission-mode", "plan"]
    r = calistir(args, cwd=istem["cwd"], env=env, stdin=subprocess.DEVNULL, capture_output=True,
                 encoding="utf-8", errors="replace", timeout=600)
    Path(ham).write_text(r.stdout or "", encoding="utf-8")
    return ayristir((r.stdout or "").splitlines())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("set")
    p.add_argument("cikti")
    p.add_argument("--ham", required=True)
    p.add_argument("--sadece", default="")
    p.add_argument("--base-url-yok", action="store_true")
    a = p.parse_args()
    sys.path.insert(0, str(Path(__file__).parent))
    from gorsel_uret import bos_ram_gb

    print(headroom_kayit(), flush=True)
    istemler = json.loads(Path(a.set).read_text(encoding="utf-8"))["istemler"]
    cikti = Path(a.cikti)
    kayit = json.loads(cikti.read_text(encoding="utf-8")) if cikti.exists() else {"sonuclar": []}
    yapilan = {d["id"] for d in kayit["sonuclar"]}
    secili = set(filter(None, a.sadece.split(",")))
    Path(a.ham).mkdir(parents=True, exist_ok=True)
    for i in istemler:
        if i["id"] in yapilan or (secili and i["id"] not in secili):
            continue
        if bos_ram_gb() < 4:
            sys.exit(f"DUR: boş RAM < 4 GB ({i['id']} öncesi)")
        d = degerlendir(i, kos(i, Path(a.ham) / f"{i['id']}.jsonl", base_url=not a.base_url_yok))
        d.update(tur=i["tur"], gercek_ortam=not a.base_url_yok)
        kayit["sonuclar"].append(d)
        kayit["ozet"] = ozet(kayit["sonuclar"])
        cikti.write_text(json.dumps(kayit, ensure_ascii=False, indent=1), encoding="utf-8")
        print(i["id"], d["isabet"], d["dogru"], d["yanlis"], d["skill_araci"], d["son"], d["ilk_ctx"], d["usd"],
              flush=True)


if __name__ == "__main__":
    main()
