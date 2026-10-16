# 03 – Bővítmények, csomagok és infrastruktúra

**Munkarend (2026-10-15):** a fejlesztés és tesztelés lokálisan történik; tesztszerverre és élesre manuálisan telepítünk, majd rövid működésellenőrzést végzünk. A korábbi staging-tesztre utalásokat e rend szerint kell értelmezni; a tárhelyfüggő kapacitás/cron/WAF külön igazolandó. Minden növekményhez a [11. telepítési útmutató](11-lokalis-fejlesztes-es-manualis-telepites.md) szerint készül csomag és konkrét konfigurációs/másolási leírás.

## 1. WordPress: megtartás, hozzáadás, saját fejlesztés

| Elem | Döntés / szerep | Licenc/költség és feltétel |
|---|---|---|
| WordPress + meglévő egyedi téma | Megtartás; publikus oldal változatlan | A jelentett helyi verzióra és éles tárhelyre teszt |
| WooCommerce | Megtartás; termék, rendelés, kosár, checkout, HPOS | Meglévő; minden rendeléskezelés WC CRUD |
| Meglévő Barion gateway | Egyszeri fizetés és D07 szerinti WooCommerce-ből indított refund megtartása | A 3.10.2 gateway `products`,`refunds` képességet deklarál, de a tényleges teljes/részleges refund és a közvetlen Barionból indított refund WooCommerce-be visszakerülése **nem igazolt**, stagingpróba kell |
| Billingo | Meglévő számlázás és D07 szerint refund-helyesbítés megtartása | WooCommerce → Barion → Billingo teljes és részleges refund és helyesbítés tesztelendő; később csak jóváhagyott recurring esetén renewal számlázás |
| WooCommerce Subscriptions vagy más kész recurring opció | **Nem MVP-kötelező; feltételes későbbi beszerzés** | A legjobb ár/értékű kompatibilis megoldás teljes licenc-/éves-/tranzakciós költségét és üzemeltetését fel kell mérni; megrendelői vállalás kell |
| Better Messages | **D11 elfogadott V1 irány:** ingyenes REST/AJAX változat stagingpróbával | Csak aktív chatnézeten kb. 10 s polling; jogosultság/read/unread/kétirányú kommunikáció igazolandó. Fizetős WebSocket csak indokolt igény és külön megrendelői költségjóváhagyás után |
| Advanced Custom Fields (Free) | **Kötelező**, PWA szövegek, oldalankénti blokkok, layout és menüikonok | Ingyenes; kizárólag Free mezők; [hivatalos telepítés](https://www.advancedcustomfields.com/resources/installation/), nem Pro |
| Ringató Core | **Saját plugin szükséges** | REST, admin, domainmodell, kapacitás, jegy/bérlet, média, push, BM adapter |
| Ringató App Shell | **Saját vékony plugin szükséges** | Build kiszolgálása `/app/`, bootstrap, origin/scope, release verzió |
| Saját Barion recurring bridge | **NEM része a jelenlegi projektnek** | Egyedi fizetési fejlesztés a rendelkezésre álló keretbe nem fér bele; kész igazolt integráció vagy manuális havi MVP |
| Action Scheduler | WooCommerce meglévő ütemezőjének használata | MVP-ben jogegyeztető munkákhoz; recurring scheduler csak későbbi kész integrációval |
| SMTP, WAF, cache | Meglévő éles szolgáltatásokhoz illesztés | API/auth/cron kivételek, app-origin e-mail regresszió |
| GiftRocket | Megtartás, konfigurátorhoz webes útvonal | `wxgiftcard` nem simple termék; licenc/Store API integráció ellenőrzése |
| CookieYes | Meglévő oldal consentjének megőrzése | PWA adatkezelés/consent külön illesztés; nem feltételezett automatikus átvétel |

**Nem szükséges alapértelmezetten:** WP PWA/SuperPWA plugin (root SW ütközés), JWT auth plugin (same-origin WP session elegendő), WooCommerce Memberships (hozzáférés Core/WCS alapján), WooCommerce Bookings / Events Manager / The Events Calendar (meglévő event és speciális családi kapacitás van), külön generic QR/ticket plugin (V1.3 egyedi szabályok), OneSignal (a saját címzettcsoport és 365 napos előzmény saját adatmodell maradna). Ezek később csak bizonyított funkcionális előnnyel és regressziós vizsgálattal kerülhetnek be.

### Core plugin modulok és átadandó elemek

- `Catalog` + termékmapping admin: minden megvásárolható típus DTO-ja, a D01 szerint kivételes PWA-szűrés, ticket/pass/event/manual_monthly_access/későbbi recurring besorolás és snapshot.
- `Events` + meglévő CPT adapter: új PWA metaadatok, end/timezone/capacity/event product mapping, ICS.
- `Commerce` és outbox: fizetési esemény feldolgozás, order-item/idempotency, refund/revocation, helyreállítás; minden mapped rendelési csatorna.
- `Entitlements`, `Reservations`, `Checkin`: own tables, atomikus beváltás/foglalás, staff scope, audit és indokolt admin korrekció.
- `Media`: CPT/taxonómia, privát forrásazonosító, playback provider adapter.
- `Preferences`: kedvencek és verziózott sor.
- `Push` (D06 elfogadva): WordPress egyéni/csoport/összes címzés; kampány előnézet/küldés, VAPID, device subscription, minden címzettnek egy app receipt push nélkül is, eszközök kézbesítése külön; 365 napos **megjelenítési** ablak (konfigurálható, 365 napos termék-alapértékkel). **D12:** nem automatikus fizikai DB-törlés; külön adatkezelői határidő és szükség esetén új scope.
- `Messaging`: D11 szerint az **ingyenes Better Messages REST/AJAX** az elsődleges, stagingben tesztelendő. Aktív chatben kb. 10 s lekérdezés, háttérben leállítás, visszatéréskor frissítés; saját parent–Virág thread, read/unread, retry/idempotencia és jogosultság. Ha az ingyenes API nem alkalmas, új döntés szükséges.
- **`Polls` (D13/P01, V1 kötelező):** „Virág kérdezi” WordPress admin kérdés-/válaszopció-kezelés, publikálás és zárás, eredményláthatósági beállítás; saját szerveroldali válaszmentés, egyediség, összesítés és PWA API. Nem opcionális és nem puszta prototípusfunkció. A részletes válaszmódosítási szabály implementálás előtt egyeztetendő.
- `Security` és `Operations`: permission callback minden route-hoz, rate limit, migráció, health/admin diagnosztika és reconciliation job. **D12 adatkezelési scope (2026-10-16):** nincs új jogi támogatás, átfogó GDPR export/erase, anonimizálási vagy tömeges törlési modul a projektkeretben. A meglévő WordPress/WooCommerce/Better Messages/Billingo támogatott adatvédelmi folyamatait nem kerüljük meg, az új funkciókhoz szükséges session-, eszköz-, jogosultság- és adatéletciklus-műveletek megmaradnak. Az érintetti kérelemhez hiányzó integráció külön kockázat és scope-döntés. A tényleges jogi megőrzési idők és tájékoztatók a megrendelő adatkezelési felelőséhez tartoznak.

Átadáskor plugin forrás, migrációk, admin használati leírás, OpenAPI fájl, szerződéstesztek, staging konfigurációs minta titkok nélkül, kiadási/rollback runbook szükséges.

### D07: Refundfolyamat, meglévő integrációra építve (2026-10-16)

**Nincs saját Barion-visszatérítési API/bridge fejlesztés.** Az ügyintéző alapértelmezetten a WooCommerce-ben indít refundot; a meglévő Barion gateway és Billingo végzi a fizetési/helyesbítési műveleteket, a Ringató Core csak az **ellenőrzött, megfelelő rendeléstételhez rendelt refund eredménye alapján** szűkíti a belépési és prémiumjogot. Teljes, még fel nem használt és egyértelmű jog esetén automatikus revoke, külön eseményjegynél szabad hely egyszeres felszabadítása; részleges/használt/összetett rendelés kézi ellenőrzés. Közvetlen Barion refund és chargeback WooCommerce-be történő szinkronizációját nem feltételezzük; külön egyeztetés/üzemeltetési eljárás.

**Kötelező staging/sandbox ellenőrzés:** teljes és részleges WooCommerce refund → tényleges Barion eredmény → WooCommerce refund rekord és rendeléstétel → Billingo helyesbítő bizonylat; hibás/dupla callback, kézi WooCommerce-only refund pénzmozgás nélkül, közvetlen Barion refund, chargeback, többtermékes/használt jegy és idempotens jog-/helykezelés. Hibánál előbb üzleti/üzemeltetési egyeztetés, nem automatikus saját gateway fejlesztés.

## 2. D09: MVP havi egyszeri vásárlás, későbbi kész recurring megoldás felmérése

**A jelenlegi projektben nincs saját Barion recurring integráció fejlesztése.** Az MVP egyszeri, bejelentkezéshez kötött WooCommerce-termékvásárlásokkal működik; a sikeresen kifizetett havi időszakot a Ringató Core kezeli. WooCommerce Subscriptions és Barion recurring jogosultság nem szükséges az MVP indításához.

**D09 részletdöntés (2026-10-16):** a recurring rendszer automatikus terhelésének hibakezelése/retry-szabályai, kártyacsere, lemondás és megújítási értesítések **csak egy később kiválasztott, tesztelt és költségjóváhagyott kész integrációhoz** tervezendők; nem MVP-feladat és nem önálló fejlesztés. A manuális prémium **D09-MVP/01** időtartama **elfogadva:** hiteles fizetéstől 1 naptári hónap célhelyi napjának végéig, `Europe/Budapest` és hónapvégi igazítás szerint; a **/02 előre újravásárlás is elfogadott**: aktív hozzáférésnél az eredeti helyi havi fordulónap megtartásával adódnak össze a hónapok, lejártnál új kezdőnap; **/03 lejárati tájékoztatás is elfogadva:** a PWA mindig mutatja a pontos lejáratot, az utolsó 7 napban kiemelt figyelmeztetést és újravásárlási CTA-t; **automatikus lejárati e-mail/push és reminder-job nem szükséges**.

**Beszerzési/megvalósíthatósági feladat a következő fázisra:**
1. Felkutatni a ténylegesen karbantartott, kész WooCommerce-kompatibilis automatikus megújítást (Barionnal, ha bizonyított, vagy más vállalható kész fizetési útvonallal).
2. Összevetni a teljes életciklus költségeit: bővítmény/licenc, évenkénti megújítás, gateway/tranzakció, konfiguráció és teszt, támogatás, szükséges megrendelői kereskedői jogosultság, későbbi migráció.
3. Sandboxban igazolni a fizetési folyamatot, sikeres megújulást, hibát és lemondást, a webes/PWA közös hozzáférést. Nem elég a termékleírás szerinti kompatibilitás.
4. **Megrendelői költségvállalás** után lehet külön későbbi fázis. Ha nincs jó ajánlat vagy költségvállalás, marad a kézi havi vásárlás.

A Barion SDK recurring mezői önmagukban nem bizonyítják a telepített gateway automatikus megújítási képességét; a helyi gateway `subscriptions` supportot nem deklarál. [WCS gateway követelmények](https://woocommerce.com/document/subscriptions/payment-gateways/)

### Korábbi egyedi bridge-technikai ellenőrzőlista – csak tájékoztató, jelenlegi scope-on kívül

Az alábbiak **nem fejlesztési feladatok az MVP-ben**, hanem a választandó kész integráció elfogadási kontrolljai. Saját bridge készítése csak külön, későbbi szerződéses projektben merülhetne fel.

A recurring integráció vizsgálandó felelősségei:

1. Külön gatewayazonosító az app-előfizetéshez, csak megvalósított WCS supports képességekkel. A hagyományos `barion` egyszeri fizetés megmarad.
2. Merchant recurring engedély/jóváhagyás; ügyfél hozzájárulás összege, periódusa, feltétele és verziózott elfogadása. Sandbox recurring engedély nem éles jóváhagyás.
3. Kezdő fizetés/recurrence azonosító, token és hozzájárulás szerveroldali biztonságos tárolása. Nincs PAN/CVV vagy kártyaadat a WordPress/app oldalon.
4. WCS scheduled renewal hook a saját gateway ID-ra; egy payment attempt/renewal order. Külső terhelés előtt tartós attempt, timeoutkor lekérdezés, nem vak újraterhelés.
5. Barion callback után hiteles szerveroldali payment state egyeztetés: POS/order kapcsolat, currency/amount, sikerállapot. Redirect és callback payload önmagában nem payment proof.
6. Renewal `payment_complete` és subscription paid-period frissítés idempotensen; sikertelen fizetés WCS failure folyamatba, user/admin jelzés.
7. Lemondás/új terhelés versenyhelyzete: charge előtti renewal-enabled ellenőrzés, már elindított fizetés determinisztikus egyeztetése. Token használatának leállítása, ha nincs más engedélyezett subscription.
8. Sikertelen fizetés rendezése és fizetési eszközcsere. Kezeljük a token lejáratát és a szükséges új ügyfélhitelesítést.
9. Refund/chargeback/duplikált webhook/válaszvesztés helyreállítása; Billingo bizonylatokat nem a bridge gyártja párhuzamosan.

A Subscriptions integrációs lépésekhez a [hivatalos gateway guide](https://woocommerce.com/document/subscriptions/develop/payment-gateway-integration/) az alap. A Barion nem ütemezi automatikusan a díjakat; a kereskedő rendszerének kell indítani az engedélyezett terhelést. [Barion subscriptions](https://docs.barion.com/Subscriptions%3A_set_up_recurring_billing)

**D09 kiadási szabály:** ha nincs igazolt és a megrendelő által finanszírozott kész recurring megoldás, **csak az automatikus megújulás későbbi fázisa nem indítható**. A manuálisan, havonta újravásárolható hozzáférésű MVP ettől függetlenül kiadható. A V1.3 F08 automatikus megújulási követelményét az új D09 üzleti döntés az MVP-re felülírja.

## 3. React/TypeScript csomagjavaslat

Az alábbi lista felelősségi ajánlás, nem most telepített vagy tesztelt lockfile. Implementáció indulásakor támogatott stabil verziók, peer dependency/Node kompatibilitás és licencellenőrzés; egzakt verziók lockfile-ba. Nem rögzítünk találomra „latest” verziószámokat.

| Csomag | Prioritás | Feladat / indok |
|---|---|---|
| `react`, `react-dom`, `typescript` | kötelező | React UI, strict TS, DOM típusok |
| `vite`, `@vitejs/plugin-react`, `@types/react`, `@types/react-dom` | kötelező dev | Build/dev server, React TypeScript integráció; nincs SSR igény |
| `react-router` | kötelező | Declarative route fa, `/app` basename, deep link |
| `@tanstack/react-query` | kötelező | API cache memóriaállapotban, invalidáció, loading/error; nincs privát persist |
| `zod` | kötelező | Runtime DTO/request validáció, szerződéseltérés felismerése |
| `vite-plugin-pwa` | kötelező dev | `injectManifest`, saját SW és frissítési prompt |
| `workbox-precaching`, `workbox-routing`, `workbox-strategies` | kötelező SW | Statikus precache és szűk allowlist; privát API NetworkOnly |
| `hls.js` | feltételes | HLS azon böngészőben, ahol nincs natív HLS; dinamikus import |
| `qrcode` + `@types/qrcode` | kötelező | Valódi QR generálás; opaque token, nem user/order ID |
| `qr-scanner` | kötelező staff | Kamera + QR dekódolás; nem építünk kizárólag BarcodeDetectorra |
| `react-hook-form`, `@hookform/resolvers` | ajánlott | Profil/üzenet űrlap validáció; minimális formsnál natív React is elég |
| `openapi-typescript`, `openapi-fetch` | ajánlott dev/runtime | Végleges OpenAPI-ból kliens típusok és typed fetch; a fetch wrapper auth/error logikát hozzáadja |
| `vitest`, `@testing-library/react`, `@testing-library/user-event`, `jsdom` | kötelező dev | Player/queue/állapot tesztek |
| `msw` | ajánlott dev | API mock a végleges szerződésből, nem éles demóállapot |
| `@playwright/test`, `@axe-core/playwright` | kötelező dev | E2E, regresszió, akadálymentességi ellenőrzés |
| `eslint`, `typescript-eslint`, `eslint-plugin-react-hooks`, `eslint-plugin-jsx-a11y`, `prettier` | kötelező dev | Kódminőség és accessibility alapszabályok |

Kezdetben nincs szükség Reduxra, külön Axiosra, IndexedDB wrapperre, DnD libraryre vagy komplett UI frameworkre. Natív `fetch`, Context/reducer a lejátszóhoz, React Query a szerverállapothoz; fel/le sorvezérlőhöz nem kell drag-and-drop. Ha később player/UI szükség indokolja, új csomagot célzottan lehet hozzáadni.

Arculat: a projektgyökér `docs/design/tokens.json`, `tokens.css`, saját fontok és engedélyezett assetek a referenciák. React-komponensekbe átvezetés és licencellenőrzés; archivált teljes vendor/theme CSS nem kerül az appba.

## 4. PHP/Composer és fejlesztőeszközök

| Elem | Használat |
|---|---|
| Composer autoload + saját namespace | Core modulok, determinisztikus build; recurring bridge nincs a jelenlegi scope-ban |
| `minishlink/web-push` | VAPID alapú Web Push; PHP/OpenSSL/cURL kompatibilitást tárhelyen igazolni |
| `sabre/vobject` (feltételes) | ICS generálás/validálás; elhagyható, ha szigorúan tesztelt kicsi ICS-serializer készül |
| Média provider SDK (feltételes) | Csak a **D10 eredményén alapuló, később kiválasztott** helyi vagy külső médiakiszolgálóhoz szükséges adapter/SDK; titkok backendben; a PWA nem köthető előre egy CDN-hez |
| PHP unit/integration framework | Core szolgáltatások + tényleges InnoDB konkurenciateszt |
| PHPCS + WordPress Coding Standards, PHPStan | WP kódminőség, HPOS/escaping/schema ellenőrzések |
| WP-CLI (fejlesztés/üzemeltetés) | Idempotens migráció, dry-run import, reconciliation riport |

A meglévő Barion SDK-t nem szerkesztjük vendor fájlban. Az MVP a meglévő egyszeri gateway-t használja, saját recurring SDK-integráció nélkül. Ha később kész bővítményt vezetünk be, a névtér/dupla verzió ütközéseket és a WC/Barion kompatibilitást tesztelni kell. Minden WP Composer-függőségnél ugyanez a szabály.

## 5. Szükséges szolgáltatások és költséghelyek

- **D12 (2026-10-15):** a meglévő tárhely PWA-kiszolgálásra alkalmas a projektgazda szerint; **tesztdomaines WP példány és fejlesztői lokális környezet már rendelkezésre áll**. A stagingben kell próbálni a `/app/` telepítését/plugint, rewrite/HTTPS/cache/WAF viselkedést, konfigurációt, frissítést és visszaállítást. Ezek sikeres eredménye még nincs dokumentálva. DB-backup/deploy és PHP/DB erőforrás valós ellenőrzés továbbra is szükséges.
- **D10 jóváhagyott eljárás (2026-10-16), mérés még nyitott:** a PWA-képes tárhely párhuzamos streamkapacitását biztonságos, üzemeltetővel egyeztetett lépcsőzetes terheléssel kell igazolni a stagingen. Készül tartalom- és várható egyidejű nézőszám/bitrate/havi forgalom becslés; mérjük a lejátszási hibát, pufferelést, sávszélességet, HTTP kapcsolatokat, CPU/memória/I/O terhelést, adatforgalmi limiteket, webshopválaszidőt, HLS/range mobil kompatibilitást. **Nincs jelenleg igazolt maximális párhuzamos szálérték.**
- **D10 szolgáltató továbbra is nyitott:** a meglévő tárhelyen megfelelően védett streaming és a külső privát streaming/CDN költségét/teljesítményét/üzemeltetését kell összevetni. Teljes ár: tárolás, havi adatforgalom, szükséges transzkódolás, beállítás/fejlesztés, fenntartás, szolgáltatási korlátok és ügyféltámogatás. Csak mérés és költségtábla után javasoljunk a megrendelőnek konkrét választást. A közvetlen publikus WP uploads URL önmagában nem megfelelő prémiumvédelem.
- MVP: ingyenes Better Messages AJAX/REST, a szükséges integrációs tesztek eredményétől függően; Ringató Core/App Shell saját fejlesztés és karbantartás. **WebSocket nem kötelező és nincs jóváhagyva:** csak indoklás, licenc-/költségellenőrzés és külön megrendelői döntés után. **Recurring csak feltételes:** több kész megoldás teljes licenc-/éves-/tranzakciós-/üzemeltetési költségének összehasonlítása és megrendelői vállalása; saját fizetési bridge nem tervezett.
- Meglévő Barion egyszeri fizetés sandboxellenőrzése, Billingo tesztüzem, SMTP tesztcímek. Barion merchant recurring jóváhagyás **csak későbbi automatikus opció esetén**.
- VAPID kulcspár backendben; nincs kötelező fizetős push SaaS. A push szolgáltatói végpontok eléréséhez tárhely egress kell.
- Valós rendszer-cron és Action Scheduler workerfuttatás; napi mentés, monitoring, hibariasztás.
- Teszteszköz: iPhone Safari/telepített PWA és Android Chrome/telepített PWA; a desktop emuláció nem elég.
- Üzemeltető, Virág/staff, fejlesztő, üzleti döntéshozó és adatkezelési felelős a döntési táblához.

Pontos licenc-/CDN-/fejlesztési összeg ellenőrzött szolgáltatóajánlat és használati igény nélkül nem állapítható meg; a D09 alapján a recurring opciók **valós, összehasonlítható költségfelmérése külön kötelező döntés-előkészítő feladat**, nem azt jelenti, hogy már meg is vásároltuk vagy jóváhagytuk a bővítményt.
