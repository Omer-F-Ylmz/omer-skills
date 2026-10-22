Örnek (kod):
İstek: "Python fonksiyonu yaz: liste_tekrarsiz(l) — sırayı koruyarak tekrarları at."
Yanıt:
```python
def liste_tekrarsiz(l):
    g = set()
    return [x for x in l if not (x in g or g.add(x))]
```
Kontrol: [3,1,3,2,1] -> [3,1,2]; [] -> [] ✔
