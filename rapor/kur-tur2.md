# KUR-TUR2 raporu (7 Kas 2026)

Girdi: kurulum-d2-sonuc.tsv son durum: HATA 115 + KURULUM-YOLU-YOK 106 + KURULDU-DOGRULANMADI 24 = 245 kalem. Hepsi planda eylem aldı (rapor/kur-tur2-plan.tsv).

| Neden grubu (kanıt) | Çözüm | Kalem |
|---|---|---|
| SKILL.md yok: repo CLI/paket/MCP/uygulama (klon dizini incelendi) | sınıf düzelt SKILL→CLI/PAKET (D2); .claude-plugin → PLUGIN; .claude/commands → KOMUT | 66 |
| Yarım/boş klon (HEAD yok; HY-WU, skool-platinum) | klonla(): HEAD yoksa _arsiv'e taşı, yeniden klonla; ls-remote boşsa çözümsüz (topview, invoice-follow-up) | 4 |
| bin'siz npm deposu → HATA (kod hatası: bin yokken `npm i -g` çalışıyordu) | bin yoksa global kurma; release/derleme; yoksa KURULDU-KAYNAK | 11 |
| repo çok büyük 10 / klon zaman aşımı 1 / checkout hatası 1 | SKILL: blobsuz+seyrek klon (yalnız SKILL dizinleri); CLI: release/derleme; --tur2 600 sn | 12 |
| npm EBUSY 6 (ana-liste-npm içinde çalışan iobroker süreci, PID 71552, dosyaları kilitliyor) | kalem başına ayrı --prefix (ana-liste-npm-t2); süreç öldürülmedi | 6 |
| npm SKILL 0 skill 12 | npm view bin → CLI ya da PAKET | 12 |
| pip/uv 13: 9'u izole `uv pip --dry-run` rc=0 (toplu koşuda çakışma); Free Claude Code requires-python≥3.14; Podman/dots flat-layout | sıralı (--is 1), uv_zincir'e py3.14, pyproject başarısızsa release yoluna düş | 12 |
| YOLU-YOK: cargo/go/cmake kaynağı | kaynak_derle(): cargo (workspace dahil) → go install → cmake VS2022 | 14 |
| YOLU-YOK: Linux araçları, WSL Ubuntu'da apt adayı var (apt-cache policy ile görüldü) | WSL `apt-get install` (aircrack-ng, wifite, tshark, binwalk, vim, wget, tar, rtmpdump, whatweb, fakeroot, dnf, afl++) | 11 |
| YOLU-YOK: repo Claude eklentisi | claude plugin marketplace add + install | 12 |
| DOĞRULANMADI 24 (komut adı/--version) | gerçek bin adı (npm view bin / uv tool list), --version/--help, hata satırı kanıt | 24 |
| ZeroGPT: PIL yok | venv'e pillow | 1 |

Çözümsüz kalan 73 (neden planda): kurulacak kod/release yok, yalnız README/boş 42; Windows yolu yok (Makefile/Linux) 14; winget kimliği doğrulanamadı 7 (nmap, Gradle, NSIS, Chocolatey, nvm-windows, Poppler, JADX); Arch/AUR 2 + BlackArch; Linux-only: systemd, Sealos, gVisor; Scoop (curl|iex yasağı); oMLX (bağımlılık git klonunda geçersiz yol, MLX Apple Silicon); sound engine (node-gyp+vcpkg portaudio); AnyPs5 (release'te exe yok).
Kodda düzeltilenler (kurulum_d2.py): klonla HEAD denetimi, seyrek_ac, bin'siz npm, pyproject→release düşüşü, kaynak_derle, py3.14, kalem başına npm prefix. Birim test: tests/test_kurulum_tur2.py (6, kırmızı görüldü).

Ömer'in TEK komutu: `.\tools\kurulum_tur2.ps1`  (önce `-Deneme`: HATA 0, 94 sn; kurulum yok). Sonuç: rapor\kur-tur2-sonuc.tsv.
Kullanılmayan uygun araç: Roast Room/jev (karar kuralları kanıta dayalı, yargı gerekmedi).
