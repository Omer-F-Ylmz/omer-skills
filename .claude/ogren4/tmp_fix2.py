import json
p = r'C:\Projeler\omer-skills\.claude\ogren4\v2-yazar-2.jsonl'
L = [json.loads(l) for l in open(p, encoding='utf-8')]
h = "=== kayıt: C:\\Users\\pc\\.claude.json · mcpServers · premiere-pro ==="
for d in L:
    if d['ad'] == 'premiere-pro':
        d['ne_yapar'] = {"deger": "belirsiz — yalnız stdio MCP sunucu kaydı: node ile adobe-premiere-pro-mcp paketinin dist/cli.js dosyasını başlatır; aracın işi kaynakta anlatılmıyor", "alinti": h}
        d['komut'] = {"deger": "belirsiz — kayıt MCP sunucusunu başlatan yapılandırma; kullanıcıya dönük komut/araç çağrısı yok", "alinti": h}
        d['sinirlar'] = {"deger": "belirsiz — kaynakta uyarı/gereksinim/sınır yok", "alinti": h}
        d['mekanizma'] = ["kurgu"]
        d['kanit'] = "adobe-premiere-pro-mcp"
open(p, 'w', encoding='utf-8', newline='\n').write(''.join(json.dumps(d, ensure_ascii=False) + '\n' for d in L))
