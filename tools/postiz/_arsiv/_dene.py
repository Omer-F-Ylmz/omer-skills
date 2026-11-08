import sys; sys.path.insert(0, '.')
import yayinci
b = {"type": "draft", "date": "2026-11-01T12:00:00.000Z", "shortLink": False, "tags": [],
     "posts": [{"integration": {"id": "yok-bogus"}, "value": [{"content": "t", "image": []}], "group": "g", "settings": {"__type": "youtube", "title": "t", "type": "private", "selfDeclaredMadeForKids": "no"}}]}
r = yayinci.istek("/posts", m="POST", json=b)
print(r.status_code, r.text[:300])
