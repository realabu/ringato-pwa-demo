# 01 – Feltárás és követelmények

**Kötelező tartalomkezelés (2026-10-16):** minden jelenlegi és későbbi PWA-blokk és szerkeszthető szöveg WordPressből, ACF Free mezőkből jön; a közös layoutszövegek és menüikonok is módosíthatók. A blokkok oldalanként csoportosítandók. A React sablon az eredeti megjelenést őrzi. Minden mérföldkő átadási feltétele a WP-szerkesztés build nélküli ellenőrzése. [Részletes szabály és kész-feltételek](12-wordpress-tartalomkezeles.md).

## 1. Bizonyíték és korlát

A felmérés a 2026-10-12-i mentésből visszaállított **helyi WordPressre** vonatkozik. Nem éles audit. Olvasási vizsgálat: aktív/inaktív pluginlista és verziók, tartalomtípus-regisztráció, nyilvános termékek, aggregált adatdarabszámok, téma esemény- és rendeléskezelő kódja, Barion gateway képességdeklaráció. Személyes rendelési adat és integrációs titok nem része e dokumentációnak.

A WordPress- és csomagverziók a helyi rendszer által jelentett értékek, nem frissítési ajánlások. Az éles környezet verzió- és konfigurációeltéréseit stagingindításkor külön ellenőrizni kell. A fizetési, számlázási, e-mail és teljes vásárlási folyamatot most nem futtattuk.

**D12 – projektgazdai pontosítás (2026-10-15; nem a korábbi helyi audit következtetése):** a jelenlegi vásárlók vendégként vásárolnak, fiók létrehozása nélkül; a tárhelyen **tesztdomaines WordPress tesztpéldány** rendelkezésre áll, és a fejlesztő **lokális fejlesztői környezetet** is épített. A tesztpéldány alkalmas a telepítési folyamat próbájának helyszínéül, a tényleges sikeres telepítést még tesztelni kell. A tárhely **PWA-kiszolgálásra alkalmasnak megerősített**, de a párhuzamos audio/video streaming kapacitása **nem mért**. **D10 2026-10-16-án elfogadott eljárás:** előbb tartalom- és forgalombecslés, aztán fokozatos, kontrollált helyi streamterhelési teszt, majd helyi vs külső védett streaming/CDN teljes költség- és alkalmasság-összevetés. **Szolgáltatóválasztás még nincs;** a mérés nem lett elvégezve. Az új fiókhoz kötött funkciók regisztrációs útvonalát ellenőrizni kell; a meglévő vendégvásárlás megőrzendő.

## 2. Ellenőrzött helyi állapot

| Terület | Megfigyelés | Következmény |
|---|---|---|
| WordPress/PHP | WP 7.1.3, PHP 8.3.35 | A fejlesztői kompatibilitási mátrix induló értékei |
| WooCommerce | 11.1.2, aktív; HPOS `yes`; `wp_wc_orders`, `wp_wc_orders_meta` jelen van | Rendeléshez kizárólag WC CRUD, nem `shop_order` post-query |
| Téma | Ringato Viraggal Theme 1.0, könyvtár: `ringatoviraggal` | Nem módosítjuk; saját pluginadapter olvassa a meglévő adatokat |
| Időzóna | `Europe/Budapest` | Üzleti időszámítás budapesti, tárolás UTC |
| Program | `event` CPT, `event_category` taxonómia; nem `show_in_rest` | Saját REST adapter szükséges, nem teljes metaadat-publikálás |
| Programmezők | `_event_date`, `_event_time`, `_event_venue`, `_event_short_desc`, `_thumbnail_id` | Ezekből képződik a PWA program DTO |
| Programdarabszám | 398 összesen: 396 publikált, 2 draft | V1-ben csak publikált és PWA-ban engedélyezett esemény |
| Termékdarabszám | 13 rekord: 6 publish, 7 `importing` | Nem 13 eladható termék; importmaradványt külön meg kell vizsgálni |
| Rendelések | 824 régi `shop_order` rekord; 1154 HPOS placeholder | Nem összeadható ügyfélrendelésszám; HPOS az olvasási forrás |
| Új appmodulok | Nincs Subscriptions, Better Messages, Ringató API névtér vagy Ringató saját tábla | A prototípus funkcióihez hiányzó backendépítés szükséges |
| API | `wp/v2`, `wc/v3`, `wc/store/v1` jelen van | Publikus katalógus elérhető; saját fiókadatokhoz egyedi API |

### Bővítményleltár

| Plugin | Verzió | Helyi állapot | PWA szerep |
|---|---|---|---|
| WooCommerce | 11.1.2 | aktív | Termék, rendelés, pénztár |
| Barion Payment Gateway for WooCommerce | 3.10.2 | inaktív helyileg | Egyszeri fizetés; recurring hiányzik a gateway deklarációból |
| Billingo Official for WooCommerce | 4.3.4 | inaktív helyileg | Meglévő számlázás; renewal-kompatibilitás vizsgálandó |
| GiftRocket – Ultimate Gift Cards for WooCommerce | 1.1.2 | aktív | Egyedi `wxgiftcard` terméktípus; webes konfigurátor szükséges lehet |
| Contact Form 7 | 6.2 | aktív | Eredeti oldalhoz tartozik |
| CookieYes | 3.5.6 | aktív | Eredeti oldali consent nem terjed automatikusan a React appra |
| Loco Translate | 2.8.9 | aktív | Meglévő fordítások |
| All-in-One WP Migration | 7.112 | aktív | Mentés/import; nem appfunkció |
| WP Mail Logging | 1.17.0 | aktív | Üzemeltetés; személyes tartalom megőrzését felülvizsgálni |
| MailerLite WooCommerce integration | 3.1.26 | inaktív helyileg | Marketing, nem push-kampány backend |
| WP Mail SMTP | 4.10.0 | inaktív helyileg | Éles tranzakciós levelek |
| Wordfence | 9.0.2 | inaktív helyileg | Éles WAF/login/API szabályok regressziója |
| WP Super Cache | 3.1.4 | inaktív helyileg | Auth és app bootstrap kizárás |
| Akismet / Hello Dolly / WordPress Importer | 5.7.2 / 1.7.2 / 0.9.6 | inaktív | Nem szükséges PWA-függőség |

A helyi mu-plugin tiltja az e-mail-küldést; WP-Cron letiltott. A Barion/Billingo/SMTP/WAF/cache helyi inaktivitása szándékos környezeti eltérés. Az éles üzemeltetési terv ezért nem építhet arra, hogy a helyi konfiguráció kiadásra kész.

### Meglévő téma üzleti logikája

- `functions.php`: `event` regisztráció, admin metabox, programmezők mentése, kategóriaszín, `?ics_event_id=` alapú naptárexport.
- `page-esemenynaptar.php`, `page-rendezvenyek.php`: programlista/naptár a fenti metaadatokból. Ezek útvonalai és megjelenése megmaradnak.
- `custom_email_by_sku_after_payment()`: `woocommerce_order_status_completed` eseményen SKU-alapú e-mail. `RINGI01`/`RINGI06`: 3 hónapos helyszíni jegy; `RINGI02`/`RINGI03`: első felhasználástól induló papírbérlet; `RINGI04`/`RINGI05`/`RINGI06`: régi online hozzáférés.
- WooCommerce checkout- és e-mailsablon-felülírások léteznek. Nem szabad egy React checkout kedvéért lecserélni őket.
- Nem találtunk a vizsgált kódban teljes digitális jegy/bérlet-beváltási nyilvántartást. E-mailben közölt érvényességi szabály nem szerveroldali jogosultságmotor.

## 3. Termékek és migrációs térkép

| Helyi ID | SKU / típus | Termék | Megfigyelt ár | Tervezett besorolás |
|---|---|---|---|---|
| 4382 | RINGI01 / simple | Családi jegy | 2 990 Ft | `family_ticket`, 1 belépés, fizetéstől 3 hónap |
| 4386 | RINGI02 / simple | Ringató 8 alkalmas bérlet | 19 990 Ft | `pass`, 8 alkalom, első használattól 8 hónap |
| 4385 | RINGI06 / simple | Helyszíni + online Ringató jegy | 4 990 Ft | Régi kombinált; D01 szerint tovább értékesíthető weben és PWA-ban; régi helyszíni/online jogosultság auditálandó |
| 4384 | RINGI05 / simple | Ringató jegy online foglalkozásra | 2 290 Ft | D01 szerint egyelőre megtartható és mindkét csatornán értékesíthető; nem ad automatikusan új PWA-médiatár-hozzáférést |
| 4387 | RINGI04 / simple | Ringató bérlet online, 1 hónap | 8 200 Ft | D01 szerint egyelőre megtartható és mindkét csatornán értékesíthető; nem az új 8 000 Ft/hó app-előfizetés |
| 6448 | nincs SKU / wxgiftcard | Ajándékutalvány | alaptermék ára üres | Megjelenítendő; árkonfiguráció a meglévő webes termékoldalon |

Mind a hat publikált termék helyileg `purchasable=true`, `instock`, `virtual=true`, `visible`. Az árak pillanatfelvétel; a kliens éles árat API-ból kap. Az ID-k kizárólag helyi példák, az éles megfeleltetés adminbeállítás és SKU/termékazonosító audit alapján történik. A témában szereplő `RINGI03` a jelenlegi publikált listában nem szerepel.

**D01 döntés (2026-10-15):** Az egységes WooCommerce-termékkínálat az irányadó: az aktív, publikus, megvásárolható webshoptermékek a PWA-ban is láthatók és megvásárolhatók, ideértve a régi Online Ringató termékeket, valamint az új előfizetés- és eseménytermékeket. Az eredeti F10–F26 ütközés üzletileg feloldva **F10 javára**: a régi Online Ringató értékesítését tiltó F26-rész új üzleti döntéssel felülírt, a következő specifikációverzióban frissítendő. Opcionális, meglévő WooCommerce alapbeállításra épülő „csak webshopban” jelölés technikailag vizsgálandó; enélkül nincs csatorna szerinti termékkizárás. Webes app-előfizetés csak bejelentkezve vásárolható; a belépett vásárló webes fiók-/előfizetésélményét fel kell mérni, de annak esetleges átdolgozása a PWA-projekt keretén kívüli, külön egyeztetendő munka.

## 4. V1.3 követelménymegfeleltetés

Az alábbi F-azonosítók **a DOCX F01–F26 listájára** hivatkoznak. A `build_spec.py` korábbi F01–F20 listája nem írja felül a DOCX-et.

| Spec ID | Követelmény / kész állapot | Backend / frontend | Teszt |
|---|---|---|---|
| F01 | WP-fiók, profil, saját adatok | WP auth + `/me`, profil | T01 |
| F02 | Legkorábban lejáró használható családi jegy/bérlet | EntitlementService + főoldal | T02 |
| F03 | Audio/video, keresés, kategória, prémium | Media CPT + DTO + médiatár | T03 |
| F04 | Egyedi lejátszás végén megáll | React PlayerController | T04 |
| F05 | Sor, fel/le rendezés, tetszőleges kezdés, végén stop | QueueService + lejátszó | T05 |
| F06 | Natív képarány, 4 mobilkombináció, fullscreen | HTMLMediaElement + HLS | T06 |
| F07 | Fiókhoz kötött kedvencek | FavoritesService | T07 |
| F08 | Havi prémium-hozzáférés; **D09-MVP/01 elfogadva:** hiteles fizetéstől 1 naptári hónap célhelyi napjának végéig, Budapest időzóna és clamp; **D09-MVP/02 elfogadva:** aktív joghoz a megvett hónapok hozzáadódnak az eredeti fordulónapot megőrizve; lejárt jognál új fizetés új sorozatot indít; automatikus újraterhelés csak később | Core paid-through + meglévő Barion egyszeri checkout; későbbi kész recurring adapter feltételes | T08; D09 |
| F09 | **D09-MVP/03 ELFOGADVA:** PWA-ban mindig pontos lejárati nap; az utolsó 7 napban kiemelt, állapot-alapú figyelmeztetés és újravásárlás; **nincs automatikus lejárati e-mail/push**; recurring lemondás/kártyacsere/retry későbbi fázis | Prémium-hozzáférési adapter + PWA kijelzés szerver `paid_through` alapján | T09; D09 |
| F10 | Élő WC-katalógus, minden támogatott terméktípus | Catalog adapter + web checkout | T10; G1 |
| F11 | **D02 elfogadva:** családi jegy hiteles sikeres fizetéstől 3 naptári hónap (WP-terméktípusból konfigurálható), budapesti lejárati nap végéig | EntitlementService + termékszabály snapshot + szerver dátumszámítás | T11; D02 |
| F12 | **D02 elfogadva:** 8 alkalmas bérlet 8 naptári hónap az első sikeres beváltástól (WP-terméktípusból konfigurálható), magyar helyi lejárati nap végéig | PassService + `first_used_at` + termékszabály snapshot | T12; D02 |
| F13 | Saját QR és szerveroldali státusz | QR token + wallet | T13 |
| F14 | **D03 elfogadva:** mindhárom típusnál (családi jegy, 8 alkalmas bérlet, külön áras eseményjegy) egy jogosultság konkrét eseményen csak egyszer váltható be; visszatéréskor nincs új levonás. A családi jegy globálisan egyszeri, a külön eseményjegy eseményhez kötött, a bérlet másik eseményen ugyanazon napon újra használható | EntryService + tranzakció + UNIQUE entitlement/event + staff visszatérésjelzés | T14; T17; T18; T24; D03 |
| F15 | Programrészlet, naptár előtte/utána | Event adapter + ICS | T15 |
| F16 | Rendszeres program, nincs foglalás | `open` event | T16 |
| F17 | **D05 elfogadva:** limitált alapdíjas foglalás + jegy/bérlet; foglalás a program kezdetéig lemondható, felszabaduló családi hely újra foglalható | ReservationService + EntryService + idempotens kapacitásfelszabadítás | T17; D05 |
| F18 | **D05 elfogadva:** külön áras jegy és családi hely csak sikeres fizetés/kapacitás mellett; vásárláskor 15 perces hold, késő fizetés nem okozhat túlfoglalást | 15m hold + WC paid event + tranzakciós kapacitásellenőrzés, `paid_capacity_conflict` | T18; D05 |
| F19 | **D04 elfogadva:** V1 egy WP-fiók = egy külön family_id, 1 család = 1 kapacitásegység/foglalkozás; nincs fiókösszekapcsolás vagy önkiszolgáló jegyátadás | FamilyService + szerveroldali családfeloldás + kapacitászár; későbbi tagságra előkészített ID | T19; T20; D04 |
| F20 | Rendelés és jogosultság státusz együtt | WC order adapter + wallet | T20 |
| F21 | D06 elfogadva: WordPressből egyéni/csoport/összes címzés, címzettenként app receipt, külön opcionális push | WP admin + PushService | T21; D06 |
| F22 | **D06/D12:** az appbeli értesítéslista alapból 365 napot jelenít meg, ez konfigurálható megjelenítési ablak, nem tényleges adatmegőrzési/törlési idő; panelmegnyitás óta „ÚJ” | Receipts + ReadCursor + WordPress beállítás; külön automatizált GDPR purge nem scope | T22; D06; D12 |
| F23 | Aszinkron szöveges üzenet Virágnak; D11: ingyenes BM V1, aktív chatben kb. 10 s polling | Better Messages REST/AJAX adapter, staging képesség- és jogosultsági ellenőrzés; fizetős WebSocket külön jóváhagyás esetén | T23; D11 |
| F24 | **D05 elfogadva:** staff ellenőrzés/beváltás alapból kezdés előtt 2 órától befejezés után 2 óráig, eseményenként WordPressből konfigurálható | Staff capability + scanner + admin időablakbeállítás | T24; D05 |
| F25 | WP admin kezeli a termék/program/push adatokat | Core admin + meglévő admin | T25 |
| F26 | A „Kuponjaim” és a rövid médiacsomag V1-beli kezelése a specifikáció szerint; a régi Online Ringató értékesítésének tiltását a 2026-10-15-i D01 döntés felülírta | Route-kezelés; egységes katalógus D01 szerint | T26; D01 |

**D12 adatkezelési projekthatár (elfogadva 2026-10-16):** nincs jogi tanácsadás, új általános anonimizálás, tömeges törlőmotor vagy külön GDPR export/erase-fejlesztés. A meglévő WP/WooCommerce/BM/Billingo eszközökre támaszkodunk; a funkcionálisan szükséges törlések és adatbiztonsági követelmények megmaradnak. A projekt által kezelt időablakokat ahol lehet WordPressből konfiguráljuk (D06 értesítési lista alap: 365 nap); törvényi értéket csak konkrét, ellenőrzött jogszabályi alap és adatkezelői jóváhagyás esetén használunk. A tényleges adatmegőrzési jogalapok és adatvédelmi szövegek a megrendelő felelőssége; hiányzó kötelező funkció külön scope-döntés.

**D07 elfogadott refund-szabály (2026-10-16):** WooCommerce-ből indított, Barionnal végrehajtott és Billingóval helyesbített visszatérítésre támaszkodunk; **nem építünk saját Barion refund integrációt**. Csak teljes, sikeresen igazolt és egyértelműen fel nem használt rendeléstétel jogosultsága vonható vissza automatikusan (fizetős eseménynél aktív hely egyszeri felszabadításával). Már használt, részleges, összetett vagy többtermékes refund kézi ellenőrzés; nincs automatikus alkalom-visszaadás, a belépési napló megmarad. Közvetlen Barion refund/chargeback WooCommerce-szinkronja nem garantált; kézi egyeztetési eljárás és **teljes/részleges WooCommerce–Barion–Billingo sandbox teszt** kötelező.

**D05 jóváhagyott foglalási és beléptetési szabályok (2026-10-16):** alapdíjas foglalás az esemény kezdését **megelőzően** lemondható; a külön áras foglalkozáshoz vásárláskor 15 perces helyfenntartás tartozik minden értékesítési csatornán. A későn igazolt fizetés csak újra ellenőrzött szabad férőhely esetén adhat jegyet/foglalást, másként `paid_capacity_conflict` és D07 szerinti pénzügyi ügyintézés. A staff alapértelmezett ideje start−2h/end+2h, eseményenként WordPressből módosítható; V1-ben nincs várólista.

**D08 elfogadott átállási stratégia (2026-10-16):** a meglévő érvényes papírjegyek és papírbérletek átmenetileg helyszíni papíros rendszerben maradnak; a kijelölt cutoff után az új digitális termékkör vásárlásai Ringató Core jogosultságot kapnak. **Teljes régi papírállomány/korábbi vendégrendelés import nem V1-kötelező.** Régi jogosultságot digitálisan csak igazolt maradék/első használat/korábbi beváltás alapján, opcionális kézi folyamattal lehet létrehozni; hiányzó bizonyíték esetén nincs aktív QR. Régi vendégrendelés csak igazolt, auditált fiókhozzárendeléssel, e-mail-egyezés nem elég. A D01 szerinti régi Online Ringató-termékek megtartása változatlan; SKU-nként tisztázni kell az új vásárlások digitális jogosultságait. Cutoff dátum, helyszíni folyamat, kommunikáció még nyitott.

**D04 jóváhagyott családmodell (2026-10-16):** egy WordPress ügyfélfiók egy önálló `family_id`-val rendelkező családot képvisel; a jegyek/bérletek/eseményjegyek/foglalások a családhoz tartoznak, két szülő külön fiókja nincs automatikusan összekapcsolva. Jegyátruházás és több család önkiszolgáló vásárlása nem V1. Kivételes esetek kézi, jogosultság- és auditált ügyintézésben; eseményenként legfeljebb egy aktív családi foglalás. A `family_id` elkülönítése lehetőséget hagy későbbi többfiókos családkezelésre, de azt most nem fejlesztjük. A D08 legacy/guest-claim ettől külön nyitott.

**D03 jóváhagyott pontosítás (2026-10-16):** családi jegy, bérlet és külön áras eseményjegy ugyanazon konkrét foglalkozásra történő visszatérésnél az első sikeres belépés ellenőrzését kapja, **újabb beváltás/levonás nélkül**. Nincs globális napi limit, de bérletnél másik esemény alkalmat fogyaszt; a már használt egyszeri jegy nem használható újra, és a külön áras jegy csak a saját programján érvényes. Meglévő D05 foglalási és időablak-feltételek érvényben maradnak.

**D02 jóváhagyott pontosítás (2026-10-16):** `Europe/Budapest` szerinti célhelyi nap végéig tartó lejárat, naptári hónap hozzáadás hiányzó célnapnál a hónap utolsó napjával; technikai exclusive UTC `expires_at` a következő helyi nap 00:00-ja. Példa: január 31-i jegy → április 30.; január 31-i első bérletbeváltás → szeptember 30. A jegy 3 és bérlet 8 hónapja a WordPressben terméktípus-szabály szerint beállítható, order-item pillanatkép véd a retroaktív átírástól. Ez nem módosítja az eseményjegy vagy a D09 havi prémium jogszabályait. A DOCX következő specifikációs kiadásában az időpont és konfiguráció pontosítását át kell vezetni.

**D09 kiegészítő döntés (2026-10-16):** az automatikus megújulás retry-ütemezése, kártyacsere, recurring lemondás és kapcsolódó értesítések a később kiválasztandó és külön jóváhagyott kész integrációhoz tartoznak, **nem MVP-követelmények**. **D09-MVP/01 ELFOGADVA:** aktív korábbi időszak hiányában az új havi prémium hozzáférés a hiteles fizetéstől, annak `Europe/Budapest` szerinti helyi dátumához hozzáadott 1 naptári hónap célhelyi napjának **végéig** érvényes, hiányzó célnap esetén a hónap végére igazítva; a szerver `paid_through` UTC exclusive határa a következő helyi nap 00:00-ja. 30 napos számítás nem helyettesítheti. **D09-MVP/02 ELFOGADVA:** az aktív hozzáféréshez előrevásárolt hónapok az eredeti Budapest szerinti fizetési naptári dátum fordulónapjához hozzáadódnak (jan. 31. → febr. 28. → márc. 31.), lejárat után új fizetés új fordulónapot indít. Párhuzamos és ismételt callback legfeljebb egyszer írhat jóvá egy rendeléstételt; refund D07 szerint. **D09-MVP/03 ELFOGADVA:** mindig látható pontos PWA lejárati nap; a lejáratot megelőző utolsó 7 napban kiemelt figyelmeztetés és újravásárlás, **automatikus e-mail/push nélkül**. Előrevásárlás után a friss szerver `paid_through` számít; meglévő webes fiók UI módosítása D01 szerint külön scope.

**D09 specifikációs eltérés (2026-10-15):** az F08–F09 szerinti automatikus havi fizetés és lemondás nem MVP-kiadási feltétel. Az új, bejelentkezéshez kötött manuálisan havonta újravásárolható prémiumterméket külön kell kezelni a meglévő RINGI04 terméktől. Kész, ár/értékben megfelelő recurring integráció csak igazolt kompatibilitás és megrendelői költségvállalás után válhat következő fázissá; egyedi fizetési bridge nem része a projektnek. A DOCX következő változatába átvezetendő.

**D13 / P01 – ELFOGADVA (2026-10-15): „Virág kérdezi” szavazás az első éles verzió kötelező része.** A prototípusban szerepel, de a V1.3-as DOCX történeti F01–F26 listájában és entitáslistájában még nincs; **új, önálló P01 V1-követelményként** fel kell venni a specifikáció következő kiadásába. Tervezett minimum: Virág WordPress adminból kezel szavazásokat, bejelentkezett PWA-felhasználók válaszolhatnak, a szerver biztosítja a szavazatonkénti felhasználói egyediséget és az aktív időablakot, eredményláthatóság konfigurálható. **D13/01 elfogadva (2026-10-16):** egy fiók szavazásonként egy **végleges** választ adhat le, PWA-beküldés előtti megerősítéssel; utólagos módosítás nincs, lezárt poll nem fogad választ. **D13/02 pontosítva (2026-10-16):** Virág egyszerre sok, akár tartósan nyitott szavazást rögzíthet WordPressben, de a bejelentkezett felhasználó a dashboardra belépve **egyszerre pontosan egy, véletlenszerűen kiválasztott, még meg nem válaszolt aktív/nyitott kérdést** lát. A válaszolt, lezárt vagy időablakon kívüli kérdéseket kizárjuk; nincs választható kérdés esetén nincs új kérdéskártya. A folyamatosan frissülő összesített eredmények megtekinthetők a **D13/03-ban jóváhagyandó hozzáférési szabályok szerint**. Nem követelmény a felhasználónak minden nyitott szavazás lapozható, szavazásra kínáló listája. **D13/03–04** még részletezendő: eredmény-hozzáférés és időzítés/értesítés.

**P01 követelménymegfeleltetés:** „Virág kérdezi” – **kötelező V1** szavazás, WP-admin kezelés és PWA szavazás/állapot/eredmény; megvalósítás: PollService + saját táblák + REST + admin + React; elfogadási teszt: **TP01**.

## 5. Prototípus értelmezése

- Az `app.html` az `app.js` után tölti a `v13.js`-t, amely számos függvényt felülír. Csak együtt értelmezhetők.
- Nincs React/TypeScript build, npm csomaglista, valódi WP-login vagy API-integráció. A `localStorage` (`ringato-v1`) fiktív fiókállapotot tárol.
- Fizetés „sikerét”, QR-beváltást, foglalást és üzenetet a kliens módosítja. Ezeket a végleges kliens nem döntheti el.
- A QR látványelem, a scanner választólista; nincs kamera-beolvasás vagy szerveroldali validáció.
- A lejátszó időzítővel szimulál; nincs valós audio/video adatfolyam. A fullscreen fallback vizuális szimuláció.
- A push kampány a demó staff nézetében látszik; a végleges kampánykezelés kizárólag WP admin. Staff beléptetés lehet az appban.
- A demó service worker minden lekérést cache-el, és minden más cache-t töröl. Ez közös originen veszélyes minta: nem vihető át élesbe.
- A DOCX képernyőképei minták. Pl. képernyőn és demó adatban eltérő rendelési dátum előfordulhat; nem migrációs bizonyíték.
- A 28 képernyő a `../screens/` mappában UX-referencia. A valós hiba, offline, üres, hozzáférés- és betöltési állapotokat hozzá kell tervezni.

## 6. Határ és kizárások

V1: telepíthető, magyar nyelvű, online funkciókra épülő PWA; saját fiók; közös WC-kereskedelem; privát prémium média; digitális jegy/bérlet; program és foglalás; staff scanner; push; üzenet.

Nem V1: natív App Store/Play Store app, prémium offline letöltés, teljes React pénztár, külön webshop/adatbázis, teljes mobiladmin, kuponkezelő képernyő, olcsó rövid hozzáférés, várólista, csoportchat, csatolmány/hanghívás, DRM, automatikus marketingkampány. A meglévő webshop kuponjai és ajándékutalvány-kezelése tovább működhet a webes checkoutban; appbeli Kuponjaim felület nem készül.
