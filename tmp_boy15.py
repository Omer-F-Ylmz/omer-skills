import sys,json
sys.path.insert(0,"tools")
import usta_kart as u
d=".kos/kopru/usta-haiku/ileri/"
n=json.load(open(d+"hakem15-adlar.json",encoding="utf-8")); K={k["ad"]:k for k in u.kartlar()}
L=[len(u.kaynak(K[a],10**6)) for a in n]; print(sum(L),max(L),sorted(L)[20])
