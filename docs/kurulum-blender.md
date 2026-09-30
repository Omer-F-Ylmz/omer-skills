# Blender + resmi Blender Lab MCP (KURULUM-3D, 2026-10-01)

Blender 5.2.1 LTS kurulu (`C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`, PATH'te değil); resmi MCP en az 5.1 istiyor.
Sunucu: `C:\blender_mcp` (projects.blender.org/lab/blender_mcp, dbbf836, GPL-3.0) · user scope: `claude mcp add -s user blender -- uv --directory C:\blender_mcp\mcp run blender-mcp`.

## Ömer'in elle adımları
1. Blender → Düzen › Tercihler › Sistem › **Allow Online Access** açık.
2. `https://projects.blender.org/lab/blender_mcp/releases/download/v1.0.3/mcp-1.0.3.zip` Blender'a bir kez sürükle-bırak → "Diskten Yükle" penceresi (User Default + Enable Add-on) → TAMAM; ikinci bırakma gerekmez.
3. Eklenti Auto Start AÇIK ve Host `localhost` ile gelir, kurulur kurulmaz sunucuyu başlatır → Düzen › Tercihler › Eklentiler › MCP: **Stop MCP Server**, Host = `127.0.0.1` (Port 9876), Auto Start kapat.
4. Oturum alışkanlığı: .blend aç → **Start MCP Server** → iş → **Stop MCP Server**.

## Güvenlik
- Sunucu modelin ürettiği Python'u Blender'da korumasız çalıştırır (belge: "without any guards"); kullanıcı yetkisiyle dosya/ağ erişimi var.
- Her oturumdan önce .blend kaydedilir; varlıklar yalnız projenin klasöründe: `<Proje>\blender\` (ör. `C:\Users\pc\Desktop\TELVE\blender\`).
- Soket yalnız 127.0.0.1; Blender'da yalnız o işin .blend dosyası açıkken bağlanılır; iş bitince Stop MCP Server.
- Paralel çalışma: Blender'ı aynı anda tek CC oturumu sürer.
- Topluluk blender-mcp (ahujasid) kurulmaz: 4 CVE, kimliksiz soket, varsayılan telemetri.

## Dört ölçüt
- Bakım: Blender Foundation Lab, v1.0.3, son commit 2026-09-29.
- CC'de çift mi: hayır (başka Blender MCP yok).
- İzin kapsamı: Blender süreci içinde keyfi Python = kullanıcı düzeyinde tam yetki.
- Context maliyeti: stdio MCP; araç şemaları ToolSearch ile ertelenir, oturum başı yalnız ad listesi (ölçülmedi).
