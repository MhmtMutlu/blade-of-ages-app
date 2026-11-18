# Blade of Ages: Çağların Kılıcı · GEO stratejisi

> **19 Kasım 2026 notu:** Oyunun adı her dilde tek: **Blade of Ages: Çağların Kılıcı** (tekil "Blade"); site alan
> adı `bladeofages.mm-apps.com`. Bu belgedeki ad ve alan adı geçişleri buna göre güncellendi; 17 Kasım'daki aday
> adlar README'deki karar tablosunda. Bundle id (`com.mhmtmutlu.agesofblades`) ve API (`api.agesofblades…`) teknik
> kimlik olarak değişmedi.

17 Kasım 2026. Konu: oyunun statik web sitesinin üretken arama ve yanıt motorlarında (ChatGPT, Claude, Perplexity,
Gemini, Google AI Overviews / AI Mode, Copilot) doğru anlatılması, alıntılanması ve kaynak gösterilmesi. Klasik SEO
(`seo.md`) ayrı bir belgede. Bu belge onu tekrar etmez, yalnız GEO'ya özgü kararları yazar.

**Etiketler:**
- **[resmî]**: platformun kendi belgesi.
- **[çalışma]**: yayımlanmış ölçüm ya da makale.
- **[sektör]**: ajans ya da satıcı iddiası, bağımsız doğrulanmadı.
- **[kardeş]**: zirve-app, suzgec-app ya da yumus-app deposu.
- **[depo]**: oyun deposu `blades-of-ages`.
- **(çıkarım)**: benim yorumum.
- **[doğrulanmadı]**: kaynağı bulunamadı ya da okunamadı.

**Temel ilke (kardeş sitelerle aynı):** sitede yalnız oyunun gerçekten yaptığı ve kaynağı gösterilebilen bilgi yazılır.
Hiçbir GEO çalışması bir yapay zekâ yanıtında anılmayı garanti etmez.

**Varsayımlar:**
- Ad: 19 Kasım 2026'dan beri her dilde tek ad, "Blade of Ages: Çağların Kılıcı" (17 Kasım varsayımı ayrı EN ve TR adlardı). Marka tescili hâlâ açık karar
  (`blades-of-ages/YAPILACAKLAR.md` §3). Bu belgedeki her varlık kararı bu varsayıma bağlı (bkz. §9 R1).
- Alan adı: kardeş desenle `<slug>.mm-apps.com`. Örneklerde `bladeofages.mm-apps.com` geçiyor (19 Kasım
  kararı).
- Barındırma: kardeşler gibi GitHub Pages ve derlenmiş statik HTML.

---

## 1. Özet: en önemli 10 karar önerisi (öncelik sırasıyla)

1. **Önce adı kilitle, sonra siteyi aç.** Varlık (entity) tutarlılığı GEO'nun temelidir; ad değişirse bütün
   alıntılar, sameAs bağlantıları ve App Store geçmişi bölünür.
   - 17 Kasım'da ad, alan adı ve kimlik birbirini tutmuyordu: görünen ad ↔ `api.agesofblades…` ↔ depo `ages-of-blades`
     [depo]. Bu, yapay zekânın oyunu sözcükleri ters sıralı adla anmasına yol açabilir (çıkarım). 19 Kasım'da görünen ad
     ve site alan adı hizalandı; bundle id ve API teknik kimlik olarak kaldı.
   - Yakın ad çakışması var: itch.io'da "Blade of Ages I" adlı bir Godot platform oyunu (§3.4).
2. **Tek olgu kaynağı: `data/facts.json`** (Zirve deseni).
   - Site, JSON-LD, `llms.txt` ve basın kiti sayıyı buradan alır; sayı metne çıplak yazılmaz.
   - Derleme, olguları oyun deposunun `data/*.json` ve `data/l10n/*.json` dosyalarıyla karşılaştırır: diyar, harita,
     boss, kahraman sayıları ve adları.
3. **"Enerji yok" iddiasını, can sistemi kararı netleşmeden yazma.** Başarısız sefer denemesinin can harcaması
   (12 Kasım, onay bekliyor; `docs/36`) yapay zekâ özetlerinde "enerji sistemi" olarak okunabilir.
   - Yanlış ya da yanıltıcı bir "adil" iddiası, asistanların en çok tekrarlayacağı cümle olur.
   - Güvenli çekirdek: "zorunlu reklam yok, ödüllü reklam isteğe bağlı" (§3, §9 R3).
4. **Kanonik tek cümlelik tanımı bir kez yaz, her yerde aynen kullan.** Site ilk paragrafı, App Store açıklamasının
   ilk cümlesi, basın kiti, `llms.txt`, IGDB ve sosyal profil biyografileri aynı cümleyi taşır (§3.1).
   - AppTweak'e göre ChatGPT oyun önerilerinde alıntıların %42,6'sı apps.apple.com'dan geliyor [çalışma].
5. **App Store sayfası en büyük GEO yüzeyidir.** Sitenin işi, mağaza metnini tamamlayan ve derin sorulara cevap veren
   sayfalar sunmak. Lansmandan önce **ön sipariş** düşünülmeli: yeni uygulamada çıkıştan 2–180 gün önce açılabilir
   [resmî]. Böylece apps.apple.com URL'si erken oluşur.
6. **İçeriğin omurgası diyar ve boss rehberleri olsun.**
   - Bestiyerdeki faz tablosu ve karşı hamle verisi "Medusa nasıl yenilir" türü sorulara birebir cevap veren, oyuna
     özgü, alıntılanabilir içerik [depo].
   - Similarweb verisinde Google AI Mode'un en çok alıntıladığı alan adı Fandom (%7,16) [sektör]. Tek konuyu derin
     anlatan ve başlıkları net sayfalar öne çıkıyor.
   - Yalnız **oyunda olan** diyarlar yayımlanır; III–V. çağ bugün taslak (§4, §9 R4).
7. **Her diyar sayfasında "Mitte" ile "Oyunda" bölümleri ayrı durur ve mit bilgisi kaynakla verilir.**
   - Bu hem kültürel hassasiyet kuralının (CLAUDE.md kural 7) hem de doğruluğun gereği.
   - GEO makalesinde kaynak ve alıntı eklemenin görünürlüğü artırdığı bildirildi [çalışma]; sonraki bir benchmark bu
     etkileri büyük ölçüde doğrulamadı [çalışma]. Bu yüzden kaynak, doğruluk için eklenir, sihir beklenmez (§4.2).
8. **Teknik politika: kardeşlerle aynı.**
   - `robots.txt` bütün arama, kullanıcı getirmesi ve eğitim botlarına açık.
   - `llms.txt` derlemeyle üretilir: ucuz, zararsız ve okunma oranı düşük.
   - `llms-full.txt` şimdilik yok.
   - JSON-LD tek `@graph` ve görünür metinle birebir.
   - Gerekçe ve trade-off: §5.
9. **Çok dilli GEO, çeviri değil yerel tür sözcüğü işidir.** Japonca, Korece ve Geleneksel Çince sayfalar o pazarın
   tür adını ve mitoloji adlarının yerleşik yazımını kullanır.
   - Çince "類倖存者/割草" teyitli [çalışma değil, kaynak sayfası].
   - Japonca "ヴァンサバ系" ve Korece "뱀서라이크" [doğrulanmadı].
   - Kore için Naver Search Advisor kaydı gerekir. Lansmanda site dilleri: tr, en, ja, ko, zh-Hant (§6).
10. **Ölçüm hukuka uygun ve elle yapılır.**
    - Sitede analitik ve çerez yok.
    - Search Console'un üretken yapay zekâ raporu, Bing'in AI Performance raporu, App Store kampanya bağlantıları
      (`ct=`) ve oyun içinde anonim, isteğe bağlı "bizi nereden duydun?" sorusu kullanılır.
    - Aylık, beş dilde sabit soru setiyle elle test yapılır (§8).

---

## 2. Kardeş sitelerden çıkan GEO desenleri

Okunan dosyalar:
- `zirve-app/README.md`, `data/facts.json`, `data/site.json`, `llms.txt`, `robots.txt`, `en/` sayfaları
- `zirve/docs/aso-geo/{README,RESEARCH,AI_VISIBILITY,OUTREACH,AUDIT}.md`
- `suzgec-app/SEO.md`, `llms.txt`
- `yumus-app/SEO.md`, `llms.txt`

| Desen | Nerede | Karar | Not |
|---|---|---|---|
| `facts.json`: tek olgu kaynağı ve sürüm bayrağı (`live`, `versions.<v>`) | Zirve | **Aynen** | Oyunda sürüm bayrağı daha da önemli. Fiyat, dil ve içerik sürümle değişir. |
| Derleme, olguları uygulama deposuyla karşılaştırır, uyuşmazsa durur | Zirve (`../zirve`) | **Uyarla** | Kaynak `blades-of-ages/data/{eras,realms,bosses,heroes,weapons}.json` ve `data/l10n/<dil>.json`. Diyar, boss ve silah adları oyundaki çeviriyle aynı olmalı. |
| Sayıyı metne çıplak yazmama (`{realms}` yer tutucusu) | Zirve | **Aynen** | 12 / 120 / 21 / 5 sayıları içerik eklendikçe değişebilir. |
| JSON-LD metinleri görünür metinde birebir geçer; tek `@graph` | Zirve, Yumuş | **Aynen** | Google da yapılandırılmış verinin görünür metinle eşleşmesini öneriyor [resmî]. |
| `VideoGame` + `MobileApplication` birlikte tip; puan ve yorum uydurulmaz | Zirve, Yumuş | **Aynen** | Google uygulama zengin sonucu `aggregateRating` ya da `review` ister [resmî]; olmadan zengin sonuç yok, sorun değil. |
| `FAQPage` yalnız destek sayfasında | Zirve | **Uyarla** | Diyar ve boss sayfalarında görünür SSS bölümü olur, `FAQPage` işaretlemesi değil. FAQ zengin sonucu 7 Mayıs 2026'da kalktı [sektör, birden çok kaynak]. |
| `llms.txt`: başta tek cümle tanım, "Facts", "Pages", "Other languages" | Zirve (EN), İçgör ve Yumuş (TR + EN) | **Aynen** (Zirve biçimi, EN) | Derleme üretir. Elle yazılmaz. |
| `robots.txt`: bütün botlar açık, AI botları adıyla listeli | Zirve | **Aynen** | Gerekçe: §5.2. |
| Basın kiti: olgu tablosu, kısa ve uzun hazır açıklama | Zirve, Yumuş | **Aynen** | Oyunda en değerli GEO sayfası (§4). |
| Yasaklı ifade denetimi ("en iyi", "#1", "garanti" …) | İçgör, Yumuş | **Uyarla** | Oyun listesi: "en iyi", "#1", "pay-to-win değil" (iddia değil olgu yaz), rakip markası başlıkta, "ilk ve tek" (doğrulanmamış özgünlük iddiası). |
| Doorway yok: niyet başına kapı sayfası açılmaz | Zirve kararı 1, Yumuş | **Aynen** | "survivor oyunları", "reklamsız oyunlar" gibi niyet sayfaları açılmaz. |
| Her oyun sayfasında oyuna özgü kural, ipucu ve gerçek ekran görüntüsü | Zirve `/games/*` | **Uyarla** | Diyar ve boss sayfaları için şablon (§4.2). |
| "What this kind of puzzle is called" bölümü (tür adı köprüsü) | Zirve | **Aynen** | "Bu türe ne denir: survivor-like / bullet heaven / reverse bullet hell". Asistanın tür sorusundan oyuna köprü kurar. |
| `lastmod` içerik hash'i değişince ilerler | Zirve, İçgör | **Aynen** | Tazelik sinyali yalandan ilerletilmez. |
| IndexNow (yayından sonra) | hepsi | **Aynen** | Bing dizini Copilot'u besler. ChatGPT'nin Bing'e bağımlılığı [doğrulanmadı]. |
| Videolar kendi sunucuda, izleme sayfası ana içerik | Yumuş | **Uyarla** | Boss videoları için. YouTube gömülmez (çerez); YouTube'a ayrıca yüklenir (§7). |
| Aylık elle AI görünürlük ölçümü ve kayıt şablonu | Zirve `AI_VISIBILITY.md` | **Aynen** | Soru seti oyuna göre (§8). |
| Site dışı keşif planı: ücretsiz, sözleşmesiz, gönderimi kullanıcı yapar | Zirve `OUTREACH.md` | **Uyarla** | Oyun basını ve toplulukları farklı (§7). |
| Wikidata yalnız ilk bağımsız yazıdan sonra | Zirve | **Aynen** | §3.3. |
| "Privacy-first" gibi gizlilik pazarlaması kullanılmaz | Zirve kararı 3 | **Aynen** | Oyunda reklam SDK'sı (AdMob) olacak. |
| Hukuk sayfaları çok dilli üretim | Zirve | **Alma (GEO için)** | Hukuk metinleri GEO hedefi değil. Kapsamı `seo.md` ve hukuk işi belirler. |
| 17 dilde oyun sayfası | Zirve | **Alma (şimdilik)** | Oyunda içerik sayfası çok (12 diyar + 12 boss + 5 muhafız). Kalite ve LQA maliyeti yüzünden önce 5 dil (§6). |
| Uygulamanın "kategori" sayfaları (E kodları vb.) | İçgör | **Alma** | Oyunun karşılığı diyar ve boss sayfaları. |

---

## 3. Varlık tanımı

### 3.1 Kanonik tek cümlelik tanım (taslak)

Kurallar:
- Sayılar `facts.json`'dan gelir.
- Cümlede şunlar olur: tür, platform, geliştirici, oyunu ayıran **mekanik**, kapsam ve bir adil oyun olgusu.
- Abartı ve üstünlük iddiası olmaz.
- "Enerji yok" ifadesi can kararına kadar dışarıda kalır (§9 R3).

**TR (taslak):**
> Blade of Ages: Çağların Kılıcı, mm-apps'in Türkiye'de geliştirdiği, iPhone ve iPad için bir survivor-like aksiyon RPG'dir:
> kahramanın etrafında uçları dışa bakan kılıçlar döner, oyuncu tek parmakla yalnızca hareket eder ve Göbeklitepe'den
> Japonya'ya {ages} çağa yayılan {realms} mitoloji diyarında {maps} haritada savaşır; zorunlu reklam yoktur.

**EN (taslak):**
> Blade of Ages: Çağların Kılıcı is a survivor-like action RPG for iPhone and iPad by mm-apps, an independent developer in Türkiye:
> swords orbit your hero with their tips pointing outward, you only move with one finger, and you fight through
> {maps} maps in {realms} mythology realms across {ages} ages, from Göbekli Tepe to Japan, with no forced ads.

**Kısa varyant (App Store alt başlığı ya da sosyal biyografi):**
- TR: "Dönen kılıçlar, 12 mitoloji diyarı" (sayı `facts.json`'dan gelir).
- EN: "Orbiting swords, 12 mythic realms".
- Alt başlıkta "reklamsız" ya da "zorunlu reklam yok" kullanılmaz (Zirve kararı 4, 2.3.7) [kardeş].

**Gerekçe:**
- "Uçları dışa bakan dönen kılıçlar" ve "tek parmak" oyunun değişmez kuralları (CLAUDE.md kural 1–2) [depo].
- Rakip listelerinde bu ifade yok (çıkarım). Asistanın oyunu ayırt etmesini sağlayan çapa bu.
- Diyar listesinin uçları (Göbeklitepe, Japonya) iki farklı arama kümesine köprü kurar: Anadolu arkeolojisi ve Doğu
  mitolojisi.
- Yalnız "mitoloji" demek ayırt edici değil (çıkarım).

### 3.2 Olgu tablosu: `data/facts.json` önerisi

Zirve şemasının oyuna uyarlanmış hali:
- `(game)` işaretli alanları derleme oyun deposundan üretir ya da onunla karşılaştırır.
- `null` henüz karar ya da yayın olmayanı gösterir. `null` alan sitede yazılmaz.

```json
{
  "_doc": "Single source of truth for every fact the site, JSON-LD, llms.txt, press kit and OG cards state. Fields marked (game) are checked against ../blades-of-ages/data at build time.",
  "live": null,
  "versions": {
    "1.0": {
      "softwareVersion": "1.0",
      "releaseDate": null,
      "appLanguages": ["tr", "en", "ja", "ko", "zh-Hant", "de", "fr", "es-419", "es-ES", "pt-BR", "it", "pl", "zh-Hans"],
      "realmsLive": ["gobeklitepe", "sumer", "misir", "yunan", "hitit", "iskandinav", "turk_altay", "kelt", "japon", "cin", "mezoamerika", "silik"],
      "modes": ["campaign", "ageGates", "rebirth", "endless", "dailyTrial", "arena"]
    }
  },
  "names": { "all": "Blade of Ages: Çağların Kılıcı", "short": "Blade of Ages" },
  "alternateNames": ["Caglarin Kilici"],
  "storeNames": { "en": null, "tr": null },
  "appStoreId": null,
  "preOrder": null,
  "developer": "mm-apps",
  "platforms": ["iPhone", "iPad"],
  "minOS": null,
  "genre": { "en": ["Survivor-like", "Action RPG", "Roguelite"], "tr": ["Survivor-like", "Aksiyon RPG"] },
  "controls": "one finger, move only; swords attack automatically",
  "ages": 5,
  "realms": 12,
  "mapsPerRealm": 10,
  "maps": 120,
  "heroes": 21,
  "ageGuardians": 5,
  "realmOrder": "(game) data/realms.json",
  "bosses": "(game) data/bosses.json + data/l10n/<lang>.json content.bosses.*.name",
  "monetization": {
    "forcedAds": false,
    "rewardedAdsOptional": true,
    "energySystem": null,
    "_energySystem": "Do not state until the lives rule in docs/36 is decided: failed expedition attempts cost a life (5 lives, 20 min).",
    "pvpPowerEqualized": true,
    "iap": ["diamond packs", "premium pack", "season pass", "cosmetics"],
    "prices": null
  },
  "contentPolicy": { "blood": false, "ageRating": null },
  "unavailableStorefronts": ["CN"],
  "_unavailableStorefronts": "Mainland China needs an ISBN licence (docs/32); RU has App Store purchases disabled since 1 Apr 2026 (docs/32) — decide whether to list RU.",
  "offlinePlay": null,
  "sameAs": [],
  "lastReviewed": null
}
```

**Notlar:**
- `realmsLive` site için en kritik alan. Bir diyar sayfası yalnız buradaki diyar için üretilir.
  - Bugün yalnız ilk beş diyar oyunda tam (`docs/31` §3) [depo].
  - Plan "lansman = 12 diyar" diyor. Gerçekleşmezse liste kısalır ve site kendiliğinden doğru kalır.
- Fiyatlar (`docs/07`'deki 5,99 $ vb.) öneri. Mağazada başlamadan sitede yazılmaz (İçgör `PRICE_SET` deseni) [kardeş].
- `offlinePlay`: oyun sunucu doğrulamalı koşu kaydı kullanıyor (`docs/14` §4.3a) [depo]. Çevrim dışı iddiası Zirve gibi
  uçak modunda doğrulanmadan yazılmaz.

### 3.3 sameAs ve kimlik tutarlılığı planı

Hedef: her yerde aynı ad, geliştirici ve tanım ve birbirine işaret eden bir bağlantı ağı. Sıra önemli; bağımsız kaynak
yokken kendi yarattığımız düğümler zayıf kalır.

| Düğüm | Ne zaman | sameAs'e girer mi | Not |
|---|---|---|---|
| Site `/` ve `/en/` | Ad kesinleşince | `@id` kendisi | `VideoGame` düğümü tek `@id` (ör. `https://<alan>/#game`), bütün dillerde aynı. |
| `mm-apps.com/<slug>/` geliştirici sayfası | Siteyle aynı gün | Evet | Zirve'de var [kardeş]. |
| App Store ürün sayfası (ön sipariş ya da yayın) | Ön sipariş açılınca | Evet | `installUrl` yalnız yayında. Ön siparişte `offers.availability = PreOrder` (çıkarım; Google desteği [doğrulanmadı]). |
| IGDB | Ön sipariş ya da yayın | Evet | Yayınlanmamış oyunların eklenip eklenmediği belirsiz [doğrulanmadı]. Zirve planında "asistanlar okur" notu var [kardeş]. |
| YouTube kanalı (fragman, boss videoları) | Lansmandan 2–4 hafta önce | Evet | YouTube AI yanıtlarında sık alıntılanıyor [sektör, çelişkili veriler]. |
| Sosyal profiller (X, Bluesky, TikTok, Instagram, Reddit) | Yalnız bakılacaksa | Evet, açıldıysa | Biyografi = kanonik kısa tanım + site bağlantısı. Hesabı kullanıcı açar. Bakılmayan profil, eskimiş olgu kaynağı olur. |
| Basın yazıları | Yayından sonra | Hayır (sameAs değil) | Basın kiti sayfasında "Hakkımızda yazılanlar" listesi olarak durur. |
| Wikidata | İlk bağımsız, ciddi yazıdan sonra | Evet | Wikidata önemliliği "ciddi ve kamuya açık kaynak" ister [resmî: wikidata.org/wiki/Wikidata:Items]. Kendi kendine erken açılan öğe silinebilir (Zirve kararı) [kardeş]. Wikipedia maddesi hedeflenmez; bağımsız ve kapsamlı yayın şartı var [resmî: WP:NVG]. |
| Steam, Google Play | Yok | Hayır | Platform yalnız Apple [depo]. |

**Tutarlılık kontrol listesi** (her yeni düğümde):
1. Ad tam olarak `names.en` ya da `names.tr`.
2. Geliştirici "mm-apps".
3. Tanım §3.1 cümlesi ya da kısa varyantı.
4. Sayılar `facts.json`'daki gibi.
5. Site bağlantısı kanonik URL.
6. Görsel olarak aynı ikon.

### 3.4 Ad çakışmaları ve ayırt etme

| Ad | Durum | Kaynak |
|---|---|---|
| Çoğul İngilizce ad (17 Kasım adayı) | Birebir eşleşen bir oyun bulunamadı. Yakın: "Blade of Ages I" (itch.io, Godot platform oyunu, geliştiriliyor). 19 Kasım notu: seçilen tekil "Blade of Ages" bununla birebir örtüşüyor | [çalışma değil, arama sonucu: lepcquiparle.itch.io/knight-adventure] |
| "Blades of Fire", "Blades of Time", "Blades of Worlds", "Rage of Blades" | Farklı oyunlar. Ad uzayı kalabalık | arama sonuçları (metacritic, mobygames, pocketgamer) |
| "Age of Blades" / sözcükleri ters sıralı Unity adı | Mobil oyun bulunamadı | arama sonucu |
| "Çağların Kılıcı" | Hiç sonuç yok | arama sonucu |

**Öneri:**
- JSON-LD `VideoGame.description` ve `disambiguatingDescription` alanında "survivor-like action RPG for iPhone and iPad
  by mm-apps" ifadesi her zaman geçsin. Ayırt edici çapa tür + platform + geliştirici üçlüsü.
- Bundle id ve API dışındaki her görünür yerde sözcükleri ters sıralı eski ad kullanılmasın (19 Kasım: sitede uygulandı).
- Marka tescil araştırması bu belgenin kapsamında değil. Ad kararı ondan sonra.

---

## 4. İçerik mimarisi

### 4.1 Sayfa türleri

Asistanların alıntıladığı sayfa çoğunlukla ana sayfa değil, tek bir soruya derin cevap veren alt sayfa
[sektör: Similarweb, "AI rarely cites homepages"]. Oyunlarda kendi web içeriği zayıf olduğu için asistan mağazaya,
Reddit'e ve Wikipedia'ya düşüyor [çalışma: AppTweak]. Bizim boşluğu doldurma fırsatımız bu.

| # | Sayfa | Örnek yol (TR / EN) | Cevapladığı soru | JSON-LD | Ne zaman |
|---|---|---|---|---|---|
| 1 | Ana sayfa | `/` · `/en/` | "Blade of Ages nedir?" | `VideoGame`+`MobileApplication`, `WebPage` | Ad kesinleşince |
| 2 | Nasıl oynanır: kılıç mekaniği | `/nasil-oynanir/` · `/en/how-to-play/` | "Kılıçlar nasıl çalışıyor, tek elle oynanır mı, savuşturma ne?" | `Article` | Lansman öncesi |
| 3 | Adil oyun sözü | `/adil-oyun/` · `/en/fair-play/` | "Pay-to-win mi, enerji var mı, reklam zorunlu mu?" | `WebPage` (+`about` → oyun) | Can kararı sonrası |
| 4 | Diyarlar dizini | `/diyarlar/` · `/en/realms/` | "Oyunda hangi mitolojiler var?" | `CollectionPage`+`ItemList` | Lansman |
| 5 | Diyar sayfası (×yayındaki diyar) | `/diyarlar/hitit/` · `/en/realms/hittite/` | "Oyunun Hitit bölümünde ne var?", "Hitit mitolojisi geçen oyun" | `Article` (+`about`/`mentions` → mit varlıkları) | Lansman |
| 6 | Boss rehberi (×12) | `/diyarlar/yunan/medusa/` · `/en/realms/greece/medusa/` | "Medusa nasıl yenilir?" | `Article` (+ isteğe bağlı `VideoObject`) | Lansman, sonra |
| 7 | Çağ Muhafızları ve Çağ Kapısı | `/cag-muhafizlari/` · `/en/age-guardians/` | "Age Gate nedir, muhafız nasıl yenilir?" | `Article` | Lansman |
| 8 | Basın kiti ve olgu sayfası | `/basin/` · `/en/press/` | Gazeteci, liste yazarı ve asistan için tek olgu yeri | `AboutPage` | Lansman öncesi |
| 9 | Destek ve SSS | `/destek/` · `/en/support/` | Hesap, satın alma, cihaz desteği | `FAQPage` (yalnız burada) | Lansman |
| 10 | Güncellemeler (sürüm notları) | `/guncellemeler/` · `/en/updates/` | "Son güncellemede ne geldi?", tazelik | `Blog`/`BlogPosting` ya da `Article` listesi | Yayından sonra |
| 11 | Geliştirme günlüğü (isteğe bağlı) | `/gunluk/…` · `/en/devlog/…` | Birinci elden tasarım deneyimi (ör. "dışa bakan kılıçları nasıl dengeledik") | `BlogPosting` | Lansman öncesi ve sonrası |
| 12 | Kahramanlar (isteğe bağlı) | `/kahramanlar/` · `/en/heroes/` | "Hangi kahraman seçilmeli?" | `CollectionPage` | Güçler kesinleşince |

**Bilerek olmayanlar:**
- **Düşman başına ayrı sayfa yok.** 3 düşman + elit diyar sayfasında bölüm olur. Tek düşman sayfası ince içerik
  (thin) ve kapı sayfası riski taşır.
- **"Vampire Survivors alternatifleri" ya da "en iyi survivor oyunları" sayfası yok.** Kendi sitemizde liste yazmak
  güvenilir değil ve spam sayılabilir. Bu listelerde yer almak site dışı iştir (§7). Google rehberi de "inauthentic
  mentions" peşinde koşmayı önermiyor [resmî].
- **Rakip karşılaştırma sayfası yok, karşılaştırma bölümü var.** Ana sayfada ve basın kitinde kısa, olgusal bir "Türün
  içinde nerede?" bölümü yer alır. Marka adı yalnız gövde metninde, tanımlayıcı olarak geçer: "Vampire Survivors'ın
  yaygınlaştırdığı survivor-like türünde…". Başlıkta ve URL'de rakip markası olmaz (§9 R7).
- **Henüz oyunda olmayan diyar ya da sistem için sayfa yok.** "Yol haritası" sayfası da yok: vaat, asistanlarda
  olgu gibi tekrarlanır.

### 4.2 Yapı şablonları

Ortak iskelet (her içerik sayfası):

```
Breadcrumb (görünür; BreadcrumbList ile aynı)
H1: <Konu>: <tek satır açıklama>              ← tek H1
Answer-first paragraf (2–3 cümle)             ← sayfanın sorusuna doğrudan cevap; konu adı + oyun adı birlikte geçer
Olgu kutusu (<dl>)                            ← facts.json / data'dan; sayı çıplak yazılmaz
Bölümler (H2, her biri tek alt soru)
SSS (görünür, 3–5 soru; FAQPage işaretlemesi yok)
Kaynaklar (mit ve tarih iddiaları için dış bağlantılar)
"Son güncelleme: <tarih> · Sürüm <v>"         ← lastmod.json'dan
App Store rozeti (ct=site)
```

Answer-first ve olgu kutusu neden önemli: Google "chunking" ya da özel yazım gerekmediğini söylüyor [resmî]. Yine de
açık başlıklı, tek konulu ve ilk paragrafı soruya cevap veren sayfa her motorda alıntılanabilir bir parça bırakır
(çıkarım; Similarweb gözlemiyle uyumlu [sektör]). Bu, okuyan insan için de iyi bir yazımdır; ayrı bir "AI metni"
yazılmaz.

**Kanıt durumu (dürüst not):**
- Princeton/IIT GEO makalesi (KDD 2024) kaynak, alıntı ve istatistik eklemenin üretken motor yanıtlarında görünürlüğü
  "%40'a kadar" artırabildiğini ve etkinin alana göre değiştiğini bildiriyor [çalışma: arxiv.org/abs/2311.09735].
  Yöntem başına yüzdeler ikincil kaynaklarda çelişkili; makalenin tablosundan doğrulamadım.
- C-SEO Bench (NeurIPS 2025 D&B) çoğu "conversational SEO" yönteminin büyük ölçüde etkisiz olduğunu, bazılarının zarar
  verdiğini ve geleneksel SEO'nun daha etkili kaldığını buldu. Benimseyen arttıkça kazanç düşüyor [çalışma:
  arxiv.org/abs/2506.11097].
- **Sonuç (çıkarım):**
  - Gerçek olgu, gerçek kaynak ve gerçek sayı yazılır, çünkü doğrudur ve oyuncuya yarar.
  - "İstatistik ekle ki AI alıntılasın" diye uydurma ya da şişirilmiş veri eklenmez.
  - Anahtar kelime yığma, orijinal makalede de taban değerin altında kalmıştı.

#### a) Diyar sayfası

```
H1: Hitit diyarı: Fırtına Dağları (41–50. haritalar)
Answer-first: "Blade of Ages: Çağların Kılıcı'nda Hitit diyarı, II. Çağ'ın son diyarıdır ve {mapRange} haritalarını kapsar.
  Fırtına Dağları'nda yıldırım düşen alanlardan kaçarken Kaya Devi, Fırtına Ruhu ve Dağ Keçisi Süvari ile savaşırsın;
  elit Ullikummi, boss İlluyanka'dır."
Olgu kutusu: Çağ · Haritalar · Harita kuralı · Düşmanlar · Elit · Boss · Diyar silahı · Zırh seti (2/4 parça) · Mit gücü
H2 Mitte: İlluyanka ve Ullikummi kimdir?     ← 1–2 paragraf, kaynakla (müze, ansiklopedi, akademik); oyun yorumu yok
H2 Oyunda: diyar nasıl oynanır              ← harita kuralı, yapılar, karşı hamleler
H2 Düşmanlar                                ← her biri: davranış, öğrettiği, karşı hamle (bestiyerden)
H2 Boss: İlluyanka → rehbere bağlantı
H2 Diyar silahı ve set
H2 SSS                                      ← "Hitit diyarı kaçıncı haritada açılır?", "Yıldırımdan nasıl kaçılır?"
Kaynaklar
```

- "Mitte" ile "Oyunda" ayrımı zorunlu. Oyunun icadı (ör. "Akbaba Ana", Göbeklitepe'nin akbaba
  kabartmalarından esinlenen bir boss) mit gibi sunulursa asistanlar bunu gerçek mit diye tekrarlar. Bu bir yanlış
  bilgi riski (§9 R5).
- Arkeolojik olarak tartışmalı yorumlar (Göbeklitepe'nin işlevi gibi) kesin olgu diye yazılmaz.
- Veri kaynağı: `docs/05-bestiyer/*.md` `tools/build_bestiary.py` ile `data/`'dan üretiliyor [depo]. Site derlemesi
  bestiyer Markdown'ını değil `data/*.json` ve `data/l10n/<dil>.json`'ı okumalı. Böylece ad ve sayı oyunla aynı kalır.
- **Bulgu: İngilizce ad tutarsız.**
  - `content.realms.hitit.name = "Hatti"`, ama silah adı "Hittite Iron Sword" [depo: `data/l10n/en.json`].
  - Japonca (ヒッタイト), Korece (히타이트) ve Çince (赫梯) "Hitit" diyor.
  - İlluyanka miti Hatti kökenli, Hitit metinlerinde korunmuş. "Hatti" yanlış değil, ama yerleşik arama terimi
    "Hittite mythology" (çıkarım).
  - Karar oyunun: sayfa başlığında "Hittite (Hatti)" kullanılabilir ya da oyun içi ad gözden geçirilebilir (§9 açık
    soru).

#### b) Boss rehberi

```
H1: Medusa nasıl yenilir · Blade of Ages: Çağların Kılıcı boss rehberi
Answer-first: "Medusa, Yunan diyarının 40. haritasındaki boss'tur ve üç fazda savaşır. Mor zehir kürelerini
  kılıçlarınla savuşturup yaklaş, taşlaştıran bakış sırasında …, Heykel Bahçesi fazında …."
Olgu kutusu: Diyar · Harita · Faz sayısı · Süre (yaklaşık) · Önerilen hazırlık (set, silah) · Ödül (ilk zafer)
H2 Fazlar (tablo: Faz · Can eşiği · Saldırı · Karşı hamle)   ← bestiyer tablosu, birebir veri
H2 Hazırlık: hangi silah, set ve yörünge formu
H2 Sık yapılan hatalar
H2 Mitte: Medusa (kaynakla, 1 paragraf)
H2 SSS: "Medusa'nın bakışı savuşturulur mu?", "Medusa'yı yenince ne açılır?"
Video (isteğe bağlı, kendi sunucuda, izleme sayfası)
```

- Faz tablosu, oyun içi `data/bosses.json` + `l10n` verisinden üretilir. Bir denge değişikliği sayfayı da günceller
  ve `lastmod` ilerler.
- "Can %, saniye" gibi denge sayıları güncellemeyle değişir. Sayfada "Sürüm {v} için" notu durur.
- Bot ölçümleri (ör. "İlluyanka zırh kademesi olmadan duvar", `docs/03`) özgün veri. Sitede yer alacaksa tarihli
  geliştirme günlüğü yazısında yer alır, rehberde değil.

#### c) Nasıl oynanır

```
H1: Nasıl oynanır: dönen kılıçlar, tek parmak
Answer-first: "Blade of Ages: Çağların Kılıcı'nda yalnızca hareket edersin; kahramanın etrafındaki kılıçlar uçları dışa bakacak
  şekilde döner ve otomatik vurur. Yürürken kılıç halkası genişler, durunca daralır ve hızlanır."
Olgu kutusu: Kontrol · Başlangıç kılıcı / üst sınır · Harita süresi · Mor mermi = savuşturulur · Kırmızı alan = kaç
H2 Hareket ve duruş (geniş/dar yörünge)
H2 Savuşturma: mor mermiler
H2 Seviye atlama ve kartlar
H2 Harita, kamp ve sefer
H2 Bu türe ne denir? (survivor-like, bullet heaven, reverse bullet hell; türün kısa, olgusal tarihi)
H2 SSS
GIF/kısa video (kendi sunucuda)
```

Sayılar (`R_WIDE 64 px`, `4 → 7 kılıç`, `180 sn`) `data/combat.json` ve `data/weapons.json`'dan gelir. Oyuncuya px
yazılmaz; "geniş / dar" yeterli. "Kaç kılıçla başlanır" gibi soruya cevap olan sayılar ise yazılır.

#### d) Adil oyun sözü

```
H1: Adil oyun · Blade of Ages: Çağların Kılıcı'nda neyi satmıyoruz
Answer-first: olgularla (iddia değil): "Zorunlu reklam yok; reklam yalnızca sen bir ödül seçersen oynar.
  Arenada güç eşitlenir. Temel özellikler için abonelik yok. İlk satın alma teklifi {firstOfferMap}. haritadan önce
  gösterilmez."
Olgu kutusu: Reklam · Satın alınabilenler · Arena · Abonelik · Can sistemi (karar sonrası, açıkça)
H2 Ne satılıyor (liste, fiyatlar yalnız mağazada başladıysa)
H2 Ne satılmıyor
H2 Can sistemi nasıl çalışır (karar verildiyse; şeffaf)
H2 Değişiklik geçmişi (tarihli; bir ilke değişirse burada yazar)
```

- Bu sayfa "is Blade of Ages pay to win" sorusunun kaynağı olmaya aday (çıkarım).
- Sözcük seçimi: "pay-to-win değil" bir iddia, "arenada güç eşitlenir" bir olgu. Yalnız olgu yazılır (yasaklı ifade
  denetimi).
- Değişiklik geçmişi zorunlu. Asistanlar eski sürümü önbellekte tutar; tarihli kayıt yanlış bilgiyi düzeltmenin tek
  yolu.

#### e) Basın kiti

Zirve `/en/press/` birebir şablon [kardeş]:
- Olgular tablosu.
- Kısa açıklama: §3.1 cümlesi.
- Uzun açıklama (~120 kelime).
- Diyar listesi (her biri bağlantılı).
- Logo, ikon ve ekran görüntüleri (indirilebilir, alt metinli).
- Fragman.
- İletişim.
- "Hakkımızda yazılanlar" (yayından sonra).

Liste yazarları ve asistanlar için tek yer burası. Bütün site dışı gönderimlerde bu sayfanın bağlantısı verilir.

---

## 5. Teknik

### 5.1 `llms.txt` ve `llms-full.txt`

**Durum (2026):**
- Google Search `llms.txt` kullanmıyor. 15 Mayıs 2026 tarihli "AI optimization guide", AI özelliklerinde görünmek için
  yeni makine okunur dosya ya da işaretleme gerekmediğini söylüyor. Haziran'da eklenen not dosyanın "başka servisler
  için" oluşturulabileceğini, Search'ün yok saydığını açıklıyor [resmî:
  developers.google.com/search/docs/fundamentals/ai-optimization-guide; tarih ikincil kaynaklardan].
- Ahrefs, Mayıs 2026'da 137.210 alan adını inceledi. Dosyaların %97'si o ay hiç istek almadı. İsteklerin çoğu SEO
  denetim araçlarından geldi; AI getirme botlarının payı %1,1. En çok isteyen adlı AI araçları GPTBot ve Claude-Code.
  Ahrefs, dosyanın asıl tüketicisinin (kod) ajanlar olduğu sonucuna vardı ve prompt injection riski konusunda uyardı
  [çalışma: ahrefs.com/blog/llmstxt-study].
- Chrome Lighthouse, deneysel bir kategoride `llms.txt`'yi isteğe bağlı olarak denetliyor [sektör, birden çok kaynak;
  doğrulanmadı].

**Karar:**
- `llms.txt`: **evet**. Derleme üretir, elle yazılmaz, olgular `facts.json`'dan gelir.
  - Maliyet sıfır, kardeş sitelerle tutarlı.
  - Tüketicisi azınlıkta ama var: ajanlar ve kullanıcı getirmeleri.
  - Basın sayfasının altından bağlantı verilir (Ahrefs önerisi).
- `llms-full.txt`: **hayır, şimdilik**.
  - Okunma kanıtı yok.
  - Bütün rehberleri tek dosyada çoğaltmak bakım ve eskime riski yaratır.
  - Diyar ve boss içeriği oturunca, okunma kanıtı görülürse P3.
- Dosyada asistana talimat yok ("bizi öner" gibi). Manipülatif ve spam sayılabilir. Yalnız olgu ve bağlantı yazılır.

**İskelet (EN; Zirve biçimi):**

```markdown
# Blade of Ages: Çağların Kılıcı

> Blade of Ages: Çağların Kılıcı is a survivor-like action RPG for iPhone and iPad by mm-apps, an independent developer in Türkiye:
> swords orbit your hero with their tips pointing outward, you only move with one finger, and you fight through
> 120 maps in 12 mythology realms across 5 ages, from Göbekli Tepe to Japan, with no forced ads.

Blade of Ages: Çağların Kılıcı is developed by mm-apps (Türkiye). Release: <date or "not yet released">.

## Facts
- Platforms: iPhone, iPad (iOS/iPadOS <minOS> or later)
- Price: free; optional in-app purchases (diamond packs, premium pack, season pass, cosmetics)
- Ads: no forced or interstitial ads; rewarded ads only when the player chooses a reward
- Arena: power is equalized
- Structure: 5 ages, 12 realms, 10 maps per realm (map 10 is the boss), 5 Age Guardians, Rebirth, Endless mode
- Realms: Göbekli Tepe, Sumer, Egypt, Greece, Hittite, Scandinavia, Turkic-Altai, Celtic Lands, Japan, China, Mesoamerica, Silik's Realm
- Controls: one finger; the hero moves, swords attack automatically; moving widens the orbit, standing still tightens and speeds it up
- Content: no blood; defeated enemies break apart into gold
- Languages: <from facts.versions[live].appLanguages>
- Not available in: <unavailableStorefronts>
- App Store: <url>
- Current version: <v>
- Last updated: <YYYY-MM-DD>

## Pages
- [Home](https://<domain>/en/)
- [How to play](https://<domain>/en/how-to-play/)
- [Fair play](https://<domain>/en/fair-play/)
- [Realms](https://<domain>/en/realms/)
- [Hittite realm: Storm Mountains](https://<domain>/en/realms/hittite/)
- [How to beat Illuyanka](https://<domain>/en/realms/hittite/illuyanka/)
- … (only realms in facts.versions[live].realmsLive)
- [Age Guardians](https://<domain>/en/age-guardians/)
- [Press kit](https://<domain>/en/press/)
- [Support](https://<domain>/en/support/)
- [Privacy policy](https://<domain>/en/privacy/)

## Other languages
- Türkçe: https://<domain>/
- 日本語: https://<domain>/ja/
- 한국어: https://<domain>/ko/
- 繁體中文: https://<domain>/zh-hant/

## Optional
- [Developer](https://mm-apps.com/)
```

Örnekteki sayılar ve adlar derlemede `facts.json` ile `l10n`'dan doldurulur. Elle yazılmış sayı Zirve'deki gibi
derleme hatasıdır.

### 5.2 `robots.txt`: AI bot politikası

| Bot | Görevi | Kapatırsan | Kaynak |
|---|---|---|---|
| OAI-SearchBot | ChatGPT arama dizini | ChatGPT arama cevaplarından çıkarsın (gezinme bağlantısı kalabilir) | [resmî: developers.openai.com/api/docs/bots] |
| GPTBot | OpenAI model eğitimi | Yalnız eğitimden çıkarsın, aramayı etkilemez | [resmî] |
| ChatGPT-User | Kullanıcı isteğiyle getirme | robots.txt uygulanmayabilir | [resmî] |
| Claude-SearchBot | Claude arama dizini | Arama görünürlüğü azalabilir | [resmî: support.claude.com/en/articles/8896518] |
| Claude-User | Kullanıcı isteğiyle getirme | Kullanıcının sorusunda getirilmez | [resmî] |
| ClaudeBot | Anthropic eğitimi | Gelecek içerik eğitimden çıkar | [resmî] |
| PerplexityBot | Perplexity arama dizini | Perplexity sonuçlarından çıkarsın | [resmî: docs.perplexity.ai/guides/bots] |
| Perplexity-User | Kullanıcı isteğiyle getirme | Genelde robots.txt'yi uygulamaz | [resmî] |
| Google-Extended | Ayrı bot değil, kontrol jetonu: Gemini eğitimi ve Gemini/Vertex "grounding" | Search'e dahil olmayı ve sıralamayı etkilemez. AI Overviews'a etkisi sayfada yazmıyor | [resmî: developers.google.com/…/google-common-crawlers] |
| Googlebot | Search, AI Overviews, AI Mode | AI Overviews ve AI Mode'u yalnız Search kontrolleri (`nosnippet`, `max-snippet`, `noindex`) sınırlar | [resmî: …/appearance/ai-features] |
| Applebot | Spotlight, Siri, Safari aramaları | Apple aramalarından çıkarsın | [resmî: support.apple.com/en-us/119829] |
| Applebot-Extended | Tarama yapmaz. Applebot verisinin Apple temel modellerini eğitmede kullanılmasını kontrol eder | Siri, Spotlight ve Safari'de kalırsın | [resmî] |
| Bingbot | Bing ve Copilot | Copilot alıntılarından çıkarsın | Bing AI Performance raporu [sektör ve resmî blog] |
| Yeti | Naver araması | Naver ve AI Briefing'den çıkarsın | [sektör; Naver resmî belgesi okunmadı] |
| CCBot | Common Crawl (birçok modelin eğitim verisi) | Gelecek modellerin oyun bilgisinden çıkarsın (çıkarım) | — |

**Öneri:** kardeşlerle aynı, hepsi açık. Zirve `robots.txt`'si birebir kopyalanır. `Yeti` adıyla eklenir (Kore pazarı
için açık niyet; `*` zaten kapsıyor).

**Gerekçe:**
- Yeni ve bilinmeyen bir oyunda risk "fazla görünmek" değil, hiç bilinmemek.
- Eğitim botlarını açmak, gelecekteki modellerin oyunu arama yapmadan da doğru tanıma ihtimalini artırır (çıkarım;
  ölçülemez).
- Sitedeki içerik pazarlama ve rehber, korunacak ticari sır değil.
- Kardeş sitelerle tek politika bakımı basitleştirir.

**Trade-off'lar (açıkça):**
- Eğitime giren içerik atıfsız kullanılabilir. Sanat görselleri de buna dahil.
  - Seçenek: yüksek çözünürlüklü konsept sanatını basın kitinde yalnız ZIP olarak vermek ve `/assets/press/`
    yolunu `GPTBot`, `ClaudeBot`, `CCBot` ve `Google-Extended` için kapatmak.
  - Arama botları açık kalır.
  - Önerim: gerek yok; görseller zaten mağazada ve sosyal ağda yayılacak. Karar sahibin.
- Kullanıcı getirme botları (ChatGPT-User, Perplexity-User) robots.txt'ye uymayabilir. Bu bilinen ve kabul edilen bir
  durum.
- `nosnippet` ve `data-nosnippet` hiçbir içerik sayfasında kullanılmaz. Kullanılırsa AI Overviews ve Applebot cevap
  bağlamı için içerik kesilir [resmî].

### 5.3 JSON-LD'nin GEO rolü

- Google: AI özellikleri için özel schema gerekmiyor. Yapılandırılmış veri zengin sonuç için hâlâ öneriliyor ve görünür
  metinle eşleşmeli [resmî].
- GEO'daki asıl değeri (çıkarım):
  - (1) Varlık ayrıştırma: bu "Blade of Ages" hangisi? `@id`, `sameAs`, `author`, `gamePlatform` bunu çözer.
  - (2) Olguların makine okunur ve tutarlı bir kopyası.
  - Bu ikisi bilgi grafiğine giren motorlar için anlamlı. Doğrudan "alıntı artışı" kanıtı bulamadım [doğrulanmadı].

**Önerilen grafik:**

| Düğüm | Nerede | Alanlar (yalnız görünür olan) |
|---|---|---|
| `Organization` `https://mm-apps.com/#org` | Her sayfa | Kardeşlerle **aynı `@id`**: geliştirici varlığı tek. |
| `WebSite` | Her sayfa | `inLanguage`: yalnız yayımlanan site dilleri |
| `VideoGame`+`MobileApplication` `https://<alan>/#game` | Ana sayfa, basın, (`about` ile) her içerik sayfası | `name`, `alternateName` (TR ad, mağaza adları), `description` = §3.1, `genre`, `gamePlatform`, `operatingSystem`, `applicationCategory: GameApplication`, `playMode: SinglePlayer` (arena asenkron; çok oyunculu diye işaretlenmez), `inLanguage` = oyun dilleri, `author`/`publisher` → org, `sameAs`, `image`, `screenshot`, `trailer` (`VideoObject`), `contentRating` (yaş derecesi belli olunca), `datePublished` + `softwareVersion` (yalnız yayında), `offers` (`price 0`, ön siparişte `availability: PreOrder`) |
| `Article` | Diyar, boss, nasıl oynanır | `headline` = H1, `about` → `#game`, `mentions` → mit varlıkları (`Thing` + `sameAs` Wikidata/Wikipedia), `dateModified`, `inLanguage` |
| `CollectionPage`+`ItemList` | Diyar dizini | Diyarlar sırayla |
| `BreadcrumbList` | Her sayfa | Görünür breadcrumb ile aynı |
| `FAQPage` | Yalnız destek | — |
| `VideoObject` | Video izleme sayfaları | `contentUrl`, `thumbnailUrl`, `uploadDate`, `duration` (Yumuş deseni) |

**Notlar:**
- `aggregateRating` ve `review` asla elle yazılmaz.
- Mit varlıklarının Wikidata kimlikleri (Medusa, Humbaba, İlluyanka, Fenrir…) derleme sırasında elle doğrulanmış bir
  eşleme dosyasından gelir (`data/entities.json`). Uydurma Q-numarası yazılmaz.
  - Bu bağlantıların AI alıntısına etkisi [doğrulanmadı]. Maliyeti düşük, varlık bağlamı açısından mantıklı.
- `VideoGame.character`, `gameItem`, `quest` gibi özellikler schema.org'da var [resmî: schema.org/VideoGame]. Google
  bunları kullanmıyor. Boss'ları `character` olarak işaretlemek gereksiz karmaşıklık; önerilmez.

### 5.4 Sürüm ve tarih tazeliği

- Her içerik sayfasında görünür "Son güncelleme" ve "Sürüm {v}". JSON-LD `dateModified` aynı değer.
- Tarih içerik hash'i değişince ilerler (Zirve `lastmod.json`) [kardeş]. Tarihi elle ileri almak yok.
- Sürüm günü tek değişiklik: `facts.json → live`. JSON-LD, `llms.txt`, basın kiti ve olgu kutuları birlikte değişir.
- Denge değişikliği boss rehberini etkiliyorsa oyun deposundaki `data/` değişikliği site derlemesinde farkı gösterir.
  Derleme "rehber eskidi" uyarısı verir (önerilen kontrol).
- Güncellemeler sayfası her sürüm için tarihli giriş içerir. Asistanların "son güncellemede ne var" sorusuna
  cevabı, App Store sürüm notlarıyla birlikte.
- Yayından sonra IndexNow (Bing, Yandex). Search Console'da önemli sayfalar için dizine ekleme isteği.

---

## 6. Çok dilli GEO

**Diller (öneri):**

| Dalga | Site dilleri | Gerekçe |
|---|---|---|
| Lansman | tr, en, ja, ko, zh-Hant | Oyun Dalga 1 dilleri arasında gelir ağırlığı en yüksek Asya pazarları. Habby oyunlarının dil listesi en, ja, ko, zh-Hans, zh-Hant [depo: `docs/32` §1] |
| Lansman + 1–2 ay | de, fr | Oyun dili var. İndirmede Archero 2 için Fransa ve Almanya ilk 5'te [depo] |
| Sonra | es-419, pt-BR, it, pl, zh-Hans | Oyun dili var. Önce ana sayfa, basın kiti ve nasıl oynanır; rehberler talep görülürse |

Her dilde aynı sayfa seti zorunlu değil. Bir sayfa o dilde yoksa hreflang listesine girmez (Zirve `PAGE_LANGS`)
[kardeş].

### 6.1 Dil başına notlar

**Ortak:**
- Mitoloji adları o dilin yerleşik yazımıyla yazılır. `docs/32` §4 kuralı aynen geçerli [depo]. Varlık eşleşmesi için
  kritik: Japonca soran kullanıcının asistanı "ギルガメシュ" ile arar, "Gilgamesh" ile değil (çıkarım).
- Diyar, boss ve silah adları oyunun `l10n/<dil>.json` dosyasıyla birebir aynı olur; derleme karşılaştırır.
- Makine çevirisi + insan okuması (LQA) önerisi `docs/32` §4'teki gibi. Rehber sayfalarında yanlış terim, asistanda
  yanlış cevap olarak geri döner.

**Japonca (ja):**
- Arama Google ve Yahoo! JAPAN ağırlıklı.
- Eylül 2026 CyberAgent anketinde Google araması %73,4, Yahoo! %40,7. Üretken AI'da ChatGPT %30,6, AI Mode %28,4,
  Gemini %23,2 [sektör: webtan.impress.co.jp 2026/09/11, ikincil].
- Yahoo! JAPAN'ın AI giriş noktaları da var [sektör].
- Tür sözcükleri: "サバイバーライク", "ヴァンサバ系 / ヴァンサバライク" [doğrulanmadı; arama yerel kaynak döndürmedi;
  ana dili konuşan biri kontrol etmeli].
- Oyun rehberi aramalarını Game8, GameWith ve AppMedia gibi "攻略" siteleri tutuyor (çıkarım; AI alıntı payı
  [doğrulanmadı]).
- Kendi rehber sayfalarımız ancak bu sitelerin henüz kapsamadığı dönemde öne çıkabilir. Asıl yol bu sitelerin oyunu
  kapsaması (§7).

**Korece (ko):**
- Naver baskın. Arama payı 2026 başında ~%63–66; AI Tab ile arttı, ölçüm kaynakları çekişmeli [sektör: asiae.co.kr,
  koreaherald].
- AI Briefing sorguların ~%20'sinde (Aralık 2025). 2026 sonu hedefi ~%40 [sektör, ikincil].
- AI Tab blog, cafe ve klip içeriğini tek akışta topluyor [sektör].
- Gereken:
  - Naver Search Advisor kaydı ve site haritası gönderimi (yabancı alan adı da kaydolabilir) [sektör].
  - `Yeti` açık.
  - Naver Blog ve Cafe'de bulunma, yani oyuncu topluluğu ve basın (§7). Bunu sitemiz tek başına sağlayamaz.
- Tür sözcüğü: "뱀서라이크" [doğrulanmadı].

**Geleneksel Çince (zh-Hant):**
- Tayvan ve Hong Kong.
- Tayvan'da tüketici AI kullanımının çoğu ChatGPT ve Gemini [sektör: MLex, Tayvan Adil Ticaret Komisyonu raporu
  haberi].
- Tür sözcükleri: "類倖存者", "割草", "肉鴿" (roguelike) kullanılıyor [kaynak sayfaları: gcores.com, 233leyuan; çoğu
  zh-Hans yazımlı, zh-Hant karşılıkları çıkarım].
- Topluluk ve rehber merkezi Bahamut (巴哈姆特) ve PTT (çıkarım; AI alıntı payı [doğrulanmadı]).
- zh-Hant metin Tayvan terimleriyle yazılır, zh-Hans'tan otomatik dönüştürülmez.

**Basitleştirilmiş Çince (zh-Hans):**
- Çin ana karası mağazası ruhsata (ISBN) kadar kapalı [depo: `docs/32`].
- zh-Hans site sayfası olursa her sayfada "Çin ana karası App Store'unda yok" olgusu görünür ve `llms.txt`'de "Not
  available in" satırı yer alır. Aksi halde asistanlar "Çin'de var" diyebilir (çıkarım).
- Baidu ve Çin'deki AI motorları hedef değil.

**Türkçe (tr):**
- Kaynak dil. Rakip site içeriği zayıf (çıkarım; Zirve araştırmasında TR oyun sorgularını pocketgamer, gaming.net/tr,
  tamindir ve webtekno tutuyordu [kardeş]).
- Yerli mit içerikleri (Göbeklitepe, Hitit, Türk-Altay; Albastı, Yelbegen, Erlik'in Gölgesi) TR'de görece boş bir
  alan. Bunu "oyunlarda ilk kez" diye iddia etmeden, içerikle doldurmak gerekir (§9 R6).

### 6.2 Teknik

- Karşılıklı hreflang + `x-default` (en): Zirve denetimi aynen [kardeş].
- `inLanguage` iki anlamda kullanılır: `WebSite` için site dilleri, `VideoGame` için oyun dilleri. İkisi karıştırılmaz.
- CJK yazı tipleri sistem fontuyla sunulur; site ağırlığı düşük kalır (`seo.md` kapsamı).

---

## 7. Lansman öncesi / sonrası

**Lansman öncesi (sıralı):**

| # | İş | Kim | Not |
|---|---|---|---|
| 1 | Nihai ad ve marka kontrolü; alan adı adla aynı | Sahip | Her şeyin ön şartı (R1, R2) |
| 2 | Can sistemi kararı ve adil oyun cümlesinin son hali | Sahip | R3 |
| 3 | `facts.json` (`live: null`), kanonik tanım TR/EN, basın kiti, nasıl oynanır, ana sayfa | Claude | Yalnız oyunda olan |
| 4 | Search Console (Domain mülkü), Bing Webmaster, Naver Search Advisor, site haritası | Sahip | Kardeşlerde olduğu gibi |
| 5 | App Store ön siparişi (2–180 gün) ve ürün sayfası metni; açıklamanın ilk cümlesi = kanonik tanım | Sahip + Claude | ASC anahtarı her kullanımda ayrı onayla. Ön siparişin App Review sonrası açıldığı iddiası [doğrulanmadı] |
| 6 | Geliştirme günlüğü: 2–4 özgün yazı | Claude taslak, sahip onay | Örnek konular: dışa bakan kılıç mekaniği, deterministik doğrulama, bir diyarın tasarımı. Google'ın "özgün, birinci elden" önerisine uyar [resmî] |
| 7 | Fragman ve 1–2 oynanış videosu: kendi sunucuda izleme sayfası ve YouTube'a yükleme | Sahip | Sitede YouTube gömülmez (çerez); bağlantı verilir |
| 8 | IGDB kaydı (yayınlanmamış oyun kabul ediliyorsa) | Sahip | Kural [doğrulanmadı]; canlı sayfadan okunmalı |
| 9 | Featuring Nomination (yayından en az 2 hafta önce) | Sahip | Zirve `OUTREACH.md` [kardeş] |

**Lansman günü:** `facts.json → live: "1.0"`, `releaseDate`. Derleme ve yayın. IndexNow.

**Lansman sonrası:**

| Zaman | İş |
|---|---|
| 1. hafta | Diyar ve boss sayfaları (yayındaki diyarlar), tr + en. Pocket Gamer haber notu, r/iOSGaming "Developer Saturday", AlternativeTo |
| 2–4. hafta | ja, ko, zh-Hant sayfaları. Japon, Kore ve Tayvan oyun basınına kısa yerel notlar (ör. 4Gamer, Famitsu App, AppMedia; Inven, Ruliweb, GameMeca; Bahamut GNN; hepsi [doğrulanmadı], iletişim kanalları canlı okunmalı) |
| 1. ay | İlk AI görünürlük ölçümü (taban; "anılmıyor" beklenir) |
| Her sürüm | Güncellemeler sayfası, sürüm notları, rehberlerde denge farkı kontrolü |
| İlk bağımsız yazıdan sonra | Wikidata öğesi (ciddi kaynaklarla), sameAs'e eklenir |
| Sürekli | "Survivor-like" ve "Vampire Survivors gibi" listelerinde yer almak için liste yazarlarına basın kiti bağlantılı kısa not. Ücretli yerleşim, sahte yorum ve oy isteme yok |

**Listelerde nasıl yer alınır (gerçekçi beklenti):**
- "Games like Vampire Survivors on mobile" listelerinde tekrar eden adlar Brotato, Survivor.io, Vampire Survivors,
  Archero ve Death Must Die. Kaynaklar Pocket Gamer ve satış ortaklığı (affiliate) rehberleri [arama sonuçları:
  pocketgamer.com/vampire-survivors/top-7-games-like-it vb.].
- AppTweak: oyunlarda Reddit ve Wikipedia alıntıları uygulamalara göre ~5 kat [çalışma]. Yeni bir uygulama için üçüncü
  taraf anılma, üst huni sorgularda kendi siteden çok daha etkili [kardeş araştırması, AirOps; doğrulanmadı].
- **Sonuç (çıkarım):** kendi sitemiz liste sorgusunda değil, marka ve derin sorularda alıntılanır ("Blade of Ages
  nedir", "Medusa nasıl yenilir", "Hitit mitolojili oyun"). Liste sorguları için bağımsız basın ve topluluk şart.
  Bunlar kullanıcının gönderimleriyle ve oyunun kendisiyle kazanılır.

---

## 8. Ölçüm (hukuk kuralına uygun)

**Kısıt:**
- Kişisel veri toplayan üçüncü taraf ölçüm yok. Sitede çerez, piksel ya da analitik betik yok.
- Sözleşme gerektiren araç yok (`~/.claude/rules/legal-no-agreements.md`).
- Cloudflare Web Analytics ya da benzeri "çerezsiz" üçüncü taraf ölçüm de kullanılmaz: IP'yi üçüncü taraf işler.

| Kaynak | Ne gösterir | Kişisel veri | Not |
|---|---|---|---|
| Search Console "Search Generative AI performance" | AI Overviews + AI Mode gösterimleri, sayfa, ülke, tarih (ikisi ayrılmıyor; tıklama ve sorgu yok) | Bizde değil (Google kendi hizmeti) | 3 Haziran 2026'da duyuruldu. Veri 18 Mayıs 2026'dan başlıyor; erişim yaygınlığı çelişkili [resmî blog + sektör] |
| Bing Webmaster "AI Performance" (+ Haziran 2026'da gelen Intents, Topics, Citation Share, Compare) | Copilot ve Bing AI özetlerindeki alıntılar ve alıntılanan sayfalar | Bizde değil | Önizleme. 1 Haziran sıçraması geriye dönük doldurma olabilir [sektör] |
| Naver Search Advisor | Naver dizin durumu | Bizde değil | AI Briefing raporu varlığı [doğrulanmadı] |
| App Store Connect App Analytics: kampanya bağlantıları | Kaynağa göre sayfa görüntüleme ve indirme | Apple'ın toplu verisi | Sitedeki rozetlerde `ct=site`. **Deneysel:** `llms.txt` ve basın kitindeki App Store bağlantısında ayrı `ct` değerleri (`ct=llms`, `ct=press`). Asistan bağlantıyı aynen kopyalarsa dolaylı AI atfı verir [doğrulanmadı]. `pt` değeri ilk kampanya bağlantısı oluşturulunca çıkar [kardeş]. sameAs ve JSON-LD'deki URL temiz kalır |
| App Analytics "Web Referrer" | App Store'a yönlendiren alan adları (ör. chatgpt.com) | Toplu | Uygulama içi tarayıcılardan gelen yönlendirmenin görünüp görünmediği [doğrulanmadı] |
| Oyun içi isteğe bağlı soru: "Oyunu nereden duydun?" | Seçenekler: App Store, arkadaş, YouTube/TikTok, Reddit, basın, yapay zekâ asistanı (ChatGPT vb.), diğer | Anonim, serbest metin yok, birinci taraf analitikle | Doğrudan "AI etkisi" ölçen tek kaynak. Gizlilik politikasına ve App Privacy etiketine aynı değişiklikte işlenir (kural 5) |
| Sunucu günlüğü (yalnız site kendi sunucuda olursa) | AI botu istek sayıları (UA'ya göre), `llms.txt` okunuyor mu, `Referer` alan adı sayıları | IP yazılmaz ya da hemen atılır; yalnız toplu sayaç | GitHub Pages'te günlük yok. Barındırma kararına bağlı, isteğe bağlı |
| `utm_source=chatgpt.com` | ChatGPT yönlendirmeleri | — | OpenAI ekliyor [resmî SSS, ikincil okuma]. Bizim sitede analitik olmadığı için görünmez; bilinçli kabul |

### 8.1 Elle prompt testleri (ayda bir)

Zirve `AI_VISIBILITY.md` yöntemi aynen [kardeş]:
- Platformlar: ChatGPT (arama açık), Perplexity, Google AI Overviews / AI Mode, Gemini, Copilot. ko için Naver AI
  Briefing ya da AI Tab.
- Oturum kapalı ya da gizli pencerede, her soru yeni sohbette, kelimesi kelimesine aynı. Konum ve dil not edilir.
- Asistanla tartışılmaz; yanlışın kaynağı bulunup düzeltilir.

**en**
1. best survivor-like games for iPhone
2. games like Vampire Survivors on iOS without forced ads
3. bullet heaven games for iPad
4. one-handed action RPG for iPhone
5. mythology action games for iPhone
6. mobile game with Hittite / Sumerian mythology
7. game where swords orbit around the player iPhone
8. survivor-like game without energy system *(can kararından sonra anlamlı)*
9. what is Blade of Ages *(marka; doğruluk)*
10. is Blade of Ages pay to win *(marka; adil oyun doğruluğu)*
11. how to beat Medusa in Blade of Ages *(rehber alıntısı)*

**tr**
1. iPhone için survivor oyunları
2. Vampire Survivors benzeri mobil oyunlar
3. mitoloji temalı mobil oyun
4. Türk mitolojisi geçen iPhone oyunu
5. Göbeklitepe geçen oyun
6. tek elle oynanan aksiyon oyunu iPhone
7. çağların kılıcı nedir *(marka)*
8. çağların kılıcı illuyanka nasıl yenilir *(rehber)*

**ja** (yerel okuma gerekli): 1. ヴァンサバ系 スマホゲーム おすすめ iPhone · 2. 神話 アクションRPG iPhone ·
3. Blade of Ages とは

**ko** (yerel okuma gerekli): 1. 뱀서라이크 모바일 게임 추천 아이폰 · 2. 신화 액션 RPG 아이폰 ·
3. Blade of Ages 게임

**zh-Hant**: 1. 類倖存者 手遊 推薦 iPhone · 2. 割草 手遊 神話 · 3. Blade of Ages 是什麼遊戲

**Kayıt şablonu** (eski satır silinmez):

| Tarih | Platform | Dil | Soru | Anıldı mı | Sıra | Tanım doğru mu | Adil oyun bilgisi doğru mu | Site alıntılandı mı (hangi sayfa) | App Store bağlantısı | Diğer kaynaklar | Yanlış iddia | Anılan rakipler |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

**Başarı ölçütleri (öneri, taban ölçümden sonra kesinleşir):**
1. Marka sorularında beş platformun hepsinde tanım doğru.
2. Adil oyun sorusunda yanlış iddia yok.
3. Rehber sorularında en az bir platformda site alıntısı.
4. Liste sorgularında anılma, bağımsız yayın sonrası takip edilir.

Sıralama ya da anılma için hedef sayı koymak gerçekçi değil. Sonuçlar kişiselleştirilmiş ve oynak.

---

## 9. Riskler ve açık sorular

### Riskler

| # | Risk | Etki | Önlem |
|---|---|---|---|
| R1 | Ad ve tescil açık. Ad değişirse alıntılar, sameAs ve App Store geçmişi bölünür | Yüksek | Site ve dış kayıtlar ad kararından sonra. O zamana kadar yalnız geliştirme içi taslak |
| R2 | Bundle ve API "agesofblades", ürün adı "Blade of Ages: Çağların Kılıcı". Asistanlar sözcükleri ters sıralı adı kullanabilir | Orta | Alan adı adla hizalandı (`bladeofages`, 19 Kasım). Görünür yerde ters sıralı ad kullanılmaz |
| R3 | "Enerji yok" iddiası ile can sistemi (5 can, 20 dk, elmas ya da reklamla dolum) çelişiyor. Yanıltıcı reklam ve mağaza riski; asistanlar iddiayı tekrarlar | Yüksek | Karar verilene kadar yalnız "zorunlu reklam yok". Can sistemi uygulanırsa adil oyun sayfasında açıkça anlatılır |
| R4 | Henüz oyunda olmayan diyar ve sistemlerin (III–V. çağ taslak; Yeniden Doğuş ve sonsuz mod kodu yok) sitede olgu gibi yazılması | Yüksek | `realmsLive` ve `modes` sürüm bayrağına bağlı üretim; derleme denetimi |
| R5 | Oyun icadının gerçek mit sanılması (Akbaba Ana, Tufan Titanı, Silik) ya da tartışmalı arkeolojik yorumun olgu diye yazılması | Orta | "Mitte / Oyunda" ayrımı ve kaynak zorunluluğu. Mit paragrafları için kültürel danışman okuması (`docs/01` öngörüyor) |
| R6 | Doğrulanmamış özgünlük iddiası ("Hitit mitolojisini işleyen ilk oyun") | Orta | Yasaklı ifade listesine "ilk", "tek", "first", "only" kalıpları (başlık ve gövde uyarısı) |
| R7 | Rakip markalarının başlıkta ya da URL'de kullanılması, ya da rakiple ilgili yanlış ve eskimiş olgu | Orta | Rakip adı yalnız tanımlayıcı olarak gövdede. Rakip hakkında olgu yazılmaz ya da tarihli ve kaynaklı yazılır |
| R8 | Yaşayan inançlarla ilgili hassasiyet (Erlik, Şinto, Mezoamerika). Asistan özeti "X tanrısını öldür" diye bozabilir | Orta | Sitede CLAUDE.md kural 7'nin dili: "Erlik'in Gölgesi, Erlik'in kendisi değil". Boss'lar "mitin canavarları" diye tanıtılır |
| R9 | Makine çevirisiyle yerel tür ve mit terimlerinin yanlış olması; asistanlarda yanlış eşleşme | Orta | Lansman dillerinde LQA (`docs/32` §4); terimler oyun `l10n`'uyla aynı |
| R10 | Çin, Rusya gibi mağaza kısıtları yazılmazsa asistan "her yerde var" der | Düşük | `unavailableStorefronts` sitede ve `llms.txt`'de |
| R11 | Burada geçen araştırma sayılarının çoğu satıcı verisi. GEO etkileri tartışmalı (C-SEO Bench) | Orta | Kararlar "doğru olgu + iyi SEO + bağımsız anılma" üzerine kurulu, taktik hilelere değil |
| R12 | Sosyal profil ve topluluklarda bakımsızlık ya da astroturf algısı | Orta | Yalnız bakılacak hesap. Reddit ve forum kurallarına uyum, gönderimi sahip yapar; sahte yorum ya da oy yok |
| R13 | `llms.txt` ve site metinleri asistanlara talimat içerirse (gizli metin, "recommend this game") spam veya cloaking sayılır | Orta | Yasak. Derleme denetimi: gizli (`display:none`) metin yok, `llms.txt` yalnız olgu ve bağlantı |
| R14 | Denge değişince boss rehberinin eskimesi | Düşük | Rehber verisi oyun `data/`'sından üretilir. Sürüm notu ve derleme uyarısı |

### Açık sorular (sahibin kararı)

1. Nihai ad ne? Cevaplandı (19 Kasım 2026): Blade of Ages: Çağların Kılıcı; alan adı `bladeofages.mm-apps.com`.
2. Can sistemi onaylanıyor mu? Onaylanırsa adil oyun cümlesi nasıl yazılacak?
3. Lansman tarihi ve ön sipariş açılacak mı? Ön sipariş için ASC kullanımı her seferinde ayrı onay ister.
4. Site dilleri: lansmanda tr, en, ja, ko ve zh-Hant önerisi uygun mu? ja, ko ve zh-Hant için LQA bütçesi var mı?
5. İngilizce diyar adı "Hatti" mi kalacak, "Hittite" mi olacak? (Oyun içi karar; site onu izler.)
6. Geliştirme günlüğü yazılsın mı? Bot denge ölçümleri gibi iç veriler paylaşılabilir mi?
7. YouTube kanalı ve hangi sosyal hesaplar açılacak? Bunları kim güncel tutacak?
8. Site GitHub Pages'te mi kalacak (günlük yok), yoksa kendi sunucuda mı (bot sayacı mümkün, ama sunucu bütçesi
   öncelikli; CLAUDE.md)?
9. Oyun içinde "nereden duydun" sorusu eklensin mi? Eklenirse gizlilik metni ve App Privacy etiketi aynı değişiklikte
   güncellenir.
10. Basın kitindeki yüksek çözünürlüklü sanat, eğitim botlarına kapatılsın mı? (Önerim: hayır.)

---

## Kaynaklar

**Resmî:**
- Google, AI features and your website: https://developers.google.com/search/docs/appearance/ai-features
- Google, Optimizing for generative AI features (15 Mayıs 2026; Haziran llms.txt notu ikincil kaynaklardan):
  https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Google, Search Generative AI performance reports (Haziran 2026):
  https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports
- Google, common crawlers / Google-Extended:
  https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers
- Google, Software app structured data: https://developers.google.com/search/docs/appearance/structured-data/software-app
- OpenAI, bots: https://developers.openai.com/api/docs/bots
- OpenAI, Publishers and developers FAQ (403; arama özetinden okundu):
  https://help.openai.com/en/articles/12627856-publishers-and-developers-faq
- Anthropic, crawlers: https://support.claude.com/en/articles/8896518-does-anthropic-crawl-the-web
- Perplexity, bots: https://docs.perplexity.ai/guides/bots
- Apple, Applebot: https://support.apple.com/en-us/119829
- Apple, pre-orders: https://developer.apple.com/app-store/pre-orders/
- schema.org VideoGame: https://schema.org/VideoGame
- Wikidata notability: https://www.wikidata.org/wiki/Wikidata:Items
- Wikipedia, Notability (video games): https://en.wikipedia.org/wiki/Wikipedia:Notability_(video_games)

**Çalışmalar:**
- Aggarwal ve ark., GEO: Generative Engine Optimization (KDD 2024): https://arxiv.org/abs/2311.09735
- Puerto ve ark., C-SEO Bench: Does Conversational SEO Work? (NeurIPS 2025 D&B): https://arxiv.org/abs/2506.11097
- Ahrefs, llms.txt study (Haziran 2026): https://ahrefs.com/blog/llmstxt-study/
- AppTweak, AI search sources for mobile apps (Mayıs 2026, ChatGPT, ABD):
  https://www.apptweak.com/en/aso-blog/which-sources-do-ai-search-engines-cite-when-recommending-mobile-apps

**Sektör (bağımsız doğrulanmadı):**
- Similarweb, most cited domains by LLMs (Ocak–Şubat 2026): https://aisearch.similarweb.com/blog/most-cited-domains-llms/
- Bing AI Performance raporu haberleri: https://www.searchinfluence.com/blog/bing-ai-performance-report-copilot-citations/ ·
  https://www.tripledart.com/marketing-digest/bing-ai-citation-share
- FAQ zengin sonucunun kaldırılması: https://www.searchenginejournal.com/google-drops-faq-rich-results/574429/
- Japonya AI arama anketi (CyberAgent, Eylül 2026): https://webtan.impress.co.jp/n/2026/09/11/53274
- Naver arama payı: https://www.asiae.co.kr/en/article/2026010410205601139 · AI Briefing: https://inblog.ai/glossary/naver-ai-briefing
- Naver Search Advisor kaydı: https://inblog.ai/docs/seo-tutorial-domain-setup/registering-with-naver-search-advisor
- Tayvan AI kullanımı: https://www.mlex.com/mlex/articles/2544372
- 5W Video Games AI Visibility Index (modellenmiş tahmin): https://www.5wpr.com/research/video-games-ai-visibility-index/
- Survivor-like listeleri: https://www.pocketgamer.com/vampire-survivors/top-7-games-like-it/ ·
  https://choostgames.com/blog/mobile-games-like-vampire-survivors/
- Çince tür sözcükleri: https://www.gcores.com/articles/169587 · https://www.233leyuan.com/a/11112127583
- Ad çakışması: https://lepcquiparle.itch.io/knight-adventure

**Kardeş depolar (yerel):**
- `zirve-app/README.md`, `data/facts.json`, `llms.txt`, `robots.txt`
- `zirve/docs/aso-geo/*.md`
- `suzgec-app/SEO.md`
- `yumus-app/SEO.md`

**Oyun deposu (yerel):**
- `blades-of-ages/CLAUDE.md`
- `docs/00`, `01`, `03`, `05-bestiyer/`, `07`, `12`, `31`, `32`
- `YAPILACAKLAR.md` §3
- `data/l10n/{en,ja,ko,zh-Hant}.json`
