# Blender Lab MCP (resmi)

- Kaynak: https://projects.blender.org/lab/blender_mcp · belge https://www.blender.org/lab/mcp-server/
- Durum: user scope'ta kurulu (2026-10-01, KURULUM-3D); ayrıntı `docs/kurulum-blender.md`.
- Lisans: GPL-3.0 (yalnız yerel kullanım; kodu dağıtırsak kaynak açma yükümlülüğü doğar).
- Güvenlik: modelin Python'u Blender'da korumasız koşar; Online Access şart; Host 127.0.0.1'e çekilir; kayıtlı .blend + proje klasörü + tek CC oturumu.
- Bakım: Blender Foundation Lab, v1.0.3, son commit 2026-09-29, 25 yıldız.
- CC'de çift mi: hayır; topluluk sürümü (ahujasid) bilerek kurulmadı.
- İzin kapsamı: Blender süreci içinde keyfi Python (kullanıcı düzeyi dosya/ağ).
- Context maliyeti: stdio MCP, araçlar ertelenmiş; oturum başı yalnız ad listesi (ölçülmedi).
