# Blade of Ages: Çağların Kılıcı · web sitesi SEO stratejisi

> **19 Kasım 2026 notu:** Oyunun adı her dilde tek: **Blade of Ages: Çağların Kılıcı** (tekil "Blade"); site alan
> adı `bladeofages.mm-apps.com`. Bu belgedeki ad ve alan adı geçişleri buna göre güncellendi; 17 Kasım'daki aday
> adlar README'deki karar tablosunda. Bundle id (`com.mhmtmutlu.agesofblades`) ve API (`api.agesofblades…`) teknik
> kimlik olarak değişmedi.

Araştırma tarihi: 17 Kasım 2026. Kapsam: statik oyun sitesi (tanıtım, oyun ve dünya sayfaları, diyar sayfaları, basın kiti,
destek, gizlilik, KVKK, koşullar, hesap silme). Bu belge bir araştırma ve öneri raporudur; hiçbir karar uygulanmadı.

**Etiketler:**
- **[resmî]** platformun kendi belgesi (Google, Apple)
- **[ikincil]** basın, blog ya da ajans
- **[depo]** yerel depolardan okunan olgu (dosya yolu verildi)
- **[gözlem]** bu oturumda `curl` ya da `dig` ile bakılan canlı durum
- **(çıkarım)** kaynaklardan benim vardığım sonuç
- **(varsayım)** doğrulanmamış çalışma kabulü
- **(doğrulanmadı)** kaynağa ulaşılamadı ya da kaynaklar çelişiyor

Hiçbir öneri sıralama, zengin sonuç ya da yapay zekâ yanıtlarında anılma garantisi vermez.

---

## 1. Özet: en önemli 10 karar önerisi (öncelik sırasıyla)

1. **Önce ad, sonra site.** Nihai ad ve alan adı kesinleşmeden hiçbir sayfa dizine açılmasın.
   - Depoda (17 Kasım) üç farklı biçim vardı: belgelerde çoğul İngilizce ad, Unity `productName`'de sözcükleri ters
     sıralı ad, bundle id ve API alt alanında `agesofblades` [depo: `blades-of-ages/game/ProjectSettings/ProjectSettings.asset`, `docs/00-vizyon.md`].
   - GitHub Pages sunucu tarafı 301 yönlendirmesi yapamaz (çıkarım). Sonradan ad ya da alan adı değişirse yalnız meta
     refresh ile taşınabilir ve sinyalin bir kısmı kaybolabilir.
   - Alt alan adı (19 Kasım kararı: `bladeofages`), JSON-LD `name`, OG başlıkları ve App Store adı aynı adı taşımalı.
2. **Zirve'nin derleme desenini aynen al.** `build.py`, tek olgu kaynağı `data/facts.json`, `content/i18n/<dil>.json`,
   derleme denetimleri (hreflang, canonical, JSON-LD, yasak ifade, ilk görünüm bütçesi) [depo: `zirve-app/README.md`].
   Yeni bir sistem kurma.
3. **Lansmanda 7 dil (Dalga 1), alt dizinle.**
   - Diller: tr, en, ja, ko, zh-Hant, de, fr. Yollar: TR kökte, diğerleri `/<dil>/`. `x-default` = `/en/`.
   - Bu, Zirve'nin desenidir [depo: `zirve-app/sitemap.xml`].
   - Dalga 2'de `es-419` hreflang kodu Google'da desteklenmez [resmî]; Latin Amerika İspanyolcası `es` ile işaretlenir
     (§5.2).
4. **İçeriğin omurgası diyar sayfaları olsun; yalnız bitmiş diyarlar yayınlansın.**
   - Lansman öncesi 12 diyardan 5'i bitmiş: Göbeklitepe, Sümer, Mısır, Yunan, Hitit [depo: `docs/31` §3].
   - Taslak diyarlara boş ya da şablon sayfa açmak "doorway / scaled content" riski taşır (§4.3).
5. **Rakip oyun adları başlıkta, H1'de ve URL'de kullanılmasın.** Tür terimi kullanılsın: survivor-like, bullet heaven,
   ヴァンサバ系, 뱀서라이크, 割草. "Games like Vampire Survivors" sorgusu sitede değil, liste ve basın üzerinden
   hedeflensin (§3.1). Bu karar Yumuş'taki yasak marka listesiyle tutarlı [depo: `yumus-app/SEO.md`].
6. **JSON-LD tek `@graph` olsun, oyun düğümü `["VideoGame","MobileApplication"]`.**
   - Google yalnız `VideoGame` tipine zengin sonuç göstermez; ikinci bir tip ister [resmî].
   - Puan ve yorum uydurulmaz. App Store puanları da sitede `aggregateRating` olarak kullanılmaz; Google başka sitelerden
     toplanan puanı yasaklar [resmî].
   - Sonuç: yazılım zengin sonucu fiilen hedef değildir. İşaretleme varlık tanımı ve yapay zekâ özetleri için konur.
7. **Lansman öncesi kayıt yolu yalnız App Store ön siparişi (pre-order) olsun; e-posta listesi kurulmasın.**
   - Pre-order, App Review onayından sonra yayına girer ve yayın tarihine en çok 180 gün kalmışken açılabilir [resmî].
   - E-posta listesi kişisel veri toplar ve hukuk kuralıyla çatışır [depo: `~/.claude/rules/legal-no-agreements.md`].
8. **Üçüncü taraf istek sıfır.**
   - YouTube gömmesi, Google Fonts, analitik ve piksel yok; CSP `default-src 'self'` (kardeş sitelerle aynı)
     [depo: `zirve-app/en/index.html`].
   - Fragman kendi dosyamızdan `<video>` ile oynar ve bir izleme sayfasında (watch page) durur. Böylece Google video
     dizinine de uygun olur [resmî].
9. **Performans bütçesi derlemede denetlensin.**
   - Hero bölümünde poster görseli LCP öğesidir; video yüklemeden sonra başlar.
   - CJK dillerinde web fontu indirilmez, sistem fontu kullanılır (oyunun kendi kararıyla aynı) [depo: `docs/32` §3].
   - Hedefler: LCP ≤ 2,5 sn, INP ≤ 200 ms, CLS ≤ 0,1 [ikincil, Google eşikleri değişmedi]. Düşük trafikte saha verisi
     (CrUX) oluşmaz; ölçüm Lighthouse ile laboratuvarda yapılır.
10. **Ölçüm çerezsiz olsun ve site dışında yapılsın.**
    - Araçlar: Search Console, Bing Webmaster (AI Performance raporu), App Store kampanya bağlantıları (`pt`/`ct`), App
      Analytics'te kaynağa göre ön sipariş ve ayda bir elle yapay zekâ görünürlük ölçümü (Zirve `AI_VISIBILITY.md`
      şablonu).
    - Siteye sayaç konmaz.

---

## 2. Kardeş sitelerden çıkan desenler

İncelenen: `zirve-app` (zirve.mm-apps.com; 17 dil, oyun sayfaları, `build.py`), `suzgec-app` (İçgör; `SEO.md`),
`yumus-app` (Yumuş; `SEO.md`, video sayfaları) ve Zirve'nin `zirve/docs/aso-geo/` araştırması [depo].

### 2.1 Aynen alınacak

| Desen | Neden iyi | Kaynak |
|---|---|---|
| Statik HTML; derlenmiş çıktı commit edilir; GitHub Pages ek derleme yapmaz | Barındırmadan bağımsız, hızlı, saldırı yüzeyi küçük | `zirve-app/README.md` |
| `data/facts.json` tek olgu kaynağı; metinde çıplak sayı yasak (`{realms}` yer tutucusu) | Site ile oyun arasında sayı kayması olmaz ("12 diyar", "120 harita", "21 kahraman") | Zirve `build.py` denetimleri |
| Olguların oyun deposuyla karşılaştırılması (`../blades-of-ages/data/*.json`) | Diyar adları, boss adları ve dil listesi oyunla birebir kalır | Zirve: `facts.json` ↔ uygulama deposu |
| `content/i18n/<dil>.json`, her anahtar `{value, state}`; `needs_review` varken yayın yok | Yarım çeviri yayına çıkmaz | Zirve |
| Sayfa başına karşılıklı hreflang + `x-default`; sitemap'te `xhtml:link` alternatifleri | Google'ın iki yönlü kuralı derlemede garanti edilir | Zirve `sitemap.xml` |
| Mutlak canonical; 404 için `noindex`, canonical ve JSON-LD yok | Standart | İçgör, Yumuş |
| Tek `@graph`: Organization (mm-apps, `@id` = `https://mm-apps.com/#org`), WebSite, WebPage, BreadcrumbList, uygulama düğümü | Varlıklar bütün mm-apps sitelerinde aynı kimlikle birbirine bağlanır | Zirve `en/index.html` |
| JSON-LD metinleri görünür metinde birebir geçer (WebPage adı = `<title>`, açıklama = meta) | Google'ın "işaretleme sayfada görünen şeyi söyler" kuralı | Zirve, İçgör |
| `FAQPage` yalnız destekte | FAQ zengin sonucu 7 Mayıs 2026'da kalktı; işaretleme zararsız ve yapay zekâ özetlerine yardımcı | Zirve `RESEARCH.md` §4; [ikincil: techwyse](https://www.techwyse.com/news/ai-search/google-faq-rich-results-deprecated-2026) |
| Yasak ifade denetimi (başlık, H1, URL hata; gövde uyarı) | "En iyi", "#1", "garanti" ve rakip markalar yayına çıkmaz | Zirve, Yumuş |
| `apple-itunes-app` meta etiketi (Smart App Banner) | Safari'den mağazaya tek dokunuş | Zirve |
| Dile göre OG görseli 1200×630, `og:locale` ve `og:locale:alternate` | Paylaşım kartı her dilde yerel | Zirve `assets/og/` |
| Yazı tiplerinin yazı sistemine göre alt kümesi, kendi sunucumuzdan | Üçüncü taraf istek yok, ilk görünüm küçük | Zirve `scripts/subset-fonts.py` |
| `robots.txt` bütün tarayıcılara açık; `llms.txt` olgular + sayfalar | Kardeş sitelerle tutarlı; Google llms.txt kullanmıyor ama zararı yok | Zirve, Yumuş |
| IndexNow anahtarı ve yayın sonrası `scripts/indexnow.sh` | Bing ve Yandex hızlı keşif (ChatGPT ve Copilot aramaları Bing dizinini kullanır) | İçgör, Yumuş |
| `app-ads.txt` sitenin kökünde | AdMob doğrulaması, App Store'daki geliştirici sitesi alan adının kökünde aranır | Zirve `README.md` §app-ads.txt |
| Basın kiti yalnız tr ve en; hreflang grubu küçük, `x-default` = en | Çeviri maliyeti düşük, hedef kitle (basın) İngilizce okuyor | Zirve `RESEARCH.md` §4 |
| Gerçek ekran görüntüsü her dilde (yerel arayüz), WebP | Doorway riskine karşı her dil sayfasına özgün değer katar | Zirve `scripts/game-shots.sh` |
| "Senin yapacakların" listesi: Search Console Domain mülkü, Bing içe aktarma, Enforce HTTPS | Sahibin işi; Claude yapamaz | İçgör, Yumuş `SEO.md` |

### 2.2 Uyarlanacak

| Desen | Kardeş sitede | Oyun sitesinde |
|---|---|---|
| Sayfa omurgası | Zirve: 11 bulmaca türü sayfası; İçgör: 72 katkı maddesi | 12 diyar sayfası; yalnız bitenler yayına çıkar. Boss'lar diyar sayfasında bölüm olarak durur, ayrı sayfa açılmaz (§4.3) |
| Video | Yumuş: 5 video sayfası, 960×960 sessiz MP4 | Tek fragman izleme sayfası (`/fragman/`, `/en/trailer/`) ve diyar başına kısa döngü klip (izleme sayfası değil, destekleyici). Altyazı WebVTT dosyasıyla, dil başına |
| `facts.json` sürüm bayrağı (`live`) | Zirve 1.0 → 1.1 | Üç aşama: `prelaunch` → `preorder` → `live`. Rozet, `offers`, `apple-itunes-app` ve metinler bu bayraktan üretilir (§6) |
| OG görselleri `scripts/og.swift` | Latin dışı yazı için ayrı font gerekti (Zirve uyarısı) | ja, ko ve zh-Hant OG kartı için baştan CJK font desteği planlanmalı. Yalnız kendi derleme makinemizde çizilir, siteye font yüklenmez |
| `alternateName` dizisi | Zirve: App Store'daki her yerel ad | 19 Kasım: ad her dilde tek (Blade of Ages: Çağların Kılıcı); site kısa adı ("Blade of Ages") `alternateName` olarak veriyor |
| Yasak ifade listesi | Yumuş: Pop It, Kinetic Sand vb.; sağlık iddiaları | Rakip oyun adları (Vampire Survivors, Survivor.io, Archero, Heroes vs Hordes, Brotato) başlık, H1 ve URL'de hata. Ayrıca "en iyi", "#1", "ilk ve tek". Doğrulanmamış iddialar da yasak listesinde: "enerji yok" (§8 R3), "7+" yaş etiketi (§8 R4), "katlanabilir iPhone" (Apple duyurmadan) |
| Smart App Banner | Yayındaki uygulama | Pre-order sırasında davranışı doğrulanamadı (§6). Banner yalnız `preorder` aşamasında bir cihazda denendikten sonra açılır |

### 2.3 Alınmayacak

| Desen | Neden |
|---|---|
| Niyet başına sayfa ("reklamsız oyunlar", "offline oyunlar") | Zirve kullanıcı kararı: spam sayılabilir [depo: `zirve/docs/aso-geo/README.md` karar 1]. Oyun sitesinde de açılmaz |
| İçgör'ün 72 sayfalık sözlük ölçeği | Oyunda gerçek arama hacmi olan bu kadar konu yok (çıkarım). 12 diyar + 5 çağ yeter |
| Yumuş'taki "nasıl yapılır" tarif rehberi | Oyunla ilgisi olmayan bilgi sorgusunu yakalamaya çalışmak, oyun sitesinin konusunu bulandırır |
| 17 dil (Zirve) | Oyunun lansman dilleri 7 + Dalga 2'de 6 [depo: `docs/32` §2]. Site oyunun dillerini geçmez |

### 2.4 Oyun sitesinde farklı yapılması gerekenler

- **Görsel ağırlık.** Kardeş siteler hafif (Zirve ilk görünüm Latin 100 KB bütçesi). Oyun sitesi sanat ve hareketle
  satar. Bu yüzden ayrı bir bütçe ve "önce poster, sonra video" kuralı gerekir (§5.6).
- **Lansman öncesi aşama.** Kardeş siteler yayındaki uygulamalar için kuruldu. Bu site mağaza sayfası yokken açılacak,
  bu yüzden üç aşamalı sürüm bayrağı gerekir (§6).
- **Kültür ve mitoloji içeriği.** Diyar sayfaları gerçek mitlere dayanır. Kaynak göstermek ve kültürel hassasiyet kuralı
  (yaşayan inançların tanrıları düşman olmaz) site metninde de geçerli [depo: `CLAUDE.md` kural 7].
- **Basın kiti ağırlıklı.** Oyunlarda keşif büyük ölçüde üçüncü taraf listelerden ve basından gelir (§3.4). Basın kiti
  ilk günden eksiksiz olmalı: fragman, GIF, logo, kapsül sanat, bilgi sayfası.

---

## 3. Anahtar kelime stratejisi

### 3.0 Yöntem ve sınırlar

- **Bu oturumda hacim ölçülmedi** (doğrulanmadı). Aşağıdaki kümeler, terimlerin varlığına ve sonuç sayfası (SERP)
  gözlemine dayanan hipotezlerdir.
- Hacim için önerilen yollar:
  - Google Trends: hesap gerekmez.
  - Google Keyword Planner: Google Ads hesabı gerekir. Hesap açmak sahibin kararı.
  - Apple Search Ads "popularity": ASA hesabı gerekir.
  - Lansmandan sonra Search Console sorguları.
  - Zirve'de olduğu gibi tarihli bir taban ölçümü yapılmalı [depo: `zirve/docs/aso-geo/README.md` P1].
- **Oyun sitelerinin gerçekçi hedefi** (çıkarım):
  1. Marka sorgusunda (oyunun adı) ilk sonuç olmak.
  2. Diyar ve mitoloji uzun kuyruğunda görünmek.
  3. Yapay zekâ özetlerinde doğru tanımlanmak.
- Tür kafa sorguları ("best survivor games iphone") liste sitelerine ve apps.apple.com'a gidiyor.
  - Gözlem: tür sorgularında sonuçları mağaza sayfaları ve liste siteleri dolduruyor
    [ikincil: [233leyuan](https://www.233leyuan.com/a/11112127583), [tw.my-best](https://tw.my-best.com/115127)].
  - Zirve araştırması: oyunlarda yapay zekâ alıntılarının %42,6'sı apps.apple.com
    [ikincil, AppTweak, `zirve/docs/aso-geo/RESEARCH.md` §1].
  - Bu sorgular sitede değil, App Store metni ve basın/liste görünürlüğüyle kazanılır.

### 3.1 Tür terimleri (dile göre doğrulanan durum)

| Dil | Tür terimi | Durum |
|---|---|---|
| en | "survivor-like", "survivors-like", "bullet heaven", "Vampire Survivors-like" | "Bullet heaven" topluluk anketini kazandı. Steam'in onu resmî etiket yaptığı söyleniyor (Mayıs 2026), ama birincil kaynak görülmedi (doğrulanmadı) [ikincil: [gamingonlinux](https://www.gamingonlinux.com/2025/12/the-results-are-in-bullet-heaven-moves-forward-to-be-an-official-genre/page=1), [PC Gamer](https://www.pcgamer.com/games/roguelike/we-need-to-decide-on-a-genre-name-for-vampire-survivors-like-games-before-a-really-terrible-one-sticks)] |
| ja | ヴァンサバ系, ヴァンサバライク, ローグライト | Terimin kullanımı bilgime dayanıyor; bu oturumdaki arama ilgili sonuç döndürmedi (doğrulanmadı) |
| ko | 뱀서라이크, 뱀서류 | Arama sonuçlarını "뱀" (yılan) yüzünden yılan oyunları doldurdu [gözlem]. Terim tek başına gürültülü; "로그라이트 액션" ile eşlenmeli |
| zh-Hant | 割草遊戲, 類吸血鬼倖存者, 肉鴿 (roguelike), 手遊 | 割草 bu türün Çince adı olarak yaygın [ikincil: [233leyuan](https://www.233leyuan.com/a/11112127583), [App Store HK örneği](https://apps.apple.com/hk/app/%E6%BB%8B%E6%BB%8B%E5%85%88%E9%8B%92%E9%9A%8A-%E4%BC%91%E9%96%92%E5%89%B2%E8%8D%89/id6468928820)] |
| de | Survivor-like, Roguelite, "Bullet Heaven" | İngilizce terim olduğu gibi kullanılıyor (çıkarım, doğrulanmadı) |
| fr | survivor-like, rogue-lite | Aynı (çıkarım, doğrulanmadı) |
| tr | "Vampire Survivors benzeri", "hayatta kalma aksiyon", "roguelite" | Yerleşik Türkçe tür adı yok (çıkarım) |

**Rakip adı kararı:**
- Rakip oyun adları başlık, H1, URL ve meta açıklamada kullanılmaz.
- Gövdede tek bir olgu cümlesi bile marka riski taşır. Önerim gövdede de kullanmamak (Yumuş kararıyla tutarlı).
- "Games like Vampire Survivors" sorgusu sitede hedeflenmez. Liste sitelerine ve topluluklara erişim yoluyla hedeflenir.
  Basın kiti bu iş içindir.

### 3.2 Dil başına kümeler

Sütunlar: **Niyet** (G = gezinme/marka, T = ticari keşif "oyun arıyorum", B = bilgi), **Sayfa** (§4'teki yol).
Hacim sütunu yok; hepsi ölçülmemiş hipotezdir.

**Türkçe (tr)**

| Küme | Örnek sorgular | Niyet | Sayfa |
|---|---|---|---|
| Marka | çağların kılıcı, çağların kılıcı oyunu, blade of ages | G | `/` |
| Tür ve platform | iphone aksiyon rpg oyunu, tek elle oynanan oyunlar iphone, roguelite iphone oyun, vampire survivors benzeri oyunlar* | T | `/`, `/nasil-oynanir/` |
| Yerli mitoloji | türk mitolojisi oyunu, göbeklitepe oyunu, hitit mitolojisi oyun, erlik, albastı, yelbegen | T/B | `/diyarlar/turk-altay/` (bittiğinde), `/diyarlar/gobeklitepe/`, `/diyarlar/hitit/` |
| Genel mitoloji | mitoloji oyunu, yunan mitolojisi oyunu, mısır mitolojisi oyunu, medusa, humbaba, illuyanka | T/B | `/diyarlar/`, ilgili diyar sayfası |
| Destek | çağların kılıcı hesap silme, satın alma geri yükleme, destek | G | `/hesap-silme/`, `/destek/` |

\* Yalnız arama gözlemi için listede; sayfada hedeflenmez (§3.1).

Türkçe "Göbeklitepe" (bitişik, resmî yazım) kullanılır. İngilizcede "Göbekli Tepe" (ayrı) yaygındır (çıkarım). Slug
dile göre farklı olur (§4.2).

**İngilizce (en)**

| Küme | Örnek sorgular | Niyet | Sayfa |
|---|---|---|---|
| Marka | blade of ages, blade of ages game, blade of ages iphone | G | `/en/` |
| Tür | survivor-like iphone, bullet heaven ios, roguelite action rpg iphone, one thumb action game, auto-attack rpg ios | T | `/en/`, `/en/how-to-play/` |
| Mekanik | spinning swords game, orbiting swords game, sword orbit roguelite | T | `/en/how-to-play/` |
| Mitoloji | mythology game iphone, greek mythology game ios, egyptian mythology game, hittite mythology, gobekli tepe game, sumerian mythology game | T/B | `/en/realms/`, `/en/realms/<slug>/` |
| Boss/canavar | medusa boss, humbaba gilgamesh, apep / apophis serpent, illuyanka dragon | B | Diyar sayfasındaki boss bölümü (`#boss`) |
| Basın | blade of ages press kit, blade of ages trailer | G | `/en/press/`, `/en/trailer/` |

Apep sorgusunda İngilizce aramalar "Apophis" adını da kullanır (bilgi, doğrulanmadı). Sayfada "Apep (Apophis)" yazılırsa
iki yazım da karşılanır; oyunun kendi metni "Apep, Serpent of Chaos" [depo: `data/l10n/en.json`].

**Japonca (ja)**

| Küme | Örnek sorgular | Niyet | Sayfa |
|---|---|---|---|
| Marka | (ja adı kesinleşince) + 日本語版 / iPhone | G | `/ja/` |
| Tür | ヴァンサバ系 スマホ, ヴァンサバライク iPhone, ローグライト アクションRPG, 片手で遊べる ゲーム | T | `/ja/`, `/ja/how-to-play/` |
| Mitoloji | 神話 ゲーム スマホ, ギリシャ神話 ゲーム, エジプト神話, ヒッタイト 神話, ギョベクリ・テペ | T/B | `/ja/realms/`, diyar sayfaları |
| Boss | メドゥーサ, フンババ, アペプ (アポピス), イルルヤンカシュ, フェンリル | B | `#boss` bölümleri |

Oyun, İlluyanka için Japoncada "イルルヤンカシュ" yazımını kullanıyor [depo: `data/l10n/ja.json`]. Yazım oyunla aynı
kalmalı; `facts.json` karşılaştırması bunu derlemede denetler.

**Korece (ko)**

| Küme | Örnek sorgular | Niyet | Sayfa |
|---|---|---|---|
| Tür | 뱀서라이크 모바일, 로그라이트 액션 RPG, 한손 게임, 자동 공격 RPG | T | `/ko/`, `/ko/how-to-play/` |
| Mitoloji | 신화 게임, 그리스 신화 게임, 이집트 신화, 히타이트 신화, 괴베클리 테페 | T/B | `/ko/realms/` ve diyarlar |
| Boss | 메두사, 훔바바, 아펩, 일루양카, 펜리르 | B | `#boss` |

**Geleneksel Çince (zh-Hant; Tayvan ve Hong Kong)**

| Küme | Örnek sorgular | Niyet | Sayfa |
|---|---|---|---|
| Tür | 割草遊戲 手遊, 類吸血鬼倖存者, 肉鴿 動作 RPG, 單手 手遊 | T | `/zh-hant/`, `/zh-hant/how-to-play/` |
| Mitoloji | 神話 手遊, 希臘神話 遊戲, 埃及神話, 赫梯 神話, 哥貝克力石陣 | T/B | `/zh-hant/realms/` ve diyarlar |
| Boss | 美杜莎, 洪巴巴, 阿佩普 (阿波菲斯), 伊盧揚卡, 芬里爾 | B | `#boss` |

Oyun Çin diyarını "華夏", Silik'i "褪影" diye adlandırıyor [depo: `data/l10n/zh-Hant.json`]. Site aynı adları kullanmalı.
Çin ana karası mağazası ruhsat alınana kadar kapalı [depo: `docs/32` §1]. zh-Hant sayfaları Tayvan ve Hong Kong içindir.

**Almanca (de)**

| Küme | Örnek sorgular | Niyet | Sayfa |
|---|---|---|---|
| Tür | Survivor-like iPhone, Roguelite Action-RPG iOS, Spiel mit einer Hand, Auto-Battler Action | T | `/de/`, `/de/how-to-play/` |
| Mitoloji | Mythologie Spiel iPhone, griechische Mythologie Spiel, ägyptische Mythologie Spiel, Hethiter Mythologie, Göbekli Tepe Spiel | T/B | `/de/realms/` ve diyarlar |
| Boss | Medusa, Humbaba, Apep, Illuyanka, Fenrir | B | `#boss` |

**Fransızca (fr)**

| Küme | Örnek sorgular | Niyet | Sayfa |
|---|---|---|---|
| Tür | survivor-like iPhone, rogue-lite action RPG iOS, jeu à une main, jeu d'action mobile | T | `/fr/`, `/fr/how-to-play/` |
| Mitoloji | jeu mythologie iPhone, jeu mythologie grecque, mythologie égyptienne jeu, mythologie hittite, Göbekli Tepe jeu | T/B | `/fr/realms/` ve diyarlar |
| Boss | Méduse, Humbaba, Apep, Illuyanka, Fenrir | B | `#boss` |

### 3.3 Mitoloji ve boss adları bir içerik fırsatı mı?

**Evet, ama sınırlı ve dürüst bir fırsat** (çıkarım):

- **Saf bilgi sorgusunu ("Medusa", "Humbaba") kazanmak gerçekçi değil.**
  - Bu sorgularda Wikipedia, ansiklopediler ve mitoloji siteleri baskın.
  - Örnek: "Illuyanka" sonuçları Wikipedia, akademik PDF ve oyun wiki'leri
    [ikincil: [Wikipedia](https://en.wikipedia.org/wiki/Illuyanka), [megatenwiki](https://megatenwiki.com/wiki/Illuyanka)].
- **Ulaşılabilir olan "mit + oyun" kesişimi.**
  - Sorgu örnekleri: "illuyanka game", "hittite mythology game", "göbeklitepe oyunu", "humbaba boss".
  - Bu kesişimde rekabet zayıf. Örnek: "Göbekli Tepe video game" sorgusunda yalnız itch.io prototipleri ve küçük
    projeler çıkıyor; mobil ticari oyun yok [ikincil: [itch.io örneği](https://lightonshell.itch.io/gobeklitepe),
    [Secrets of the Past](https://aadonis.itch.io/secrets-of-the-past)].
  - Illuyanka daha önce Tales of Zestiria ve Megami Tensei'de boss ya da şeytan olarak kullanılmış, yani boşluk yok
    değil [ikincil: [gamerguides](https://www.gamerguides.com/tales-of-zestiria/walkthrough/post-game-2582/calix-iii)].
- **En güçlü ayrışma Anadolu ve bozkır mitleri** (Göbeklitepe, Hitit, Türk-Altay). Oyunun vizyonu da bunu söylüyor
  [depo: `docs/00-vizyon.md` "Neden ayrışıyor"]. Bu üç diyar sayfası TR ve EN'de en özenli sayfalar olmalı.
  - "İlk", "tek" gibi doğrulanamayan iddialar yazılmaz (yasak ifade listesi).
  - Basın açısı ("Hitit ve Göbeklitepe mitlerini konu alan bir mobil aksiyon oyunu") basın kitinde kullanılabilir.
- **Diyar sayfasının içerik kuralı** (doorway riskine karşı). Her sayfa şunları içerir:
  1. Mitin 2–4 paragraflık özeti ve kaynakları: akademik ya da müze kaynağı tercih edilir; Wikipedia tek kaynak
     olmamalı.
  2. Oyunda o diyar: harita kuralı, 3 düşman, elit, boss, silah ve set adı. Kaynak `facts.json` ← `data/*.json`.
  3. O dilde gerçek oyun içi ekran görüntüsü ve 1 kısa döngü klip.
  4. Oyunun mitten nerede ayrıldığı (yaratıcı yorum). Bu hem dürüstlük hem kültürel saygı için gerekir.
  5. Kültürel not: "Erlik'in Gölgesi" Erlik'in kendisi değil, gölgesidir [depo: `docs/01`]. Sitede de aynı dikkat.
- **Boss'lara ayrı sayfa açılmaz.**
  - Boss, diyar sayfasında `id="boss"` bölümü olur.
  - Ayrı sayfa ancak gerçek bir izleme sayfası (boss dövüşü videosu) ya da yeterli özgün içerik olursa açılır.
  - 13 boss + 5 muhafız için ince sayfalar "scaled content" riskidir (çıkarım).

### 3.4 Marka adı: çakışma ve ayırt edilebilirlik riski

- **17 Kasım adayı (çoğul İngilizce ad) tam adıyla bir oyun bulunmadı.** Yakın adlar var:
  - "Blade of Ages I": itch.io'da Godot platform oyunu, geliştirmede
    [ikincil: [itch.io](https://lepcquiparle.itch.io/knight-adventure)]. **19 Kasım notu:** seçilen tekil ad
    "Blade of Ages" bununla birebir örtüşüyor; marka taramasında ele alınmalı
  - "Blades of Fire": MercurySteam / 505 Games, 2025, PC ve konsol [ikincil: [Epic](https://store.epicgames.com/p/blades-of-fire-f8178f)]
  - "Blades of Time", "Blades of Worlds", "The Elder Scrolls: Blades"
    [ikincil: [MobyGames](https://www.mobygames.com/game/55930/), [Wikipedia](https://wikipedia.com/wiki/The_Elder_Scrolls:_Blades)]
- **Sözcükleri ters sıralı Unity adıyla ya da "Age of Blades" adıyla mobil oyun bulunmadı** [ikincil, arama sonucu].
  - "Age of …" önekinin güçlü sahipleri var (Age of Empires Mobile). Bu bir ayırt edilebilirlik riski (çıkarım).
- **Sonuç** (çıkarım):
  - "Blade(s) of …" kalıbı kalabalık. Marka sorgusunda ilk sonuç olmak için ad tek başına zayıf.
  - Başlıkta ad + tanımlayıcı birlikte kullanılmalı. Örnek: "Blade of Ages: Mythic Sword Roguelite".
- **"Çağların Kılıcı" tam ifadesiyle sonuç yok.**
  - Yakın bir Türkçe kitap adı var: "Kılıçlar Çağı" (Michael J. Sullivan çevirisi)
    [ikincil: [Goodreads](https://www.goodreads.com/user_status/book/52122107)].
  - Ad Türkçede genel bir söz öbeği. Marka sorgusunu "çağların kılıcı oyunu" biçiminde sahiplenmek gerekir.
- **Marka tescili bu raporun kapsamı dışında ve yapılmadı.**
  - TÜRKPATENT, EUIPO, USPTO ve WIPO taraması gerekir. Sınıf 9 ve 41 önerilir (varsayım).
  - Açık karar: `YAPILACAKLAR.md` "Oyunun nihai adı ve marka tescil kontrolü: Bekliyor" [depo].
- **Alan adı dersi** [gözlem]:
  - `survivor.io` bugün Habby'nin oyununa değil, ilgisiz bir "Survive the Day" mini oyun sitesine açılıyor.
  - `vampiresurvivors.com` bir yönlendirme (`/lander`) döndürüyor.
  - Bu alan adlarının geçmişte kime ait olduğu doğrulanmadı.
  - Ders: marka arama sonucu, alan adına sahip olmadan da kalabalıklaşabilir. Kendi alt alan adımız + App Store
    sayfası + basın kiti marka sorgusunu tutmak için yeterli olmalı (çıkarım).

---

## 4. Bilgi mimarisi ve URL yapısı

### 4.1 Rakip sitelerden gözlemler [gözlem, 17 Kasım]

| Oyun | Site | Gözlem |
|---|---|---|
| Archero 2 / Survivor.io (Habby) | `habby.com`, `archero2.habby.com` | İstemci tarafında çiziliyor. Ana sayfanın meta açıklaması create-react-app varsayılanı ("Web site created using create-react-app"); Archero 2 sayfası 629 bayt, başlık "\*Archero2". SEO'ya yatırım yok; trafik mağazadan |
| Heroes vs Hordes | `heroesvshordes.com` → `aresinteractive.com/games/heroesvshordes/` | WordPress. Sayfalar: download, events, news, parents-guide, store (web mağazası), privacy, terms. JSON-LD yalnız WebPage/WebSite/Organization/Breadcrumb; `VideoGame` yok, hreflang yok. Başlık "Homepage - Heroes vs Hordes" |
| Vampire Survivors (poncle) | `vampiresurvivors.com`, `poncle.games` | Birincisi `/lander` yönlendirmesi; ikincisinin başlığı yalnız "poncle". Keşif Steam ve mağaza sayfası üzerinden ([Steam](https://store.steampowered.com/app/1794680/Vampire_Survivors/)) |
| Hades (Supergiant) | `supergiantgames.com/games/hades/` | Tek sayfa: kısa tanım, SSS bağlantısı, mağaza düğmeleri, basın alıntıları, basın kiti zip'i, 5 fragman, galeri, mağaza; yalnız İngilizce ([sayfa](https://www.supergiantgames.com/games/hades/)) |

**Çıkarım:**
- Türün büyük oyunları web SEO'suna neredeyse hiç yatırım yapmıyor; marka gücü ve mağaza trafiği yetiyor.
- Küçük bir geliştirici için fırsat iki yerde:
  1. Diyar ve mitoloji uzun kuyruğu
  2. Yapay zekâ özetlerinin kaynak alacağı temiz, olgu odaklı sayfalar
- HvH'nin "parents-guide" sayfası iyi bir fikir. 7+ hedefli, reklam ve satın alma içeren bir oyunda ebeveyn sorularını
  yanıtlar. Önerim bunu ayrı sayfa değil, destek SSS'sinin bir bölümü yapmak.

### 4.2 Sayfa listesi ve yollar

Zirve deseni: TR kökte ve Türkçe slug'la; diğer diller İngilizce slug'ları kendi önekleriyle kullanır (`/ja/realms/hittite/`).
Alan adı: `https://bladeofages.mm-apps.com` (19 Kasım kararı; 17 Kasım varsayımı `agesofblades` idi). Bugün DNS kaydı yok; `api.agesofblades.mm-apps.com`
ve `mm-apps.com` aynı sunucuya (46.45.137.111) çözülüyor [gözlem: `dig`].

| Sayfa | TR | EN (ve `/<dil>/` ile diğerleri) | Diller | Lansman |
|---|---|---|---|---|
| Tanıtım | `/` | `/en/` | 7 | Evet |
| Nasıl oynanır (dönen kılıç, tek parmak, hareket/duruş yörüngesi, savuşturma, seviye kartları) | `/nasil-oynanir/` | `/en/how-to-play/` | 7 | Evet |
| Dünya: Çağlar Ağacı, 5 çağ, Silik, Hatırlayıcı; Çağ Muhafızları ve Yeniden Doğuş özeti | `/dunya/` | `/en/world/` | 7 | Evet |
| Diyarlar dizini (yalnız yayındakiler; diğerleri "yakında" satırı, bağlantısız) | `/diyarlar/` | `/en/realms/` | 7 | Evet |
| Diyar sayfası × 5 (lansman öncesi) → 12 | `/diyarlar/gobeklitepe/`, `/diyarlar/sumer/`, `/diyarlar/misir/`, `/diyarlar/yunan/`, `/diyarlar/hitit/` | `/en/realms/gobekli-tepe/`, `sumer/`, `egypt/`, `greece/`, `hittite/` | 7 | Bittikçe |
| Kahramanlar (21 kahraman; yalnız bitmiş sanatla) | `/kahramanlar/` | `/en/heroes/` | 7 | Sanat hazırsa |
| Fragman izleme sayfası (VideoObject) | `/fragman/` | `/en/trailer/` | 7 (altyazı dile göre) | Fragman hazırsa |
| Destek + SSS (ebeveyn bölümü, satın alma geri yükleme, hesap bağlama) | `/destek/` | `/en/support/` | 7 | Evet |
| Basın kiti | `/basin/` | `/en/press/` | tr, en | Evet |
| Gizlilik politikası | `/gizlilik/` | `/en/privacy/` | 7 (hukuk metni çevirisi ayrıca incelenmeli) | Evet |
| Kullanım koşulları | `/kosullar/` | `/en/terms/` | 7 | Evet |
| KVKK aydınlatma metni | `/kvkk/` | – | tr | Evet |
| Hesap silme (Sign in with Apple hesabı için) | `/hesap-silme/` | `/en/delete-account/` | 7 | Evet |
| Haberler / güncelleme notları (isteğe bağlı, RSS) | `/haberler/` | `/en/news/` | tr, en | Lansman sonrası |
| 404 | `/404.html` | – | – | Evet |

Kök dosyalar: `robots.txt`, `sitemap.xml`, `llms.txt`, `app-ads.txt`, `<IndexNow anahtarı>.txt`, `CNAME`.

**Slug kuralları:**
- Küçük harf, ASCII, tire ile ayrılır. Türkçe karakter slug'a girmez: `gobeklitepe`, `turk-altay`.
- Dil önekinde zh-Hant için `/zh-hant/` (Zirve ile aynı), hreflang değeri `zh-Hant`.
- Ad değişse bile slug'lar diyar kimliğinden gelir (`data/realms.json` id'leri). Oyunun adı URL'de geçmez.
- Henüz bitmemiş diyarlar için URL rezerve edilmez, boş sayfa açılmaz.

**Neden TR kökte:** kardeş sitelerle tutarlılık; oyunun kaynak dili Türkçe. Gelirin büyük kısmı ABD, Japonya ve Kore'den
beklendiği için [depo: `docs/32` §1] `x-default` İngilizce. Alternatif olarak EN kökte, TR `/tr/` altında olabilirdi.
Tutarlılık ve Zirve'nin denetim kodunun yeniden kullanımı için önermiyorum (çıkarım).

### 4.3 İç bağlantı

- **Üst menü:** Oyun (`/`), Nasıl oynanır, Dünya, Diyarlar, Basın, Destek, dil seçici. Mağaza rozeti sağda (aşamaya
  göre: yok / Pre-order / Download).
- **Ana sayfa:** kısa tanım cümlesi, hero (poster + döngü video), 3 sütun (dönen kılıç, 12 mitoloji diyarı, adil
  ilerleme), diyar şeridi (her kart diyar sayfasına), "nasıl oynanır" kısa bölümü, SSS'den 3 soru, rozet.
- **Diyar sayfası:**
  - Bölümler: önceki ve sonraki diyar, çağ bağlamı (`/dunya/#cag-2`), boss bölümüne çapa (`#boss`).
  - Mitlerle ilgili dış kaynak bağlantıları sayfa sonunda.
  - Görünür breadcrumb (Ana sayfa › Diyarlar › Hitit) ve aynı BreadcrumbList JSON-LD.
- **Alt bilgi:** gizlilik, koşullar, KVKK (yalnız TR), hesap silme, destek, basın, geliştirici (`https://mm-apps.com/`),
  Apple ticari marka satırı (Zirve `site.json` deseni).
- **mm-apps.com hub sayfası:** `https://mm-apps.com/agesofblades/` kısa kart sayfası olur, kendi canonical'ı ile oyun
  sitesine bağlanır. Bu, Zirve için `https://mm-apps.com/zirve/` deseni [gözlem]. JSON-LD `sameAs` ikisini bağlar.
- **Doorway ve "scaled content" kuralları:**
  - Google'ın spam politikaları, nasıl üretildiğine bakmaksızın sıralamayı manipüle etmek için çoğaltılmış sayfaları
    hedef alır.
  - Kötü çevrilmiş ya da yalnız adı değişen şablon sayfa risklidir
    [ikincil: [SEJ](https://www.searchenginejournal.com/in-depth-look-at-google-spam-policies-updates/511005/);
    Zirve `RESEARCH.md` §4, resmî politika: [Google spam policies](https://developers.google.com/search/docs/essentials/spam-policies)].
  - Her dil sayfası o dilde gerçek ekran görüntüsü ve gözden geçirilmiş çeviri taşımalı.

---

## 5. Teknik SEO kontrol listesi

### 5.1 Canonical
- [ ] Her sayfada kendine işaret eden mutlak canonical (`https://<alan>/en/realms/hittite/`), sonda eğik çizgi.
- [ ] Dil sürümleri birbirine canonical vermez; her biri kendi canonical'ını taşır, bağı hreflang kurar.
- [ ] Kampanya parametreli bağlantılar (ör. `?ct=`) sitede yalnız App Store'a giden bağlantılarda kullanılır, site içi
      URL'de değil.
- [ ] CPI testi için ayrı landing page yapılırsa `noindex` ve sitemap dışı tutulur [depo: `docs/11`, çıkarım].

### 5.2 hreflang
- [ ] HTML `<link rel="alternate" hreflang>` ve sitemap `xhtml:link` (Zirve ikisini de yapıyor). Google üç yöntemden
      birini yeterli sayar; ikisi tutarlı olmalı [resmî: [localized-versions](https://developers.google.com/search/docs/specialty/international/localized-versions)].
- [ ] Her sürüm kendini ve bütün kardeşlerini listeler; iki yönlü değilse Google yok sayar [resmî].
- [ ] Kodlar:
  - Dalga 1: `tr`, `en`, `ja`, `ko`, `zh-Hant`, `de`, `fr`. `zh-Hant` geçerli (ISO 15924 yazı kodu) [resmî].
  - Dalga 2: `es-419` desteklenmez [resmî]. Önerim `es-ES` (İspanya) ve `es` (Latin Amerika içeriği, genel İspanyolca
    yedeği), ayrıca `pt-BR`, `it`, `pl`, `zh-Hans`.
- [ ] `x-default` → `/en/` (dil seçici işlevi gören sayfa).
- [ ] Yalnız bazı dillerde olan sayfalar (basın: tr, en; KVKK: tr) kendi küçük gruplarını listeler.
- [ ] Dile göre otomatik yönlendirme yapılmaz; dil seçici ve `x-default` yeter. Google dili `lang` özniteliğinden değil
      içerikten anlar [resmî].
- [ ] `<html lang>` doğru (`zh-Hant`), `og:locale` eşlemesi: `tr_TR`, `en_US`, `ja_JP`, `ko_KR`, `zh_TW`, `de_DE`,
      `fr_FR` (Zirve tablosu).

### 5.3 Sitemap ve robots
- [ ] `sitemap.xml`: yalnız 200 dönen, canonical, indekslenebilir sayfalar; dil alternatifleri ile.
- [ ] `lastmod` yalnız içerik değişince ilerler: Zirve'nin `data/lastmod.json` hash deseni.
- [ ] Video site haritası gerekmez; VideoObject ve `<video poster>` yeterli [resmî: [video SEO](https://developers.google.com/search/docs/appearance/video)].
- [ ] `robots.txt`: kardeş sitelerle aynı açık politika ve `Sitemap:` satırı [depo: `zirve-app/robots.txt`].
      Eğitim tarayıcıları (GPTBot, Google-Extended, ClaudeBot, CCBot) için karar sahibin; varsayılan kardeşlerle aynı (açık).
- [ ] `llms.txt`: §1 olguları ve sayfa listesi; `facts.json`'dan üretilir.
- [ ] Lansman öncesi aşamada (`prelaunch`) site henüz ad kararı verilmeden açılacaksa: tüm sayfalarda
      `<meta name="robots" content="noindex">` ve sitemap yok. Karar verildiği gün kaldırılır (§6).

### 5.4 Yapılandırılmış veri (JSON-LD `@graph`)

**İlkeler:**
- Sayfa başına tek `<script type="application/ld+json">` ve tek `@graph`. Kimlikler (`@id`) sayfalar arasında sabit.
- Oyun düğümü `["VideoGame","MobileApplication"]`. Yalnız VideoGame zengin sonuç almaz [resmî:
  [software-app](https://developers.google.com/search/docs/appearance/structured-data/software-app)].
- Yazılım zengin sonucu için `aggregateRating` ya da `review` zorunlu [resmî]. Google başka sitelerden puan toplamayı
  yasaklar ("Don't aggregate reviews or ratings from other websites") [resmî:
  [review-snippet](https://developers.google.com/search/docs/appearance/structured-data/review-snippet)].
  - App Store puanı sitede işaretlenemez. Site içi yorum toplamak kişisel veri demektir; yapılmaz.
  - Sonuç: yıldızlı sonuç hedeflenmez, `aggregateRating` hiç yazılmaz.
- `offers.price` Google'ın yazılım belgesinde yer alıyor; ücretsiz uygulamada `0` önerilir [resmî]. Belgenin bunu
  "zorunlu" diye etiketleyip etiketlemediği bu oturumdaki okumada net değildi (doğrulanmadı).
- `FAQPage` yalnız destek sayfasında. Görünür soru-cevapla birebir; zengin sonuç beklenmez.
- `VideoObject` yalnız fragman izleme sayfasında. `name`, `description`, `thumbnailUrl` (benzersiz), `uploadDate`,
  `duration`, `contentUrl`. Video sayfanın ana içeriği olmalı [resmî: video SEO].
- Diyar sayfası: `WebPage` + `BreadcrumbList`. Mit anlatımı için `Article` yerine `WebPage` + `about` kullanılır;
  makale değil, oyun içeriği (çıkarım). İsteğe bağlı `mentions` ile mit varlığının Wikidata bağlantısı (ör. Illuyanka
  için `sameAs`) eklenebilir. Faydası doğrulanmadı.
- Diyar dizini: `CollectionPage` + `ItemList` (İçgör'ün katkı listesi deseni).
- Basın: `AboutPage`.
- Yaş: Apple, Temmuz 2025'te derecelendirmeyi 4+, 9+, 13+, 16+, 18+ olarak değiştirdi [ikincil:
  [MacRumors](https://www.macrumors.com/2025/07/25/apple-overhauls-app-store-age-ratings/)].
  - Oyun belgelerindeki "7+ yaş" bir tasarım hedefi, App Store derecesi değil.
  - JSON-LD `contentRating` ve metin yalnız App Store Connect'te çıkan dereceyi yazar; o güne kadar boş.
- `datePublished`, `softwareVersion`, `installUrl` ve `sameAs` (apps.apple.com) yalnız `live` aşamasında.
  `preorder` aşamasında `offers.availability = PreOrder`, App Store bağlantısı ile.

**Örnek: `/en/`, `preorder` aşaması** (ad, kimlik ve sayılar yer tutucu; derleme `facts.json`'dan doldurur):

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://mm-apps.com/#org",
      "name": "mm-apps",
      "url": "https://mm-apps.com/"
    },
    {
      "@type": "WebSite",
      "@id": "https://bladeofages.mm-apps.com/#site",
      "url": "https://bladeofages.mm-apps.com/",
      "name": "Blade of Ages: Çağların Kılıcı",
      "inLanguage": ["tr", "en", "ja", "ko", "zh-Hant", "de", "fr"],
      "publisher": { "@id": "https://mm-apps.com/#org" }
    },
    {
      "@type": "WebPage",
      "@id": "https://bladeofages.mm-apps.com/en/#webpage",
      "url": "https://bladeofages.mm-apps.com/en/",
      "name": "Blade of Ages: Çağların Kılıcı · Mythic Sword Roguelite for iPhone & iPad",
      "description": "Swords spin around your hero and strike on their own. Fight through 12 mythic realms, from Göbekli Tepe to the Hittite storm mountains. One thumb, short runs.",
      "inLanguage": "en",
      "isPartOf": { "@id": "https://bladeofages.mm-apps.com/#site" },
      "about": { "@id": "https://bladeofages.mm-apps.com/#game" },
      "primaryImageOfPage": {
        "@type": "ImageObject",
        "url": "https://bladeofages.mm-apps.com/assets/shots/en/hero-hittite.webp"
      },
      "dateModified": "2026-12-01"
    },
    {
      "@type": ["VideoGame", "MobileApplication"],
      "@id": "https://bladeofages.mm-apps.com/#game",
      "name": "Blade of Ages: Çağların Kılıcı",
      "alternateName": ["Blade of Ages"],
      "description": "Blade of Ages: Çağların Kılıcı is an action roguelite for iPhone and iPad by mm-apps, an independent developer in Türkiye. Swords orbit the hero and attack automatically; the player only moves. 5 ages, 12 mythology realms, 120 maps.",
      "url": "https://bladeofages.mm-apps.com/en/",
      "image": "https://bladeofages.mm-apps.com/assets/icon-512.png",
      "screenshot": [
        "https://bladeofages.mm-apps.com/assets/shots/en/play-gobeklitepe.webp",
        "https://bladeofages.mm-apps.com/assets/shots/en/boss-medusa.webp"
      ],
      "applicationCategory": "GameApplication",
      "applicationSubCategory": "Action",
      "operatingSystem": "iOS 15.0 or later, iPadOS 15.0 or later",
      "gamePlatform": ["iPhone", "iPad"],
      "genre": ["Action RPG", "Roguelite"],
      "playMode": "SinglePlayer",
      "inLanguage": ["tr", "en", "ja", "ko", "zh-Hant", "de", "fr"],
      "isAccessibleForFree": true,
      "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD",
        "availability": "https://schema.org/PreOrder",
        "url": "https://apps.apple.com/app/id0000000000"
      },
      "trailer": { "@id": "https://bladeofages.mm-apps.com/en/trailer/#video" },
      "sameAs": ["https://mm-apps.com/agesofblades/"],
      "author": { "@id": "https://mm-apps.com/#org" },
      "publisher": { "@id": "https://mm-apps.com/#org" }
    }
  ]
}
```

Notlar:
- `operatingSystem` bugünkü Unity ayarından geliyor (`iOSTargetOSVersionString: 15.0`) [depo]. Yayın sürümünde
  değişebilir, `facts.json`'dan okunur.
- `trailer` düğümü yalnız fragman sayfası varsa yazılır. Derleme, `@id` ile gösterilen düğümün o sayfada var olduğunu
  denetlemeli.
- `availability: PreOrder` ve tarih (`availabilityStarts`) yalnız tarih kesinse yazılır. Apple, değişebilecek tarihi
  pazarlamada kullanmamayı öneriyor [resmî: [pre-orders](https://developer.apple.com/app-store/pre-orders/)].
- Açıklamadaki "12 realms" ve "120 maps" iddiası lansmanda tam oyun çıkarsa doğru olur [depo: `docs/31` §1]. Kapsam
  daralırsa `facts.json` ile birlikte değişir. Göbekli Tepe/Hittite örneği dile göre seçilir.

### 5.5 Open Graph ve X (Twitter) kartları, dil başına
- [ ] `og:title`, `og:description` = sayfanın `<title>` ve meta açıklaması (derleme eşitliği denetler).
- [ ] `og:image` dile göre: `assets/og/og-<dil>.jpg`, 1200×630, yerel metinli. Diyar sayfalarında diyara özgü kart
      (`og-<dil>-<diyar>.jpg`).
- [ ] `og:image:alt` dile göre; `og:locale` ve `og:locale:alternate` listesi.
- [ ] `twitter:card = summary_large_image`.
- [ ] OG görselinde yayın tarihi yazılmaz (değişebilir); "Pre-order" yazısı aşamaya göre değişir, derleme günceli denetler.
- [ ] CJK OG kartları için derleme makinesinde CJK yazı tipi (sistem fontu) ile çizim. Siteye font gönderilmez.

### 5.6 Performans bütçesi (ağır görsel ve animasyonlu tanıtım sayfası)

| Kalem | Bütçe (öneri, çıkarım) | Not |
|---|---|---|
| İlk görünüm toplamı (HTML + CSS + JS + font + poster) | ≤ 250 KB (Latin), ≤ 200 KB (CJK, font yok) | Zirve'nin 100 KB'lık Latin bütçesinin oyun için genişletilmiş hali; derleme uyarısı |
| Hero poster (LCP öğesi) | ≤ 120 KB WebP, `srcset` 480/750/1080/1440 | `fetchpriority="high"`, `loading="eager"`, `width` ve `height` |
| Hero döngü videosu | ≤ 1,5 MB, 6–10 sn, H.264 MP4, 720p, sessiz, `muted playsinline loop`, `preload="none"` | `load` olayından sonra başlatılır; `prefers-reduced-motion` ve `Save-Data` açıksa hiç yüklenmez, poster kalır |
| JS | ≤ 10 KB, satır içi yok, framework yok | Kardeş sitelerde tek `site.js` |
| CSS | ≤ 30 KB, kritik CSS satır içi olabilir (CSP `style-src 'unsafe-inline'` Zirve'de var) | |
| Web fontu | Latin alt kümesi ≤ 2 dosya, `woff2`, `font-display: swap`, `preload` | CJK: Hiragino Sans, Apple SD Gothic Neo, PingFang TC sistem fontları |
| Görseller | WebP; AVIF yalnız güvenilir kodlayıcıyla (Zirve'de `sips` AVIF'i Chrome'da boş çıktı) | Ekran altı görseller `loading="lazy"`, `decoding="async"` |

**LCP:**
- Chrome 116'dan beri videonun ilk karesi de LCP adayıdır; poster ve ilk kareden hangisi önce gelirse o sayılır.
  Ekranın üstündeki videoda LCP pratikte poster olur [resmî/ikincil: [web.dev LCP](https://web.dev/lcp/),
  [Chromium changelog](https://chromium.googlesource.com/chromium/src/+/main/docs/speed/metrics_changelog/2023_08_lcp.md),
  [DebugBear](https://www.debugbear.com/blog/optimize-video-lcp)].
- Poster videonun ilk karesiyle aynı olmalı ve `object-fit: cover` taşımalı. Poster hero değilse `preload` edilmez,
  bant genişliği için yarışır [ikincil: [web.dev video performance](https://web.dev/learn/performance/video-performance)].

**CLS:**
- Her `<img>` ve `<video>` için `width`/`height` ya da `aspect-ratio`. Derleme `<img>` için zaten denetliyor; `<video>`
  da eklenmeli.
- Font değişimine karşı `size-adjust` ya da metrik uyumlu yedek.

**INP:**
- Kaydırmaya bağlı JS animasyonu yok. Animasyonlar yalnız `transform` ve `opacity` ile CSS'te çalışır.
- Dönen kılıç efekti CSS ya da tek `<video>` ile yapılır, `<canvas>` döngüsü değil.
- Dil seçici ve menü dışında etkileşim yok.

**Eşikler:** LCP ≤ 2,5 sn, INP ≤ 200 ms, CLS ≤ 0,1 (75. yüzdelik). Bazı bloglar Mart 2026'da sıkılaştırma iddia ediyor;
Google kaynağında bulunamadı (doğrulanmadı)
[ikincil: [metadigital](https://www.metadigital.co.nz/core-web-vitals-in-2026-what-they-measure-and-whats-actually-worth-fixing/)].

**Ölçüm:** Düşük trafikte CrUX saha verisi oluşmaz; Lighthouse (mobil, yavaş 4G) ile her yayından önce laboratuvar
ölçümü yapılır. Zirve `RESEARCH.md` §4 aynı sonuca varmış.

### 5.7 Görsel ve video SEO
- [ ] Dosya adları açıklayıcı ve dilden bağımsız: `boss-medusa.webp`, `realm-hittite-lightning.webp`. Yerelleştirilmiş
      ekran görüntüleri `assets/shots/<dil>/` altında (Zirve deseni).
- [ ] `alt` dile göre ve betimleyici: "Medusa boss fight: the hero's orbiting swords parry purple projectiles". Anahtar
      kelime doldurma yok.
- [ ] Ekran görüntüleri gerçek oyun içi görüntü olur. Pazarlama sanatı ayrı etiketlenir ("Key art"). Bu, App Store
      kuralı 2.3 ruhuyla da tutarlı (çıkarım).
- [ ] Fragman izleme sayfası: video ana içerik, sayfanın başında, başka öğenin arkasında değil.
  - Sabit `contentUrl` ve `thumbnailUrl`. Robots ya da `noindex` ile engellenmez [resmî: video SEO].
- [ ] Altyazı: WebVTT dile göre `<track kind="subtitles">`. Fragmanda konuşma yoksa ekrandaki metinler için
      `kind="captions"`.
- [ ] YouTube'a da yüklenebilir (kanal sahibin kararı), ama sitede gömülmez. YouTube gömmesi ziyaretçinin IP'sini ve
      çerezini Google'a gönderir; hukuk kuralı bunu engeller (çıkarım). Sitede yalnız bağlantı olur.
- [ ] Google Discover ve görsel arama için büyük görsel izni: `<meta name="robots" content="max-image-preview:large">`.
      Discover'ın 1200 px öneriyi Google belgesinde var; bu oturumda açılmadı (doğrulanmadı).

### 5.8 Erişilebilirlik
- [ ] Tek H1, mantıklı başlık sırası, "skip to content" bağlantısı (mm-apps.com'da var [gözlem]).
- [ ] Kontrast WCAG AA. "Gün Kili" açık temasında beyaz kart üstü açık renk metinlere dikkat [depo: `CLAUDE.md`].
- [ ] `prefers-reduced-motion`: video ve dönen kılıç animasyonu durur, poster kalır.
- [ ] Video otomatik oynarsa sessiz olur ve durdurma düğmesi bulunur (WCAG 2.2.2, 5 saniyeden uzun hareket).
- [ ] Klavyeyle gezilebilir dil seçici, görünür odak halkası.
- [ ] Renk tek bilgi taşıyıcısı değil. Oyunun renk kodları (mor = savuşturulabilir mermi) sitede anlatılırken metinle
      de söylenir.
- [ ] Rozetlerin `alt` metni dile göre ("Download on the App Store" Apple'ın yerel karşılığı).

### 5.9 Güvenlik ve gizlilik başlıkları (statik sitede `<meta>` ile)
- [ ] Bütün kaynaklar kendi alan adımızdan.
  - CSP: `default-src 'self'; script-src 'self'; img-src 'self' data:; media-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'self'; form-action 'none'; upgrade-insecure-requests`.
  - Zirve'ye ek: `media-src 'self'`.
- [ ] `referrer: strict-origin-when-cross-origin`.
- [ ] Form yok. Destek e-postayla (`destek@mm-apps.com`, kardeş sitelerle aynı) [depo: `suzgec-app/SEO.md`].
- [ ] GitHub Pages "Enforce HTTPS" açık (sahibin işi).

---

## 6. Lansman öncesi ve sonrası

`facts.json → stage` bayrağı: `prelaunch` → `preorder` → `soft-launch` → `live`. Derleme rozeti, JSON-LD'yi, Smart App
Banner'ı, `llms.txt`'yi ve metinleri bu bayraktan üretir.

### 6.1 `prelaunch` (App Store sayfası yok)

| Konu | Ne yapılır |
|---|---|
| Ad kesin değilse | Site yayına alınabilir ama `noindex`, sitemap yok, OG yok. Yalnız hukuk sayfaları (gizlilik, koşullar, destek) dizine açık olabilir; TestFlight dış testi ve App Store Connect bunların URL'sini ister (çıkarım) |
| Ad kesinse | Tam site, `noindex` yok. Rozet yerine "Coming to iPhone and iPad" metni; bağlantı yok |
| JSON-LD | Oyun düğümünde `offers`, `installUrl`, `datePublished`, `sameAs: apps.apple.com` yok |
| Smart App Banner | Yok (`app-id` yok) |
| Kayıt | Yok. E-posta listesi kişisel veridir: yurt dışı e-posta hizmeti sözleşme gerektirir. Kendi sunucumuzda tutulsa bile ticari ileti için Türkiye'de İYS yükümlülüğü doğabilir (doğrulanmadı, hukuk incelemesi gerekir). Önerim: kurulmasın |
| İçerik | Ana sayfa, nasıl oynanır, dünya, bitmiş diyarlar, basın kiti (tr/en), fragman (hazırsa) |
| Basın ve topluluk | Basın kiti ilk günden. Zirve `OUTREACH.md`'deki ücretsiz listeler: IGDB, Pocket Gamer, r/iOSGaming Developer Saturday vb. [depo] |

### 6.2 `preorder` (App Review onayı alındı, pre-order yayında)

Apple kuralları [resmî: [pre-orders](https://developer.apple.com/app-store/pre-orders/)]:
- Yeni uygulamada yayın tarihi, pre-order yayınından 2–180 gün sonra olabilir. Bölgeye göre farklı tarih verilebilir.
- Pre-order ancak uygulama gönderilip App Review'dan geçtikten sonra yayınlanabilir.
- Sınırlı bir ürün sayfası yayınlanır ve beklenen yayın tarihini gösterir. Arama sonuçlarında çıkar.
- Yayın günü uygulama ön sipariş verenlerin cihazına otomatik iner.
- Tarih değişir ya da pre-order kaldırılırsa Apple müşteriye haber vermez; bunu geliştirici duyurmalı.
- "Pre-order on the App Store" rozeti Apple'ın pazarlama yönergelerinde var.
- Değişebilecek yayın tarihi pazarlamada yazılmamalı.
- App Analytics ön siparişleri tarih, bölge ve kaynak türüne göre gösterir.

Sitede değişenler:
- [ ] Rozet: Apple'ın resmî, yerel "Pre-order on the App Store" rozeti; bağlantı kampanya parametreli
      (`?pt=<sağlayıcı>&ct=site-home&mt=8`). `pt`, App Analytics'te ilk kampanya bağlantısı oluşturulunca çıkar [depo:
      Zirve `RESEARCH.md` §4].
- [ ] JSON-LD `offers.availability = PreOrder`, `offers.url` = App Store bağlantısı. Tarih kesinse `availabilityStarts`.
- [ ] `apple-itunes-app` meta etiketi. Pre-order sayfasında banner'ın davranışı bu oturumda doğrulanamadı; Apple'ın
      belgesi açılamadı. Bir iPhone'da Safari ile denendikten sonra açılır.
- [ ] Bir "Yayın tarihi değişti" duyuru alanı (haberler sayfası ya da ana sayfa şeridi). Apple bu bildirimi yapmaz.
- [ ] Soft launch bölgeleri (`docs/14`: Kanada, Filipinler; yeniden seçilecek [depo]) yalnız oradaysa: metin "şu
      ülkelerde" der, "dünya çapında" demez. Rozet, App Store bölge dışı kullanıcıya "kullanılamıyor" gösterebilir
      (çıkarım).

### 6.3 `live` (yayın günü)

- [ ] Rozet "Download on the App Store"; `apple-itunes-app` açık.
- [ ] JSON-LD: `offers.availability = InStock` (ya da `offers` yalnız `price: 0`), `installUrl`, `datePublished`,
      `softwareVersion`, `sameAs` içine apps.apple.com, `contentRating` (App Store'daki derece).
- [ ] `llms.txt`: yayın tarihi, sürüm, diller, kullanılabilir olmadığı bölgeler (Çin ana karası) Zirve biçiminde.
- [ ] Basın kiti: "Now available", App Store bağlantısı, yeni ekran görüntüleri.
- [ ] Search Console'da ana sayfa ve `/en/` için dizine ekleme isteği; `scripts/indexnow.sh`.
- [ ] App Store açıklamasının ilk cümlesi sitedeki tanım cümlesiyle aynı çizgide [depo: İçgör ve Yumuş "Senin
      yapacakların" 5].
- [ ] Pre-order döneminin bütün "yakında" metinleri derleme denetimiyle aranır (yasak ifade listesine geçici olarak
      eklenir).

### 6.4 Yayın sonrası

- Yeni diyar (her 6–8 haftada bir hedef [depo: `docs/01`]): diyar sayfası + OG kartı + ekran görüntüleri +
  `facts.json`, aynı derlemede.
- In-App Event ve sezon (ör. "Sezon 1: Nil'in Sırları" [depo: `docs/07`]) için haberler sayfasında kısa duyuru. Ayrı
  açılış sayfası açılmaz.
- Wikidata girişi ancak ilk bağımsız basın yazısından sonra (Zirve yol haritası P3 [depo]).

---

## 7. Ölçüm (hukuk kuralına uygun)

**İlke:** sitede çerez, analitik betiği, piksel, parmak izi ve üçüncü taraf istek yok. Ölçüm, platformların kendi
toplu raporlarından yapılır. Kişisel veri bizim tarafımızda işlenmez.

| Araç | Ne ölçer | Kişisel veri | Not |
|---|---|---|---|
| Google Search Console (Domain mülkü, DNS TXT) | Sorgular, gösterim, tıklama, dizin durumu, video raporu | Bizde yok; Google'ın toplu raporu | Sahibin hesabı ve işi |
| Bing Webmaster Tools | Aynı + "AI Performance" (Copilot alıntıları, önizleme, Şubat 2026) | Bizde yok | [resmî: [Bing blog](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview)] |
| App Store Connect kampanya bağlantıları (`pt`/`ct`) + App Analytics | Siteden gelen sayfa görüntüleme, indirme, ön sipariş (kaynağa göre) | Apple'ın toplu raporu; Apple eşik altı veriyi gizler (bilgi, doğrulanmadı) | `ct` değerleri sayfa başına: `site-home`, `site-realm-hittite`, `site-press` |
| Lighthouse (yerel, her yayından önce) | LCP, CLS, INP yerine TBT, erişilebilirlik puanı | Yok | Derleme sonrası betik olarak çalıştırılabilir |
| Aylık yapay zekâ görünürlük ölçümü (elle) | ChatGPT, Perplexity, Google AI Modu, Gemini, Copilot oyunu doğru tanıyor mu, kaynak ne | Yok | Zirve `AI_VISIBILITY.md` şablonu. Sorular: "blade of ages game", "mythology roguelite iphone", "game with hittite mythology", "göbeklitepe oyunu", "survivor-like with spinning swords" |

**Önerilmeyenler ve neden:**
- Kendi sunucumuzda çerezsiz sayaç: IP adresi geçici de olsa işlenir, sunucu belleği paylaşımlı ve öncelik verimlilik
  [depo: `CLAUDE.md` "Sunucuyu verimli kullanmak birinci öncelik"]. Getirisi Search Console + App Analytics'in
  üstünde değil (çıkarım).
- Google Analytics, Plausible Cloud, Cloudflare Web Analytics: veri yurt dışına gider; sözleşme ya da DPA gerektirir;
  kural gereği yok [depo: `~/.claude/rules/legal-no-agreements.md`].
- UTM'li site içi bağlantılar: gereksiz. Kampanya ölçümü yalnız App Store bağlantılarında.

**Açık hukuk notu:**
- GitHub Pages, siteyi sunarken ziyaretçi IP'sini kendi günlüklerinde işler (bilgi, GitHub gizlilik bildirimi bu
  oturumda açılmadı, doğrulanmadı).
- Bu, kardeş sitelerde de kabul edilmiş bir durum. Gizlilik politikasında barındırma sağlayıcısı olarak dürüstçe
  yazılmalı.

---

## 8. Riskler ve açık sorular

### 8.1 Riskler

| # | Risk | Etki | Öneri |
|---|---|---|---|
| R1 | **Ad ve alan adı kesin değildi** (19 Kasım kararı: Blade of Ages: Çağların Kılıcı, `bladeofages.mm-apps.com`). Belgelerde çoğul İngilizce ad, Unity'de ters sıralı ad, alt alan `agesofblades` vardı. "Blade(s) of …" kalıbı kalabalık; tescil taraması yapılmadı | Ad sonradan değişirse URL, OG, JSON-LD, basın kiti ve dış bağlantılar kırılır; GitHub Pages 301 veremez | Ad kararı ve tescil taraması siteden önce |
| R2 | **Taslak diyarlar.** 12 diyardan 7'si taslak | Boş ya da şablon sayfa doorway ve scaled content sayılabilir | Yalnız bitmiş diyar yayınlanır; dizinde "yakında" satırı bağlantısız |
| R3 | **"Enerji yok" iddiası ve can sistemi.** Monetizasyon ilkesi "enerji yok" diyor, ama 12 Kasım kararıyla sefer denemesi can harcıyor (5 can, 20 dk). Karar sabah onayı bekliyor [depo: `docs/07`, `docs/36`] | Sitede "enerji yok" yazılırsa yanıltıcı beyan riski (hukuk kuralı 3) ve kullanıcı güveni kaybı | Can sistemi kesinleşene kadar sitede "enerji yok" yazılmaz. "Zorunlu reklam yok" ve "isteğe bağlı ödüllü reklam" söylenebilir |
| R4 | **Yaş etiketi.** Belgelerde "7+"; Apple'ın 2025 sonrası dereceleri 4+, 9+, 13+, 16+, 18+ | Sitede uydurma bir derece | Yalnız App Store Connect'teki derece yazılır |
| R5 | **Katlanabilir iPhone ("Duo").** Belgeler Apple'ın cihazını varsayıyor, teyit bekliyor [depo: `docs/14`] | Duyurulmamış bir cihazdan söz etmek | Sitede yalnız "iPhone ve iPad" |
| R6 | **Çeviri kalitesi.** Oyun çevirileri makine + Claude; LQA önerildi ama karar yok [depo: `docs/32` §4] | Kötü yerelleştirilmiş sayfalar hem kullanıcıyı hem kaliteyi düşürür | Zirve'deki gibi her dilde çevirmen + ayrı dilbilimci denetimi; hukuk metinleri ayrıca |
| R7 | **Mitoloji doğruluğu ve kültürel hassasiyet** | Yanlış ya da saygısız bilgi; yaşayan inançlarla ilgili hassasiyet (Erlik, Japon ve Çin halk inançları) | Diyar metni kaynaklı; "oyunun yorumu" ayrımı; danışman kontrolü (`docs/01`, "Kültürel danışmanlar: Belirlenmedi") |
| R8 | **Hacim ölçülmedi** | Kümeler hipotez; yanlış önceliklendirme | Trends + Search Console tabanı; lansmandan 4–6 hafta sonra yeniden sıralama |
| R9 | **Smart App Banner pre-order davranışı ve `offers.price` zorunluluğu** doğrulanamadı | Küçük teknik hata | Cihazda deneme; Rich Results Test ile kontrol |
| R10 | **Rakip ve tür adlarının sitede kullanılmaması** | "Games like Vampire Survivors" trafiği kaçar | Bilinçli değiş tokuş; liste ve basın erişimiyle telafi |
| R11 | **es-419 hreflang** desteklenmiyor | Dalga 2'de hatalı işaretleme | `es-ES` + `es` |
| R12 | **Ağır görsel sayfa** | LCP ve veri tüketimi | §5.6 bütçesi derlemede uyarı; poster öncelikli |
| R13 | **GitHub Pages IP günlükleri** | Gizlilik metninde eksik beyan | Barındırma sağlayıcısı ve rolü gizlilik politikasında |

### 8.2 Kullanıcıya sorulacaklar

1. **Nihai ad:** cevaplandı (19 Kasım 2026): her dilde tek ad, Blade of Ages: Çağların Kılıcı.
2. **Alan adı:** cevaplandı (19 Kasım 2026): `bladeofages.mm-apps.com`.
3. **Ne zaman yayına alınsın:** ad kararından hemen sonra mı, yoksa pre-order açılınca mı? Ad kararı gecikirse
   `noindex` ile yalnız hukuk sayfaları kabul mü?
4. **Pre-order:** lansman öncesi App Store pre-order açılacak mı? Hangi bölgelerde (soft launch ülkeleri mi, global
   mi)? Hukuk kuralı nedeniyle e-posta listesi olmayacağını onaylıyor musun?
5. **Diller:** site lansmanda yalnız Dalga 1 (7 dil) mi, yoksa oyunla birlikte Dalga 2 (13 dil) mi? Hukuk metinleri
   kaç dilde?
6. **Rakip adları:** sitede (gövde dahil) hiçbir rakip oyun adı geçmesin kararını onaylıyor musun?
7. **Can sistemi:** `docs/36` kesinleşti mi? Sitede "enerji yok" söylenebilecek mi?
8. **Fragman:** fragman ve diyar klipleri kim tarafından, ne zaman üretilecek? YouTube kanalı açılacak mı (yalnız
   bağlantı, gömme yok)?
9. **Kahramanlar sayfası:** 21 kahramanın bitmiş sanatı lansmanda hazır olacak mı? Değilse sayfa sonraya kalır.
10. **Yapay zekâ eğitim tarayıcıları:** kardeş sitelerdeki gibi açık mı kalsın?
11. **Kültürel danışman:** diyar sayfalarındaki mit metinleri yayından önce bir uzmana okutulacak mı?
12. **mm-apps.com hub sayfası** (`/agesofblades/`) eklensin mi?

---

## Kaynaklar

**Google (resmî)**
- Software app yapılandırılmış verisi: https://developers.google.com/search/docs/appearance/structured-data/software-app
- Review snippet yönergeleri: https://developers.google.com/search/docs/appearance/structured-data/review-snippet
- Video SEO: https://developers.google.com/search/docs/appearance/video
- Yerelleştirilmiş sürümler (hreflang): https://developers.google.com/search/docs/specialty/international/localized-versions
- Spam politikaları: https://developers.google.com/search/docs/essentials/spam-policies
- Arama sonuçlarının sadeleştirilmesi (Haziran 2025, 7 tip kaldırıldı; yazılım uygulaması listede değil): https://developers.google.com/search/blog/2025/06/simplifying-search-results
- LCP: https://web.dev/lcp/ · Video performansı: https://web.dev/learn/performance/video-performance · Chrome 116 LCP değişikliği: https://chromium.googlesource.com/chromium/src/+/main/docs/speed/metrics_changelog/2023_08_lcp.md

**Apple (resmî)**
- Pre-order: https://developer.apple.com/app-store/pre-orders/
- Uygulama tanıtımı: https://developer.apple.com/app-store/promote
- Smart App Banner (bu oturumda içerik alınamadı): https://developer.apple.com/documentation/webkit/promoting-apps-with-smart-app-banners
- Pazarlama yönergeleri ve rozetler (Zirve araştırmasından): https://developer.apple.com/app-store/marketing/guidelines/

**Bing (resmî)**
- AI Performance raporu: https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview

**İkincil**
- FAQ zengin sonucunun kaldırılması (7 Mayıs 2026): https://www.techwyse.com/news/ai-search/google-faq-rich-results-deprecated-2026
- Apple yaş derecelendirmesi değişikliği: https://www.macrumors.com/2025/07/25/apple-overhauls-app-store-age-ratings/ · https://9to5mac.com/2025/07/24/apple-notifies-developers-of-new-app-store-age-rating-system/
- Tür adı tartışması: https://www.pcgamer.com/games/roguelike/we-need-to-decide-on-a-genre-name-for-vampire-survivors-like-games-before-a-really-terrible-one-sticks · https://www.gamingonlinux.com/2025/12/the-results-are-in-bullet-heaven-moves-forward-to-be-an-official-genre/page=1
- Core Web Vitals 2026 (eşikler değişmedi): https://www.metadigital.co.nz/core-web-vitals-in-2026-what-they-measure-and-whats-actually-worth-fixing/
- Video LCP: https://www.debugbear.com/blog/optimize-video-lcp
- Spam politikaları yorumu: https://www.searchenginejournal.com/in-depth-look-at-google-spam-policies-updates/511005/
- Ad taraması: https://lepcquiparle.itch.io/knight-adventure · https://store.epicgames.com/p/blades-of-fire-f8178f · https://www.mobygames.com/game/55930/ · https://www.goodreads.com/user_status/book/52122107
- Mitoloji SERP örnekleri: https://en.wikipedia.org/wiki/Illuyanka · https://megatenwiki.com/wiki/Illuyanka · https://www.gamerguides.com/tales-of-zestiria/walkthrough/post-game-2582/calix-iii · https://lightonshell.itch.io/gobeklitepe · https://aadonis.itch.io/secrets-of-the-past
- Çince tür terimi: https://www.233leyuan.com/a/11112127583 · https://tw.my-best.com/115127
- Rakip siteler: https://www.supergiantgames.com/games/hades/ · https://aresinteractive.com/games/heroesvshordes/ · https://store.steampowered.com/app/1794680/Vampire_Survivors/

**Yerel depolar (salt okundu)**
- `blades-of-ages`: `CLAUDE.md`, `docs/00`, `01`, `07`, `12`, `14`, `21`, `31`, `32`, `36`, `YAPILACAKLAR.md`, `data/l10n/*.json`, `game/ProjectSettings/ProjectSettings.asset`
- `zirve-app`: `README.md`, `robots.txt`, `sitemap.xml`, `llms.txt`, `en/index.html`; `zirve/docs/aso-geo/README.md`, `RESEARCH.md`
- `suzgec-app/SEO.md`, `yumus-app/SEO.md`

**Bu oturumda doğrulanamayanlar:** anahtar kelime hacimleri; ja ve ko tür terimlerinin arama hacmi; Smart App Banner'ın
pre-order sayfasındaki davranışı; Google yazılım belgesinde `offers.price`'ın zorunlu etiketi; Steam'in "Bullet Heaven"
etiketinin resmî tarihi; GitHub Pages IP günlüğü ayrıntısı; İYS yükümlülüğünün kapsamı; Discover görsel boyutu önerisi;
rakip alan adlarının geçmiş sahipliği.
