"""FABLE-AJAN SubagentStart hook'u: dosyası değiştirilemeyen (plugin/skill) alt ajanlara protokolü additionalContext olarak verir.
  settings: {"hooks": {"SubagentStart": [{"matcher": ".*", "hooks": [{"type": "command", "command": "python <bu> <harita.json>"}]}]}}
harita.json = {"metin": {"sonnet": "...", "haiku": "..."}, "ajan": {"plugin:ad": "sonnet"}}; haritada olmayan ajan → çıktı yok
(kendi ajanlarımız tanımdan/skills: satırından alır; çift ekleme olmaz). Hata ajanı durdurmaz: her durumda rc 0."""
import json, sys


def baglam(girdi, harita):
    anahtar = harita.get("ajan", {}).get(girdi.get("agent_type") or "")
    return harita.get("metin", {}).get(anahtar or "")


if __name__ == "__main__":
    try:
        m = baglam(json.load(sys.stdin), json.load(open(sys.argv[1], encoding="utf-8")))
        if m:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "SubagentStart", "additionalContext": m}}, ensure_ascii=False))
    except Exception:  # noqa: BLE001 — hook asla alt ajanı düşürmez
        pass
