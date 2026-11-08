# memvid (A13), WSL kurulumu

Defender istisnası yok; Windows tarafında Tantivy IO hatası (os error 5) olduğu için WSL (Ubuntu) kullanılır.

- venv: `/root/memvid/.venv` (`memvid-sdk`, Python 3.14), betik `/root/memvid/build.py`
- Kasa: `/mnt/c/Users/pc/Desktop/Obsidian` → üst klasör başına `~/memvid/obsidian-<klasör>-<n>.mv2` (13 dosya, en büyüğü 25,6 MB < 45 MB)
- Bilinen sınır: `put_many` toplu çağrısı WAL'i bozuyor (MV012); build.py tek tek ekler. Var olan .mv2 atlanır, yeniden kurmak için dosyayı silip betiği çalıştır.

## Kullanım

```powershell
wsl -d Ubuntu -u root -e bash -c "cd /root/memvid && .venv/bin/python -c \"import memvid_sdk,glob;[print(f, h['title']) for f in glob.glob('*.mv2') for h in memvid_sdk.Memvid(f).find('parsel',k=3)['hits']]\""
wsl --shutdown   # işin bitince RAM'i geri ver
```

## Sınama (27 Eki)
- "parsel": 2 isabet (`root-1`: 2026-10-27-parsel-drone-video.md; `20-icgoru-1`)
- "clodfarm": 0 isabet, kasada metin olarak geçmiyor (Grep ile de 0 doğrulandı)
