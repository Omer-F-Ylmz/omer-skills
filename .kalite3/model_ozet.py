import csv, collections

def f(x, k):
    try:
        return float(x[k])
    except ValueError:
        return None

r = [x for x in csv.DictReader(open('docs/kutuphane/olcum/kalite3-model.tsv', encoding='utf-8'), delimiter='\t')
     if x['kip'].startswith('karsi')]
g = collections.defaultdict(dict)
for x in r:
    g[(x['aile'], x['ajan'])][x['kol']] = x
for k, v in sorted(g.items()):
    s = ' '.join(f"{m}:{v[m]['puan']}/${f(v[m],'usd') or 0:.3f}/{int(f(v[m],'jeton') or 0)//1000}k/{f(v[m],'sure') or 0:.0f}s"
                 for m in sorted(v))
    print(f'{k[0]}|{k[1]}|{s}')
print(len(r), 'satir', len(g), 'ajan')
