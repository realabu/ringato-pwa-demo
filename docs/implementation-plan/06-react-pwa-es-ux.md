# 06 – React alkalmazás, PWA és UX

## 1. React felépítés

Új alkalmazás külön `ringato-pwa/` könyvtárban (későbbi implementáció); a `ringato-pwa-demo/` változatlan referencia marad. Vite React/TypeScript, strict mode és strict TS, `/app/` base. A demó globális függvényeit és `localStorage`-beli üzleti állapotát nem portoljuk. Modulonként komponens/hook/DTO/service; közös PlayerProvider a navigációk felett.

```text
ringato-pwa/                     # tervezett, még nem létrehozott app
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
wordpress-plugins/              # tervezett saját pluginek
  ringato-core/
  ringato-app-shell/
  # recurring gateway plugin NINCS az MVP-ben; később csak külső kész megoldás
contracts/openapi.yaml          # M0-ban készülő gépi API-szerződés
```

Szerverállapot: React Query, query key user ID/session generációval; logoutkor `queryClient.clear()`. Privát cache nincs persistelve. Player/UI: Context + reducer; audio/video `HTMLMediaElement` objektum state-től külön referenciában. Nincs böngészőállapotból létrehozott `plus=true` vagy remaining számláló.

Kérések: typed fetch + same-origin credentials + nonce; runtime schema, közös error mapping; GET korlátozott retry, mutáció csak idempotens szabály szerint. Entitlement/foglalás/vásárlás után célzott invalidáció: `/home`, wallet, orders, events/reservations, subscription. Backgroundba kerülés után visszatéréskor friss szerverállapot.

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
| `/events/:id` | Részlet, ICS, foglalás/lemondás/vásárlás | 10-open-detail – 14-paid-booked |
| `/shop` | Élő katalógus + app-előfizetés | 15-shop |
| `/subscription` | MVP: havi prémium aktív/lejárt, kifizetett időszak, újravásárlás CTA; **nincs lemondás vagy automatikus megújulás**. Később recurring módhoz feltételes lemondás | 16-subscription, 17-sub-ending (recurring design csak később) |
| `/checkout/:intentId` | Szerver payment/provisioning státusz | Új valós folyamatképernyő |
| `/wallet` | Jegyek, bérletek, rendeléselőzmény | 18-wallet |
| `/wallet/:id` | Érvényesség, QR, beváltási történet | 19-ticket-valid – 22-pass |
| `/orders/:id` | Saját rendeléstétel és kapcsolt jogosultság | 18-wallet részlet |
| `/notifications` | 365 nap, ÚJ, deep link | 25-notifications |
| `/messages` | Saját szülő–Virág szöveges beszélgetés | 27-messages |
| `/profile` | WP fiókadatok, saját beállítások, logout | 28-profile |
| `/staff/checkin` | Eseményválasztás, kamera, inspect, redeem | 23-checkin, 24-ticket-scanned |

A `26-push-admin` demonstrációs kampányfelület véglegesen WP adminban valósul meg; nincs hozzá ügyfél/PWA kampányroute. A modalokból valódi deep-linkelhető részletoldal lesz, böngésző Back kompatibilitással. Home opcionális poll csak P01-scope igen esetén.

Minden adatigényes képernyő: loading skeleton, üres, hálózati hiba+retry, jogosultság/login, offline, success. Vásárlás: pending és paid_processing külön, háttérbe vitt app visszatérésekor frissítés. Staff: „ellenőrzés sikeres” nem azonos a „belépés rögzítve” állapottal.

## 3. Lejátszó és sor

A source valódi `<audio>`/`<video>`, szerver PlaybackGrant alapján. PlayerController állapot: `idle/loading/playing/paused/ended/error`; a médiaelemből `timeupdate`, `durationchange`, `ended`, `error`, `waiting`, `playing`. Nem időzítő szimulálja a zenét.

- Egyedi lejátszás a tárból/kedvencekből: `ended` után megáll, nem folytatja másik elemmel.
- Sor: kijelölt indexről, `ended` után következő; az utolsó után stop. Külön „sor” üzemmód, globális player nem keveri a single/queue indítást.
- Következő prémium elem előtt új playback jogosultság. Tiltáskor a sor megáll és előfizetési ajánlat; nem ugrik át és nem játszik cache-ből.
- Audio play/pause/seek/idő, hiba/retry, kedvenc/sor. Videón ugyanez + natív fullscreen, `playsinline`, `object-fit: contain`, fix source aspect ratio. Nincs képarányváltó.
- iOS natív HLS támogatás először, más böngészőn feature-detect + dinamikusan importált `hls.js`. MP4/audio esetén range request és megfelelő MIME; CDN CORS és token-cookie modell tényleges tesztje.
- Forgatáskor ugyanaz a médiaelem marad, a pozíció és play/pause megmarad. Fullscreen eszközfüggő fallback; a vizuális CSS fullscreen nem jelölhető garantált natív fullscreennek.
- Autoplay a felhasználó korábbi gesztusa után próbálható. `play()` rejection esetén látható Folytatás gomb. iOS background/lockscreen/audio sorfolytatás csak eszközön igazolt támogatásként ígérhető.
- Signed grant TTL például 10 perc, refresh_after 8 perc; szolgáltató és streammodelltől függ. Lejárat/hosszú videó esetén új grant azonos időpozícióval, ha jogosult. Lemondás/expiry után új grant nem jár; már kiadott token hozzáférési maradványa legfeljebb TTL, szigorú azonnali revocationhoz külön providerképesség.
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

Feliratkozást a user explicit gombja indítja; elutasított OS permissiont nem kérjük újra automatikusan. Külön állapot: nem támogatott / telepítés szükséges / még nincs kérve / granted / denied / subscription hibás. Az app kapcsolója nem tudja önmagában visszaállítani a böngésző denied jogát.

iOS/iPadOS Web Push a Home Screenre felvett webappban, iOS/iPadOS 16.4-től jelent meg; tényleges készülék/böngésző követelményt induláskor és kiadáskor ellenőrizni kell. Permission kérés felhasználói interakcióból. [WebKit dokumentáció](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/)

SW push payload: kampány/receipt ID, rövid nem érzékeny cím/szöveg, allowlist `/app/...` deep link. `notificationclick` fókuszálja a meglévő ablakot vagy appablakot nyit; session nélkül login és biztonságos visszatérés. Nincs auth nonce/session token a payloadban. Az inbox szerverről jön, nem a SW notification listájából.

Panelnyitás: előző cursor alapján ÚJ jelzés, lista observed_cursor után seen POST. Inbox pushengedély nélkül is hozzáférhető a jóváhagyott D06 szemantika szerint. Több eszköz egy fiók, egy előzmény; opt-out device leválasztás és operációs kulcstörlés. Marketingcsoporttagság és OS permission két külön fogalom.

## 6. Staff scanner és üzenet UX

Staff először programot választ. HTTPS camera permission, hátsó kamera, `qr-scanner`; stream bezárás navigáció/background esetén. Többszöri dekódolás debounce, sikeres scan után kamera szünet. Inspect minimális család/termék/státusz, majd explicit Beváltás. Response megmutatja a rögzített eventet, időpontot, maradékot. Retry ugyanazzal a műveleti key-vel; offline egyértelmű tiltás. Kamera hibánál manuális opaque kód megadás, ugyanazon szerverjogokkal, nem jogosultságfelülíró gomb.

Üzenet: csak Virág címzett; plain text és szerverkorlát. AJAX polling aktív képernyőn ajánlott 10 s, tab háttérben leáll; visszatéréskor azonnal refresh. Pending send látható, retry azonos client message/idempotency key; vesztes válasznál nincs dupla üzenet. Better Messages adapterpróba zárja a read/unread/cursor pontos viselkedést. WebSocket csak igazolt hivatalos kliens/PWA licenc-kompatibilitás után.

## 7. Design és hozzáférhetőség

A meglévő arculati tokenek a projekt `docs/design` könyvtárából: szín/font/spacing/minták. A PWA önálló stíluscsomag, a teljes theme/vendor CSS nélkül. Asset licencek és valódi cover/thumbnail/alt szövegek ellenőrzése.

Cél: WCAG 2.2 AA elvek szerinti kezelhetőség, billentyűzet és screen reader, legalább 44px kényelmes touch target, látható fókusz, safe-area, hibákhoz szöveges jelzés, `aria-live` beváltási eredmény, reduced motion, megfelelő kontraszt. Dialog focus trap/return focus, sor fel/le gomb accessible label, aktuális tétel jelzés. Szín/lakat önmagában nem magyaráz jogosultságot. Videóhoz megfelelő felirat/átirat tartalmi munkacsomag.

Mobilmátrix: 320/375/390/430 px, tablet/desktop, landscape, nagyított betű, iOS safe-area. Hálózat: lassú 4G, megszakadás, provider timeout, háttérbe tett app. Célzott kezdeti budget: app JS gzip <=250 kB a dinamikus HLS/scanner chunkok nélkül; LCP <=2.5s, INP <=200ms, CLS <=0.1 mérhető tesztprofilban. Ezek tervezési célok, nem most elért mérési eredmények.
