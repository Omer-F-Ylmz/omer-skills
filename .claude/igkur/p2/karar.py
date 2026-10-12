"""IG-40-KUR P2 (sira 41–220) toplu karar: sirali.tsv + meta_p2.tsv → karar.tsv (d4 sütunları)."""
import csv, collections, sys
from pathlib import Path

BU = Path(__file__).parent
GIRDI = Path('C:/Projeler/omer-skills-wt/igkur/.claude/igkur/sirali.tsv')
DEVIR = Path('C:/Projeler/omer-skills/.kos/kopru/devir')
HEDEF = {'blender': 'blender-2', 'animasyon': 'animasyon-1', 'tasarim': 'tasarim-1', 'fable': 'fable-1', 'router': 'router-1'}

# anahtar → (karar, kanal, gerekce); listede olmayan teknik satır REF (genel ürün/model/platform/terim)
OZEL = {
    'makercheckersplit': ('UYARLA', 'CC+claude.ai(kendi)', 'departman-surec-inceleme Kapılar: yapan denetlemez, kabul denetimi taze bağlamlı ayrı alt ajanla'),
    'skillauthoringbestpractices': ('UYARLA', 'CC+claude.ai(kendi)', 'departman-surec-ajan-arac Kapılar: SKILL.md gövdesi ≤500 satır, fazlası references/'),
    'skilldescription': ('UYARLA', 'CC+claude.ai(kendi)', 'departman-surec-ajan-arac Kapılar: description 3. tekil kişi, ne yapar + ne zaman'),
    'asdste100': ('UYARLA', 'CC+claude.ai(kendi)', 'departman-belge Kapılar: STE ölçüsü (kısa cümle, etken çatı, tek anlam); standart metni kopyalanmaz'),
    'python': ('KURULU', 'CC', 'Python 3.12 kurulu'),
    'pytest': ('KURULU', 'CC', 'suitler pytest ile koşuyor'),
    'chrome': ('KURULU', 'CC', 'chrome-devtools MCP + playwright-cli karşılar'),
    'websearch': ('KURULU', 'CC', 'CC WebSearch + brave-search karşılar'),
    'cloudflare': ('KURULU', 'CC', 'security-audit skill kurulu (d4 sira 36)'),
    'sqlinjection': ('KURULU', 'CC', 'semgrep p/security-audit + departman-guvenlik kapsıyor'),
    'xss': ('KURULU', 'CC', 'semgrep p/security-audit + departman-guvenlik kapsıyor'),
    'snapzy': ('RED', '-', 'yalnız macOS; Windows karşılığı yok, ekran kaydı ffmpeg ile'),
    'screenstudio': ('RED', '-', 'ücretli + yalnız macOS'),
    'mixboard': ('RED', '-', 'Google Labs deneyi kapatıldı (ölü)'),
    'opal': ('REF', '-', 'kapanıyor; yerine Gemini skills, bizde CC skill düzeni var'),
    'browseruse': ('REF', '-', 'd4 kararı: bulut LLM anahtarı ister; agent-browser + chrome-devtools karşılar'),
    'yamliaklar': ('REF', '-', 'Archon YAML iş akışı; d4 kararı: gsd/departman-surec-plan karşılar'),
    'sona': ('REF', '-', 'Ruflo öz-öğrenme; RUFLO-1 görevi yürütüyor (çift iş yok)'),
    'ruvector': ('REF', '-', 'Ruflo vektör DB; RUFLO-1 görevi yürütüyor'),
    'aidefence': ('REF', '-', 'Ruflo güvenlik katmanı; RUFLO-1 görevi yürütüyor'),
    'openchatcut': ('REF', '-', 'AGPL-3.0 masaüstü video düzenleyici; video-uygula + ffmpeg karşılar'),
    'camofoxbrowser': ('REF', '-', 'bot tespiti atlatma tarayıcısı; kurulmaz (hizmet şartı riski)'),
    'librechat': ('REF', '-', 'kendi sunuculu sohbet arayüzü; CC/claude.ai ile çakışır'),
    'meetily': ('REF', '-', 'masaüstü toplantı not uygulaması; kapsam dışı, gerekirse Ömer kurar'),
    'airllm': ('REF', '-', 'katman katman GPU yükleme; yerel büyük model kullanmıyoruz'),
    'katmankatmankarm': ('REF', '-', 'AirLLM yöntemi; yerel büyük model kullanmıyoruz'),
    'filebrowser': ('REF', '-', 'repo arşivlenmiş; dosya gezintisi gerekmiyor'),
    'billionmail': ('REF', '-', 'AGPL e-posta sunucusu; kapsam dışı'),
    'elevenlabs': ('REF', '-', 'ses servisi, hesap ister; gerekirse elevenlabs/elevenlabs-mcp (MIT)'),
    'youtubeapi': ('REF', '-', 'Google API anahtarı ister; video-tarama yt-dlp ile karşılar'),
    'stax': ('REF', '-', 'Google ürünü; kendi testli A/B karşılaştırma olcum kosucu ile var'),
    'codewiki': ('REF', '-', 'Google ürünü; graphify wiki karşılar'),
    'gemininotebook': ('REF', '-', 'NotebookLM; graphify + markitdown karşılar'),
    'adaptaviralreel': ('REF', '-', 'içerik üretim akışı; reel yapı analizi video-tarama raporunda var'),
    'jev': ('REF', '-', 'TypeSafe kapalı modeli; bizim jev aracıyla yalnız ad benzerliği'),
    'localllamatypeddecisions': ('REF', '-', 'kıyas veri seti; repo bulunamadı'),
}


def oku(yol):
    r = list(csv.reader(open(yol, encoding='utf-8'), delimiter='\t'))
    return [dict(zip(r[0], x)) for x in r[1:]]


def meta():
    m = {}
    for s in open(BU / 'meta_p2.tsv', encoding='utf-8'):
        p = s.rstrip('\n').split('\t')
        if len(p) >= 4:
            m[p[0]] = (p[1], p[2] or 'yok', f'★{p[3]}')
    return m


def karar_ver(d, m):
    if d['devir'] != '-':
        return 'DEVIR', HEDEF[d['devir']], f"{d['devir']} departman ajanı yapıyor"
    k = OZEL.get(d['anahtar'])
    if k:
        return k
    return 'REF', '-', 'genel ürün/model/platform/terim; kurulacak araç değil'


def main():
    m = meta()
    satir, dagilim, eksik = [], collections.Counter(), []
    devir_metin = {h: (DEVIR / f'{h}.tsv').read_text(encoding='utf-8', errors='ignore').lower()
                   for h in HEDEF.values() if (DEVIR / f'{h}.tsv').exists()}
    for d in oku(GIRDI):
        if not 41 <= int(d['sira']) <= 220:
            continue
        karar, kanal, gerekce = karar_ver(d, m)
        repo, lisans, yildiz = m.get(d['anahtar'], (d['repo'], d['lisans'], ''))
        if karar == 'DEVIR' and d['anahtar'] not in devir_metin.get(kanal, '') and d['ad'].lower() not in devir_metin.get(kanal, ''):
            eksik.append(f"{d['sira']}:{d['anahtar']}→{kanal}")
        if yildiz and karar not in ('DEVIR',):
            gerekce += f' ({yildiz})'
        satir.append([d['sira'], d['ad'], repo, lisans, karar, kanal, gerekce])
        dagilim[karar] += 1
    with open(BU / 'karar.tsv', 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(['sira', 'ad', 'repo', 'lisans', 'karar', 'kanal', 'gerekce']) + '\n')
        for s in satir:
            f.write('\t'.join(c.replace('\t', ' ') for c in s) + '\n')
    print(len(satir), dict(dagilim))
    print('devir TSV\'de yok:', len(eksik), ' '.join(eksik))
    return satir, dagilim


if __name__ == '__main__':
    satir, dagilim = main()
    assert len(satir) == 180 and sum(dagilim.values()) == 180
    assert all(s[4] in ('KUR', 'UYARLA', 'REF', 'RED', 'DEVIR', 'KURULU') for s in satir)
    sys.exit(0)
