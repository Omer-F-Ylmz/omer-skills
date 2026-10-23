import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import oyun_modu as om

S = 10000.0


def p(pid, ppid, name, create=1000.0, cmd="", idle=True, rss=50):
    return {"pid": pid, "ppid": ppid, "name": name, "create": create, "cmd": cmd, "idle": idle, "rss_mb": rss}


class OyunEsleme(unittest.TestCase):
    def test_exe_eslesir(self):
        self.assertEqual(om.oyun_var(["Chrome.exe", "ZenlessZoneZero.exe", "yuanshen.exe"]), ["yuanshen.exe", "zenlesszonezero.exe"])
        self.assertEqual(om.oyun_var(["GenshinImpact.exe", "Client-Win64-Shipping.exe"]), ["client-win64-shipping.exe", "genshinimpact.exe"])

    def test_oyun_yok(self):
        self.assertEqual(om.oyun_var(["chrome.exe", "node.exe"]), [])


class Yetim(unittest.TestCase):
    def ad(self, procs):
        return [x["pid"] for x in om.yetim_adaylar(procs, S, pid_kendi=999)]

    def test_ebeveyn_yok_yetim(self):
        self.assertEqual(self.ad([p(1, 77, "node.exe")]), [1])

    def test_ebeveyn_canli_dokunulmaz(self):
        self.assertEqual(self.ad([p(10, 4, "claude.exe", 500), p(1, 10, "node.exe", 1000)]), [])

    def test_pid_yeniden_kullanimi_yetim(self):
        # ebeveyn pid'i var ama çocuktan sonra doğmuş → gerçek ebeveyn ölmüş
        self.assertEqual(self.ad([p(10, 4, "explorer.exe", 2000), p(1, 10, "conhost.exe", 1000)]), [1])

    def test_mcp_ve_yoneticiler_korunur(self):
        self.assertEqual(self.ad([p(1, 77, "node.exe", cmd="node mcp-server.js"), p(2, 77, "python.exe", cmd="python ajan_sira.py")]), [])

    def test_genc_ya_da_mesgul_dokunulmaz(self):
        self.assertEqual(self.ad([p(1, 77, "node.exe", create=S - 10), p(2, 77, "python.exe", idle=False)]), [])

    def test_baska_ad_dokunulmaz(self):
        self.assertEqual(self.ad([p(1, 77, "ZenlessZoneZero.exe"), p(2, 77, "Discord.exe")]), [])

    def test_kendi_pid(self):
        self.assertEqual(self.ad([p(999, 77, "python.exe")]), [])


if __name__ == "__main__":
    unittest.main()
