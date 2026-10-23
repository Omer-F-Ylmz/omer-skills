"""CODE-MODE-AB-1: cm.suz çıktı süzme + cm_ab.dogru puanlama + mcp_profil.codemode birim testi."""
import json
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import cm  # noqa: E402
import cm_ab  # noqa: E402
import mcp_profil  # noqa: E402


class CmSuz(unittest.TestCase):
    def test_gurultu_dusur_json_ozet(self):
        ham = '[McpCommunicationProtocol] x\nCalling tool a\nSuccessfully registered b\n{"success":true,"result":5,"logs":[]}\nUTCP Client closed\n'
        self.assertEqual(json.loads(cm.suz(ham)), {"success": True, "result": 5})

    def test_logs_dolu_kalir(self):
        self.assertIn("logs", json.loads(cm.suz('{"result":1,"logs":["a"]}')))

    def test_json_olmayan_aynen(self):
        self.assertEqual(cm.suz("Calling tool x\nsatır1\nsatır2"), "satır1\nsatır2")

    def test_stderr_json_ozetsiz(self):
        self.assertEqual(cm.suz('{"result":1,"logs":[]}', json_ozet=False), '{"result":1,"logs":[]}')


class AbPuan(unittest.TestCase):
    def test_a(self):
        self.assertTrue(cm_ab.dogru("a", '{"etiket_sayisi":18,"dosya":204,"en_cok":"X 3"}'))
        self.assertFalse(cm_ab.dogru("a", '{"etiket_sayisi":18,"dosya":null,"en_cok":"X 3"}'))

    def test_b(self):
        self.assertTrue(cm_ab.dogru("b", "\n".join(f"- madde numarası {i} yeterince uzun" for i in range(5))))
        self.assertFalse(cm_ab.dogru("b", "- kısa"))

    def test_c(self):
        iyi = '[{"url":"https://example.com","title":"Example Domain","links":1},{"url":"http://info.cern.ch","title":"http://info.cern.ch","links":4}]'
        self.assertTrue(cm_ab.dogru("c", iyi))
        self.assertFalse(cm_ab.dogru("c", iyi.replace('"links":4', '"links":5')))


class CodemodeKip(unittest.TestCase):
    def test_bayrak(self):
        eski = os.environ.pop("CC_CODEMODE", None)
        try:
            self.assertIn("cm.py run", mcp_profil.codemode())
            os.environ["CC_CODEMODE"] = "1"
            self.assertIn("cm.py run", mcp_profil.codemode())
            os.environ["CC_CODEMODE"] = "0"
            self.assertEqual(mcp_profil.codemode(), "")
        finally:
            os.environ.pop("CC_CODEMODE", None)
            if eski is not None:
                os.environ["CC_CODEMODE"] = eski


if __name__ == "__main__":
    unittest.main()
