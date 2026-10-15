# 01 – Feltárás és követelmények

## 1. Bizonyíték és korlát

A felmérés a 2026-10-12-i mentésből visszaállított **helyi WordPressre** vonatkozik. Nem éles audit. Olvasási vizsgálat: aktív/inaktív pluginlista és verziók, tartalomtípus-regisztráció, nyilvános termékek, aggregált adatdarabszámok, téma esemény- és rendeléskezelő kódja, Barion gateway képességdeklaráció. Személyes rendelési adat és integrációs titok nem része e dokumentációnak.

A WordPress- és csomagverziók a helyi rendszer által jelentett értékek, nem frissítési ajánlások. Az éles környezet verzió- és konfigurációeltéréseit stagingindításkor külön ellenőrizni kell. A fizetési, számlázási, e-mail és teljes vásárlási folyamatot most nem futtattuk.

**D12 – projektgazdai pontosítás (2026-10-15; nem a korábbi helyi audit következtetése):** a jelenlegi vásárlók vendégként vásárolnak, fiók létrehozása nélkül; a tárhelyen **tesztdomaines WordPress tesztpéldány** rendelkezésre áll, és a fejlesztő **lokális fejlesztői környezetet** is épített. A tesztpéldány alkalmas a telepítési folyamat próbájának helyszínéül, a tényleges sikeres telepítést még tesztelni kell. A tárhely **PWA-kiszolgálásra alkalmasnak megerősített**, de a párhuzamos audio/video streaming kapacitása **nem mért**: terhelési vizsgálat szükséges, és csak az eredmény alapján dönthető el, kell-e külön streaming/CDN (D10). Az új fiókhoz kötött funkciók regisztrációs útvonalát ellenőrizni kell; a meglévő vendégvásárlás megőrzendő.

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
| F08 | Havi prémium-hozzáférés; a V1.3 automatikus megújítási elvárását D09 az MVP-ben manuálisan újravásárolható WooCommerce-termékre cseréli | Core paid-through + meglévő Barion egyszeri checkout; későbbi kész recurring adapter feltételes | T08; D09 |
| F09 | Kifizetett időszak végéig hozzáférés; a V1.3 automatikus megújítás lemondása csak későbbi, jóváhagyott recurring esetén értelmezett | Prémium-hozzáférési adapter; manuális MVP lejárat/újravásárlás | T09; D09 |
| F10 | Élő WC-katalógus, minden támogatott terméktípus | Catalog adapter + web checkout | T10; G1 |
| F11 | Egyszeri családi jegy, 3 naptári hónap | EntitlementService | T11 |
| F12 | 8 alkalom, első használattól 8 hónap | PassService | T12 |
| F13 | Saját QR és szerveroldali státusz | QR token + wallet | T13 |
| F14 | Globálisan egyszer beváltható jegy | EntryService + tranzakció | T14 |
| F15 | Programrészlet, naptár előtte/utána | Event adapter + ICS | T15 |
| F16 | Rendszeres program, nincs foglalás | `open` event | T16 |
| F17 | Limitált alapdíjas: foglalás ÉS jegy/bérlet | ReservationService + EntryService | T17 |
| F18 | Külön áras: fizetés = családi hely + eseményjegy | Hold + WC paid event | T18 |
| F19 | 1 család = 1 kapacitásegység | FamilyService + kapacitászár | T19 |
| F20 | Rendelés és jogosultság státusz együtt | WC order adapter + wallet | T20 |
| F21 | Virág manuális egyéni/csoportos push | WP admin + PushService | T21 |
| F22 | 365 nap előzmény, panelmegnyitás óta új | Receipts + ReadCursor | T22 |
| F23 | Aszinkron szöveges üzenet Virágnak | Better Messages adapter | T23 |
| F24 | Staff ellenőrzés, beváltás, napló | Staff capability + scanner | T24 |
| F25 | WP admin kezeli a termék/program/push adatokat | Core admin + meglévő admin | T25 |
| F26 | A „Kuponjaim” és a rövid médiacsomag V1-beli kezelése a specifikáció szerint; a régi Online Ringató értékesítésének tiltását a 2026-10-15-i D01 döntés felülírta | Route-kezelés; egységes katalógus D01 szerint | T26; D01 |

**D09 specifikációs eltérés (2026-10-15):** az F08–F09 szerinti automatikus havi fizetés és lemondás nem MVP-kiadási feltétel. Az új, bejelentkezéshez kötött manuálisan havonta újravásárolható prémiumterméket külön kell kezelni a meglévő RINGI04 terméktől. Kész, ár/értékben megfelelő recurring integráció csak igazolt kompatibilitás és megrendelői költségvállalás után válhat következő fázissá; egyedi fizetési bridge nem része a projektnek. A DOCX következő változatába átvezetendő.

**D13 / P01 – ELFOGADVA (2026-10-15): „Virág kérdezi” szavazás az első éles verzió kötelező része.** A prototípusban szerepel, de a V1.3-as DOCX történeti F01–F26 listájában és entitáslistájában még nincs; **új, önálló P01 V1-követelményként** fel kell venni a specifikáció következő kiadásába. Tervezett minimum: Virág WordPress adminból kezel szavazásokat, bejelentkezett PWA-felhasználók válaszolhatnak, a szerver biztosítja a szavazatonkénti felhasználói egyediséget és az aktív időablakot, eredményláthatóság konfigurálható. Válaszmódosítás, egyidejű aktív szavazások és az eredmények pontos üzleti szabályai részletezendők.

| P01 / D13 | „Virág kérdezi” – **kötelező V1** szavazás, WP admin kezelés, PWA szavazás/állapot/eredmény | PollService + saját táblák + REST + admin + React | TP01 (korábban opcionális) |

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
