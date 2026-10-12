"""ROUTER-1: `claude -p` adımı için kural tabanlı yönlendirme — model DÜŞÜRÜLMEZ (Ömer 12 Eki: tasarruf yolu değil).
Tasarruf bağlamdan gelir (CLAUDE.md/skill/hook/MCP yükü olmayan yalın oturum), kalite effort'tan: zor sınıf yüksek effort,
geri düşüş bir üst kademe (effort ↑, en sonda opus). Sınıflar docs/router-1/tasarim.md. Bayrak: ROUTER_1=1 (varsayılan kapalı).
  python tools/model_sec.py <sinif> [--model M] [--arac Read,Bash] [--kademe N]  → bayrak listesi (JSON)"""
import json
import os
import sys

EFFORT = ["low", "medium", "high", "xhigh"]
# sınıf → başlangıç effort'u; araçsız sınıflar yalın oturum (--safe-mode: CLAUDE.md, skill, hook, MCP kapalı)
SINIF = {
    "mekanik": "low",     # sınıflandırma, alan çıkarımı, biçim dönüşümü; kısa girdi, tek doğru yanıt
    "ozet": "medium",     # bölüm/rapor özeti, dönüşüm; içerik korunmalı
    "yargi": "high",      # rubrik puanı, Jev, karşılaştırma, tasarım kararı
    "ajan": "medium",     # araç gerekir (dosya okur/yazar); yalnız istenen araç + gereken MCP
}
YALIN = ["--strict-mcp-config", "--disable-slash-commands", "--no-session-persistence"]


def acik():
    return os.environ.get("ROUTER_1") == "1"


def bayraklar(sinif, model="sonnet", arac=(), kademe=0, mcp_config=None):
    """kademe 0 = sınıfın başlangıcı; her geri düşüş +1 (effort bir üst; xhigh'tan sonra opus/xhigh)."""
    i = EFFORT.index(SINIF[sinif]) + kademe
    if i >= len(EFFORT):
        model, i = "opus", len(EFFORT) - 1
    b = ["--model", model, "--effort", EFFORT[i], *YALIN]
    if not arac:
        return b + ["--safe-mode", "--tools", ""]
    b += ["--setting-sources", "", "--tools", ",".join(a.split("(")[0] for a in arac), "--allowedTools", *arac]
    return b + (["--mcp-config", mcp_config] if mcp_config else [])


if __name__ == "__main__":
    a = sys.argv[1:]
    al = lambda k, v: a[a.index(k) + 1] if k in a else v
    arac = [x for x in al("--arac", "").split(",") if x]
    print(json.dumps(bayraklar(a[0], al("--model", "sonnet"), arac, int(al("--kademe", "0")))))
