# Tasarım adayları: tanıtım sitesi (17 Kasım 2026)

Kaynak: Dribbble araması ("game landing page", "mobile game landing page", "fantasy game website", "mythology
website", "game website illustration", "cozy game website", "rpg game landing", "3d clay website", "toy website",
"parallax illustration website"). Yaklaşık 200 çalışma tarandı, 30'u yakından incelendi. Sonuçların çoğu koyu, neon ve
kripto temalıydı; bunlar oyunun **Gün Kili** diline (gökten naneye geçiş, beyaz kil kartlar, dudaklı düğmeler, kil
figürler) uymadığı için elendi.

Referanslar yalnız **yön** içindir. Hiçbir görsel, düzen ya da metin kopyalanmaz. Bütün çizimler oyunun kendi
varlıklarından (kil figürler, diyar zeminleri, yapılar, ikon) üretilir.

Ortak sabitler (hangi yön seçilirse seçilsin):
- **Marka işareti:** uygulama ikonundaki dönen kılıç halkası. Kılıçların ucu her zaman dışa bakar; halka çizgisi yok.
- **Renk kodları oyundaki gibi:** kılıç beyaz-mavi, ganimet altını `#F5C451` yalnız altın için, mor mermi, kırmızı
  uyarı, turkuaz elit.
- **Tek parmak:** sitede de birincil etkileşim tek dokunuş ya da kaydırma; mobil önce.
- **Performans:** LCP öğesi statik görsel; animasyon ve etkileşim ilk boyamadan sonra yüklenir.
  `prefers-reduced-motion` desteklenir.
- **Dil:** 7 lansman dili (tr, en, ja, ko, zh-Hant, de, fr); Latin dışı yazılar için yazı tipi alt kümeleri.

---

## A · Çağlar Yolculuğu (kaydırmalı katmanlı diorama)

**Referanslar:**
- [Chumbi Valley · Crypto Game Landing Page](https://dribbble.com/shots/22865510) (Zajno)
- [Osnaria Game Web Landing Page With Illustrations](https://dribbble.com/shots/18008814) (Karakaya)

**Ne alıyoruz:** aydınlık, katmanlı bir manzara hero'su (ön plan, orta plan, gök) ve logo merkezde. Kaydırdıkça
kamera ilerler.

**Bize uyarlanışı:**
- Sayfa aşağı indikçe beş çağdan geçer: Göbeklitepe'nin bozkırı → Mısır'ın kumu → Yunan mermeri → Kuzey'in karı →
  Silik'in mor boşluğu.
- Gök rengi çağa göre değişir. Her çağda o diyarın kil figürleri ve yapıları ön planda belirir.
- Kahramanın dönen kılıçları sabit bir "rehber" olarak ekranın ortasında kalır.

**Artısı:** dünya yapısını (5 çağ × 12 diyar) tek bakışta anlatır. Her durak, diyar sayfasına iç bağlantı olur
(SEO/GEO).
**Riski:** en çok sanat isteyen yön. Diyar başına katmanlı sahne gerekir; mobilde parallax dikkatli bütçelenmeli.

## B · Kil Oyuncak Vitrini (3D/kil koleksiyon)

**Referanslar:**
- [Creating a 3D Toy Website](https://dribbble.com/shots/26373563) ve
  [A 3D Toy Website on Scroll](https://dribbble.com/shots/26428847) (tubik)
- [Monta: Playful Handmade Monster Toys Website](https://dribbble.com/shots/25950603) (Ihdizein)
- [Gemoycorn · Game Website Design](https://dribbble.com/shots/26142803) (Emura)

**Ne alıyoruz:** cesur, düz renk blokları; iri, tok tipografi; karakterleri koleksiyon oyuncağı gibi kartlarda sergileme.

**Bize uyarlanışı:**
- Gün Kili kartları ve dudaklı düğmeler doğrudan siteye taşınır; site oyunun menüsünün devamı gibi görünür.
- Bestiyer bir "koleksiyon rafı": her düşman ve boss kendi renk bloğunda döner. Kart çevrilince arkasında mit notu ve
  karşı hamle yazar.

**Artısı:** oyunla bire bir aynı dil; mevcut kil varlıklarıyla en ucuz üretilen yön; çok hızlı yüklenir.
**Riski:** "oyuncak" algısı aksiyon ve mitoloji derinliğini zayıflatabilir; hero'da güçlü bir aksiyon anı gerekir.

## C · Gün Işığında Mit Müzesi (editoryal ansiklopedi)

**Referanslar:**
- [Mytholog · Storytelling Landing page](https://dribbble.com/shots/27047113) (Emura)
- [Greek Mythology Explorer](https://dribbble.com/shots/15376193) (Elliott Wilkie)
- [Echoes of Atlantis · Relic Auction Website](https://dribbble.com/shots/26454641) (Arian Atmar)

**Ne alıyoruz:** müze sergisi düzeni: büyük serif başlıklar, "eser" etiketleri (köken, dönem, kaynak), tek nesneye
odaklanan sahne.

**Bize uyarlanışı:**
- Referansların karanlık havası yerine gün ışığında bir müze.
- Her boss bir sergi parçası: Akbaba Ana taşı, Humbaba, Apep, Medusa, İlluyanka. Etiket kartında mitin kaynağı, oyundaki
  üç faz ve karşı hamle yer alır.

**Artısı:** GEO için en güçlü yön. Ansiklopedik, kaynak gösteren, alıntılanabilir içerik; "Göbeklitepe akbaba
kabartması", "Humbaba kimdir" gibi aramalara sayfa olur.
**Riski:** tek başına fazla "okul" gibi durabilir. Oyunun hızını ve eğlencesini göstermek için A, B ya da D ile
birlikte kullanılmalı.

## D · Oynanabilir Giriş (sitenin kendisi oyun)

**Referans:** [Pixel Picnic · Playable Arcade Game Website](https://dribbble.com/shots/27828373) (designsucks)

**Ne alıyoruz:** hero bir mini oyun. Ziyaretçi sayfayı okumadan oynuyor; dev logo harfleri oyunun malzemesi.

**Bize uyarlanışı:**
- Hero'da parmak ya da imleç kahramanı yürütür ve dönen kılıçlar çevresindekini keser. Duruşta kılıçlar daralır ve
  hızlanır; oyunun tek mekaniği 5 saniyede öğrenilir.
- Akan düşmanlar kesilince altına dönüşür, altın sayacı "İndir" düğmesine akar.
- Simülasyon, tasarım tuvalindeki `HUD.dc.html` hissiyle aynı.

**Artısı:** en sıradışı ve paylaşılabilir yön; reklam kreatifleriyle (CPI) aynı "kılıç keyfi" mesajı; ziyaretçi oyunun
hissini doğrudan yaşar.
**Riski:** en çok mühendislik isteyen yön (canvas, 60 fps, dokunma). LCP/INP bütçesi için oyun ilk boyamadan sonra
yüklenmeli; içerik metni oyundan bağımsız, taranabilir HTML kalmalı.

## E · Sefer Yolu (sayfa bir harita rotası)

**Referanslar:**
- [Sunly Map Selection Illustration](https://dribbble.com/shots/26293312) (Hellsjells)
- [Guide travel website](https://dribbble.com/shots/16317924) (Layo)

**Ne alıyoruz:** sayfayı yukarıdan bakılan resimli bir harita gibi kurmak; bölümler haritadaki duraklar.

**Bize uyarlanışı:** sayfa, oyunun sefer haritası gibi duvarlı, kıvrılan bir yol. Kaydırdıkça kahraman yolda ilerler
ve duraklara gelir:
- Kamp 1 · Nasıl oynanır
- Kamp 2 · Diyarlar
- Kamp 3 · Kahramanlar
- Kamp 4 · Adil oyun sözü
- Bekçi · SSS ve İndir

Durak düğümleri oyundaki harita düğümleriyle aynı: kazanılmış yeşil, açık beyaz, kilitli gri.

**Artısı:** oyunun kendi ilerleme metaforu; bölümler doğal olarak sırayla okunur; mobilde dikey yol rahat.
**Riski:** yol çizimi her ekran boyutunda ayrı ayarlanmalı; içerik çok uzarsa yol monotonlaşır.

## F · Gece Sineması (koyu, altın, video hero)

**Referanslar:**
- [Anubis Landing Page · Cinematic Web Design](https://dribbble.com/shots/26099031) (Ahmed Massoud)
- [Ukrainian Mermaids · Website & Illustration](https://dribbble.com/shots/19840208) (BL/S®)
- [Crown Beast Slayer · Promotion Game Landing Page](https://dribbble.com/shots/25478271) (Rafif Fauzi)

**Ne alıyoruz:** sinematik açılış: koyu zemin, ışıklı başlık, ortada oynatılan fragman, altında özellik kartları.

**Bize uyarlanışı:**
- Oyunun "Gece" teması (alacakaranlık `#2C4C63 → #355F58`) zemin olur.
- Boss'ların karşılaşma anları kısa döngü videolar olarak oynar.
- Altın yalnız ganimet ve CTA vurgusunda kullanılır.

**Artısı:** türün alışık olduğu "AAA fragman" havası; App Store önizleme videolarıyla ortak üretim.
**Riski:** Gün Kili ile çelişir; sektördeki yüzlerce koyu oyun sitesine benzer, en az ayırt edici yön. Video LCP'yi
zorlar.

## G · Masal Defteri (yırtık kâğıt, eskiz ve boya)

**Referanslar:**
- [Eddy · Words to be · Landing page for mobile games](https://dribbble.com/shots/27371661) (Dario Esposito)
- [The Wake · Online Game Website](https://dribbble.com/shots/24661820) (Piplz Studio) — mobil düzen için

**Ne alıyoruz:** eskiz ve boyalı sahnelerin yırtık kâğıt kenarlarıyla bölündüğü bir hikâye defteri; el yazısı notlar.

**Bize uyarlanışı:**
- Bestiyer çizimleri (tasarım tuvalindeki eskizler) kalemle çizilmiş defter sayfaları gibi durur.
- Kaydırınca eskiz renklenir ve kil figüre dönüşür. Bu dönüşüm "Hafıza Kılıcı / Silik" hikâyesine bağlanır: unutulan
  mitler yeniden hatırlanıyor.

**Artısı:** hikâye ile görsel geçiş arasında güçlü bir bağ; sıcak ve özgün.
**Riski:** eskiz-boya geçişi için her figürün iki sürümü gerekir; "çocuk kitabı" algısı riski.

---

## Öneri

**Ana yön: D + A.** Hero oynanabilir kılıç halkası (D). Altında Çağlar Yolculuğu (A): her çağ durağı, oyunun kendi kil
figürleri ve zeminleriyle kurulur.

- **Diyar ve boss sayfaları:** C'nin "gün ışığında müze" düzeni. Bu sayfalar SEO ve GEO içeriğinin ana taşıyıcısı.
- **Bileşenler:** düğmeler, kartlar ve çipler doğrudan Gün Kili'den (B).

**Gerekçe:** sıradışılık ve paylaşılabilirlik D'den, dünya ölçeği A'dan, aranabilir ve alıntılanabilir içerik C'den,
oyunla tutarlılık ve düşük üretim maliyeti B'den gelir.
**Trade-off:** D en yüksek mühendislik riskini taşır. Hero'nun statik bir LCP görseli olarak açılıp oyunun sonradan
uyanması şart.

İkinci seçenek (daha az risk): **B + E.** Gün Kili vitrin ve sefer yolu; oynanabilir hero yok, kısa bir döngü video var.
