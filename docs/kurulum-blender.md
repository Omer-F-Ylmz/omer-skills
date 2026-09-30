# Blender + resmi Blender Lab MCP (KURULUM-3D, 2026-10-01)

Blender 5.2.1 LTS kurulu (`C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`, PATH'te değil); resmi MCP en az 5.1 istiyor.
Sunucu: `C:\blender_mcp` (projects.blender.org/lab/blender_mcp, dbbf836, GPL-3.0) · user scope: `claude mcp add -s user blender -- uv --directory C:\blender_mcp\mcp run blender-mcp`.

## Ömer'in elle adımları
1. Blender → Edit › Preferences › System › **Allow Online Access** açık (eklenti kapalıyken sunucuyu başlatmıyor).
2. Eklenti: `https://projects.blender.org/lab/blender_mcp/releases/download/v1.0.3/mcp-1.0.3.zip` → Blender'a iki kez sürükle-bırak (1. depo, 2. eklenti) ya da Install from Disk.
3. Eklenti tercihleri: **Host = 127.0.0.1** (varsayılan `localhost`), Port 9876; autostart kapalı kalsın.
4. İşin .blend dosyasını aç → eklenti tercihlerinde **Start MCP Bridge Server** → CC'de yeni oturum.

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
