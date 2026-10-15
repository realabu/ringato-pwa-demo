# 04 – Adatmodell és üzleti szabályok

## 1. Adatforrások és konvenciók

WP User: egyetlen fiókazonosító. Az MVP-ben WC Product/Variation és Order/Item az eredeti WooCommerce tároló és CRUD; WC Subscription és WCS csak feltételes jövőbeli kész recurring integráció esetén adatforrás. Meglévő `event` CPT/meta: programleírás és időpont. Új `ringato_media` CPT + `ringato_media_category`: médiametadata, WordPress adminnal. Better Messages: üzenet/thread adatforrás. A Core saját táblái az egyedi tranzakciós nyilvántartást tárolják.

Táblanévprefix az aktív `$wpdb->prefix`; nem hardcode-olt `wp_`. Saját táblák InnoDB, utf8mb4. ID `BIGINT UNSIGNED`; az API stringként serializál, JS számkorlát miatt. Időpontok UTC, ISO 8601 `Z` API-formátumban; budapesti üzleti időzóna külön mező. Pénz API-ban egész minor unit string + deviza + minor unit skála, nem lebegőpontos Ft. A kliens sosem számol kereskedelmi összeget.

Közös own-table mezők: `id`, `created_at`, `updated_at`, szükség szerint `version`. Referenciális integritás saját táblák közt ellenőrzött; WP/WC táblákhoz nem adunk idegen kulcsot, mert plugin törlés/frissítés/HPOS más tárolót használhat. Idempotencia és konkurenciabiztonság DB unique indexen/záron, nem csak PHP „ha nincs” ellenőrzésen múlik.

## 2. Táblaterv

A mezők tervezett logikai sémát írnak le. Az implementáció első backendmunkája ebből migráció és géppel ellenőrzött OpenAPI/DTO készítése.

| Tábla | Fő mezők | Kulcs / index / invariáns |
|---|---|---|
| `ringato_families` | user_id, display_name, status | UNIQUE user_id; V1 egy fiók = egy család |
| `ringato_product_rules` | product_id, variation_id (0=base), kind, app_enabled?, event_id?, uses?, validity_months?, rule_version | UNIQUE product_id+variation_id; kind: ordinary/family_ticket/pass/event_ticket/manual_monthly_access/future_recurring; app_enabled csak D01 szerinti egyszerű, indokolt kivétellel; régi Online termékek nem alapból kizártak |
| `ringato_event_config` | event_id, app_enabled, type, end_local?, timezone, capacity_families?, product_id?, checkin_from/to?, cancellation_deadline?, revision | UNIQUE event_id; `open` kapacitás NULL, `paid` product kötelező |
| `ringato_staff_event_access` | staff_user_id, event_id, active | UNIQUE staff+event; capability mellett eseményhatókör; admin globális scope külön explicit beállítás |
| `ringato_event_inventory` | event_id, capacity, confirmed_units, held_units, version | UNIQUE event_id; zárolható sor, 0 <= confirmed+held <= capacity |
| `ringato_reservations` | event_id, family_id, state, units=1, order_item_id?, hold_id?, confirmed_at?, cancelled_at? | UNIQUE event_id+family_id; ugyanazt a sort újrafoglaláskor állítjuk, előzmény auditban |
| `ringato_holds` | event_id, family_id, checkout_intent_id, order_id?, units=1, state, expires_at | UNIQUE intent+event; index event+state+expires_at; aktív családi foglalás mellett új hold tiltott |
| `ringato_checkout_intents` | user_id, product/variation/quantity snapshot, state, token_hash, expires_at, order_id?, provisioning_state | UNIQUE token_hash; index user+created_at; magas entrópia, hash tárolás |
| `ringato_entitlements` | owner_id, family_id, kind, source_order_id, source_item_id, unit_index, product_id, rule_snapshot, purchased_at, expires_at?, event_id?, total_uses, remaining, first_used_at?, used_at?, state, qr_version | UNIQUE source_item_id+unit_index+kind; owner+state+expires_at; egy tétel darabszámonként külön jegy/bérlet |
| `ringato_qr_tokens` | entitlement_id, token_hash, expires_at, revoked_at?, token_version | UNIQUE token_hash; index entitlement; nyers token csak kiállításkor, rövid életű |
| `ringato_redemptions` | entitlement_id, event_id, family_id, staff_id, consumed_units=1, before/after snapshot, redeemed_at, idempotency_id | UNIQUE entitlement_id+event_id (V1 egy belépés/család/program); UNIQUE idempotency_id |
| `ringato_subscription_access` | owner_id, access_source_type (`manual_order` vagy későbbi `recurring`), paid_through, state, source_order_id?, wc_subscription_id?, renewal_enabled? (MVP null/false), revision | Egy hozzáférési állapot/fiók; az MVP-ben hitelesen fizetett egyszeri WC rendeléstételek a források. WCS ID csak későbbi opcionális recurring adapterrel; nincs kötelező WCS-függés |
| `ringato_payment_attempts` (későbbi recurring) | renewal_order_id, gateway, attempt_key, provider_payment_id?, state, amount, currency, last_verified_at | **Nem MVP kötelező**; csak kész recurring integráció bevezetésekor, ha a csatlakozó ezt igényli. Az MVP WC rendelés/idempotens provisioning alapján működik |
| `ringato_favorites` | user_id, media_id, added_at | UNIQUE user+media |
| `ringato_queues` | user_id, revision | UNIQUE user_id; revision optimistic lock |
| `ringato_queue_items` | queue_id, media_id, position | UNIQUE queue+media, UNIQUE queue+position; V1 nincs duplikált média |
| `ringato_push_groups` | title, active, created_by | Admincsoport, nem WP role |
| `ringato_push_memberships` | group_id, user_id, active | UNIQUE group+user |
| `ringato_push_devices` | user_id, endpoint_hash, endpoint, p256dh, auth, state, last_seen_at, consent_at | UNIQUE endpoint_hash; endpoint/keys titkosított vagy erősen korlátozott hozzáférés; logoutkor leválasztás |
| `ringato_push_campaigns` | sender_id, title, body, internal_path, audience_type, audience_spec, state, sent_at?, recipient_count | draft/queued/sending/sent/partial/failed; küldés után tartalom immutábilis |
| `ringato_push_receipts` | campaign_id, user_id, snapshot_title/body/path, sent_at, transport_state, clicked_at? | UNIQUE campaign+user; index user+sent_at+id; 365 napos appelőzmény |
| `ringato_push_deliveries` | receipt_id, device_id, state, attempts, next_attempt_at, provider_result | UNIQUE receipt+device; szolgáltató átvétel nem olvasási bizonyíték |
| `ringato_notification_cursors` | user_id, last_seen_receipt_id, last_panel_opened_at | UNIQUE user; monoton cursor, user több eszközén közös |
| `ringato_polls` (P01 / V1) | id, question, status (`draft`,`open`,`closed`), opens_at?, closes_at?, results_visibility, created_by, created_at, updated_at | Csak publikált, nyitott időablakban szavazható; WordPress-adminjog a szerkesztéshez |
| `ringato_poll_options` (P01 / V1) | id, poll_id, label, position | Pollon belüli opció; a közzétett kérdés opcióinak megváltoztatása szavazatok mellett külön ellenőrzést igényel |
| `ringato_poll_responses` (P01 / V1) | id, poll_id, option_id, user_id, created_at | UNIQUE poll_id+user_id; FK-logikai ellenőrzés: opció ugyanahhoz a pollhoz tartozik; idempotens válaszmentés, lezárt kérdésnél nincs új szavazat |
| `ringato_outbox` | event_key, type, reference_id, payload_minimal, state, attempts, available_at, processed_at? | UNIQUE event_key; replay/reconciliation ugyanazt a domain service-t használja |
| `ringato_idempotency` | user_id, route, key_hash, request_hash, response_status/body, state, expires_at | UNIQUE user+route+key_hash; eltérő body ugyanazzal a kulccsal 409 |
| `ringato_audit` | actor_id, action, target_type/id, reason?, before/after minimal, request_id, happened_at | Append-only üzleti napló; token/üzenet/adatvédelmi titok nélkül |

A push audience snapshot külön recipient lista vagy receipt sorok formájában materializálódik küldéskor; a csoport későbbi módosítása nem változtat egy már elküldött kampány címzettlistáján. Token/body titkok nem kerülhetnek általános debug logba.

**D13 elfogadva (2026-10-15): P01 V1 kötelező.** A fenti három szavazástábla az első verzió adatmodelljének része. A szerver a szavazat rögzítésekor felhasználói azonosítót a hitelesített sessionből veszi, ellenőrzi a szavazás állapotát/időablakát és hogy az opció valóban a pollhoz tartozik; UNIQUE (poll_id,user_id) és tranzakció védi a párhuzamos beküldést. Más felhasználó egyedi szavazata az ügyfél-API-ból nem olvasható. Az összesítés csak jóváhagyott eredményláthatósággal kerül az appba. A szavazat módosítása, aktív szavazások száma és eredmények pontos láthatósága **nem végleges üzleti döntés**, a fejlesztés előtt tisztázandó. A szavazatok megőrzési/exportálási szabályai a külön D12 adatkezelési kérdéshez tartoznak.

## 3. Programadatok és kapacitás

| Régi WP mező | PWA DTO | Szabály |
|---|---|---|
| post ID / title | id / title | Csak publish, app_enabled |
| `_event_date` + `_event_time` | starts_at + timezone | Europe/Budapest lokális adat → UTC, hibás/hiányos idő karantén, nem kitalált időpont |
| `_event_venue` | venue.name | V1 szöveg; helyszín-ID csak későbbi normalizálás |
| `_event_short_desc` | description_text / description_html? | HTML csak WP allowlist és frontend sanitization mellett; alapértelmezett plain text |
| `_thumbnail_id` | artwork | Publikus kép; licenc/alt ellenőrzés |
| `event_category` | categories | Meglévő taxonómia; kategória nem automatikusan kapacitás/típus |
| Saját event config | type/end/capacity/product_id | Admin kitöltés/validáció; régiből nem következtetünk fizetős/foglalós típusra |

Egy `event` ID V1-ben **egy konkrét időpont**, nem teljes ismétlődő sorozat. Az egyes alkalmaknak saját ID/kapacitás/beváltás van. Minden régi esemény alapból `app_enabled=false`, amíg időadat és besorolás nincs ellenőrizve; a webes naptár ettől nem változik.

- `open`: nincs foglalás; érvényes családi jegy/bérlet elég.
- `reservation`: 1 család = 1 hely; aktív saját foglalás **és** érvényes családi jegy/bérlet kell.
- `paid`: pontosan az adott eseményre érvényes külön jegy és fizetett foglalás kell; családi jegy/bérlet nem jó.

Ajánlott V1 családmodell: egy WP ügyfélfiók egy család. Családtagok száma nem kapacitásegység; gyermeknevet/születési adatot nem szükséges gyűjteni. Két külön fiók ugyanazon családhoz automatikusan nem kapcsolódik. Több család egy vásárlásban, jegyátadás, összevont fiók üzleti döntést igényel.

### Foglalás tranzakció

1. Session/család/esemény/type/határidő validáció.
2. BEGIN; inventory sor `SELECT ... FOR UPDATE`; lejárt holdok rendezése ugyanebben a zárban.
3. Meglévő event+family aktív reservation/hold ellenőrzése. Duplikált foglalás visszaadja a meglévő állapotot.
4. Ha nincs férőhely: rollback, 409 `event_full`. Ha van: reservation/hold és counter együtt frissítése.
5. Audit/outbox INSERT, COMMIT. Utána külső kommunikáció/jobs.

Lemondás csak valóban aktív foglalásra szabadít egy helyet; ismételt lemondás nem növeli újra a countert. Az inventory counter helyreállítható a reservation/hold sorokból, és rendszeresen egyeztetendő. Kapacitás csökkentése nem mehet az aktív confirmed+hold alá. Publikált esemény időpont-/ár-/termékmódosítása meglévő foglalás esetén admin figyelmeztetést és auditot igényel.

## 4. Jegy és bérlet

### Családi jegy

`pending_payment → active → used | expired | revoked`. A pending rendelésből még nincs beváltható entitlement. `purchased_at` ajánlottan a **hitelesen sikeres fizetés** időpontja, nem order creation. Egy jegy globálisan egyszer használható, bármely nem külön áras alkalmon. Felhasznált/lejárt/visszavont jegy nem állítható vissza ügyfélkéréssel.

### Bérlet

`unactivated (remaining=8) → active (first_used_at) → exhausted | expired | revoked`. Első **sikeres tranzakcióban** levonáskor rögzül `first_used_at`, és egyszer számolódik `expires_at`. Előzetes QR-megtekintés/ellenőrzés nem aktivál. Több külön megvásárolt bérlet külön entitlement, nem összemosott összeg; user látja az összeset.

### Külön eseményjegy

`pending_payment → active_for_event → used | expired | revoked`. Fizetéskor ugyanabban a provisioning folyamatban létrejön jegy és reservation. A konfigurált beléptetési időablak végén lejár; a staff időablak ajánlott start−2h és end+2h, de eseményenként adminbeállítás és lezárandó üzleti döntés. Téves eseményre mindig tiltás.

### Naptári hónapok – ajánlott pontosítás

Budapesti helyi dátumhoz 3 vagy 8 naptári hónap hozzáadása, hónap végén az utolsó létező napra clamp; az év/DST kezelés timezone libraryvel. Ajánlott lejárat: a célhelyi nap **végéig**, adatbázisban exclusive `expires_at` a következő helyi nap 00:00 UTC-re konvertálva. Érvényes, ha szerver `now < expires_at`.

Példa: január 31-i vásárlás → április 30. nap végéig; augusztus 31-i első bérletbeváltás → következő április 30. végéig. A demó délre állítja a dátumot, ezt nem tekintjük elfogadott üzleti határidőnek. Az időpont vs nap vége és a paid_at fogalma D02-ben jóváhagyandó.

Főoldali választás: nem használt, nem refundált, még érvényes családi jegyek és remaining>0 aktív/unactivated bérletek. Első használat nélküli bérlet `expires_at=NULL`, végtelennek rendezve. Korábbi expiry előre, holtversenyben purchased_at, majd ID. Külön eseményjegy nem helyettesíti ezt a kártyát; külön eseményblokkon jelenik meg.

## 5. QR-ellenőrzés és atomikus beléptetés

V1 ajánlott QR: backend által kiadott, 256 bites random opaque token, token hash tárolás, 5 perces lejárat, entitlement/owner/token_version kötés. QR payload verzióprefix + token; nincs személyes adat. Online wallet frissíti; screenshot nem bizonyít tulajdonjogot, rövid lejárat mérsékli újrafelhasználását. Offline QR-beváltás nincs.

Két művelet: **inspect** (read-only, staff + esemény scope) és **redeem** (explicit staff megerősítés, idempotencia). Inspect eredménye nem garantálja, hogy egy másik staff addig nem váltotta be; redeem újraellenőriz.

Tranzakció: esemény/inventory, reservation, entitlement konzisztens zárolási sorrendben; token ellenőrzés; program/type/időablak; limitáltnál saját family reservation; aktív/remaining állapot. Jegy `used_at IS NULL` feltételes update; bérlet `remaining > 0` feltételes decrement és első aktiválás; redemption unique index + audit; COMMIT. Külső HTTP nincs a zár alatt.

Ajánlott invariáns: egy entitlement egy konkrét eseményen csak egyszer váltható be. Ez a bérlet dupla scan ellen véd, de új eseményen új alkalom vonható. Ha ugyanazon alkalmon újra belépés szükséges, read-only „már belépett” ellenőrzés történik, nem új levonás. A napi/alkalmankénti szabály D03 döntés.

Két staff párhuzamos redeem: egyik nyer, másik már felhasznált / már belépett választ kap. Azonos idempotency key retry pontosan ugyanazt a sikeres választ adja. Másik key nem vonhat újra. Admin korrekció csak külön capability, indok, append-only napló; az eredeti audit nem törölhető. Jegy újrakiadás külön entitlement/művelet, nem történet nélküli visszaállítás.

## 6. Rendeléstétel, visszatérítés és előfizetés

A termékszabály snapshot az **order itemhez** kötött: későbbi admin mapping-/termékátnevezés nem változtatja a régi jegyet. `quantity=n` családi jegy/bérlet n entitlement; event ticket V1 max 1/family/event, subscription max 1 aktív/user. Mixed cartnál minden tétel külön processed.

Fizetési input: `woocommerce_payment_complete` és szükséges állapotváltás trigger; mind közös idempotens service-be kerül. Manuális „completed” státusz önmagában nem hiteles gateway-fizetés; készpénz/kézi jóváhagyás külön admin action audit indokkal. Forrás paid-at/order meta és gateway-egyeztetés. UNIQUE source_item+unit+kind kizárja a dupla kiállítást. Failed/cancelled/pending/on-hold nem állít ki automatikusan digitális belépést.

Refund: teljes visszatérítés visszavonja a még használható kapcsolt jogot és külön eseménynél felszabadítja a helyet. Részleges refund item/quantity alapján kezelendő; összeg nélküli/mennyiség nélküli arányos refund nem mappelhető automatikusan, admin review. Már beváltott jog és kapacitásváltozás külön auditált üzleti kivétel; nem generálunk automatikusan új alkalmat. Chargeback hozzáférés-revocation és staff ügyintézés. Ezek D07-ben pontosítandók.

D09 MVP: a `ringato_subscription_access` a **manuálisan újravásárolt havi prémium-hozzáférést** is tárolja, bár nincs WooCommerce Subscriptions rekord. A sikeresen kifizetett WC rendeléstétel azonosítható forrása a hozzáférési időszaknak; az ismételt callback nem hosszabbítja meg kétszer. Hozzáférés csak `now < paid_through` esetén. Havi időszak, előrevásárlás, átfedés és lejárati értesítés részletszabályai még jóváhagyandók; nincs önkényes, kliensoldali +30 nap. Az ügyfél maga vásárol új időszakot, **nincs automatikus renewal, subscription cancel vagy fizetési token**. Refund/chargeback a jóváhagyott szabály szerint módosíthatja a hozzáférést.

Későbbi recurring adapter (kizárólag külön jóváhagyott kész szolgáltatással): sikeres kezdeti/renewal fizetésekből ugyanebbe a fiókalapú `paid_through` nézetbe vezetjük át a jogosultságot, a meglévő manuális időszak megőrzésével és ütközés/átfedés kezelésével. WCS/egyéb kész rendszer a recurring ütemezés és lemondás forrása, nem az app; sikertelen megújítás nem ad plusz hozzáférést.

WooCommerce és own tables nem egy végtelen, külső API-t tartalmazó DB-tranzakció. Hiteles WC paid event után outbox/retry, event capacity + entitlement saját tranzakciója, majd processed jelzés. Crash utáni reconciliation ugyanazokat a unique key-ket használja; az app `paid_processing` állapotot mutat, amíg minden domainírás kész.

## 7. Push és üzenet adatszabályok

Kampány előzmény: egy receipt fiókonként, akkor is, ha az adott fiók pushengedély nélkül csak az appban látja. Ajánlott értelmezés: az admin által címzett és publikált appértesítés kerül az előzménybe, device kézbesítés külön státusz. Ez a „kapott push” szóhasználat D06-ban lezárandó.

ÚJ: receipt ID nagyobb, mint előző panelcursor. Lista első lekérése visszaadja snapshot `observed_cursor`; panel megnyitás visszaigazolása csak eddig a cursorig frissít. Közben érkező új értesítés nem válik tévesen olvasottá. Last panel opened timestamp is tárolandó, de rendezés/cursor szerver ID alapján.

365 nap a receipt `sent_at` szerveridejétől; lista és napi retention job ugyanazt a szabályt követi. 404/410 push endpoint törlés/inaktiválás, 429/5xx korlátozott backoff, több eszköz nem ad több inbox sort. `delivered_at` csak bizonyított provider állapot, nem kitalált érték; kattintás sem teljes olvasási bizonyíték.

**D11 (2026-10-16):** a V1-chat elsődleges adatforrása a **Better Messages ingyenes** integrációja, amennyiben a staging megfelelőségi próba bizonyítja a funkciókat és az engedélyezett API-hozzáférést. A WP userből saját szülő–Virág threadhez kapcsolunk; résztvevőellenőrzés minden olvasás/írás előtt, a kliens által beküldött thread ID nem jogosultsági forrás. Plain text, limitált hossz, nincs attachment vagy user-user chat. **Kb. 10 s polling csak aktív chatképernyőn, háttérben leáll; visszatéréskor azonnali frissítés.** Az ismételt kérés nem okozhat kettős üzenetet; BM raw response domain DTO-ra normalizálva, HTTP 200-nál jelzett üzleti hibát is ellenőrizve. Fizetős WebSocket nincs az MVP függőségei között; csak külön indoklás és jóváhagyott költség esetén.

## 8. Migráció és személyes adatok

1. Staging backup; forrás- és HPOS read-only export/aggregáció, nem éles írás.
2. Termékszabályok admin felvitele és review; régi/Online kombinált termékek külön osztály.
3. Esemény időadat/típus/end/capacity besorolás; hiányzó adat nem publikus appesemény.
4. **D12 megerősítés:** a jelenlegi webshopvásárlók fiók nélkül, vendégként rendelnek; a globális vendégvásárlás megőrzendő. A jövőbeli fiókhoz kötött app-/prémiumtermék-vásárlásokhoz WP-regisztráció és bejelentkezés kell. A történeti guest rendelés **nem automatikusan e-mail-egyezéssel** saját rendelés. Igazolt claim vagy staff hozzárendelés auditálva; a D08 átvezetési szabályai később döntendők el.
5. Papírbérletek/korábbi jegyek használatának leltára: maradék, első használat, régi beváltás, lejárat. Ha nem bizonyítható, `legacy_review_required`, nincs aktív QR. Új vásárlások egy kijelölt élesítési cutoff után automatikusak.
6. Dry-run riport (darabszám, kihagyás, konfliktus), jóváhagyott valós import batch ID-val. UNIQUE source-item kulcs miatt ismételhető; kontrollcsoporttal egyeztetés.
7. Core táblák schema verziója WP optionben, expand/contract migráció. Plugin deactivate/uninstall alapból nem törli a kereskedelmi és audit adatot.

Adatminimalizálás: push endpoint/keys korlátozottan kezelendők; chat és családadat privát. Profil export/erase integráció kell WP adatvédelmi eszközeivel és BM-mel. Üzenet/audit/order külön megőrzési szabályt kap; a 365 nap csak a push appelőzményre megadott termékszabály. A pénzügyi/audit adatmegőrzés és consent szöveg adatkezelési felelőssel jóváhagyandó, ez a dokumentum nem határoz meg jogszabályi megőrzési időt.
