# 06 – React alkalmazás, PWA és UX

**Kötelező tartalomkezelés (2026-10-16):** minden jelenlegi és későbbi PWA-blokk és szerkeszthető szöveg WordPressből, ACF Free mezőkből jön; a közös layoutszövegek és menüikonok is módosíthatók. A blokkok oldalanként csoportosítandók. A React sablon az eredeti megjelenést őrzi. Minden mérföldkő átadási feltétele a WP-szerkesztés build nélküli ellenőrzése. [Részletes szabály és kész-feltételek](12-wordpress-tartalomkezeles.md).

**Munkarend (2026-10-15):** a fejlesztés és tesztelés lokálisan történik; tesztszerverre és élesre manuálisan telepítünk, majd rövid működésellenőrzést végzünk. A korábbi staging-tesztre utalásokat e rend szerint kell értelmezni; a tárhelyfüggő kapacitás/cron/WAF külön igazolandó. Minden növekményhez a [11. telepítési útmutató](11-lokalis-fejlesztes-es-manualis-telepites.md) szerint készül csomag és konkrét konfigurációs/másolási leírás.

## 1. React felépítés

Az MF01–MF03-ban elkészült alkalmazás a `ringato-dev/ringato-pwa/` könyvtárban; a `ringato-pwa-demo/` változatlan referencia marad. Vite React/TypeScript, strict mode és strict TS, `/app/` base. A demó globális függvényeit és `localStorage`-beli üzleti állapotát nem portoljuk. Modulonként komponens/hook/DTO/service; közös PlayerProvider a navigációk felett.

```text
ringato-dev/ringato-pwa/          # MF01–MF03 alkalmazás; a feature-modulok később bővülnek
  src/app/                      # router, providers, shell, auth bootstrap
  src/features/auth/
  src/features/home/
  src/features/media/            # library, favorites, queue, player
  src/features/events/
  src/features/shop/             # catalog, checkout handoff/status
  src/features/wallet/
  src/features/subscription/
  src/features/messages/
  src/features/notifications/
  src/features/staff/
  src/shared/api/                # generated types, fetch, error mapping
  src/shared/ui/                 # form/button/dialog/status/empty-state
  src/shared/design/             # tokens, fonts, CSS Modules
  src/sw.ts
  public/                       # app ikonok, offline.html
  tests/
ringato-dev/wordpress-plugins/  # MF01–MF03 saját pluginek
  ringato-core/
  ringato-app-shell/
  # recurring gateway plugin NINCS az MVP-ben; később csak külső kész megoldás
ringato-dev/contracts/openapi.yaml # MF03 korai gépi API-szerződés
```

Szerverállapot: React Query, query key user ID/session generációval; logoutkor `queryClient.clear()`. Privát cache nincs persistelve. Player/UI: Context + reducer; audio/video `HTMLMediaElement` objektum state-től külön referenciában. Nincs böngészőállapotból létrehozott `plus=true` vagy remaining számláló.

Kérések: typed fetch + same-origin credentials + nonce; runtime schema, közös error mapping; GET korlátozott retry, mutáció csak idempotens szabály szerint. Entitlement/foglalás/vásárlás után célzott invalidáció: `/home`, wallet, orders, events/reservations, subscription. Backgroundba kerülés után visszatéréskor friss szerverállapot.

**D08 elfogadott fokozatos átállás (2026-10-16):** a régi, érvényes papírjegyek/bérletek továbbra is a helyszíni rend szerint használhatók, az alkalmazás nem ígéri, hogy a korábbi papíros vásárlások mind automatikusan láthatók. Az új digitális termékkör a később kijelölt cutoff után a Core-tól kapja a használható jegy- és bérletstátuszt. Régi jog csak ellenőrzött kézi átvétellel jelenhet meg digitális QR-ként; bizonytalan esetben nincs QR és az ügyfél kézi segítséget kérhet. Régi vendégrendelés nem kapcsolható puszta e-mail-egyezéssel. Átállási dátum és ügyféltájékoztatás az indulás előtt egyeztetendő.

**D12 – vendégből regisztrált felhasználó:** a webshop jelenleg fiók nélküli vendégvásárlásra épül; az app publikus felületei vendégként is böngészhetők, de a prémium vásárlás, saját médiák/jegyek/foglalások előtt egyértelmű bejelentkezés/regisztráció felhívás kell a meglévő WP/WooCommerce-fiókfolyamatba. Az éles webes általános vendégvásárlás nem változik; a havi prémium terméket a webes pénztár is csak bejelentkezve engedi. A staging tesztdomaines példány rendelkezésre áll a telepítési és login-visszatérési UX tesztjéhez; a streaming kapacitás ettől külön mérendő (D10).

## 2. Útvonalak és képernyőmegfeleltetés

Minden alábbi útvonal `/app` prefix alatt. Mobil elsődleges nav: Főoldal, Tár, Programok, Vásárlás, Jegyeim, Üzenet, ahogy a demóban; kis szélességen tap-target és szöveg olvashatóság ellenőrzendő. Fejléc: értesítések és profil. Staff route csak capability alapján látható.

| Route | Funkció | Prototípus-képek |
|---|---|---|
| `/` | Lejáró jogosultság, előfizetés, média, program | 01-home |
| `/library` | Keresés, kategóriák, audio/video, paywall | 02-library |
| `/media/:id` | Egyedi audio/video, kedvenc/sorhoz adás | 03-audio, 04-video-landscape, 05-video-portrait |
| `/favorites` | Fiókhoz kötött kedvenc, egyedi lejátszás | 06-favorites |
| `/queue` | Sor lista, fel/le, törlés, tételről indítás | 07-queue, 08-queue-playing |
| `/events` | Három típus, foglalásaim | 09-events |
| `/events/:id` | Részlet, ICS, **D05**: alapdíjas foglalás/kezdésig lemondás, betelt állapot várólista nélkül, fizetős 15 perces helyfenntartás és késői fizetésnél külön státusz | 10-open-detail – 14-paid-booked |
| `/shop` | Élő katalógus + app-előfizetés | 15-shop |
| `/subscription` | MVP: manuális havi prémium aktív/lejárt, kifizetett időszak, újravásárlás CTA; **nincs lemondás, kártyacsere vagy automatikus megújulás**. **D09-MVP/01–02 elfogadva:** a naptári hónapok aktív jogosultságnál az eredeti havi fordulónapot megtartva hozzáadódnak; **D09-MVP/03 elfogadva:** a pontos lejárati nap mindig látszik; az utolsó 7 napban kiemelt figyelmeztetés és újravásárlási CTA van; automatikus lejárati e-mail/push nincs. Később külön recurring integrációhoz feltételes lemondás | 16-subscription, 17-sub-ending (recurring design csak később) |
| `/checkout/:intentId` | Szerver payment/provisioning státusz | Új valós folyamatképernyő |
| `/wallet` | Jegyek, bérletek, rendeléselőzmény | 18-wallet |
| `/wallet/:id` | **D02 szerinti szerver által számolt lejárat**, QR, beváltási történet; bérlet első sikeres használat előtt „még nem indult” | 19-ticket-valid – 22-pass |
| `/orders/:id` | Saját rendeléstétel és kapcsolt jogosultság | 18-wallet részlet |
| `/notifications` | Alapértelmezett 365 napos, konfigurálható megjelenítés, ÚJ, deep link (D06/D12) | 25-notifications |
| `/polls` | **D13/P01 kötelező V1** „Virág kérdezi” – aktív kérdés, válaszopciók, saját szavazati státusz, megengedett összesített eredmény; nincs szavazásnál üres állapot | Prototípus „Virág kérdezi” funkció + új hibás/lezárt képernyők |
| `/messages` | Saját szülő–Virág szöveges beszélgetés | 27-messages |
| `/profile` | WP fiókadatok és D04 szerinti saját család megjelenítése, beállítások, logout; nincs több szülős összekapcsolás vagy átadás V1-ben | 28-profile |
| `/staff/checkin` | Eseményválasztás, kamera, inspect, redeem | 23-checkin, 24-ticket-scanned |

A `26-push-admin` demonstrációs kampányfelület véglegesen WP adminban valósul meg; nincs hozzá ügyfél/PWA kampányroute. A modalokból valódi deep-linkelhető részletoldal lesz, böngésző Back kompatibilitással. **D13 miatt a „Virág kérdezi” szavazás kötelező V1:** a főoldalon aktív poll összefoglalója/hivatkozása, a `/polls` útvonalon bejelentkezett felhasználói szavazás, eredmény csak jóváhagyott láthatósággal; Virág admin oldali kérdés- és opciókezelést kap. Szerver dönt az egyszeriségről, a kliens csak állapotot mutat; szavazat válaszmódosítása részletszabály még nyitott.

**D07 V1 refund-UX (2026-10-16):** az app nem indít Barion-visszatérítést. A WooCommerce adminban kezelt, ellenőrzötten sikeres teljes refundból származó, még fel nem használt érintett jegy/bérlet/hozzáférés „visszavonva” státuszra kerül; fizetős eseménynél a még aktív hely egyszer szabadítható fel. Részleges refund, részben felhasznált jegy/bérlet, többtermékes vagy közvetlen Barion/chargeback helyzet **ügyintézés alatt** státusz, esetleg ideiglenes felfüggesztés; nincs automatikus alkalom-visszaadás és nincs visszavonás más terméknél. A belépési előzmény megmarad; a pénzügyi ügyeket a meglévő WooCommerce-admin vagy feljogosított ügyintéző rendezi. Az állapot minden esetben szerveroldali, nem kliensből kikövetkeztetett.

**D05 V1 program- és fizetési UX (2026-10-16):** a limitált alapdíjas esemény foglalása csak az esemény kezdete előtt mondható le; az app a szerveridő/státusz alapján engedi a gombot, a kezdési határt szerver ellenőrzi. Betelt foglalkozásnál „Megtelt” állapot jelenik meg, **várólistagomb nélkül**. A külön áras esemény webes pénztárra átadásakor a helyfenntartás **15 perc**, de a kliens nem tekintheti automatikusan véglegesnek a helyet vagy a fizetési visszairányítást. Lejárt hold utáni, férőhely nélkül beérkező sikeres fizetésnél `paid_capacity_conflict`: tájékoztatás a kifizetett, de még nem teljesíthető vásárlásról és ügyintézési útvonalról; nem jelenik meg használható jegy vagy megerősített foglalás. A D05 szerinti staff beléptetés start−2h/end+2h alap időablaka WordPress adminban eseményenként módosítható; a UI kizárólag a szerver eredményét mutatja.

**D04 V1 fiók- és család-UX (2026-10-16):** az appban a belépett fiók a hozzá rendelt egyetlen család jegyeit/bérleteit, külön eseményjegyeit, foglalásait látja. Másik szülő önálló WP-fiókjában ezek nem válnak automatikusan láthatóvá; nincs V1 családmeghívó, fiókegyesítés, jegyátadás vagy több család kezelő. A kivételes több családos vásárlás/átadás ügyfélszolgálati megkereséssel, Virág vagy illetékes munkatárs ellenőrzött kézi ügyintézésével történik, nem kliensoldali jogosultságmódosítással. A későbbi bővíthetőséghez a PWA csak a szerver family-model DTO-ját használja, nem feltételezi, hogy family ID = user ID.

**D09 kiegészítés és MVP/01 elfogadva (2026-10-16):** az automatikus előfizetés retry, kártyacsere, lemondás és megújulási figyelmeztetés felületei nem V1-követelmények. Csak későbbi kész, külön jóváhagyott recurring integráció esetén jelenhetnek meg. A manuális havonta megvásárolható prémium **új, aktív időszak nélküli** sikeres fizetésétől egy `Europe/Budapest` szerinti naptári hónap célhelyi napjának végéig érvényes (hónapvégi clamp). A szerver által közölt `paid_through` UTC exclusive határból a UI **helyi lejárati napot** jelenít meg; sem fix +30 napot, sem saját kliensoldali lejáratszámítást nem végez. **D09-MVP/02 elfogadva:** előre megvett hónapok nem vesznek el, a szerver az eredeti havi fordulónapot megőrizve halmozza őket (jan. 31. → febr. 28. → márc. 31.). Lejárat után új vásárlás új időszakot indít; a UI kizárólag a szerver `paid_through` szerinti helyi lejáratot mutatja. **/03 jóváhagyva:** a lejárat napja mindig megjelenik a PWA-ban, az utolsó 7 napban kiemelt (de nem automatikusan kiküldött) figyelmeztetés és „Újravásárlás” művelet látható. A fizetett időszak meghosszabbításakor a PWA a friss `paid_through` alapján újraszámolja a megjelenítendő állapotot, és nem figyelmeztet a korábbi dátumra. Lejárt jogosultságnál lejárt állapot + újravásárlás. Nincs automatikus e-mail vagy push, illetve elkülönült reminder-lista.

**D02 UI-szabály (2026-10-16):** a kliens nem kalkulál fix 3/8 hónapot és nem írja felül a kapott `expires_at` értéket; a WP-terméktípushoz konfigurált szabály szerinti szerverstátuszt és a `Europe/Budapest` helyi lejárati dátumát jeleníti meg. A bérlet `first_used_at` nélkül még nem aktivált, lejárati nap helyett „első beváltáskor indul” feliratot kap; a tényleges érvényességet a szerver ellenőrzi. A speciális eseményjegy és D09 prémium külön szabályt követ.

Minden adatigényes képernyő: loading skeleton, üres, hálózati hiba+retry, jogosultság/login, offline, success. Vásárlás: pending és paid_processing külön, háttérbe vitt app visszatérésekor frissítés. Staff: „ellenőrzés sikeres” nem azonos a „belépés rögzítve” állapottal.

## 3. Lejátszó és sor

A source valódi `<audio>`/`<video>`, szerver PlaybackGrant alapján. PlayerController állapot: `idle/loading/playing/paused/ended/error`; a médiaelemből `timeupdate`, `durationchange`, `ended`, `error`, `waiting`, `playing`. Nem időzítő szimulálja a zenét.

- Egyedi lejátszás a tárból/kedvencekből: `ended` után megáll, nem folytatja másik elemmel.
- Sor: kijelölt indexről, `ended` után következő; az utolsó után stop. Külön „sor” üzemmód, globális player nem keveri a single/queue indítást.
- Következő prémium elem előtt új playback jogosultság. Tiltáskor a sor megáll és előfizetési ajánlat; nem ugrik át és nem játszik cache-ből.
- Audio play/pause/seek/idő, hiba/retry, kedvenc/sor. Videón ugyanez + natív fullscreen, `playsinline`, `object-fit: contain`, fix source aspect ratio. Nincs képarányváltó.
- iOS natív HLS támogatás először, más böngészőn feature-detect + dinamikusan importált `hls.js`. MP4/audio esetén range request és megfelelő MIME; **a D10 során kiválasztandó helyi vagy külső** médiaszolgáltató CORS/range/HLS/token-cookie kompatibilitását valós mobilon tesztelni kell.
- Forgatáskor ugyanaz a médiaelem marad, a pozíció és play/pause megmarad. Fullscreen eszközfüggő fallback; a vizuális CSS fullscreen nem jelölhető garantált natív fullscreennek.
- Autoplay a felhasználó korábbi gesztusa után próbálható. `play()` rejection esetén látható Folytatás gomb. iOS background/lockscreen/audio sorfolytatás csak eszközön igazolt támogatásként ígérhető.
- Signed grant TTL például 10 perc, refresh_after 8 perc; ezek **tervezési példák**, a D10-ben még nyitott médiaszolgáltató biztonságos streammodelljétől függenek. Lejárat/hosszú videó esetén új grant azonos időpozícióval, ha jogosult. Lemondás/expiry után új grant nem jár; már kiadott token hozzáférési maradványa legfeljebb TTL, szigorú azonnali revocationhoz külön providerképesség.
- Navigációkor audio mini-player ajánlott; videó részlet elhagyásakor pause, user újraindítás. Kijelentkezéskor minden lejátszás azonnal leáll, URL/reference törlődik.
- Sor módosítás több eszközről revision lockkal. Lejátszás közbeni rendezéskor aktuális media ID marad, a következő az új sorból; törölt aktuális elem befejezhető, majd stop. Ez UX-pontosítás, tesztelendő.

## 4. Manifest, telepítés, SW és cache

Manifest: stabil app ID `/app/`, start_url `/app/`, scope `/app/`, display `standalone`, magyar név/lang, arculati theme/background szín. Ikon: PNG 192 és 512, külön maskable safe-area ikon, iOS apple-touch-icon 180; a demó egyetlen SVG-je nem teljes végleges ikoncsomag. Telepítési UX böngésző/OS alapján, nem mindenhol létező install prompt feltételezésével.

Vite PWA `injectManifest`, kézzel kontrollált fetch/push/notificationclick/SW-update. [Vite PWA](https://vite-pwa-org.netlify.app/guide/inject-manifest)

**Scope önmagában nem cache-védelem:** a `/app/` által kontrollált lap más útvonalakra küldött fetch kéréseit is láthatja a SW. Ezért URL- és módszer-allowlist szükséges, nem általános fetch cache wrapper.

| Erőforrás | Stratégia |
|---|---|
| `/app/assets/` hash-elt saját JS/CSS/font és statikus appikon | Precache/CacheFirst csak buildlista, saját cacheprefix |
| Statikus, nem személyes `/app/offline.html` | Precache; appnavigáció hálózati hibájának fallbackje |
| `/app/` és SPA route személyes WP shell | NetworkOnly vagy hálózat-first **tárolás nélkül**; hiba offline.html |
| `/app/bootstrap.json`, saját privát `/wp-json/ringato/v1/*`, BM, WC session/order/checkout | NetworkOnly, SW storage tiltott; HTTP private,no-store |
| Publikus media/event/product metadata | V1 NetworkOnly; később külön anonimizált cache opt-in max TTL-lel |
| Prémium stream/manifest/segment/key, QR, push device token | Nincs cache; stream provider szabály szerint hálózat |
| POST/PUT/PATCH/DELETE, fizetés, checkin | Nem cache, nincs Background Sync |
| Régi WP oldal/admin/pénztár | Nem appnavigáció-fallback, nem PWA cache |

Csak `ringato-app-<build>` prefixű saját cache törölhető. Nem más plugin teljes CacheStorage-a. Statikus hash-elt assetek 1 év immutable HTTP cache; SW/manifest frissítést újraellenőrző rövid/no-cache policy. Deploykor az előző build assetei megmaradnak az aktív régi kliensek idejére.

**Frissítés:** új SW waiting állapot + „Új verzió elérhető” prompt. Reload csak user biztonságos műveleti pontján; nincs demóbeli feltétlen skipWaiting/clients.claim. Fizetés vagy beváltás alatt nem indul automatikus újratöltés. API kompatibilitás legalább előző kliensverzióval; rollback SW-szempontból is tesztelendő.

**Offline V1:** telepített keret és tájékoztató működik; nincs checkout, foglalás/lemondás, staff beváltás, QR-frissítés, prémium stream, üzenetküldés. Nincs offline műveletsor. A már betöltött képernyő megjelenhet memóriából „nem friss” jelzéssel, de nem tekintjük bizonyított jogosultságnak. Nyers QR nem kerül tartós offline tárolóba. A személyes állapot teljes offline böngészhetősége későbbi külön scope/adatvédelmi döntés.

## 5. Push és értesítések

D06 elfogadva: az app első megnyitásakor nem kérünk pushengedélyt. A feliratkozást csak a felhasználó explicit gombja indítja; elutasított OS permissiont nem kérjük újra automatikusan. A címzett **alapból 365 napos, WordPressből konfigurálható megjelenítési ablakú** appbeli értesítéslistája push nélkül is látható. **D12:** ez nem fizikai törlési határidő; új GDPR törlés/anonimizálás UI-t nem tervezünk. Külön állapot: nem támogatott / telepítés szükséges / még nincs kérve / granted / denied / subscription hibás. Az app kapcsolója nem tudja önmagában visszaállítani a böngésző denied jogát.

iOS/iPadOS Web Push a Home Screenre felvett webappban, iOS/iPadOS 16.4-től jelent meg; tényleges készülék/böngésző követelményt induláskor és kiadáskor ellenőrizni kell. Permission kérés felhasználói interakcióból. [WebKit dokumentáció](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/)

SW push payload: kampány/receipt ID, rövid nem érzékeny cím/szöveg, allowlist `/app/...` deep link. `notificationclick` fókuszálja a meglévő ablakot vagy appablakot nyit; session nélkül login és biztonságos visszatérés. Nincs auth nonce/session token a payloadban. Az inbox szerverről jön, nem a SW notification listájából.

Panelnyitás: előző cursor alapján ÚJ jelzés, lista observed_cursor után seen POST. Inbox pushengedély nélkül is hozzáférhető a jóváhagyott D06 szemantika szerint. Több eszköz egy fiók, egy előzmény; opt-out device leválasztás és operációs kulcstörlés. Marketingcsoporttagság és OS permission két külön fogalom.

## 6. Staff scanner és üzenet UX

Staff először programot választ. HTTPS camera permission, hátsó kamera, `qr-scanner`; stream bezárás navigáció/background esetén. Többszöri dekódolás debounce, sikeres scan után kamera szünet. Inspect minimális család/termék/státusz, majd explicit Beváltás. Response megmutatja a rögzített eventet, időpontot, maradékot. Retry ugyanazzal a műveleti key-vel; offline egyértelmű tiltás. Kamera hibánál manuális opaque kód megadás, ugyanazon szerverjogokkal, nem jogosultságfelülíró gomb.

**D03 – elfogadott egységes staff UX (2026-10-16):** családi jegy, bérlet és külön áras eseményjegy **első** érvényes beléptetésekor típusnak megfelelő beváltás történik. Ha ugyanaz a család ugyanarra a konkrét foglalkozásra visszatér, a rendszer megmutatja a korábbi belépés időpontját, egyértelmű „már belépett – visszatérés” felirattal; **nincs új levonás, második sikeres beváltás vagy egyéb fogyasztás**. Nem piros hiba, de nem is új sikeres check-in. Másik foglalkozáson ugyanazon nap bérlet új alkalommal használható; az elhasznált egyszeri jegy és más eseményhez tartozó fizetős jegy nem. Az állapotot kizárólag szerveradat alapján mutatjuk.

**D11 jóváhagyott V1 üzenet-UX:** a szülő csak Virágnak írhat plain textet szerverkorláttal; az **ingyenes Better Messages REST/AJAX** integráció az elsődleges, stagingpróba még szükséges. **Kb. 10 s polling csak aktív, látható chatképernyőn**; háttérben/navigálás után leáll, visszatéréskor azonnal frissül. A pending és hibás küldés látható; azonos client message/idempotency key-vel retry nem dupláz. Kétirányú kommunikáció, read/unread és másik ügyfél threadjének tiltása igazolandó. A fizetős WebSocket csak külön bizonyított szükség, kompatibilitási/költségvizsgálat és **megrendelői költségjóváhagyás** után válhat opcióvá, nem V1-kötelező.

## 7. Design és hozzáférhetőség

A meglévő arculati tokenek a projekt `docs/design` könyvtárából: szín/font/spacing/minták. A PWA önálló stíluscsomag, a teljes theme/vendor CSS nélkül. Asset licencek és valódi cover/thumbnail/alt szövegek ellenőrzése.

Cél: WCAG 2.2 AA elvek szerinti kezelhetőség, billentyűzet és screen reader, legalább 44px kényelmes touch target, látható fókusz, safe-area, hibákhoz szöveges jelzés, `aria-live` beváltási eredmény, reduced motion, megfelelő kontraszt. Dialog focus trap/return focus, sor fel/le gomb accessible label, aktuális tétel jelzés. Szín/lakat önmagában nem magyaráz jogosultságot. Videóhoz megfelelő felirat/átirat tartalmi munkacsomag.

Mobilmátrix: 320/375/390/430 px, tablet/desktop, landscape, nagyított betű, iOS safe-area. Hálózat: lassú 4G, megszakadás, provider timeout, háttérbe tett app. Célzott kezdeti budget: app JS gzip <=250 kB a dinamikus HLS/scanner chunkok nélkül; LCP <=2.5s, INP <=200ms, CLS <=0.1 mérhető tesztprofilban. Ezek tervezési célok, nem most elért mérési eredmények.
