# jev-dotnet — kopyalanabilir Jev istemcisi (.NET 10, NuGet paketi değil)

`Jev/` klasörünü projene kopyala. Bağımlılıklar: Microsoft.Extensions.Http, Options.ConfigurationExtensions. Testler: `dotnet test Jev.Tests`.

- `IJevClient` / `JevClient`: typed HttpClient, 408/429/5xx tekrarı (Retry-After), çift tavan (`MaxBatches` ≤200'lük parça · `MaxRequests` HTTP, tekrarlar dahil; ikisi de ağa çıkmadan kontrol edilir), `BatchAsync` ≤8 eşzamanlı.
- `TurkishRedactor`: anahtar · IBAN · kart (Luhn) · TCKN · telefon · e-posta. **Kapatılamaz**: `JevClient` her state'e önce bunu uygular, `IStateRedactor` kayıtları ek katmandır.
- `JevBands`: varsayılan 0.85/0.60; noul kesinliği max(p, 1−p). `FakeJevClient`: ağsız test ikizi.

```csharp
builder.Services.AddJev(builder.Configuration);   // "Jev": { "ApiKey": "<secret store>", "Model": "jev-1.13", "MaxRequests": 500 }
```

> **KVKK:** state (müşteri mesajı, belge metni) yurt dışındaki sağlayıcıya gider. Redaksiyon kişisel veriyi azaltır ama sıfırlamaz. Canlıya almadan önce `use-case-triage` (gerekirse `pia-generation`) çalıştır.

## Intent routing
```csharp
var q = new Dictionary<string, JevQuestion>
{
    ["niyet"] = new("choice", "`mesaj` hangi ekibin işi?", new Dictionary<string, string?>
    {
        ["kargo"] = "Gönderi, teslimat, takip", ["iade"] = "Geri gönderme, değişim",
        ["ödeme"] = "Çekim, fatura, para iadesinin hesaba geçmesi",
    }),
    ["acil"] = new("noul", "`mesaj` bugün dönüş gerektiriyor mu?"),
};
var a = await jev.EvaluateAsync(mesaj, q, ct);
var bands = JevBands.From(options.Value);
var kuyruk = bands.Of(a["niyet"]) == Band.Act ? a["niyet"].Choice! : "insan-triage";
var oncelik = a["acil"].Noul >= 0.5 && bands.Of(a["acil"]) != Band.Escalate ? "yüksek" : "normal";
```

## Composite scoring
```csharp
var q = new Dictionary<string, JevQuestion>
{
    ["uyum"] = new("score", "Aday ilanın gereksinimlerine ne kadar uyuyor?", new[] { "hiç", "kısmen", "büyük ölçüde", "tam" }),
    ["deneyim"] = new("score", "İlgili deneyim düzeyi?", new[] { "yok", "az", "orta", "çok" }),
    ["risk"] = new("noul", "Özgeçmişte tutarsızlık var mı?"),
};
var sonuclar = await jev.BatchAsync(adaylar.Select(x => x.Metin).ToList(), q, ct);
var puanlar = adaylar.Zip(sonuclar, (x, a) => (x.Id,
    Puan: 0.5 * a["uyum"].Score!.Value / 3 + 0.3 * a["deneyim"].Score!.Value / 3 + 0.2 * (1 - a["risk"].Noul!.Value),
    Guven: a.Values.Min(JevBands.Certainty)))
  .OrderByDescending(x => x.Puan);   // Guven düşükse puanı gösterme, insana gönder
```

## Confidence routing
```csharp
var a = await jev.EvaluateAsync(talep, new Dictionary<string, JevQuestion>
{
    ["onay"] = new("noul", "`talep` iade politikasına uyuyor mu?", new Dictionary<string, string> { ["true"] = "30 gün içinde, faturalı", ["false"] = "süre dışı ya da belgesiz" }),
}, ct);
switch (bands.Of(a["onay"]))
{
    case Band.Act: await (a["onay"].Noul >= 0.5 ? iade.OnaylaAsync(id) : iade.ReddetAsync(id)); break;
    case Band.Flag: await kuyruk.EkleAsync(id, "hızlı-inceleme", a["onay"].Noul); break;
    default: await kuyruk.EkleAsync(id, "uzman", a["onay"].Noul); break;   // Escalate: otomatik karar yok
}
```

## Select, not generate (OCR adayından alan seçimi)
```csharp
// Jev metin üretmez; OCR'ın çıkardığı adaylar arasından seçer. Değer her zaman belgede geçen bir dizedir.
var adaylar = ocr.Satirlar.Where(s => Regex.IsMatch(s, @"\d")).Distinct().Take(254).ToList();
var q = new Dictionary<string, JevQuestion>
{
    ["toplam"] = new("choice", "Faturanın ödenecek genel toplamı hangisi?",
        adaylar.Append("yok").ToDictionary(s => s, s => (string?)null)),
};
var a = await jev.EvaluateAsync(ocr.TamMetin, q, ct);
var toplam = a["toplam"].Choice is { } c && c != "yok" && bands.Of(a["toplam"]) == Band.Act ? c : null;   // null → elle giriş
```

## Hiyerarşik sınıflama (tools/jev `jev skill`'in iki aşaması)
```csharp
// Aşama 1: çok sayıda sınıf ≤210'luk dilimlere bölünür, her dilim bir choice + "hiçbiri"; tek istek.
var dilimler = siniflar.OrderBy(s => s.Ad).Chunk(210).ToList();
var s1 = dilimler.Select((d, i) => (Key: $"d{i}", Q: new JevQuestion("choice", "`istem` hangi sınıfın işi?",
    d.ToDictionary(s => s.Ad, s => (string?)s.Aciklama).Append(new("hiçbiri", "hiçbiri uymuyor")).ToDictionary()))).ToDictionary(x => x.Key, x => x.Q);
var a1 = await jev.EvaluateAsync(istem, s1, ct);
var ilk = a1.Values.SelectMany(x => x.Probabilities!).Where(p => p.Key != "hiçbiri" && p.Value >= 0.02)
    .OrderByDescending(p => p.Value).Take(10).Select(p => p.Key).ToList();
// Aşama 2: aday başına noul, açıklama criteria'da; tek istek. Yalnız p ≥ act olanlar döner.
var s2 = ilk.Select((ad, i) => (Key: $"a{i}", Q: new JevQuestion("noul", $"`istem` `{ad}` sınıfının işi mi?",
    new Dictionary<string, string> { ["true"] = aciklama[ad], ["false"] = "değil" }))).ToDictionary(x => x.Key, x => x.Q);
var a2 = await jev.EvaluateAsync(istem, s2, ct);
var sonuc = ilk.Where((ad, i) => a2[$"a{i}"].Noul >= 0.85).ToList();
```
