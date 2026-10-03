14 gün · 2150 dosya · toplam ağırlıklı 508.012 M · Headroom k medyan 2.04 · genel 1.37 (211 oturum, 2039 temiz adım) · katkı ham → düz (×k)

en büyük 10 kaynak | kategori | adet | token | ham M | düz M | pay %
sed | bash | 753 | 622708 | 3.187 | 4.568 | 0.90
cat | bash | 543 | 424254 | 2.460 | 4.151 | 0.82
python | bash | 1276 | 403479 | 1.782 | 2.525 | 0.50
grep | bash | 1013 | 367849 | 1.701 | 2.506 | 0.49
Read >300 satır, aralıksız (rehber dışı) | limitsiz>300 | 300 | 580629 | 1.760 | 2.439 | 0.48
aynı dosyanın tekrar okunması | tekrar | 538 | 286138 | 1.537 | 2.093 | 0.41
echo | bash | 379 | 190706 | 1.294 | 1.815 | 0.36
ls | bash | 655 | 223971 | 1.112 | 1.623 | 0.32
for | bash | 229 | 93772 | 0.417 | 1.094 | 0.22
wc | bash | 115 | 67633 | 0.500 | 0.714 | 0.14

Read 2343 · aralıklı 1111 · rehber 294 · 2149111 tok · ham 8.064 → düz 11.191 M · aralıklı medyan 350 tok
limitsiz satır dağılımı (rehber dışı) | adet | ham M | düz M
1-100 | 404 | 0.979 | 1.369
101-300 | 257 | 0.944 | 1.376
301-500 | 62 | 0.764 | 1.032
501-1000 | 90 | 0.933 | 1.321
1001-2000 | 19 | 0.036 | 0.049
>2000 | 129 | 0.027 | 0.037

limitsiz >300 satır (ilk 10) | adet | satır | ham M | düz M
C:/Projeler/omer-skills/docs/denemeler/gorevler-okuma/fixture/degisiklik.diff | 16 | 837 | 0.229 | 0.315
C:/Projeler/omer-skills/tools/video/video/uygula.py | 4 | 365 | 0.168 | 0.239
C:/Projeler/omer-skills/tools/video/video/cli.py | 5 | 546 | 0.163 | 0.235
C:/Projeler/omer-skills/docs/kurulum-7.md | 2 | 342 | 0.154 | 0.211
C:/Projeler/omer-skills/tools/video/video/kur.py | 4 | 897 | 0.142 | 0.206
C:/Projeler/omer-skills/docs/denemeler/gorevler-okuma/fixture/test-ciktisi.txt | 5 | 634 | 0.104 | 0.143
C:/Users/pc/.claude/projects/C--Projeler-omer-skills/66fc22bf-232b-4fea-b0ca-07a4ea093db2/tool-results/bjaqbzqns.txt | 1 | 716 | 0.068 | 0.094
C:/Users/pc/Desktop/TELVE/src/prototip/sahne.ts | 2 | 369 | 0.062 | 0.085
C:/Projeler/omer-skills/tools/video/olcum_m4b.py | 3 | 436 | 0.058 | 0.080
C:/Projeler/omer-skills/tools/yukle10.py | 2 | 735 | 0.060 | 0.075

Bash ailesi (ilk 5, çıktı) | adet | token | medyan (rtk/rtksız) | rtk | pipe | tail/head | ham M | düz M
sed | 753 | 622708 | 573 (558/587.5) | 317 | 430 | 280 | 3.187 | 4.568
cat | 543 | 424254 | 293 (745.5/120) | 268 | 340 | 231 | 2.460 | 4.151
python | 1276 | 403479 | 126 (168/122) | 171 | 766 | 450 | 1.782 | 2.525
grep | 1013 | 367849 | 212 (190/315.0) | 783 | 911 | 694 | 1.701 | 2.506
ls | 655 | 223971 | 169 (173/122.0) | 581 | 517 | 438 | 1.112 | 1.623

tekrar okuma (ilk 10) | tekrar | değişmeden | aynı aralık | ham M | düz M
C:/Users/pc/Desktop/Kendi oyun modlarim/scripts/vucut2_yap.py | 28 | 24 | 0 | 0.324 | 0.445
C:/Projeler/omer-skills/tools/video/video/parti.py | 22 | 22 | 0 | 0.104 | 0.142
C:/Projeler/omer-skills/tools/video/video/akil.py | 41 | 37 | 0 | 0.091 | 0.126
C:/Projeler/omer-skills/tools/video/video/uygula.py | 31 | 29 | 0 | 0.087 | 0.123
C:/Projeler/omer-skills/tools/video/video/cli.py | 36 | 35 | 0 | 0.068 | 0.094
C:/Projeler/omer-skills/skills/blender-uretim/references/isik_kur.py | 15 | 15 | 0 | 0.060 | 0.082
C:/Projeler/omer-skills/tools/gorsel_uret.py | 12 | 10 | 0 | 0.045 | 0.062
C:/Projeler/omer-skills/tools/blender_dogrula.py | 11 | 11 | 0 | 0.043 | 0.060
C:/Users/pc/.claude/plugins/cache/thedotmack/claude-mem/13.25.2/hooks/hooks.json | 4 | 4 | 1 | 0.023 | 0.057
C:/Users/pc/Desktop/Kendi oyun modlarim/scripts/vucut1_analiz.py | 5 | 5 | 0 | 0.038 | 0.052

headroom_retrieve 229 · önceki araç {'Read': 64, 'Bash': 61, 'ToolSearch': 68, 'PowerShell': 1, 'Grep': 11, 'Write': 4, 'mcp__mcp-filesystem__read_text_file': 12, 'Edit': 2, 'mcp__blender__search_api_docs': 1, 'mcp__blender__execute_blender_code': 1, 'ExitPlanMode': 1, 'Skill': 3} · sn medyan 7.7 · tur medyan 1
tetikleyen Read (ilk 10) | adet | token | ham M | düz M
C:/Users/pc/Desktop/Kendi oyun modlarim/scripts/vucut2_yap.py | 9 | 13579 | 0.176 | 0.242
C:/Projeler/omer-skills/tools/video/video/akil.py | 6 | 9579 | 0.050 | 0.069
C:/Projeler/omer-skills/.kos/altin/86HM0RUWhCk/kaynak.txt | 1 | 9095 | 0.035 | 0.049
C:/Projeler/omer-skills/tools/video/video/parti.py | 6 | 6010 | 0.029 | 0.040
C:/Projeler/omer-skills/tools/video/olcum_m3b.py | 1 | 4710 | 0.024 | 0.033
C:/Users/pc/.claude/plans/gentle-sauteeing-conway.md | 1 | 2184 | 0.022 | 0.030
C:/Projeler/omer-skills/.kos/altin/kHtOSJRUkLs/kaynak.txt | 1 | 5745 | 0.018 | 0.025
C:/Projeler/omer-skills/tools/blender_bekci.py | 1 | 1828 | 0.017 | 0.023
C:/Projeler/omer-skills/.kos/altin/g89FJiNAlEs/kaynak.txt | 1 | 4957 | 0.015 | 0.020
C:/Users/pc/Desktop/TELVE/docs/storyboard.md | 1 | 998 | 0.012 | 0.016

tur: 13962 istek · araçlı 12294 · paralel 2410 (%19.6) · araç sayısı {'1': 9884, '2': 1710, '5': 68, '0': 1668, '3': 390, '6': 40, '4': 157, '9': 4, '12': 1, '7': 22, '10': 4, '8': 4, '14': 2, '15': 2, '29': 1, '13': 3, '11': 1, '20': 1} · küçük Read dizisi 50 (110 istek, kazanç 60 istek = 1.040 M)
arşiv | gerçek/tavan | oran
TOKEN-1.md | 21/25 | 0.84
TOKEN-1.md | 59/40 | 1.48
TOKEN-3b.md | 17/12 | 1.42
TOKEN-3b.md | 8/10 | 0.8
TOKEN-3b.md | 12/15 | 0.8
TOKEN-3b.md | 17/20 | 0.85
TOKEN-3b.md | 17/20 | 0.85
TOKEN-3b.md | 21/25 | 0.84
TOKEN-3b.md | 33/40 | 0.82
TOKEN-3b.md | 25/40 | 0.62

>200k oturum 85 · tek dalga 77 · çok dalga 8 · dalga bölme tasarrufu 7.020 M

kaldıraç günlük | ham M | düz M | Headroom örtüşmesi M
L8a eşik >300 satır | 0.119 | 0.165 | -0.046
L8a eşik >500 satır | 0.068 | 0.096 | -0.028
L8a eşik >1000 satır | 0.004 | 0.006 | -0.002
L8a eşik >2000 satır | 0.002 | 0.003 | -0.001
L8b | 0.021 | 0.030 | -0.010
L8b_ust | 0.317 | 0.457 | -0.140
L8c | 0.002 | 0.004 | -0.002
L8c_ust | 0.104 | 0.141 | -0.037
L7 küçük Read birleştirme | usage 0.074 | 4.3 istek/gün
L14 dalga bölme | usage 0.501
