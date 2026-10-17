# 08 – Forrásjegyzék és bizonyíték

Ellenőrzés: 2026. október 12. A technikai linkek elsődleges források; a csomagok/kereskedelmi licencek pontos támogatási és árfeltételeit implementáció/beszerzés indulásakor ismét ellenőrizni kell.

## Helyi források

| Forrás | Felhasználás |
|---|---|
| [Ringato_V1_3_specifikacio.docx](../Ringato_V1_3_specifikacio.docx) | Elsődleges termékkövetelmény, F01–F26, entitások, folyamatok és nyitott kérdések |
| [app.html](../../app.html) | Demó layout és `app.js`→`v13.js` betöltési sorrend |
| [app.js](../../app.js), [v13.js](../../v13.js) | Helyi demóállapot, V1.3 jegy/bérlet/media/push folyamatok és felülírások |
| [manifest](../../manifest.webmanifest), [sw.js](../../sw.js) | Jelenlegi PWA prototípus és élesbe nem átvihető általános cache-minta |
| [Képernyőképek](../screens/) | 28 statikus UX-referencia; részletesen a 06-os route táblában |
| [build_spec.py](../build_spec.py) | Generálási forrás; régebbi F01–F20 lista, ezért nem fő requirement mapping |
| [WordPress helyi környezet](../../../wordpress-local/README.md), [ellenőrzési napló](../../../wordpress-local/ELLENORZES.md) | Import/éles eltérések, mail/cron/gateway korlátok |
| [Design referencia](../../../docs/design/README.md), [tokenek](../../../docs/design/tokens.json) | Arculat és assetforrások, külön licencellenőrzéssel |

Élő helyi olvasási forrás: `ringatoviraggal-local-wordpress-1` konténerben WordPress `get_plugins()`, `get_post_types()`, `get_option(woocommerce_custom_orders_table_enabled)`, `wp_timezone_string()`, `wc_get_products()`, `rest_get_server()->get_namespaces()`; aggregált post státusz/count és event metakulcs-lekérdezés. Titkok és személyes rendelési adatok nem kerültek a dokumentációba.

Vizsgált konténerfájlok: `wp-content/themes/ringatoviraggal/functions.php` (event metabox/regisztráció, SKU completed e-mail, ICS), `page-esemenynaptar.php`, `page-rendezvenyek.php`; `wp-content/plugins/pay-via-barion-for-woocommerce/class-wc-gateway-barion.php` (gateway `supports=['products','refunds']`), plugin PHP-fájlok WCS hook/recurring keresése; helyi mu-plugin. Ezek a Docker kötetben vannak, nem állítjuk, hogy a projektből közvetlenül fájllinkkel elérhetők.

## Elsődleges technikai források

| Téma | Forrás | Milyen döntést támaszt alá |
|---|---|---|
| WP REST auth | [WordPress Authentication](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/) | Cookie+nonce és szerveroldali capability; nincs frontend application password |
| Woo Store API | [Store API](https://developer.woocommerce.com/docs/category/store-api) | Publikus customer-facing API, nem admin rendeléskulcs a kliensbe |
| Woo nonce | [Nonce Tokens](https://developer.woocommerce.com/docs/apis/store-api/nonce-tokens) | Store cart/checkout saját nonce szabály; a WP REST nonce nem ugyanaz |
| Headless kosár | [Cart Tokens](https://developer.woocommerce.com/docs/apis/store-api/cart-tokens) | Alternatív natív headless checkout esetén session/kosár megoldás |
| Subscriptions gateway | [Payment Methods & Gateways](https://woocommerce.com/document/subscriptions/payment-gateways/) | Automatic renewal külön gateway képesség, nem minden Barion pluginból következik |
| WCS gateway fejlesztés | [Integration Guide](https://woocommerce.com/document/subscriptions/develop/payment-gateway-integration/) | Supports, signup/renewal/failure/payment method change implementáció |
| Barion recurring | [Subscriptions setup](https://docs.barion.com/Subscriptions%3A_set_up_recurring_billing) | Merchant engedély és token; kereskedő által indított terhelés |
| Meglévő Barion plugin | [WordPress plugin oldal](https://wordpress.org/plugins/pay-via-barion-for-woocommerce/) | Plugin azonosítása; a helyi 3.10.2 képességeit konkrét helyi kód igazolja |
| Better Messages REST | [REST API](https://www.better-messages.com/rest-api/) | Saját React frontendhez REST és WP user auth; thread permission és hibamodell |
| BM development | [Developer API](https://www.better-messages.com/docs/features/wordpress-api/) | Adapter/integrációs vizsgálat kiindulása |
| React | [React Learn](https://react.dev/learn) | Komponensalapú új UI |
| Vite | [Vite Guide](https://vite.dev/guide/) | React/TS build és backend asset-integráció |
| Router | [React Router declarative install](https://reactrouter.com/start/declarative/installation) | Kliensoldali route fa |
| API state | [TanStack Query overview](https://tanstack.com/query/latest/docs/framework/react/overview) | Szerverállapot és cache invalidáció |
| DTO validáció | [Zod](https://zod.dev/) | Runtime szerződésellenőrzés |
| PWA build | [Vite PWA injectManifest](https://vite-pwa-org.netlify.app/guide/inject-manifest) | Saját push/cache/update SW logika |
| iOS push | [WebKit Web Push](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/) | Home Screen webapp és interakcióból permission, eszközteszt szükségessége |
| PHP push | [web-push-php](https://github.com/web-push-libs/web-push-php) | `minishlink/web-push` Composer könyvtár és környezeti függőségek |
| QR scanner | [nimiq/qr-scanner](https://github.com/nimiq/qr-scanner) | Kamera/dekóder csomagjavaslat |
| Bunny hivatalos WordPress-plugin | [bunny.net – WordPress CDN Plugin](https://wordpress.org/plugins/bunnycdn/) | D10: hivatalos `bunnycdn` plugin azonosítása és kompatibilitás ellenőrzési forrása; a projekt kizárólag Streamet használ |
| Bunny Stream WordPress-integráció | [Gyártói ismertető](https://bunny.net/blog/bunny-stream-now-available-in-our-wordpress-plugin-for-instant-video-embedding/) | Stream feltöltési/kezelési integráció; a Core prémiumjogosultság és a PWA-illesztés külön igazolandó |
| HLS kliens | [hls.js](https://hlsjs.video-dev.org/) | Natív HLS nélküli böngésző lejátszóadapter |

A `/app/` origin, own tables, hold/cursor algoritmus, rövid QR-élettartam, checkout handoff és munkacsomagok **tervezői javaslatok** a helyi rendszer és V1.3 alapján; nem külső forrásból átvett vagy jelenleg működő funkciók. Jogi/consent/retention kérdések felelőssel lezárandó üzleti és adatkezelési feladatok, nem jogi megfelelőségi állítások.
