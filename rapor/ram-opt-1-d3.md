# ram-opt-1-d3 (28 Eki)
Kok: tools/mcp_paylasim.py PAYLASIM yalniz 21 durumsuz adi sunuyordu; onay/ram_opt_1_d3.py 9 adi "havuzda yok" goruyordu.
Yapilan: PAYLASIM'a mcp-filesystem mcp-git obsidian claude-design binlog claude-mem puppeteer playwright blender eklendi; ~/.claude/mcp-paylasim/sunucular.json'a proxy_config ile 9 girdi eklendi (env degeri yazdirilmadi); mcp-proxy (47800) yeniden baslatildi (bekci kaldirdi).
--kuru: 9/9 havuzda (14,12,7,23,46,17,8,25,26 arac). Gercek kosu: Desktop config'te 9 sunucu mcp_koprusu.py'ye cevrildi (25 sunucu). Etki icin Desktop yeniden baslatilmali.
Geri alma: `python -X utf8 onay/ram_opt_1_d3.py --geri` (yedek claude_desktop_config.json.ram-opt-1-d3.bak); ek yedek ...ram-opt-1-d3-onceki.bak (script oncesi); havuz: ~/.claude/mcp-paylasim/sunucular.json.ram-opt-1-d3.bak + git revert. Not: scripti `python -X utf8` ile kos (cp1254 '→' hatasi).
Dogrulama bekliyor: Desktop yeniden baslatma sonrasi 9 sunucunun araclari + tek kopya surec sayisi.
