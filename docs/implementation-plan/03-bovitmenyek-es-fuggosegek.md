# 03 – Bővítmények, csomagok és infrastruktúra

## 1. WordPress: megtartás, hozzáadás, saját fejlesztés

| Elem | Döntés / szerep | Licenc/költség és feltétel |
|---|---|---|
| WordPress + meglévő egyedi téma | Megtartás; publikus oldal változatlan | A jelentett helyi verzióra és éles tárhelyre teszt |
| WooCommerce | Megtartás; termék, rendelés, kosár, checkout, HPOS | Meglévő; minden rendeléskezelés WC CRUD |
| Meglévő Barion gateway | Egyszeri fizetés megtartása | A 3.10.2 gateway `products`,`refunds` képességet deklarál, recurringot nem |
| Billingo | Meglévő számlázás megtartása | Subscription renewal/refund bizonylat és dupla számla kizárása próbával |
| WooCommerce Subscriptions | **Új kötelező bővítmény** havi előfizetéshez | Kereskedelmi licenc; aktuális ajánlat/licencfeltétel beszerzéskor ellenőrzendő |
| Better Messages | **Új integrációs jelölt** szülő–Virág chathez | V1 free AJAX/polling vizsgálat; WebSocket opcionális fizetős licenc |
| Ringató Core | **Saját plugin szükséges** | REST, admin, domainmodell, kapacitás, jegy/bérlet, média, push, BM adapter |
| Ringató App Shell | **Saját vékony plugin szükséges** | Build kiszolgálása `/app/`, bootstrap, origin/scope, release verzió |
| Ringató Barion Subscriptions Bridge | **Várhatóan saját fejlesztés szükséges** | Másik igazolt kompatibilis gateway helyettesítheti, ha ugyanazt a követelményt bizonyítja |
| Action Scheduler | WC/WCS meglévő ütemezőjének használata | Nem telepítünk újabb független schedulert; elérhetőséget/verziót vizsgálni |
| SMTP, WAF, cache | Meglévő éles szolgáltatásokhoz illesztés | API/auth/cron kivételek, app-origin e-mail regresszió |
| GiftRocket | Megtartás, konfigurátorhoz webes útvonal | `wxgiftcard` nem simple termék; licenc/Store API integráció ellenőrzése |
| CookieYes | Meglévő oldal consentjének megőrzése | PWA adatkezelés/consent külön illesztés; nem feltételezett automatikus átvétel |

**Nem szükséges alapértelmezetten:** WP PWA/SuperPWA plugin (root SW ütközés), JWT auth plugin (same-origin WP session elegendő), WooCommerce Memberships (hozzáférés Core/WCS alapján), WooCommerce Bookings / Events Manager / The Events Calendar (meglévő event és speciális családi kapacitás van), külön generic QR/ticket plugin (V1.3 egyedi szabályok), OneSignal (a saját címzettcsoport és 365 napos előzmény saját adatmodell maradna). Ezek később csak bizonyított funkcionális előnnyel és regressziós vizsgálattal kerülhetnek be.

### Core plugin modulok és átadandó elemek

- `Catalog` + termékmapping admin: minden megvásárolható típus DTO-ja, PWA tiltások, ticket/pass/event/subscription besorolás és snapshot.
- `Events` + meglévő CPT adapter: új PWA metaadatok, end/timezone/capacity/event product mapping, ICS.
- `Commerce` és outbox: fizetési esemény feldolgozás, order-item/idempotency, refund/revocation, helyreállítás; minden mapped rendelési csatorna.
- `Entitlements`, `Reservations`, `Checkin`: own tables, atomikus beváltás/foglalás, staff scope, audit és indokolt admin korrekció.
- `Media`: CPT/taxonómia, privát forrásazonosító, playback provider adapter.
- `Preferences`: kedvencek és verziózott sor.
- `Push`: címzettcsoport admin, kampány előnézet/küldés, VAPID, device subscription, receipt/cursor, job retry/retention.
- `Messaging`: Better Messages adapter + polling; opcionális szavazás modul csak scope-döntés után.
- `Security` és `Operations`: permission callback minden route-hoz, rate limit, migráció, GDPR export/erase integráció, health/admin diagnosztika és reconciliation job.

Átadáskor plugin forrás, migrációk, admin használati leírás, OpenAPI fájl, szerződéstesztek, staging konfigurációs minta titkok nélkül, kiadási/rollback runbook szükséges.

## 2. Barion recurring integrációs munkacsomag

A Barion SDK recurring mezőinek jelenléte **nem jelenti**, hogy a telepített WooCommerce gateway támogatja a WCS automatikus megújulását. A helyi gateway deklarációjában nincs `subscriptions`, és a vizsgált pluginban nem találtunk WCS renewal hookot. [WCS gateway követelmények](https://woocommerce.com/document/subscriptions/payment-gateways/)

### Beszerzés vagy saját bridge

Először igazolt, karbantartott Barion–WCS kompatibilis extension vizsgálata, sandboxpróbával. Pusztán „Barion kompatibilis” marketingállítás nem elegendő. Ha nincs megfelelő csomag, külön bridge fejlesztése szükséges a meglévő egyszeri gateway módosítása nélkül.

A bridge minimális felelőssége:

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

**Kill criterion:** ha a recurring jóváhagyás vagy kompatibilitás nem bizonyítható, F08 kiadása megáll. Egyszeri havi kézi vásárlás nem helyettesíti az automatikus megújulás követelményét.

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
| Composer autoload + saját namespace | Core és bridge modulok, determinisztikus build |
| `minishlink/web-push` | VAPID alapú Web Push; PHP/OpenSSL/cURL kompatibilitást tárhelyen igazolni |
| `sabre/vobject` (feltételes) | ICS generálás/validálás; elhagyható, ha szigorúan tesztelt kicsi ICS-serializer készül |
| Média provider SDK (feltételes) | Csak a kiválasztott storage/CDN szükséges minimális kliens; titkok backendben |
| PHP unit/integration framework | Core szolgáltatások + tényleges InnoDB konkurenciateszt |
| PHPCS + WordPress Coding Standards, PHPStan | WP kódminőség, HPOS/escaping/schema ellenőrzések |
| WP-CLI (fejlesztés/üzemeltetés) | Idempotens migráció, dry-run import, reconciliation riport |

A meglévő Barion SDK-t nem szerkesztjük vendor fájlban. Bridge SDK-hozzáférést verziózott interfészen vagy saját, ellenőrzött SDK-függőséggel oldunk meg; mindkettőnél névtér/dupla verzió ütközést vizsgálni kell. A WP-ben minden Composer függőségnél ugyanilyen ütközési teszt szükséges.

## 5. Szükséges szolgáltatások és költséghelyek

- Meglévő WordPress tárhely, HTTPS, deploy hozzáférés, staging és DB-backup. `/app/` útvonal vagy plugin rewrite támogatás, megfelelő PHP/DB erőforrás.
- Privát média objektumtár + CDN/streaming/transzkódolás: signed HLS/MP4/audio, bélyegkép, tartomány/CORS, titkos storage. A választás előtt tényleges forgalom/tárhely/átviteli igény becslése kell.
- WooCommerce Subscriptions licenc, opcionális Better Messages WebSocket licenc; saját plugin/bridge fejlesztési és karbantartási költség.
- Barion merchant recurring jóváhagyás és sandbox hozzáférés, Billingo tesztüzem, SMTP tesztcímek.
- VAPID kulcspár backendben; nincs kötelező fizetős push SaaS. A push szolgáltatói végpontok eléréséhez tárhely egress kell.
- Valós rendszer-cron és Action Scheduler workerfuttatás; napi mentés, monitoring, hibariasztás.
- Teszteszköz: iPhone Safari/telepített PWA és Android Chrome/telepített PWA; a desktop emuláció nem elég.
- Üzemeltető, Virág/staff, fejlesztő, üzleti döntéshozó és adatkezelési felelős a döntési táblához.

Pontos licenc-/CDN-/fejlesztési összeg most nem állapítható meg ellenőrzött használati volumen, tárhelyadat és szolgáltatóválasztás nélkül. Beszerzési lista igen, fiktív árajánlat nem része a tervnek.
