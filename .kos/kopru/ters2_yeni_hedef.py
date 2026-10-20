"""TERS-2 d2: hedefler.json'a 3 yeni hedef (site ses, js ortak-js, dotnet Halka) ekler; tekrar koşulursa eklemez."""
import json
from pathlib import Path

P = Path(r"C:\Projeler\omer-skills\docs\ters\kapi\hedefler.json")
K = "C:/Projeler/omer-skills/"
DN = K + ".kos/kopru/ogren/lab/test-qa/dn/Halka/"


def m(madde, dosya, satir, alinti): return {"madde": madde, "kanit": {"dosya": dosya, "satir": satir, "alinti": alinti}}


YENI = [
    {"id": 11, "ad": "ses", "tur": "site", "yol": K + "labs/ses/index.html", "sayfa": "/ses/index.html",
     "kaynaklar": [K + "labs/ses/index.html", K + "labs/ortak.js"],
     "sorular": "Ses laboratuvari sayfasinda kaydirmayla ilerleyen kamera ve ses dugmesi nasil kurulmus?",
     "maddeler": [
         m("Sayfa tek canvas uzerinde Three.js sahnesi cizer; renderer ve kamera ortak kur() ile, sahne dunya() ile kurulur.", K + "labs/ses/index.html", 18, "const { r, kam } = kur(cv);"),
         m("Kamera, konum ve hedef noktalari dizisinden kameraYolu ile 0..1 ilerleme degerine gore yol boyunca gezer.", K + "labs/ses/index.html", 20, "const git = kameraYolu(kam,"),
         m("Kaydirma Lenis ile yumusatilir; ScrollTrigger ile gsap.to(o, {t:1}) ilerlemeyi scrub eder ve her guncellemede sahne yeniden cizilir.", K + "labs/ses/index.html", 29, "gsap.to(o, { t: 1, ease: 'none', onUpdate() { iste(); sx.ayarla(o.t); }, scrollTrigger: kosu() });"),
         m("Sag ustteki #ses dugmesi aria-pressed ile ses acma/kapamayi taşir; ses motoru kaydirma ilerlemesini sx.ayarla(o.t) ile alir.", K + "labs/ses/index.html", 24, "const sx = ses(dugme);"),
         m("Sahne kahve temali: tornalanmis bakir cezve, seramik fincanlar, koz halkasi ve isik/sis ortak.js dunya() icinde uretilir.", K + "labs/ortak.js", 37, "const cezve = new THREE.Mesh(new THREE.LatheGeometry("),
     ]},
    {"id": 12, "ad": "ortak-js", "tur": "js", "yol": K + "labs/ortak.js", "kaynaklar": [K + "labs/ortak.js"],
     "sorular": "ortak.js laboratuvar yardimci kutuphanesi neler sagliyor ve nasil calisiyor?",
     "maddeler": [
         m("window.lab sozlesmesi kare sayaci, hazir bayragi ve git() ile disaridaki kare.py'nin sayfayi okumasini saglar.", K + "labs/ortak.js", 9, "export const lab = (window.lab = { kare: 0, hazir: false, git: async () => {} });"),
         m("kur() WebGLRenderer'i ACES ton esleme ve en cok dpr piksel orani ile kurar, resize'da boyutu ve kamera en-boy oranini gunceller.", K + "labs/ortak.js", 13, "const r = new THREE.WebGLRenderer({ canvas: cv, antialias: true, alpha: true, powerPreference: 'high-performance' });"),
         m("dunya() sahneyi RoomEnvironment'tan PMREM ortam haritasi ile aydinlatir; cezve, fincanlar ve koz halkasi LatheGeometry/Torus ile uretilir.", K + "labs/ortak.js", 32, "s.environment = new THREE.PMREMGenerator(r).fromScene(new RoomEnvironment(), 0.04).texture;"),
         m("arka null verilirse sahne saydam olur: arka plan, sis ve zemin eklenmez, yalniz arka verildiginde FogExp2 ve zemin plani konur.", K + "labs/ortak.js", 64, "if (arka !== null) {"),
         m("kaydir() Lenis'i ScrollTrigger ile tek saatte birlestirir (gsap.ticker) ve lab.git(p) sayfayi anlik p oranina atlatip scrub yetissin diye 1800 ms bekler.", K + "labs/ortak.js", 75, "export function kaydir() {"),
     ]},
    {"id": 13, "ad": "Halka", "tur": "dotnet", "yol": DN.rstrip("/"), "derlenmis": DN + "bin/Debug/net10.0/Halka.dll",
     "kaynaklar": [DN + "Class1.cs", DN + "bin/Debug/net10.0/Halka.dll"],
     "sorular": "Halka kutuphanesindeki HalkaTampon nasil calisiyor?",
     "maddeler": [
         m("Halka ad alaninda genel tipli mühürlü HalkaTampon<T> sinifi var.", DN + "Class1.cs", 3, "public sealed class HalkaTampon<T>"),
         m("Kapasite kurucuda sabit bir dizi olarak ayrilir; sifir ya da negatif kapasite ArgumentOutOfRangeException firlatir.", DN + "Class1.cs", 11, "if (kapasite <= 0) throw new ArgumentOutOfRangeException(nameof(kapasite));"),
         m("Ekle() ogeyi (_bas + _sayi) % uzunluk konumuna yazar; modulo ile dizi basa sarar.", DN + "Class1.cs", 19, "_ogeler[(_bas + _sayi) % _ogeler.Length] = oge;"),
         m("Tampon doluyken Ekle en eski ogenin ustune yazar: _bas ileri alinir, Sayi artmaz.", DN + "Class1.cs", 20, "if (_sayi == _ogeler.Length) _bas = (_bas + 1) % _ogeler.Length;"),
         m("TryAl() en eskiyi (FIFO) dondurur ve boskeyken false verip default dondurur; basarida _bas ilerler, _sayi azalir.", DN + "Class1.cs", 26, "if (_sayi == 0) { oge = default!; return false; }"),
     ]},
]

d = json.loads(P.read_text(encoding="utf-8"))
var = {h["id"] for h in d["hedefler"]}
d["hedefler"] += [h for h in YENI if h["id"] not in var]
P.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print(len(d["hedefler"]))
