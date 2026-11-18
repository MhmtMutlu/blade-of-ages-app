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

## Yapı

`python3 build.py` siteyi depo köküne üretir ve denetler (hata varsa çıkış kodu 1). Derlenmiş HTML commit'lenir.

| Yer | İçerik |
| --- | --- |
| `data/facts.json` | Olguların tek kaynağı: aşama (`prelaunch` → `preorder` → `live`), sayılar, çağlar, vitrin kahramanları |
| `data/site.json` | Taban adres, iletişim, telif ve Apple ticari marka satırı |
| `src/<sayfa>.<dil>.html` | Hukuk ve destek sayfalarının gövdesi (gizlilik, KVKK, koşullar, hesap silme, destek). `{{CONTACT}}` ve `{{page:<id>}}` derlemede dolar. Sayfa yalnız dosyası olan dillerde üretilir; KVKK yalnız Türkçe |
| `content/i18n/<dil>.json` | Bütün metinler. Sayılar `{eras}` gibi yer tutucularla yazılır. `era.`, `realm.`, `boss.`, `hero.` adları oyunun verisiyle aynı olmalı |
| `build.py` → `LANGS` | Diller. Yayında tr ve en; ja, ko, zh-Hant, de, fr metinleri gelince `published` açılır |
| `assets/site.css` | Gün Kili stili (oyunun `UiKit.cs` token'ları), gece teması `prefers-color-scheme` ile |
| `assets/arena.js` | Oynanabilir giriş: dışa bakan kılıçlar, yürü = geniş yörünge, dur = dar ve hızlı, dört yönden ve halka dalgalarıyla gelen düşmanlar. İlk boyamadan sonra başlar, ekran dışında durur, hareket azaltma tercihinde kendiliğinden başlamaz |
| `assets/site.js` | Dil menüsü ve Çağlar Yolculuğu'ndaki katmanlı kayma |
| `assets/art/` | Oyunun kil SVG'lerinden üretilen WebP'ler (`scripts/art.py`) |
| `data/game.json` | Diyar sayfalarının verisi ve oyunun 7 dildeki metinleri (`scripts/sync-game.py`). Elle düzenlenmez; oyun deposundan kayarsa derleme durur |
| `content/myth.json` | Diyar sayfalarının "Mitte ve tarihte" bölümü ve kaynakları (doğrulanmış bağlantılar) |
| `assets/og/` | Paylaşım kartları, 1200×630, dil ve diyar başına (`scripts/og.py`) |
| `assets/shots/` | Oyunun PlayMode test koşularından gerçek ekran görüntüleri (`scripts/shots.py`; Türkçe arayüz) |
| `assets/press/` | Basın kiti dosyaları: 1024 px simge, marka işareti SVG |
| `assets/fonts/` | Baloo 2 ve Nunito alt kümeleri (`scripts/subset-fonts.py`, SIL OFL) |

**Denetimler:**
- Eksik metin anahtarı
- Tek H1
- `<img>` alt, genişlik ve yükseklik
- Kırık iç bağlantı
- Satır içi `style` (CSP engeller)
- JSON-LD'deki ad ve açıklamaların sayfada görünür olması
- Başlıkta üstünlük iddiası
- Olgu ve adların oyun deposuyla karşılaştırılması (`../blades-of-ages` ya da `AOB_GAME_REPO`)

**Sanat ve font yeniden üretimi:**

```
python3 -m venv .venv && .venv/bin/pip install pillow numpy fonttools brotli
.venv/bin/python scripts/art.py
.venv/bin/python scripts/subset-fonts.py
.venv/bin/python scripts/og.py          # paylaşım kartları
.venv/bin/python scripts/shots.py       # oyun içi ekran görüntüleri
python3 scripts/sync-game.py            # diyar verisi ve oyun metinleri
```

**Yerel önizleme:** `python3 -m http.server 8742`

## Durum (18 Kasım 2026)

**Var:**
- Tanıtım sayfası (tr, en), 404, `robots.txt`, `sitemap.xml`, `llms.txt`
- Gizlilik, KVKK (yalnız tr), kullanım koşulları, hesap silme, destek (tr, en). Oyunun 18 Kasım'daki gerçek veri
  akışından yazıldı: anonim hesap, ilerleme, savaş kayıtları, günlük sınav, satın alma (RevenueCat yalnız mağaza
  açılınca). Reklam, Apple ile giriş ve sunucuya giden analitik bu sürümde yok; metinler de öyle söylüyor
- Oynanabilir giriş
- Çağlar Yolculuğu: I–III. çağ diorama; IV–V. çağ "Silik'in sildiği" çağlar olarak
- Nasıl oynanır, kahramanlar, adil oyun, SSS

- Diyarlar dizini ve bitmiş 6 diyarın sayfası (Göbeklitepe, Sümer, Mısır, Yunan, Hitit, İskandinav): müze düzeni,
  düşmanlar, boss fazları ve karşı hamleler, diyar donanımı, oyun içi görüntüler, BreadcrumbList
- Paylaşım kartları (ana sayfa ve her diyar, tr/en), basın kiti (`/basin/`, `/en/press/`)

**Sırada:**
- ja, ko, zh-Hant, de ve fr metinleri.
- İngilizce arayüzle ekran görüntüleri (şimdi Türkçe; İngilizce sayfalar bunu bir notla söylüyor).
- DNS (`bladesofages.mm-apps.com`) ve GitHub Pages.

## Hukuk metinleri ve oyun birlikte değişir

Oyuna şunlardan biri eklendiğinde aynı değişiklikte `src/privacy.*`, `src/kvkk.tr.html`, `src/terms.*`,
`src/delete.*` ve `src/support.*` güncellenir (App Privacy etiketi ve `PrivacyInfo.xcprivacy` de):
- Ödüllü reklam (AdMob, UMP, ATT): reklam bölümü, sağlayıcılar, yurt dışı aktarım, rıza
- Apple ile giriş: hesap bölümü, cihazlar arası taşıma, silmede Apple jeton iptali
- Sunucuya giden analitik (`game.analytics_events`, 90 gün): veri tablosu, hukuki sebep, AEA rızası, kapatma anahtarı
- Oyuncu adı ya da sıralama tablosu (`docs/40` 2. aşama): "diğer oyunculara görünenler", moderasyon maddesi
- Bildirim, Game Center, tanılama (MetricKit)

## Açık sorular

Raporlarda sahibe sorulacaklar listesi var (`seo.md` §8.2, `geo.md` §9). Siteyi bloklamayanlar sonraya kaldı:
- Pre-order açılıp açılmayacağı
- Fragman üretimi
- Kahramanlar sayfası
- Kültürel danışman
- mm-apps.com hub bağlantısı

**Oyun deposuna düşen iş:** ad kararı gereği Unity `productName` "Ages of Blades" → "Blades of Ages" hizalanmalı. API
alt alanı (`api.agesofblades…`) görünür bir yer değil; değiştirmek isteğe bağlı.
