"""ASR hattı: ücretsiz API'ler sırayla, yerel large-v3 yalnız kota/ağ hatasında yedek.

Sıra (wer_hakem.py leave-one-out ölçümü, fark gürültü içinde): groq → gemini → yerel. Groq verbose_json segment avg_logprob'u
30 sn'lik pencere başına sabit geliyor (güven eşiği ayırt etmez), bu yüzden eşikli oylama yok; hata → sıradaki kaynak.
Kullanım: python tools/asr_hat.py <wav>   (metin ve kullanılan kaynak yazdırılır)
"""
import sys
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def yerel(wav):
    import video_derin as vd  # CUDA DLL PATH'i süreçte kurulur
    from faster_whisper import WhisperModel

    seg, _ = WhisperModel("large-v3", device="cuda", compute_type=vd.WHISPER["cuda"][1]).transcribe(str(wav), language="tr", vad_filter=True)
    return " ".join(s.text for s in seg)


def varsayilan():
    import wer_altin as wa

    return [("groq", wa.groq), ("gemini", wa.gemini), ("yerel", yerel)]


def donustur(wav, kaynaklar=None):
    """(metin, kullanılan kaynak). Kota (429/503), ağ ya da zaman aşımı → sıradaki; son kaynak hata verirse yükselir."""
    kaynaklar = kaynaklar or varsayilan()
    for ad, f in kaynaklar:
        try:
            metin = f(wav)
            if metin and metin.strip():
                return metin, ad
        except (urllib.error.URLError, TimeoutError, KeyError) as e:  # HTTPError URLError'ın alt sınıfı; KeyError = anahtar yok
            if ad == kaynaklar[-1][0]:
                raise
            print(f"asr_hat: {ad} düştü ({type(e).__name__} {getattr(e, 'code', '')}), sıradaki", file=sys.stderr)
    raise RuntimeError("tüm kaynaklar boş döndü")


if __name__ == "__main__":
    t, k = donustur(Path(sys.argv[1]))
    print(k, "|", t)
