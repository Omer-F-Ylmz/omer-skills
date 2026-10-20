import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import kapi


def mesaj(rol, *bloklar):
    return json.dumps({"message": {"role": rol, "content": list(bloklar)}}, ensure_ascii=False)


def metin(t):
    return {"type": "text", "text": t}


class Satirlar(unittest.TestCase):
    def kur(self, satirlar):
        d = Path(tempfile.mkdtemp())
        (d / "s1.jsonl").write_text("\n".join(satirlar), encoding="utf-8")
        return d

    def test_cevap_onceki_mesajda_result_son_mesaj(self):
        d = self.kur([
            mesaj("user", metin("sorular")),
            mesaj("assistant", metin('{"id":1,"cevap":"a","kaynak":"x:1"}\n{"id":2,"cevap":"b","kaynak":"y:2"}')),
            mesaj("assistant", {"type": "tool_use", "name": "Bash"}),
            mesaj("assistant", metin("Tamamlandı.")),
        ])
        s = kapi.satirlar({"result": "Tamamlandı.", "session_id": "s1"}, d)
        self.assertEqual({x["id"] for x in s}, {1, 2})

    def test_son_gelen_ayni_idyi_ezer(self):
        d = self.kur([mesaj("assistant", metin('{"id":1,"cevap":"eski"}')),
                      mesaj("assistant", metin('{"id":1,"cevap":"yeni"}'))])
        s = kapi.satirlar({"result": "", "session_id": "s1"}, d)
        self.assertEqual([x["cevap"] for x in s], ["yeni"])

    def test_transkript_yoksa_result(self):
        s = kapi.satirlar({"result": '{"id":3,"d":1}', "session_id": "yok"}, Path(tempfile.mkdtemp()))
        self.assertEqual(s[0]["id"], 3)

    def test_bash_ihlali(self):
        d = self.kur([
            mesaj("assistant", {"type": "tool_use", "name": "Bash", "input": {"command": 'python tools/beyin.py ara "x" --k 5'}}),
            mesaj("assistant", {"type": "tool_use", "name": "Bash", "input": {"command": "grep -r foo ."}}),
        ])
        self.assertEqual(kapi.ihlal({"session_id": "s1"}, d), 1)


if __name__ == "__main__":
    unittest.main()
