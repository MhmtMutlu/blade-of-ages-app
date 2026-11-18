# ages-of-blades-app

Blades of Ages (TR: Çağların Kılıcı) tanıtım sitesi: tanıtım sayfası, diyar ve boss sayfaları, gizlilik politikası,
KVKK aydınlatma metni, kullanım koşulları, hesap silme, destek ve basın kiti. Statik, GitHub Pages ile yayınlanır.
Kurulum deseni kardeş sitelerle aynı (`zirve-app`: `build.py`, `data/facts.json`, `content/i18n/`).

## Kararlar (18 Kasım 2026, sahip)

| Konu | Karar |
| --- | --- |
| Tasarım yönü | **D + A**: oynanabilir giriş (dönen kılıçlarla kes, altın topla) ve altında Çağlar Yolculuğu. Diyar ve boss sayfaları "Gün Işığında Mit Müzesi" düzeninde, bileşenler oyunun Gün Kili dilinden (`docs/research/tasarim-adaylari.md`) |
| Ad | EN **Blades of Ages**, TR **Çağların Kılıcı** |
| Alan adı | `bladesofages.mm-apps.com` (DNS henüz yok) |
| Diller | Dalga 1, 7 dil: tr (kök), en, ja, ko, zh-Hant, de, fr |
| Adil oyun cümlesi | Yalnız "zorunlu reklam yok, ödüllü reklam isteğe bağlı". Can sistemi netleşene kadar "enerji yok" yazılmaz |

Araştırma: `docs/research/seo.md`, `docs/research/geo.md`, `docs/research/tasarim-adaylari.md`.

## Açık sorular

Raporlarda sahibe sorulacaklar listesi var (`seo.md` §8.2, `geo.md` §9). Siteyi bloklamayanlar sonraya kaldı:
- Pre-order açılıp açılmayacağı
- Fragman üretimi
- Kahramanlar sayfası
- Kültürel danışman
- mm-apps.com hub bağlantısı

**Oyun deposuna düşen iş:** ad kararı gereği Unity `productName` "Ages of Blades" → "Blades of Ages" hizalanmalı. API
alt alanı (`api.agesofblades…`) görünür bir yer değil; değiştirmek isteğe bağlı.
