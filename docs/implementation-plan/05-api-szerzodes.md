# 05 – Tervezett API-szerződés

**Munkarend (2026-10-15):** a fejlesztés és tesztelés lokálisan történik; tesztszerverre és élesre manuálisan telepítünk, majd rövid működésellenőrzést végzünk. A korábbi staging-tesztre utalásokat e rend szerint kell értelmezni; a tárhelyfüggő kapacitás/cron/WAF külön igazolandó. Minden növekményhez a [11. telepítési útmutató](11-lokalis-fejlesztes-es-manualis-telepites.md) szerint készül csomag és konkrét konfigurációs/másolási leírás.

## 1. Általános szabályok

Ez a **megvalósítandó** Ringató API, nem a jelenlegi WordPress végpontjainak leírása. Base: `/wp-json/ringato/v1`. Az implementáció első munkacsomagjában az alábbi DTO-kból és végpontokból teljes OpenAPI 3.1 dokumentum, Zod schema és typed kliens generálandó; az itt megadott neveket és üzleti szemantikát közös review zárja le.

- JSON UTF-8; minden ID string, dátum ISO8601 UTC, `null` explicit nincs adat. Enum ismeretlen értékét a kliens hibás contractként kezeli. Money: `{amount_minor:"800000", currency:"HUF", minor_unit:2}` példa 8 000 Ft-ra; a szolgáltatott minor_unit alapján formázunk.
- `P` = publikus; `U` = bejelentkezett WP-user+REST nonce+saját objektum; `S` = staff capability+hozzárendelt esemény; `A` = megnevezett admin capability. A frontend route guard nem helyettesíti a szerver permission callbacket.
- Sikeres egyedi válasz `{data: DTO, meta:{request_id,server_time}}`; lista `{data: DTO[], meta:{next_cursor,has_more,request_id,server_time}}`. Kivétel az ICS, raw vendor API és bootstrap.
- Listák `limit` alap 20, max 100; opaque `cursor`, stabil idő+ID rendezés. Search max 120 karakter. Privát adatok `Cache-Control: private,no-store`.
- Mutációkon `X-WP-Nonce`, megfelelő JSON content type, same-origin. Publikus üzleti mutáció nincs; az ingyenes média playback grant POST-ja a végponttáblában jelölt, rate-limitelt kivétel, nem módosít kereskedelmi állapotot.
- `Idempotency-Key` kötelező checkout intent, reservation create/cancel, **csak ha később enabled: recurring subscription cancel**, staff redeem, message send és a **D13 szerinti V1 poll response** esetén. UUID/szűk karakterkészlet, max 128 byte. Ugyanazon user+route+key és request hash replay ugyanazt a status/body-t adja; eltérő body 409. Ajánlott általános replay 24h; kereskedelmi/beváltási unique domain index tartósan megakadályozza a duplikációt.
- Kedvenc PUT/DELETE önmagában idempotens; sorhoz `If-Match: "revision"` szükséges. Cursor mark monoton.
- 200 olvasás/update/replay; 201 új objektum; 202 provisioning/kampányfolyamat elfogadva; 204 body nélküli sikeres törlés; 400 schema, 401 session, 403 jogosultság, 404 saját szűrés után nem elérhető, 409 állapot/kapacitás/verzió, 410 lejárt token, 422 üzleti input, 429 rate limit, 503 átmeneti providerhiba.

WP-kompatibilis hiba:

```json
{"code":"event_full","message":"Nincs több szabad családi hely.","data":{"status":409,"request_id":"req-demo","retryable":false}}
```

A kliens code alapján magyar UX-üzenetet mutat; nem a provider raw hiba-/stack trace szövegét. `Retry-After` 429/503 esetén. Kezdeti rate limit ajánlás: checkout/foglalás 10/perc/user, message send 20/perc/user, staff scan 60/perc/staff; staging terhelés alapján állítandó. WAF/IP limit mellett useralapú limit is szükséges.

## 2. Végpontkatalógus

### Fiók, kezdőlap, katalógus

| Method és útvonal | Auth | Input | Output / hatás |
|---|---|---|---|
| GET `/config` | P | – | api_version, minimum_client_version, features, timezone, public support URL; nincs titok |
| GET `/me` | U | – | UserProfile: id, display_name, email, family (V1: önálló `family_id`, egyetlen WP-fióktulajdonos), capabilities, subscription_summary; D04: nincs többfiókos családtagság |
| PATCH `/me` | U | display_name, family_display_name | Saját megjelenítési adatok; e-mail/jelszó módosítás webes WP/WC folyamat |
| GET `/home` | U | – | next_admission, subscription, featured_media, upcoming_events, unread_count; **V1 P01 aktív poll összefoglaló / link, ha van** |
| GET `/products` | P | cursor, limit, search?, category? | Product[]: alapból ugyanazok az aktív, weben látható és megvásárolható WC-termékek (régi Online Ringató és új app-előfizetés/eseménytermék is); opcionális „csak webshopban” kivétel D01 szerint |
| GET `/products/{id}` | P | – | Product + variations/configurator információ |
| GET `/orders` | U | cursor, limit | Saját OrderSummary[], jogosultságokkal; D08 szerint a korábbi vendégrendelés csak ellenőrzött, opcionális claim után jelenhet meg; e-mail-egyezés alapján automatikusan nem |
| GET `/orders/{id}` | U | – | Saját OrderDetail + WooCommerce-ben igazolt refund/ügyintézési státusz, ha releváns (D07); nem más ügyfél/számla adatai |
| POST `/checkout-intents` | U | product_id, variation_id?, quantity, attributes?; idempotency | CheckoutIntent + egyszeri handoff_url; szerverár és férőhely |
| GET `/checkout-intents/{id}` | U | – | Saját payment_state/provisioning_state/order_id/entitlement_ids; nem token újrakiadás |

**D04 V1 család-/API-határ (2026-10-16):** egy bejelentkezett WordPress-fiók egy külön belső `family_id`-hoz kapcsolódik. A saját `/me`, jegy-, foglalás- és rendelésvégpontok kizárólag a szerveroldalon feloldott tulajdonos/család adatait adják vissza; idegen családazonosítóval nem lehet lekérdezni vagy módosítani őket. Nincs V1 publikus családegyesítés, több szülős tagság, jegyátruházás vagy több család önkiszolgáló checkout API. Manuális kivétel kizárólag korlátozott admin capability, hitelesítés és audit mellett. Későbbi tagsági API-hoz új, külön jóváhagyott szerződés kell.

**D07 API-határ (2026-10-16):** a Ringató nem biztosít ügyféloldali pénzvisszatérítés-végpontot és nem hív közvetlenül Barion refund API-t. A rendelés-/jegystátusz a WooCommerce-ben igazolt pénzügyi visszatérítésből és a Core szerveroldali, rendeléstételre szűkített idempotens jogkorrekciójából ered. A manuálisan vizsgálandó részleges/használt/chargeback esetek csak megfelelő felülvizsgálati státuszként jelenhetnek meg a PWA-ban, személyes pénzügyi részletek szivárgása nélkül. A konkrét adminreview-műveletek jogosultságait implementáció előtt kell szerződésbe foglalni.

A login/logout/reset/regisztráció a meglévő WordPress/WC útvonalakon történik. **D12:** a webshopban jelenleg vendégvásárlás működik és alapból megmarad; a fiókhoz kötött PWA- és havi prémiumtermékhez regisztráció/bejelentkezés szükséges. A prémiumtermék **webes pénztárnál is szerveroldali termékszintű login-korlátot** kap, nem globális guest checkout tiltást. A regisztráció tényleges WooCommerce-beállításai és UX-e stagingben ellenőrizendők. `GET /app/bootstrap.json` a Shell nem-REST útvonala az auth/nonce frissítéséhez. A `/app/checkout-handoff` a Shell szűk, sessionhöz kötött tokenfelhasználó útvonala; nem általános REST/kosár API.

### Programok és belépési jogosultságok

| Method és útvonal | Auth | Input | Output / hatás |
|---|---|---|---|
| GET `/events` | P | from?, to?, type?, cursor, limit | EventSummary[]; legfeljebb 366 napos intervallum |
| GET `/events/{id}` | P | – | EventDetail; logged-in kliens saját foglalását külön `/reservations` alapján kapja |
| GET `/events/{id}/calendar.ics` | P | – | `text/calendar`, UID, UTC idő, escaped leírás; csak publikus program |
| GET `/reservations` | U | event_id?, cursor, limit | Saját confirmed/cancelled/held státuszok |
| POST `/events/{id}/reservations` | U | body `{}`; idempotency | D04/D05: a szerver WP-userhez rendelt family_id-jára egy aktív családi hely; nincs kliens választotta család; csak `reservation` type; teltháznál `event_full`, V1 várólista nincs |
| POST `/reservations/{id}/cancel` | U | body `{}`; idempotency | D05: saját alapdíjas foglalás csak `now < event.starts_at` feltétellel mondható le; pontos kezdéstől tiltás, idempotens felszabadítás; paid jegy refund külön D07 workflow |
| GET `/entitlements` | U | kind?, state?, cursor, limit | Saját jegyek/bérletek aktuális szerverállapota |
| GET `/entitlements/{id}` | U | – | EntitlementDetail, redemption history minimális staff-adattal |
| POST `/entitlements/{id}/qr` | U | body `{}` | QRPayload: opaque payload, expires_at; csak használható saját entitlement |
| GET `/subscription` | U | – | PremiumAccessSummary vagy null; MVP: `mode=manual_monthly`, `paid_through` (D09-MVP/01: Budapest 1 naptári hónap, célhelyi nap végéhez tartozó UTC exclusive határ), `access_active`, `renewal_enabled=false`, újravásárlás; **D09-MVP/02 elfogadva:** előrevásárlás az eredeti havi fordulónaphoz és hónapszámhoz adódik, lejárt hozzáférés új sorozatot indít; **D09-MVP/03 jóváhagyva:** a PWA `paid_through` szerveradatából mindig megjeleníti a pontos helyi lejárati napot és az utolsó 7 napban kiemelt figyelmeztetést, újravásárlási lehetőséggel; automatikus lejárati e-mail/push nincs; később `mode=recurring` |
| POST `/subscription/{id}/cancel-renewal` | U | body `{}`; idempotency | **Nem MVP-route**; csak későbbi recurring feature flag és külön jóváhagyott kész integrációval, annak lemondási szabályainak pontosítása után. MVP manuális vásárlásnál nincs ilyen művelet (feature off) |
| GET `/staff/events` | S | from?, to? | Hozzárendelt/scannelhető programok |
| POST `/staff/checkins/inspect` | S | event_id, qr_payload | D03/D05: read-only eligibility / `already_checked_in`, eredeti belépés ideje; staff event-scope és konfigurált start−2h/end+2h vagy eseményenként módosított check-in időablak ellenőrzése; nincs levonás |
| POST `/staff/checkins/redeem` | S | event_id, qr_payload; idempotency | D03/D05: első beváltás Redemption + entitlement_after, tranzakció és staff időablak újraellenőrzése; ugyanazon eseményre visszatérés semmit nem fogyaszt; időablakon kívül `not_checkin_window` |

### Média és preferenciák

| Method és útvonal | Auth | Input | Output / hatás |
|---|---|---|---|
| GET `/media/categories` | P | – | MediaCategory[] |
| GET `/media` | P | search?, category_id?, type?, cursor, limit | MediaSummary[]; prémium raw source nélkül |
| GET `/media/{id}` | P | – | MediaDetail metadata; premium entitlement nincs publikus cache-ben |
| POST `/media/{id}/playback` | U vagy P ingyenesnél | body `{}` | PlaybackGrant; premium U jogosultság kötelező, ingyenes route is rate-limitelt |
| GET `/favorites` | U | cursor, limit | Kedvenc media DTO-k |
| PUT `/favorites/{media_id}` | U | `{}` | Idempotens kedvenc hozzáadás |
| DELETE `/favorites/{media_id}` | U | – | 204, hiányzónál is idempotens |
| GET `/queue` | U | – | Queue: revision + items + playable állapot |
| PUT `/queue` | U | media_ids[], `If-Match` | Teljes sorcsere max 100 egyedi publikált média; revision+1 |

Publikus metadata nem tartalmaz user-specifikus `is_favorite` vagy `can_play_premium` mezőt; ez a session/entitlement adatokból és privát playback válaszból származik. Így nem kerül egyik user jogosultsága másik cache-elt válaszába.

### Push és üzenetek

| Method és útvonal | Auth | Input | Output / hatás |
|---|---|---|---|
| POST `/push/devices` | U | endpoint, keys:{p256dh,auth}, consent_version | Subscription regisztrálás/frissítés aktuális fiókhoz |
| DELETE `/push/devices/{id}` | U | – | Saját eszköz leválasztás, 204 |
| GET `/notifications` | U | cursor, limit | D06: elmúlt **alapértelmezésben 365 nap** címzett Receipt[]-je, pushengedélytől/kézbesítéstől függetlenül, fiókonként egy; a megjelenítési ablak D12 szerint konfigurálható, **nem adatok fizikai törlése**; previous_seen_cursor, observed_cursor, unread_count |
| POST `/notifications/seen` | U | observed_cursor | Monoton frissítés; csak saját megfigyelt receiptig |
| POST `/notifications/{id}/click` | U | `{}` | Saját receipt click jelzés; idempotens |
| GET `/messages/thread` | U | – | Saját szülő–Virág ThreadSummary |
| GET `/messages/thread/messages` | U | cursor, limit, after_id? | Normalizált Message[] és unread; **D11: aktív chatképernyőn kb. 10 s polling, háttérben leáll és visszatéréskor frissül** |
| POST `/messages/thread/messages` | U | text (1–2000 karakter); idempotency | Saját threadbe plain text küldés; recipientet szerver határozza meg |
| POST `/messages/thread/read` | U | last_message_id | Csak saját thread, monoton olvasási cursor |

**D12 adatkezelési API-scope (2026-10-16):** nincs külön új általános PWA GDPR/export/anonimizálási/tömeges törlési endpoint. A meglévő WordPress/WC/BM képességek és a projekt funkcionális életciklus-műveletei megmaradnak (például saját push eszköz leválasztása). A tényleges adatmegőrzési szabályokat az adatkezelő biztosítja, jogi tanácsadás és a hiányzó integráció külön scope. 

Push endpoint csak valid HTTPS Web Push szolgáltató endpoint: provider allowlist/frissíthető policy, privát/loopback/link-local címek tiltása, redirect/destination ellenőrzés, méretlimit. Backend HTTP-hívásból nem lehet tetszőleges URL-lekérő SSRF. Egy közös böngésző subscription másik fiókra bejelentkezéskor leválasztandó/újrakötendő explicit consenttel, nem küldhet az előző ügyfél tartalmát.

**D13 / P01 – V1 kötelező szavazásvégpontok:**

| Method és útvonal | Auth | Input | Output / hatás |
|---|---|---|---|
| GET `/polls/current` | U | – | Aktuális, publikált szavazás(ok) és a saját szavazati státusz; ha nincs, üres állapot |
| POST `/polls/{id}/responses` | U | `option_id`; idempotency | **D13/01 elfogadva:** PWA a POST előtt megerősítést kér; szerver aktív pollt, opciót, bejelentkezett usert ellenőriz; UNIQUE poll+user. Első sikeres szavazat végleges; azonos idempotens retry nem dupláz, más opcióra újabb POST nem írhatja át; lezárt poll nem fogad új szavazatot |
| GET `/polls/{id}/results` | U | – | Összesített, személyes választ nem tartalmazó eredmény, csak ha az admin eredményláthatósági beállítása engedi |

A WordPress-admin szavazás-/opciókezelése szűk capability-vel és auditálással biztosítandó; ez nem publikus ügyfél-írási végpont. **D13/01 jóváhagyva (2026-10-16): a sikeres szavazat végleges, felhasználói módosító API nincs**, beküldés előtt PWA-megerősítés szükséges. A már szavazott fiók másik opcióra történő új beküldése nem módosíthatja az eredményt; visszatéréskor a szerver által tárolt saját választ mutatjuk. **D13/02–04** még nyitott: egyidejű aktív szavazások, eredményláthatóság és időzítés/értesítés. A V1.3 F01–F26 történeti listájához képest ez **új P01 kötelező API**, nem opcionális.

## 3. DTO-k minimális mezőszerződése

| DTO | Kötelező mezők és szemantika |
|---|---|
| Product | id, type, title, money (nullable configurable árnál), price_label, stock_status, purchasable, purchase_mode (`handoff`,`web_configurator`), permalink, image?, variations[], entitlement_kind? |
| EventDetail | id, title, type (`open`,`reservation`,`paid`), starts_at, ends_at, timezone, venue:{name}, description_text, artwork?, capacity_families (null open), available_families (null open), product_id?, calendar_url, **D05**: waitlist_enabled=false (V1), checkin_from?, checkin_to? (szerveroldali default vagy admin override) |
| Reservation | id, event_id, family_id, units=1, state (`held`,`confirmed`,`cancelled`,`expired`), hold_expires_at?, order_id?, created_at; **D05**: alapdíjas lemondhatóság a kezdési határig, paid hold 15 perc, visszaigazolt kapacitás nélkül nem confirmed |
| Entitlement | id, kind (`family_ticket`,`pass`,`event_ticket`), state (`unactivated`,`active`,`used`,`exhausted`,`expired`,`revoked`,`legacy_review_required`), source_order_id/item_id, purchased_at, expires_at?, event_id?, total_uses, remaining, first_used_at?, used_at?, display_status; **D02:** expiry szerveroldali, bérlet first redeem előtt expires_at=null; **D07:** refund miatti revocation vagy felülvizsgálat/felfüggesztés státusza szerveroldalon jelenik meg, más tétel érintetlen |
| EntitlementDetail | Entitlement + redemption_history:[{id,event_id,redeemed_at,consumed_units}], next_action; nincs nyers QR hash/token |
| OrderSummary | id, created_at, paid_at?, wc_status, total_money, items:[{item_id,product_id,title,quantity,entitlement_ids,provisioning_state}], summary_status |
| PremiumAccessSummary (korábban SubscriptionSummary) | id?, plan_product_id, mode (`manual_monthly`,`recurring`), status, paid_through?, price_money, access_active, renewal_enabled, next_payment_at?, cancellable; MVP `renewal_enabled=false`, `next_payment_at=null`, `cancellable=false` |
| MediaSummary | id, title, type (`audio`,`video`), category_ids[], duration_seconds, premium, artwork?, aspect_ratio (video 16:9/9:16; audio null) |
| PlaybackGrant | media_id, protocol (`audio_file`,`mp4`,`hls`), playback_url, expires_at, refresh_after, subtitles[], authorization_mode (`signed_url`,`signed_cookie`,`provider_token`); nincs provider secret |
| Queue | revision integer, items:[{media_id,position,media,availability}], ETag header; nincs kliensoldali jogosultságengedély |
| Receipt | id,campaign_id,title,body,internal_path,sent_at,is_new,transport_state; nincs csoporttaglista |
| Message | id,thread_id,sender_role (`parent`,`staff`),text,sent_at,read_at?,client_message_id? |
| PollSummary (P01) | id, question, status, options:[{id,label,position}], opens_at?, closes_at?, has_responded, my_option_id?; idegen user választ nem ad vissza |
| PollResults (P01) | poll_id, total_responses, options:[{option_id,count,percentage}]; csak engedélyezett eredményláthatóság mellett |
| CheckoutIntent | id,state (`created`,`handed_off`,`pending_payment`,`paid_processing`,`fulfilled`,`failed`,`expired`,`paid_capacity_conflict`), payment_state, provisioning_state, order_id?, entitlement_ids[], hold_expires_at?; handoff_url csak létrehozáskor |
| Eligibility | eligible,reason_code,family_display_name?,entitlement_summary?,event_id,server_time,revision; read-only tájékoztató |
| Redemption | id,event_id,entitlement_id,redeemed_at,consumed_units,entitlement_after; D03: típusfüggetlen egyedi entitlement+event, visszatérés az eredeti rekordra hivatkozik, nincs új consumed_units |

**D09 (2026-10-16):** nincs MVP-kártyacsere, automatikus terhelés/retry, automatikus renewal-értesítés vagy recurring lemondás API. Ezek a későbbi kiválasztott kész integrációhoz tartozó, külön jóváhagyandó szerződések. **D09-MVP/01 elfogadva:** a hitelesen fizetett új manuális havi időszak Budapest szerinti 1 naptári hónap célhelyi napjának végéig tart, hónapvégi clamp-pel; az API `paid_through` értéke **UTC exclusive** időpont (következő helyi nap 00:00), a felület ezt helyi lejárati napként mutatja. A **D09-MVP/02 elfogadva**: az aktív prémiumhoz megvásárolt hónapok az eredeti helyi havi fordulónapot megtartva összeadódnak, a lejárt hozzáférés új hiteles fizetéssel új sorozatot indít. A forrás rendeléstételek szerveroldali feldolgozása idempotens, több visszaigazolás nem hosszabbíthat kétszer. **A /03 lejárati tájékoztatás elfogadva:** a kliens az aktuális szerver `paid_through` és a `Europe/Budapest` szerinti lejárati nap alapján mindig mutat dátumot, az utolsó 7 napban figyelmeztetést és újravásárlási CTA-t; nincs automatikus e-mail/push. Előrevásárlás után a friss dátum számít, a korábbi figyelmeztetés megszűnik; az API nem kínál reminder-küldési műveletet.

`ends_at` régi eseménynél hiányozhat az adatbázisban; PWA publikálás előtt admin kitöltés kell, nem becsült érték. Számított `state` mindig szerveridőre érvényes; UI határidő elérésekor újratölt.

## 4. Konkrét példák

### Fizetős eseményjegy-vásárlás

```http
POST /wp-json/ringato/v1/checkout-intents
X-WP-Nonce: <session-nonce>
Idempotency-Key: 75bca704-2c17-4c4e-9429-797c0c1b91c5
Content-Type: application/json

{"product_id":"example-event-product","quantity":1}
```

```json
{"data":{"id":"intent-demo","state":"created","payment_state":"unpaid","provisioning_state":"not_started","order_id":null,"entitlement_ids":[],"hold_expires_at":"2026-10-12T20:15:00Z","handoff_url":"/app/checkout-handoff?token=example-opaque-token"},"meta":{"request_id":"req-demo","server_time":"2026-10-12T20:00:00Z"}}
```

A példabeli ID/token nem létező éles adat. Lejárt handoffra 410, elfogyott kapacitásra 409; a frontend nem módosítja a fizetési státuszt.

### Sor konkurens módosítás

```http
PUT /wp-json/ringato/v1/queue
X-WP-Nonce: <session-nonce>
If-Match: "7"
Content-Type: application/json

{"media_ids":["media-a","media-b"]}
```

200 revision=8; ha közben másik eszköz módosított, 409 `queue_revision_conflict`, a kliens lekéri a friss sort és felajánlja az újrarendezést. Nincs néma felülírás.

### Beléptetés

```http
POST /wp-json/ringato/v1/staff/checkins/redeem
X-WP-Nonce: <staff-session-nonce>
Idempotency-Key: b8a6680d-c59a-479b-8441-d3ac2a39b208
Content-Type: application/json

{"event_id":"event-demo","qr_payload":"ringato:v1:example-opaque-token"}
```

201 Redemption; azonos key replay 201 ugyanazzal az ID-val, nem új levonás. **D03:** ugyanazon konkrét eseményre visszatérés mindhárom jogtípusnál `already_checked_in` és az eredeti belépési rekord/időpont alapján ellenőrizhető; másik idempotency key sem készíthet új redemptiónt. Ez **nem új sikeres redeem**. Domain hibák: `ticket_used` (másik eseményen elhasznált egyszeri jegy), `pass_exhausted`, `entitlement_expired`, `entitlement_revoked`, `event_mismatch` (másik eseményre szóló külön áras jegy), `reservation_required`, `not_checkin_window`, `already_checked_in`; 409/422 a lezárt OpenAPI szerint. Másik user saját jegy-végpontjára 404; staff számára a szükséges állapotkód kiadható, PII nélkül.

## 5. Admin API és vendor-határ

V1 admin lehet hagyományos WP-admin form nonce/capability ellenőrzéssel. Az alábbi use case-ek akkor is kötelezők, ha nincs hozzájuk publikus REST végpont:

| Admin művelet | Capability | Validáció / eredmény |
|---|---|---|
| Termékszabály create/update | ringato_manage_events + WC megfelelő product jog | Rule version, audit; meglévő rendelés snapshot nem változik |
| Event PWA-config | ringato_manage_events | Programtípus/kapacitás/product/end; inventory limit |
| Média create/update/publish | ringato_manage_media | Privát forrás, premium, aspect ratio, metadata és tesztstream |
| Csoport create/update/tagok | ringato_manage_groups | Aktív user, duplikációmentes tagság, audit |
| Kampány draft/preview | ringato_manage_push | Egyéni/csoport/all deduplikált címzettek, belső allowlist deep link |
| Kampány send | ringato_manage_push | Explicit admin send, címzettpillanatkép, idempotens outbox; nincs demó PWA-küldés |
| Entitlement adjustment/import (D08, opcionális régi jogátvétel) | ringato_adjust_entitlements | Kötelező bizonyíték, indok, before/after és batch; ismeretlen legacy joghoz nincs aktív QR; az ügyfél nem írhat remaininget; a teljes papírmigráció nem V1-követelmény |
| Audit/reconciliation | ringato_view_audit | Szűrt riport, korlátozott személyes adat |

Ha React admin készül később, ezek `/admin/...` végpontokat kapnak ugyanilyen jogokkal; V1 mobilstaff nem kampányadmin. Barion callbacket a megfelelő gateway kezeli, nem kliens Ringató végpont; Core csak a hitelesített paid/failed eseményt dolgozza fel. Better Messages raw API nincs közvetlenül összekeverve a Ringató DTO-szerződéssel.

## 6. Szerződés lezárása és kompatibilitás

M0-ban minden route request/response és hiba schema OpenAPI-ba; **D11 szerinti ingyenes Better Messages REST/AJAX stagingpróba után** üzenet cursor/idempotencia, kétirányú küldés, read/unread, thread-jogosultság és hiba mapping konkretizálás. A WebSocket nem V1-feltétel, és csak külön költségjóváhagyással válhat integrációvá. Kliens és backend közös fixture-ökkel tesztel. V1 breaking változás új névtér (`v2`); opcionális mező hozzáadható, enum bővítés kezelése contract review. Régi aktív SW/kliens esetén `/config.minimum_client_version` kontrollált frissítést kér; checkout/beléptetés közepén nem indít automatikus reloadot.
