# 10 – Inkrementális fejlesztési mérföldkövek

**Kötelező tartalomkezelés (2026-10-16):** minden jelenlegi és későbbi PWA-blokk és szerkeszthető szöveg WordPressből, ACF Free mezőkből jön; a közös layoutszövegek és menüikonok is módosíthatók. A blokkok oldalanként csoportosítandók. A React sablon az eredeti megjelenést őrzi. Minden mérföldkő átadási feltétele a WP-szerkesztés build nélküli ellenőrzése. [Részletes szabály és kész-feltételek](12-wordpress-tartalomkezeles.md).

**Készült:** 2026-10-15. **Állapot:** MF01–MF09 implementálva, lokális ellenőrzésre kész (MF05: 2026-10-17); az MF10–MF14 továbbra is tervezett. A fizikai mobilpróba és a távoli manuális telepítés külön igazolandó.

A cél minden lépés végén külön kipróbálható, ellenőrizhető és visszaállítható növekmény. Először a már eldöntött architektúrára épülő feladatok következnek; a nyitott üzleti szabályokat csak az érintett modul előtt kell lezárni. A regisztráció és belépés önálló, korai mérföldkő, a meglévő WordPress/WooCommerce-fiókrendszerre építve.

Az **MF01–MF14 az inkrementális fejlesztés sorrendje**. A 07. dokumentum M0–M10/M8a jelölései megmaradnak munkacsomag-hivatkozásnak; nem azonosak az új mérföldkőszámokkal. Az elfogadott üzleti döntések forrása továbbra is a 09. dokumentum, a teszteké a 07. dokumentum.

## Fejlesztési és telepítési rend – pontosítás, 2026-10-15

**A fejlesztés és a funkcionális, integrációs, regressziós, konkurencia- és eszköztesztek lokális környezeten zajlanak. A tesztszerverre és éles környezetre a kiadás manuális másolással/telepítéssel kerül ki.** Nincs automatikus deploy; egy mérföldkő lokálisan elfogadható távoli hozzáférés nélkül. A kézi telepítés után a telepítő rövid működésellenőrzést végez a célkörnyezeten; ez nem a fejlesztési tesztelés áthelyezése.

Minden mérföldkő kötelező része a [11 – Lokális fejlesztés és kézi telepítés](11-lokalis-fejlesztes-es-manualis-telepites.md) frissítése: mit, hova, milyen sorrendben másolunk, mely plugin/verzió kell, mit kell beállítani, van-e migráció és hogyan állítható vissza a változás. Az útmutatóban most még tervezett csomagútvonalakat az első tényleges builddel kell igazolni. Minden kiadáshoz a műszaki `INSTALL.md` mellett kötelező a közérthető `INSTALL-DOC.md` elkészítése és aktualizálása is, konkrét WordPress-menüpontokkal, fájlmásolási lépésekkel és ellenőrzésekkel; mindkettő a kiadási csomag része.

Tárhelyfüggő tényeket (például streamkapacitás, szervercron és WAF) lokális sikerből nem tekintünk igazoltnak. A célkörnyezeti feltételt az üzemeltető igazolja; ha ehhez külön mérés kell, azt külön feladatként rögzítjük. Ettől a lokális fejlesztés és tesztelés haladhat.

## 1. Mi indítható el?

| Csoport | Mérföldkő | Indíthatóság |
|---|---|---|
| Eldöntött alapok | MF01 PWA-alap; MF02 layout; MF03 Core és session-alap | Nincs nyitott üzleti kérdés. Egymás technikai eredményeire épülnek; MF01 indulhat elsőként. |
| Korai, technikai ellenőrzéssel | MF04 regisztráció/belépés; MF05 olvasó nézetek | Az irány elfogadott; a meglévő WP/WC-folyamatot, adatokat és beállításokat ellenőrizni kell. Ez végrehajtandó feladat, nem általános üzleti stop. |
| Szolgáltatófüggetlen kliens | MF06 lejátszó alap | Saját vagy engedélyezett tesztmédiával elkezdhető; prémium éles stream és tartós személyes preferenciák nélkül. |
| Elfogadott modulszabályokkal fejleszthető | MF07 jegyek/bérletek és staff; MF08 foglalás; MF12 chat; MF13 értesítések | D02–D07 és D11 elfogadva. A technikai előfeltételek teljesülése után fejleszthetők; az integrációs próbák a munka részei. MF12/MF13 éles személyesadat-kezeléséhez a D12 szerint **külső adatkezelői paraméterek és szükséges jogi/üzemeltetési követelmények biztosítása**, **D06 (2026-10-17) szerint nincs szükség előre megadott csoportokra**: Virág WP-adminban maga hozza létre és kezeli őket, WordPress-alapú megoldás előnyben. |
| Lezárt üzleti szabályokkal fejleszthető | MF09 prémium; MF11 szavazás | **D09-MVP/01–03 és D13/01–04 elfogadva, az üzleti döntési kapuk lezárva.** A technikai előfeltételek, termékbeállítások, implementáció és elfogadási tesztek még végrehajtandók. |
| Lezárt szolgáltató- és pluginválasztással fejleszthető | MF10 médiatár | **D10: Bunny Stream + hivatalos `bunnycdn` WordPress-plugin, kizárólag Stream.** A választás lezárt; konfiguráció, Core–PWA illesztés, audio-only próba és védelmi/mobilos/terhelési igazolás még feladat. |
| Teljes V1 átadás | MF14 | Minden kötelező modul, migrációs és kiadási kapu teljesülése után. |

**Konkrét első fejlesztési kör: MF01 → MF02 → MF03 → MF04.** Ennek végén telepíthető, arculatos alkalmazás működik valós regisztrációval, belépéssel és saját fiókazonosítással. Az MF05 adja hozzá az első valós tartalmi nézeteket. Jegy-, foglalási vagy fizetési üzleti döntést ehhez még nem kell előre meghozni.

A „nincs nyitott üzleti kérdés” nem jelent már igazolt tárhelyet, csomagkompatibilitást vagy hibamentes integrációt: ezek ellenőrzése az adott mérföldkő feladata. A feltárt, ténylegesen új termék- vagy scope-kérdést a döntési naplóba kell visszavezetni.

## 2. Fejleszthető mérföldkövek – elfogadott üzleti iránnyal

### MF01 – Projektalap és elkülönített PWA-keret

**Előfeltétel:** jelen terv, D12 elfogadott `/app/` és közös origin iránya. **Nyitott üzleti kapu:** nincs. **Korábbi csomag:** M1, M0 technikai része.

Feladatok:
- Új `ringato-dev/ringato-pwa/` React/TypeScript/Vite alkalmazás; a demó referencia marad. Könyvtárstruktúra, strict TS, lint/build, lockfile és titokmentes konfigurációminta.
- Ringató App Shell plugin: build betöltése csak `/app/` alatt, kliensoldali routing és közvetlen részletoldal-megnyitás. A bootstrap/session az MF03-ban kapcsolódik hozzá.
- Manifest, ikoncsomag, kizárólag `/app/` scope-ú saját service worker; statikus assetlista és offline tájékoztató. A személyes shell és API nem cache-elhető.
- Frissítésjelzés és kontrollált újratöltés; korábbi assetek megtartása, verzióazonosítás, telepítési és rollback-leírás.
- Lokális build-, telepítési és rollback-próba; a manuális tesztszerveres/éles kitelepítés csomagjának, másolási útvonalainak és HTTPS/rewrite/cache követelményeinek dokumentálása.

**Átadandó:** működő üres alkalmazáskeret, telepíthető build és App Shell plugin.

**Kész, ha:** `/app/` és egy mély útvonal frissítéssel is megnyílik; támogatott készüléken telepíthető; hálózat nélkül tájékoztat; a SW nem veszi át a webshop útvonalait és nem tárol privát adatot. Build/lint és T28/T29 ide tartozó része lokálisan sikeres; a lokális telepítés és visszaállítás kipróbált, a kézi kitelepítési útmutató elkészült. A későbbi szerveres telepítés külön jegyzőkönyvet kap.

### MF02 – Arculat, reszponzív layout és közös UI

**Előfeltétel:** MF01. **Nyitott üzleti kapu:** nincs. **Korábbi csomag:** M1 és a későbbi UI-csomagok közös része.

Feladatok:
- A `docs/design` tokenjeinek, fontjainak és ellenőrzött felhasználhatóságú assetjeinek átvétele; önálló app CSS.
- Fejléc, mobil navigáció, tartalomkeret, safe-area és későbbi mini-player helye; tablet/desktop elrendezés.
- Közös gombok, mezők, kártyák, dialógusok, státusz- és hibaelemek, skeleton, üres/offline/tiltott állapot.
- A 06. dokumentum route-vázai, köztük a kötelező szavazás; böngésző Back és deep link. Az adatokra váró modulok egyértelmű fejlesztési állapotot mutatnak, működő vásárlást vagy jogosultságot nem szimulálnak.
- Fókusz, billentyűzet, kontraszt, nagyított betű, reduced motion és érintési célok ellenőrzése.

**Átadandó:** végigjárható, arculatos alkalmazásváz és újrahasználható komponenskészlet.

**Kész, ha:** 320/375/390/430 px-en, tableten, desktopon és fekvő nézetben használható; a navigáció nem takar tartalmat; a közös állapotok bemutathatók. Az eredeti WP-oldal stílusa nem változik. Ez UI-átadás, nem az üres modulok funkcionális elkészülte.

### MF03 – Core plugin, API-kliens és session-alap

**Előfeltétel:** MF01; a layouttól külön is fejleszthető. **Nyitott üzleti kapu:** nincs a körülhatárolt technikai alaphoz. **Korábbi csomag:** M0 API-alap, M1 bootstrap, M2 Core-alap.

Feladatok:
- Ringató Core plugin rétegei, verziózott migrációs keret, capability-kezelés, konfiguráció és diagnosztika.
- A korai végpontok gépi OpenAPI-szerződése, DTO-validáció, typed fetch, közös hibakódok, request ID; csak a most készülő szerződések véglegesítése. A döntésfüggő DTO-k később bővülnek.
- `/config`, minimális saját `/me` és nem-REST `/app/bootstrap.json`; WP session és memóriabeli REST nonce, biztonságos nonce-frissítés.
- React Query sessionhöz kötött kulcsokkal; tulajdonosi ellenőrzés, privát cache-tiltás és kontrollált hiba/retry.
- Modul-feature flag-ek; még el nem készült modul nem szolgáltat kitalált üzleti státuszt. A családmodell és prémiumösszegzés véglegesítése későbbi kapuhoz kötött.

**Átadandó:** valódi WP-backenddel kommunikáló kliens, vendég/session-felismeréssel.

**Kész, ha:** egy meglévő tesztfiók sessionje felismerhető; védett hívás vendégnek tiltott; lejárt nonce kontrolláltan frissül; más fiók adata nem olvasható. Build/lint és célzott auth/API-integrációs ellenőrzés sikeres. Üzleti táblák végleges sémáját még nem rögzíti.

### MF04 – Regisztráció, belépés, jelszó-visszaállítás és kilépés

**Előfeltétel:** MF02 + MF03. **Üzleti irány:** D12 elfogadva; **technikai kapu:** a meglévő WP/WC fiókfolyamat korai próbája. **Korábbi csomag:** M0/M1 fiókkezelés, T01.

Feladatok:
- Először ellenőrizni a WooCommerce My Account, regisztráció és jelszó-visszaállítás beállításait, levélküldését, cookie-jait és az appba visszatérést.
- **Pontosítás (2026-10-16):** vendég felhívások és saját PWA-fiókűrlapok, a meglévő WP/WC natív felhasználó- és jelszóműveletekkel. A felület nem léphet ki az `/app/` scope-ból, új publikus WordPress-oldal vagy globális fiókbeállítás-módosítás nem hozható létre. Visszatérés csak engedélyezett appútvonalra.
- Saját profil minimum: azonosító, név, fiókadatok megtekintése; e-mail/jelszó módosítása az app saját fiókűrlapján, natív WP-validációval. A családadatok a **jóváhagyott D04** alapján egy külön `family_id`-hoz kapcsolódnak az MF07/MF08 üzleti modulokban; az MF04 nem fejleszt két szülős közös családhozzáférést.
- Route guard, sessionlejárat, nonce-os logout, több lap közötti kilépésjelzés és memóriabeli személyes állapot törlése.
- Új, korábban vendégként vásárló személy regisztrálhat; a régi rendeléseit csak a későbbi igazolt D08 folyamat kapcsolhatja hozzá.

**Átadandó:** teljes újfiók → belépés → app → kilépés és elfelejtett jelszó felhasználói út.

**Kész, ha:** lokális tesztfiókkal regisztráció és tesztlevél, jelszó-visszaállítás, hibás belépés, lejárt session, logout és belépés utáni deep link igazolt; az általános webes vendégvásárlás működik. A T01 fiókrésze teljesül; havi prémiumtermék webes vásárlási korlátja az MF09 része.

**Határ:** saját React jelszókezelő backend nem szükséges. Ha a próba nagyobb webes fiókoldal-átalakítást tesz szükségessé, az D01 szerinti külön scope-döntés; a támogatott alapfolyamat az első cél. Éles személyesadat-kezelés előtt a D12 elfogadott projekthatára szerint a megrendelő biztosítja a szükséges adatkezelési és jogi paramétereket; az új GDPR-törlőmotor nem fejlesztési kapu.

### MF05 – Valós katalógus, programlista és saját adatok olvasása

**Előfeltétel:** MF03 + MF04. **Nyitott üzleti kapu:** nincs a már létező adatok szűk olvasó nézeteihez. **Korábbi csomag:** M2 és M5 olvasó részei.

Feladatok:
- WC terméklista/részlet, élő ár és megvásárolhatóság a D01 szerinti egységes kínálattal. Az opcionális „csak webshopban” kivétel egyszerű WC-megoldásának vizsgálata; hiányában nincs új adminrendszer vagy alapértelmezett kizárás.
- Meglévő események olvasó adaptere és listája/részlete; hiányos vagy draft esemény nem jelenik meg kész appeseményként. Foglalható típusok és férőhelyek az MF08-ban véglegesülnek.
- Saját, már fiókhoz tartozó rendeléselőzmény WC CRUD/HPOS használatával. A rendelés fizetettsége nem jelent felhasználható jegyet; vendégrendelés automatikus bekötése nincs.
- Főoldal valós publikus tartalommal és fiókállapottal; a jogosultsági, értesítési és pollblokkok az illetékes modul elkészültekor kapcsolódnak be.
- Keresés/listázás és loading/üres/hiba/offline állapotok; hiányzó tartalom korrekt jelzése.

**Átadandó:** valódi WordPress-adatokkal használható böngészési növekmény.

**Kész, ha:** adminban módosított publikus termék/program a PWA-ban helyesen megjelenik; saját rendelés olvasható, idegen nem; nincs demóadat vagy kitalált QR/foglalási/jogosultsági státusz. T10/T15/T20 releváns olvasó része sikeres.

### MF06 – Szolgáltatófüggetlen lejátszó alap

**Előfeltétel:** MF02 + MF03. **Nyitott üzleti kapu:** nincs az izolált kliensalaphoz. **Korábbi csomag:** M7 kliensrésze.

Feladatok:
- Valódi audio/video elemre épülő controller: play/pause/seek, loading/ended/error/retry, single mód, mini-player és navigációs életciklus.
- Saját vagy engedélyezett tesztfájlok; 16:9/9:16 videó, forgatás, natív fullscreen és visszautasított autoplay kezelése.
- Sorvezérlés kliensállapot-gépe és fel/le/törlés UI tesztadatból; API-/PlaybackGrant-csatlakozási határ. Tartós kedvenc és többeszközös sor az MF10-ben készül.
- Session megszűnésekor stop és forrástörlés; a média nem kerül SW-cache-be.

**Átadandó:** technikailag működő lejátszó demonstrálható tesztmédiával.

**Kész, ha:** single végén megáll; sor végén megáll; a lejátszás és hibaállapotok valódi médiaeseményekből származnak; iOS/Android próba rögzített. Ez a T04–T06 kliensrésze, nem prémium-médiaátadás és nem streamkapacitás-bizonyíték.

### Elfogadott üzleti szabályokkal fejleszthető modulok

**Besorolás frissítve: 2026-10-17.** Az MF07, MF08, MF09, MF11, MF12 és MF13 üzleti szabályai elfogadottak; az MF09 D09-MVP/01–03 és az MF11 D13/01–04 üzleti döntési kapui lezártak. Az alábbi technikai függőségek sorrendet jelentenek, nem új üzleti jóváhagyást. A lokális fejlesztés és tesztelés tesztadatokkal indulhat; a műszaki megfelelőségi próbák, az MF13 kezdeti csoportbeállításai és a D12 éles adatkezelési feltételei továbbra is kötelező átadási kapuk. A besorolás nem változtatja a mérföldkövek tervezett készültségi állapotát.

| Mérföldkő | Előfeltétel és döntési kapu | Feladat és átadandó eredmény | Készültség bizonyítéka | Régi csomag |
|---|---|---|---|---|
| **MF07 – Vásárlási átadás, jegyek/bérletek és staff** | MF04–MF05; **D02, D03, D04 és D07 elfogadva**. D04 már a családhoz kötött jogok sémája előtt szükséges. | Termékszabály-mapping, nem férőhelyes termékek WC checkout-átadása, saját intentstátusz; idempotens fizetett rendeléstétel → jog; jegy/bérlet nézet, lejárat, QR; staff capability, inspect/redeem, audit és kézi korrekció. **D03 szerint a családi jegy, bérlet és külön áras jegy egyazon eseményre történő visszatéréskor nem vonódik le ismételten** (külön áras esemény tényleges vásárlása és foglalása MF08). D05 időablak/foglalás az MF08-cal zárul. | Sandbox siker/hiba, dupla callback és párhuzamos beváltás, dátumhatárok, idegen QR tiltása; **mindhárom jogtípus re-entry esetén korábbi check-in, 0 új levonás**, azonos nap másik eseményre típushelyes korlátok. T11–T14, T20 és T24–T25. | M3 + M5 alap |
| **MF08 – Programtípusok és foglalás** | MF05 + MF07; **D04, D05 és D07 elfogadva**. | Eseménykonfiguráció, nyílt/alapdíjas limitált/fizetős limitált típus; kapacitás, **kezdésig lemondható alapdíjas foglalás**, ICS, **15 perces fizetős hold minden checkoutcsatornán**, késő fizetésnél atomikus kapacitásellenőrzés és `paid_capacity_conflict` kezelése. Staff alap időablak start−2h/end+2h és WP-admin eseményenkénti felülírás; **nincs várólista**. A férőhelyes termék csak e védelem elkészülte után vásárolható. **D03 közös visszatéréslogika a külön áras eseményjegyre is kiterjed.** | Utolsó helyre csak egy siker; **15 perces hold lejárata**, ismételt lemondás és kezdéskori tiltás, késő callback esetén nincs túlfoglalás, web/PWA közös kapacitás; **fizetős eseményjeggyel azonos eseményre visszatérés új beváltás nélkül**, eltérő eseményen tiltás. T15–T19, T24 és eseményes T10. | M4 + M5 eseményrésze |
| **MF09 – Manuális havi prémium-hozzáférés** | MF04 + MF07; **D09-MVP/01–02 elfogadva: 1 helyi naptári hónap a célhelyi nap végéig; előrevásárlás az eredeti fordulónap megtartásával (jan. 31. → febr. 28. → márc. 31.), lejártnál új kezdet; /03 elfogadva: mindig látható PWA lejárat, utolsó 7 nap kiemelve és újravásárlás, nincs automatikus e-mail/push; D07 elfogadva; recurring retry/kártyacsere/lemondás elhalasztva**; aktuális ár és termékmapping rögzítése. D01 szerinti webes fiókélmény felmérése. | Havonta újravásárolható egyszeri WC/Barion termék, mindkét csatornán termékszintű szerveroldali login-korlát; fizetési adaptertől független paid-through; aktív/lejárt státusz, mindig látható pontos PWA-lejárat, az utolsó 7 napban kiemelt figyelmeztetés/újravásárlási CTA; **nincs automatikus lejárati e-mail/push**. | Vendég a prémiumot weben sem veheti meg; más termék vendégként vásárolható; paid/failed/refund, ismételt vásárlás és dupla callback tesztelt. T08–T09 és T01 prémiumrésze. | M6 |
| **MF11 – „Virág kérdezi” szavazás, kötelező V1** | MF04; **D13/01 jóváhagyva:** **2026-10-17-i UX-pontosítás:** egy fiók/poll egy válaszgomb/link közvetlen kattintásával végleges, külön megerősítés nélküli válasz, lezárás után nincs új válasz; **D13/02 elfogadva:** sok, tartósan nyitva hagyható szavazás és aktuális összesített eredmény; **D13/03 elfogadva:** csak Virág WordPress-adminja lát élő eredményaggregátumot, felhasználó válasz után köszönetet lát, PWA-ban nincs eredmény; **D13/04 elfogadva:** kizárólag kézi WordPress nyitás/zárás, határozatlan nyitva tartás, nincs automatikus kérdésértesítés vagy időzített állapotváltás; **D12 projekthatár eldöntve, szükséges adatkezelői paraméterek külső feladatok**. | WP admin kérdés/opció és **kézi** publikálás/zárás, több párhuzamosan és határozatlan ideig nyitott kérdés; nincs automatikus e-mail/push, kérdésütemezés vagy automatikus szavazási cron; saját szavazatmodell és API: dashboardra belépéskor a felhasználó által még meg nem válaszolt, aktuálisan nyitott szavazásokból szerveroldalon egy véletlenszerű kérdés; nem a teljes aktív listát mutató PWA. Aktuális eredményaggregátum kizárólag megfelelő jogosultságú WordPress-adminban; PWA-ban **egyetlen dashboard-kérdésblokk**, közvetlen válaszgombok/linkek; kattintás után sikeres szervermentéskor **ugyanott köszönő üzenet**, új kérdés csak következő dashboard-belépéskor, megfelelő kérdés nélkül **blokk nincs**. | TP01 teljesül: aktív/lezárt, jogosultság, egyediség, párhuzamos kattintás és retry, adminjog, mobilállapotok. | M8a |
| **MF12 – Szülő–Virág üzenetek** | MF04; **D11 elfogadva**; a Better Messages megfelelőségi próba a fejlesztés első feladata. **D12 projektscope eldöntve:** új teljes anonimizálás/export/erase modul nem készül; a meglévő BM/WP folyamat megfelelőségét és a megrendelői adatkezelési döntést élesítés előtt ellenőrizni kell. | BM adapter, kizárólag saját Virág-beszélgetés, aktív képernyőn polling, olvasottság és biztonságos újraküldés. | T23, idegen thread és szülő–szülő küldés tiltása; elveszett válasz nem dupláz; háttérben nincs aktív polling. | M8 chatrésze |
| **MF13 – Push és appbeli értesítéselőzmény** | MF04; **D06 elfogadva**; VAPID/cron/worker próba a fejlesztés része. **Nincs kezdeti csoportlista mint függőség**; WordPress Core Users/user_meta vagy kompatibilis meglévő plugin alkalmasságát ellenőrizni kell, WP role nem célcsoport; **D12 adatkezelési projekthatár elfogadva**, tényleges adatkezelői paraméterek/jogi megfelelőség élesítés előtt biztosítandó, nem fejlesztői jogi szolgáltatás. | WP admin **szabadon létrehozható/átnevezhető csoportok és több csoporttagság/fiók** (preferált WP-alapú megoldással), egyéni/egy vagy több csoport/összes kampány/előnézet/küldés, címzettpillanatkép, fiókonkénti receipt, eszközregisztráció és SW push/deep link. | T21–T22; több eszköz és fiókváltás, denied/unsupported/410, cursorverseny és ismételt küldés kezelése; inbox pushengedély nélkül a jóváhagyott szabály szerint. | M8 pushrésze |

**MF07 és MF08 kiadási határa:** a részben elkészült staff/fizetős eseményfunkció feature flag mögött marad, amíg a foglalási és időablak-feltételek nem teljesülnek. Nem nyitunk meg férőhelyes terméket védetlen webes checkouton sem.

**D09 további döntés (2026-10-16):** az automatikus megújulás sikertelen terhelési retry, kártyacsere, lemondás és kapcsolódó értesítési részletszabályai a később ténylegesen kiválasztott, igazolt és külön költségjóváhagyott kész integrációhoz tartoznak; **nem tartoznak az MF09/MVP feladatba**. Az **MF09 D09-MVP/01 időtartamszabálya már jóváhagyott**: a hiteles fizetés Budapest szerinti helyi napja +1 naptári hónap a célhelyi nap végéig, hónapvégi clamp, `paid_through` következő helyi nap UTC exclusive határ. **A /02 előrevásárlás/összeadás már elfogadva:** az eredeti fordulónapot őrző felhalmozás tranzakciósan, rendeléstételenként egyszer; január 31. → február 28. → március 31., lejárat után új anchor. **D09-MVP/03 is jóváhagyva:** állandó PWA-beli pontos lejárat, az utolsó 7 napban kiemelt figyelmeztetés/újravásárlás, automatikus e-mail vagy push nélkül. Így az MF09 mindhárom D09-MVP üzleti részletszabálya lezárt; a megvalósítás és tesztek, prémiumtermék ár/mapping és a D01 webes fiókélmény ellenőrzése még feladat.

**MF09 nem vár automatikus előfizetésre.** A recurring kész megoldások ár/érték-felmérése külön munka, bevezetésük csak későbbi MF09+ növekmény, igazolt integrációval és megrendelői költségvállalással. Saját fizetési bridge nincs a projektben.

## 3. Lezárt szolgáltatóválasztás: MF10 – Bunny Stream

Az MF10 szolgáltató- és pluginválasztása **lezárt (D10, 2026-10-17)**: Bunny Stream + a hivatalos `bunnycdn` WordPress-plugin, kizárólag Stream funkcióval. Minden más pluginmodul kikapcsolva marad. A teljes modul élesítéséhez a konkrét konfiguráció, a Core-jogosultság és a PWA-lejátszó illesztése, az audio-only próba, valamint a mobilos/védelmi és legfeljebb 30 párhuzamos lejátszós tesztek még szükségesek. Ezek végrehajtási kapuk; új szolgáltatóválasztás nem előfeltétel. Teljes V1-et kötelező modul nélkül nem adunk át.

| Mérföldkő | Előfeltétel és döntési kapu | Feladat és átadandó eredmény | Készültség bizonyítéka | Régi csomag |
|---|---|---|---|---|
| **MF10 – Védett médiatár, prémium lejátszás és preferenciák** | MF05 + MF06; prémiumhoz MF09; **D10 lezárt: Bunny Stream + hivatalos `bunnycdn` plugin, csak Stream**; D12 adatkezelői paraméterek | Stream-only konfiguráció; WordPress-kezelés/Core médiaazonosító/PWA PlaybackGrant; privát forrás és teljes streamvédelem, audio-only próba, kedvencek és verziózott sor. Más pluginmodul nem használható. | T03–T07/T30: jogosulatlan playback és közvetlen forrásmegkerülés tiltása; lejárat/tokenfrissítés/logout, mobilos lejátszás és legfeljebb 30 párhuzamos lejátszó; webshopregresszió; beállítások és tényleges költség dokumentálva | M7 |

### MF14 – Migráció, teljes V1 pilot és éles átadás

**Előfeltétel:** MF01–MF13; **D08 jóváhagyott fokozatos átállás**: megőrzött régi papíros helyszíni beváltási eljárás, kijelölt új digitális termékkör/cutoff, az esetleg átvezetett régi jogok bizonyítása és kettős beváltás kizárása – **a teljes történeti papír- és vendégrendelés-import nem kiadási feltétel**; **D12 fejlesztési scope lezárva; adatkezelői jogi/megőrzési paraméterek biztosítása**; G4 integrációk és G5 regresszió teljesülése. **Korábbi csomag:** M9 + M10.

Két külön átadási ponttal:
1. **MF14a – Lokálisan ellenőrzött kiadásjelölt és telepítőcsomag:** D08 szerint régi papíros helyszíni folyamat és új digitális vásárlások termékenkénti átállásának terve, cutoff, személyzeti ügyintézési eljárás; **csak ténylegesen átvett régi jogosultságoknál** igazolt claim/import dry-run és idempotencia. Bizonytalan régi joghoz nincs aktív QR; teljes történeti import nem szükséges. Összes kötelező T01–T31 és TP01 eredmény, valós teszttartalom, web/shop/e-mail regresszió, backup/rollback és előző kliens/SW kompatibilitás lokálisan dokumentálva. Verziózott csomag, fájllista, pluginlista, konfigurációs eltérések, migrációs és rollback-útmutató mellékelve. A D01/D09 által felülírt eredeti követelményeket az elfogadott döntés szerint értékeljük.
2. **MF14b – Manuális tesztszerveres, majd éles telepítés és átadás:** a telepítő az útmutató alapján kézzel kitelepíti ugyanazt az ellenőrzött kiadást, környezetenkénti beállításokkal; telepítés utáni működésellenőrzés, korlátozott pilot és fokozatos feature flag-ek. A feltárt hibák javítása és tesztje lokálisan történik. Migráció, monitoring, napi egyeztetés, admin/staff oktatás és kiadási jegyzőkönyv szükséges.

**Kész, ha:** a pilot elfogadási feltételei teljesülnek, minden kötelező V1-modul működik, üzemeltetési és incidensfelelősök megnevezve, a visszaállítás kipróbált. A korai növekmények lokális átadása nem jelenti a teljes V1 éles kiadhatóságát.

## 4. Korán elindítandó felmérések

Ezek az MF01-től külön technikai feladatként haladhatnak; nem kell minden eredményüket megvárni a layout kialakításához.

| Felmérés | Elvárt eredmény | Legkésőbb szükséges |
|---|---|---|
| Lokális WP és pluginmásolás, HTTPS/eszközelérés, deploy/rollback; célkörnyezeti követelménylista | Lokálisan kipróbált csomag és telepítési leírás; célkörnyezeti értékek külön kitöltendők | MF01 lokális átadásához; szerverértékek a kézi telepítés előtt |
| WC regisztráció, My Account, resetlevél, app-visszatérés és cookie | Kipróbált ajánlott alapút; esetleges webes többletmunka elkülönítve | MF04 elején |
| HPOS, terméktípusok, meglévő event mezők, webes belépett fiókélmény | Adaptermapping és feltárt adathiányok; checkout/fiók scope tisztázása | MF05; vásárlási rész MF07/MF09 előtt |
| Egyszeri Barion, Billingo, SMTP tesztmód és cron/Action Scheduler | Lokális levélfogó és jobfuttatás; **D07 szerint WooCommerce → Barion → Billingo teljes és részleges refund, téves/dupla refund, közvetlen Barion refund/chargeback egyeztetés** sandboxja; szükség esetén ideiglenes callback-elérés | MF07/MF08/MF09, illetve MF13 előtt |
| D02–D05/D07 elfogadott szabályainak műszaki igazolása | **D02/D03/D04/D05 elfogadva**, család külön `family_id`-val, alapdíjas lemondás kezdésig, 15 perces fizetős hold, start−2h/end+2h eseményenként felülírható beléptetés, várólista nincs; **D07 refund/chargeback jóváhagyva**; a WooCommerce–Barion–Billingo teljes/részleges refund és közvetlen Barion/chargeback egyeztetés technikai próbája nyitott | MF07/MF08 megvalósítása során, elfogadásukig |
| Bunny Stream + hivatalos WordPress-plugin, kizárólag Stream (D10 lezárt) | 800 perc videó + 60 perc audio; 50 felhasználó, 200 óra/hó, max. 30 párhuzamos lejátszó; konfiguráció, audio-only, Core/PWA védelem és célterhelési próba | MF10 megvalósítása során, élesítés előtt |
| Better Messages REST/AJAX, licenc és klienskompatibilitás | Működő izolált próba vagy dokumentált akadály és új döntési igény | MF12 első fejlesztési feladata; elfogadása előtt igazolandó |
| D13 pollrészletek; D06 szabadon kezelhető címzettcsoportok | **D13/01 végleges szavazat, D13/02 sok tartósan nyitott szavazás + fiókonként egy véletlen megválaszolatlan dashboard-kérdés jóváhagyva; D13/03 csak-admin eredmény jóváhagyva; **D13/04 kézi nyitás/zárás és kérdésértesítés nélküli működés elfogadva – D13/01–04 teljesen lezárt****; **D06 csoportkezelés 2026-10-17-én elfogadva: nincs előzetes csoportlista, Virág WordPressben szabadon kezelheti a csoportokat és tagságukat; WP-alapú megoldás előnyben** | MF11 implementáció előtt; MF13 technikai WP-integráció és push-próba során |
| D08 fokozatos átállás és D12 adatkezelés | D08 elfogadva: csak választott új digitális termékkör és igazolt opcionális régi import; papíros jogosultságok elfogadási rendje, cutoff és tájékoztatás tisztázandó. D12: nincs jogi vagy külön GDPR törlés/export motor a fejlesztési scope-ban; saját időablakok WordPressből beállíthatók, adatkezelő által megadott szükséges megőrzési és érintetti eljárások külön feladatok | D08 működési rend MF14 pilot/élesítés előtt; **teljes legacy import nem kiadási kapu**. D12 az éles személyesadat-kezelés előtt |

A terv két külön **D12** jelölést használ. Minden feladatnál ki kell írni, hogy **környezet/fiókkezelés** vagy **adatkezelés/megőrzés**. **Mindkettő projektszintű iránya elfogadott**; az adatkezelői jogi megőrzési/érintetti részletszabályokat a megrendelő külön biztosítja, a környezeti integrációs próbák pedig végrehajtandók.

## 5. Egy mérföldkő lezárásának menete

- Induláskor rögzíteni a konkrét scope-ot, előfeltételeket és az aktuális döntéseket; a technikai feltárás eredményét külön vezetni az üzleti döntéstől.
- A szükséges adatmodell/API, backend, UI és admin együtt alkosson kipróbálható növekményt. Ahol csak kliensalap készül (MF02/MF06), ezt az átadás külön jelzi.
- Átadás: build/plugin verzió, bemutatható felhasználói út, lokális pozitív és negatív teszteredmények, ismert korlátok; frissített telepítési útmutató és verziózott kiadási csomag fájllistával, plugin-/konfigurációs változásokkal és visszaállítási lépésekkel. A célkörnyezetre másolás külön, manuális művelet.
- Az adott mérföldkő ellenőrzése azonnal történjen; az MF14 teljes regresszió, nem az első alkalom az egyes modulok tesztelésére.
- Állapotok: **tervezett → folyamatban → ellenőrzésre kész → elfogadott**; tényleges akadálynál a blokkoló kérdés és az érintett rész megnevezendő. MF01–MF06 állapota **ellenőrzésre kész**, a többi mérföldkőé **tervezett**.

Nem rögzítünk naptári határidőt vagy munkanapbecslést feltárás és kapacitásismeret nélkül. A következő fejlesztési feladatok MF-azonosítóval hivatkozhatók, például: „MF01 megvalósítása”, majd „MF02 megvalósítása”.


## MF01–MF03 implementációs átadás – 2026-10-15

- Forrás a `ringato-dev/` alatt: `ringato-pwa/`, `wordpress-plugins/ringato-app-shell/`, `wordpress-plugins/ringato-core/`, `contracts/openapi.yaml`. A scriptek, tesztek, kiadások és kiadási dokumentáció szintén ide kerültek.
- Komponensverziók: 0.3.0; API 1; schema 1. A pontos buildazonosítót a kiadás `versions.json` fájlja tartalmazza.
- Kiadási és ellenőrzési dokumentáció: [MF01–MF03 kiadás](../../../ringato-dev/docs/releases/mf01-mf03/RELEASE.md), [helyi teszteredmények](../../../ringato-dev/docs/releases/mf01-mf03/local-test-results.md).
- Telepített helyi ellenőrzési cím: `http://localhost:8081/app/`, a fejlesztői WP-klónon. A 8080-as eredeti mentéshez nem nyúltunk.
- MF01: saját Shell, verziózott build/assetek, manifest/PNG ikonok, szűk SW-cache, statikus offline lap, explicit frissítés és kipróbált rollback.
- MF02: önálló arculati CSS, licenccel csomagolt Nunito/Montserrat, minden előírt route váza (köztük polls), közös UI, mobil/desktop layout. A bizonytalan jogú Girly Sunrise/fotók/logó nem kerültek át.
- MF03: rétegzett Core, idempotens schema/capability-keret, admin diagnosztika, korai OpenAPI/DTO/API-kliens, valódi WP-session, nonce-frissítés, sessionhez kötött memóriacache. Nincs üzleti tábla vagy kitalált jogosultságstátusz.
- A készülékes iOS/Android telepítés/safe-area ellenőrzés és a célkörnyezeti HTTPS/rewrite/cache/WAF nem tekinthető lokálisan igazoltnak. Ezért az állapot nem „elfogadott”.


## MF04 implementációs átadás – javított irány, 2026-10-16

- Felhasználói pontosítás: **a teljes fiókfolyamat a PWA-n belül marad**, és az eredeti weboldal működése, oldalai és globális fiókbeállításai nem változhatnak. A korábbi webes átvezetési megoldást a 0.4.1 felváltja.
- PWA/Core/Shell 0.4.1, API 1, schema 1, ACF-tartalom 3. Saját React login/register/forgot/reset/edit a `/app/account/*` útvonalakon; a backend natív WP/WC műveleteket használ, nincs külön jelszótárolás.
- `/app/auth/*` non-REST POST-adapter, same-origin custom header, no CORS/no-store, próbálkozáskorlát. Edithez WP-cookie és nonce; érzékeny adatokhoz jelenlegi jelszó. Resetlevél appba vezet, egyszer használható kulccsal a fragmentben.
- Mélylink-visszatérés, saját profil, route guard, nonce-os logout, több lap szinkronja és memóriacache-törlés. A D08 automatikus vendégrendelés-kapcsolási tiltás csak az app auth-kéréseiben él; az eredeti webes hookokat nem módosítjuk.
- Nincs új publikus WP-oldal vagy WC-regisztrációs opciómódosítás. A korábbi, hibás helyi próbából származó 6630-as `/fiokom/` oldal visszavonhatóan lomtárba került; eredeti opciók visszaállítva, fiókok és rendelések megőrizve.
- Új feliratok: **PWA tartalmak → Profil → Alkalmazáson belüli fiókűrlapok**, ACF Free, build nélkül szerkeszthető.
- [Kiadás](../../../ringato-dev/docs/releases/mf04/RELEASE.md), [tesztek](../../../ringato-dev/docs/releases/mf04/local-test-results.md), [telepítés](../../../ringato-dev/docs/releases/mf04/INSTALL.md). Külső SMTP, HTTPS/Secure cookie, fizikai standalone mobil és D12 adatkezelés továbbra is külön igazolandó.

## MF05 implementációs átadás – 2026-10-17

- PWA/Core/Shell 0.5.0, API 1, DB-schema 1, ACF-tartalom 4. Állapot: **ellenőrzésre kész**; MF06–MF14 tervezett.
- `/app/shop` és termékrészlet: élő WC ár, katalógusláthatóság, készlet/megvásárolhatóság; nincs csatorna szerinti kizárás. Külön „csak webshopban” opciót a WC közös katalógusláthatósága nem biztosít, új adminrendszer nem készült.
- `/app/events` és részlet: a meglévő event mezők adaptere, Budapest szerinti időpont, mai/későbbi napok, hiányos/draft/jelszavas/tiltott program kizárva. ACF Free PWA-láthatóságkapcsoló; hiányában érvényes publikus program engedett.
- `/app/orders` és részlet: saját customer_id alapján, WC CRUD/HPOS. Vendég 401, idegen/guest/nem létező 404; tulajdonosszűrőt a kliens nem küldhet. Nincs automatikus e-mail-kapcsolás, QR, foglalási vagy jogosultsági státusz.
- Főoldal valós publikus előnézetekkel/fiókállapottal; keresés, lapozás és betöltési/üres/hiba/offline állapotok. ACF hozzáadó migráció, üres/szerkesztett értékek megőrzése és build nélküli szövegmódosítás igazolva.
- [Kiadás](../../../ringato-dev/docs/releases/mf05/RELEASE.md), [tesztek](../../../ringato-dev/docs/releases/mf05/local-test-results.md), [telepítés](../../../ringato-dev/docs/releases/mf05/INSTALL.md). T10/T15/T20 szűk olvasó részei teljesültek. Konfigurátor/checkout, ICS/foglalás és digitális jogosultságok későbbi modulfeladatok; célkörnyezeti és fizikai mobilpróba külön igazolandó.

MF05 0.5.1 felületi pontosítás (2026-10-17): a felhasználó kérésére keresőmezők nélkül; dátumjelvényes tömör programsorok a demó felépítésével, részletekbe helyezett leírás/kép, év/hónap szerinti csoportok és hozzáfűző betöltés. Tartalomverzió 5.

## MF06 implementációs átadás – 2026-10-17

PWA/Core/Shell 0.6.0, API 1, schema 1, ACF-tartalom 7. Valódi audio/video tesztfájlok, controller és PlaybackGrant-határ, single/queue állapotgép, mini-player, natív fullscreen, playsInline/contain, navigációs pause és session-stop/forrástörlés. Helyi sor vendégként is kipróbálható; a tartós személyes sor MF10. Nincs streamintegráció vagy prémiumtartalom. ACF Free feliratok a Média részletei MF06 blokkjában, build nélküli szerkesztés. [Kiadás](../../../ringato-dev/docs/releases/mf06/RELEASE.md), [tesztek](../../../ringato-dev/docs/releases/mf06/local-test-results.md), [telepítés](../../../ringato-dev/docs/releases/mf06/INSTALL.md). Állapot: implementált, lokális ellenőrzésre kész; fizikai iOS/Android, standalone, háttér/lockscreen és célkörnyezeti próba még nem igazolt. Az MF06 teljes készülékes elfogadási feltétele ezért nem lezárt.

MF06 0.6.1 felületi pontosítás: WordPressben fájlonként választható borító, play/típusjelző és üres/teli szíves sorhozzáadás; függőleges egér/érintés drag helyjelölővel, billentyűzetes rendezés. ACF 8, adatmegőrző migráció; 28 unit és 14 érintett böngészőteszt sikeres.

MF06 0.6.2 felhasználói UX-pontosítás: nincs mini-player; közvetlen cover-/címnavigáció teljes saját médiaoldalra, X stop sor megőrzésével, audio cover, sor módú Következik blokk és oldalváltó sorfolytatás. ACF 9, 29 unit és 14 lejátszó-böngészőteszt sikeres; fizikai eszközpróba továbbra is külön.

## MF07 implementációs állapot – 2026-10-17

A 0.7.0 helyi növekmény elkészült: biztonságos WC-pénztárátadás és saját intent, explicit termék-cutoff és rendeléstétel-pillanatkép, darabonként idempotens digitális jog, külön family_id, szerveres D02-lejárat, saját wallet/QR/előzmény, D03 közös inspect/redeem és naplózott admin korrekció. A vásárlási és staff modul saját InnoDB táblái schema 2, az oldalankénti ACF Free feliratok tartalom 10.

Az MF07/MF08 kiadási határ érvényes: staff csak local + tesztkapcsoló; nem-local kódban tiltott. Férőhelyes termék nem vásárolható egyik checkoutcsatornán sem, külön eseményjogot a közös motor tesztjében szintetikus adattal ellenőrzünk. D05 kapacitás/foglalás/időablak MF08. T24/T25 foglalási részei későbbi kapuk; teljes éles staff-elfogadást az MF07 nem állít.

Barion sandbox siker/hiba, teljes és részleges gateway refund lokálisan igazolt. Távoli szolgáltatói IPN, Billingo helyesbítés és fizikai mobil még külön ellenőrizendő. [Kiadás](../../../ringato-dev/docs/releases/mf07/RELEASE.md), [telepítés](../../../ringato-dev/docs/releases/mf07/INSTALL.md), [tesztbizonyíték](../../../ringato-dev/docs/releases/mf07/local-test-results.md).

## MF08 implementációs állapot – 2026-10-18

0.8.0: ACF Free programtípus/befejezés/kapacitás/termékmapping és staff időablak; saját inventory/reservation/hold táblák, prefixelt InnoDB, family → inventory → entitlement zársorrend és aktuális zároló olvasások. A programkonfiguráció a meglévő event postmeta mezőkben marad; ACF-mentés inventory-zárban, kapacitás-/szerkezetvédelemmel és audittal. Schema 3, tartalom 13.

Nyílt programon nincs foglalás; alapdíjason foglalás és külön jegy/bérlet; kezdésig lemondás, belépés után tiltás, idempotens helyfelszabadítás. Minden checkoutcsatornán 15 perces fizetős hold; lejárat cron nélkül, késő fizetés kapacitásellenőrzéssel vagy tartós paid_capacity_conflict. Igazolt fel nem használt teljes refund egyszer szabadít helyet. Staff tesztkapcsoló helyett valós esemény/foglalás/időablak és D03 visszatérés. ICS valódi befejezéssel; PWA-feliratok WordPressből.

A korábbi programok explicit besorolása/befejezése telepítési feladat, automatikus besorolás nincs. [Kiadás](../../../ringato-dev/docs/releases/mf08/RELEASE.md), [tesztek](../../../ringato-dev/docs/releases/mf08/local-test-results.md), [telepítés](../../../ringato-dev/docs/releases/mf08/INSTALL.md). A helyi tesztek szintetikus fizetési boundaryt is használnak; távoli HTTPS/IPN, Billingo-helyesbítés és fizikai mobil/naptárimport külön célkörnyezeti kapu marad.

MF08 0.8.1: az eseményoldali ACF Free post_object kereshető listája az egyetlen szerkeszthető termékkapcsolat. A terméken automatikus programnév/időpont/hivatkozás szerepel, fordított ID-mező nincs. A régi eseményoldali kapcsolatok megmaradnak; a terméken lévő régi fordított meta nem jogosultsági vagy kapcsolati forrás. Egy termék két programhoz rendelését szerveroldali validáció és sorosított adminmentés védi.

## MF09 implementáció – 2026-10-18

0.9.0: manuális havi prémium, hiteles fizetéshez és egyedi rendeléstételhez kötött időszaktörténet, eredeti fordulónap, Budapest naptári clamp/DST, késő callback és tranzakciós duplikációvédelem. Mindkét csatornán login, normál vendégvásárlás megőrizve. Saját státusz/pontos lejárat/hét napos kiemelés és újravásárlás; nincs automatikus terhelés/e-mail/push. Lokális teszttermék projektgazdai kérésre 8999 Ft, ID 8503; célkörnyezeti ár/mapping és Barion/Billingo/HTTPS/fizikai mobil külön kapu. Schema 4, tartalom 14. [Kiadás](../../../ringato-dev/docs/releases/mf09/RELEASE.md), [tesztek](../../../ringato-dev/docs/releases/mf09/local-test-results.md).
