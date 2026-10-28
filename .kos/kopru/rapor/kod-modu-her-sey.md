TUR BITTI (KOD-MODU-HER-SEY: Bölüm 2 tam, Bölüm 1 ölçüldü ama azaltma uygulanmadı)
BÖLÜM 2 (tools/arka_uygulama.py + docs/arka-uygulama.md): 122 uygulama → başsız 41 · sanal masaüstü 57 · yok/izinle 24 (+31 bileşen). Blender -b render ve sanal masaüstünde notepad: ön plan penceresi AYNI, sızan pencere 0; VRAM ≤1,5/12,3 GB, RAM ≤%78.
BÖLÜM 1 ölçüm (boş oturum, haiku, --strict-mcp-config, toplam girdi jetonu): taban 139,4k (11,5k + 109,6k yazım + 18,2k okuma, $0,116) · --disable-slash-commands 69,2k ($0,013) → skill/komut katmanı ≈ 70k.
Denenen azaltma 1: 1748 eklenti skill'i user-invocable-only (--settings ile) → 134,7k (−4,7k, %3). Tüm skill'ler user-invocable-only → 134,4k (−5k). Denenen azaltma 2: skillListingBudgetFraction 0,02→0,002 → 139,4k (etkisiz).
Sonuç: skill adlarını gizlemek yükü düşürmüyor (listeleme bütçesi zaten kırpıyor; /context: Skills 52k, Custom agents 32k, System tools 13,8k, Memory 9k). Kaldıraç ajan tanımları (290 ajan = 32k) ve skill/komut katmanının asıl kaynağı; ikisi de silme/kapatma gerektirir → yapılmadı. Global ayara dokunulmadı, araç eklenmedi (kural: araç kaldırılmaz).
Tam (MCP'li) kol bu turda da asıldı (240 sn, çıktı 0 bayt; RAM %75'te bile) → 3 örnek iş jeton A/B ve bağımsız hakem YAPILMADI. (c) CLI kapısı = arka_uygulama.py komut; (a) kapı = arac_ara.py --tam zaten var.
AÇIK: tam kolun asılma nedeni (MCP başlatma), ajan tanımı yükü (32k) için silmeden yol, ComfyUI üretim düşmesi (WinError 10054/10061).
Ölçüm oturumları tek tek, RAM ≤%85 kapısıyla koştu; hepsi --strict-mcp-config (MCP süreci açılmadı).
