"""yetimler() sahte süreç ağacıyla: python .kos/kopru/test_yetim.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yetim import yetimler

N = 10_000


def s(pid, ppid, ad, cmd="", t=1):
    return pid, {"ProcessId": pid, "ParentProcessId": ppid, "Name": ad, "WorkingSetSize": 1, "T": t, "Cmd": cmd}


p = dict([
    s(1, 0, "claude.exe"), s(2, 1, "node.exe", "mcp canli"),                       # canlı oturum çocuğu
    s(3, 99, "node.exe", "excalidraw server"),                                      # ebeveyn ölü → yetim
    s(4, 98, "pythonw.exe", "mcp_paylasim bekci"), s(5, 4, "python.exe", "mcp-x"),  # korunan ağaç
    s(6, 97, "python.exe", "video_ek50_kos.py"), s(7, 97, "conhost.exe"),           # korunan koşu + kardeş konsolu
    s(8, 96, "python.exe", "headroom proxy"),                                       # korunan vekil
    s(9, 95, "python.exe", "yetim sunucu"), s(10, 9, "conhost.exe"),                # yetim + çocuğu
    s(11, 99, "chrome.exe", "chrome"),                                              # hedef dışı
])
sonuc = {x["ProcessId"] for x, _, _ in yetimler(p, simdi=N)}
assert sonuc == {3, 9, 10}, sonuc
assert {x["ProcessId"] for x, _, _ in yetimler(p, simdi=N, benim={3})} == {9, 10}
print("tamam")
