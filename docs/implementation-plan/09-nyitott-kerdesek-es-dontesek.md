## Munkarendi pontosítás – 2026-10-15

A fejlesztés és a tesztek **lokális környezeten** zajlanak; a tesztszerverre és élesre **manuálisan telepítünk**. A lenti, korábbi D12 és más döntések staging-tesztre utaló feladatait a [10. mérföldkőterv](10-inkrementalis-merfoldkovek.md) és a [11. telepítési útmutató](11-lokalis-fejlesztes-es-manualis-telepites.md) szerint hajtjuk végre: lokális teszt, verziózott csomag és kézi kitelepítés, majd rövid célkörnyezeti működésellenőrzés. A szerverfüggő streamkapacitás, cron és WAF igazolása továbbra is nyitott üzemeltetési feltétel. Ez munkarendi pontosítás, a nyitott üzleti részletszabályokat nem zárja le.

**1. Az érdemi implementálás elején eldöntendő kérdések**

**D01 – Termékkínálat – ELFOGADOTT ÜZLETI DÖNTÉS (2026. október 15.)**

Eredeti kérdés: A régi Online Ringató termékek csak az appból tűnnek el, vagy a webshopból is? Hol jelenjenek meg az új előfizetés- és eseménytermékek?

**Döntés: Egységes WooCommerce-termékkínálat a webshopban és a PWA-ban.**

- Alapértelmezésben minden, a webshopban nyilvánosan látható és megvásárolható WooCommerce-termék az alkalmazásban is látszik és megvásárolható, beleértve az új előfizetés- és eseménytermékeket. Nem feltételezzük, hogy minden vásárló használja az alkalmazást.
- A korábbi Online Ringató termékek (RINGI04/05/06) egyelőre megmaradhatnak és mindkét felületen értékesíthetők. E termékek korábbi jogosultsági logikáját külön kell kezelni; megvásárlásuk önmagában nem adja meg az új PWA-előfizetés jogosultságait.
- Opcionálisan legyen egyszerű „csak webshopban” kivétel, **de csak ha meglévő, alap WooCommerce termékbeállítással (például címkével vagy kategóriával) és egyszerű PWA-szűréssel megoldható**. Nem indokolt ehhez új, összetett termékadminisztrációt építeni. Az elérhető natív beállítás és a pontos szűrés technikai ellenőrzést igényel.
- Az új app-előfizetés a webes webshopban is megvásárolható legyen, **kizárólag bejelentkezett felhasználó által**. A webes és az appos vásárlás ugyanahhoz a WordPress/WooCommerce-fiókhoz, ugyanazon előfizetési és hozzáférési logikához kapcsolódjon; a vendégként történő webes előfizetés-vásárlást szerveroldalon meg kell akadályozni.
- Meg kell vizsgálni, mit lát és hogyan tudja kezelni előfizetését a belépett vásárló a meglévő weboldalon (fiókoldal, vásárlás, előfizetési státusz és lemondás). Ez **feltárási és egyeztetési feladat**; a meglévő weboldal felhasználói felületének esetleg szükséges átalakítása **nem automatikusan része a PWA-projektnek**. Az ilyen webes munkát a jelenlegi webmester végezheti, vagy külön ajánlat és jóváhagyás után készülhet el.

**Hatás a tervre:** az eredeti, RINGI04/05/06 kizárását és az új apptermékek webes elrejtését javasló megoldás elvetve. Az F10 szerinti egységes katalógus az irányadó; a V1.3 specifikáció F26-os „új Online Ringató értékesítés kizárása” kitétele ennél a pontnál az új üzleti döntéssel felülírt, a specifikáció következő kiadásában átvezetendő. A D01/G1 döntési kapu üzletileg lezárt; a webes előfizetés vásárlási és fiókkezelési ellenőrzése, valamint az opcionális kivétel technikai vizsgálata végrehajtandó.

**D09 – Havi prémium-hozzáférés és későbbi automatikus megújulás – ELFOGADOTT IRÁNY (2026. október 15.)**

Eredeti kérdés: Milyen Barion–WooCommerce Subscriptions megoldással biztosítható az automatikus megújulás, ki fizeti a licencet és milyen fizetési jogosultság kell?

**Üzleti döntés:**

- Az **MVP-t a meglévő WooCommerce + Barion egyszeri fizetésére épülő, havonta újra megvásárolható prémium-hozzáféréssel** tervezzük. Nem történik automatikus havi terhelés; az ügyfél maga vásárolja meg a következő időszakot. A hozzáférést a hitelesen kifizetett rendelésből, szerveroldalon számítjuk és kezeljük. Weben és PWA-ban is vásárolható, csak bejelentkezve (D01).
- **Saját Barion recurring gateway/bridge vagy egyedi ismétlődő fizetési rendszer fejlesztése nincs benne a jelenlegi projektkeretben, és nem MVP-feltétel.** Ha nem találunk vállalható kész megoldást, az MVP és a további működés is maradhat havi manuális vásárlású.
- Fel kell térképezni a **legjobb ár/érték arányú, bizonyíthatóan kompatibilis kész megoldásokat**, a konkrét WooCommerce/Barion környezet és szükség esetén más kész fizetési integráció figyelembevételével. A felmérés tartalmazza: kezdeti/licenc/éves díjak, gateway- és tranzakciós költségek, támogatás/karbantartás, esetleges migráció és konfiguráció, Barion merchant recurring engedély, sandbox-bizonyíték, felhasználói élmény és összköltség. Nem feltételezzük, hogy az aktuális Barion plugin tud ismétlődő terhelést.
- **Automatikusan megújuló előfizetésre csak akkor térünk át**, ha megfelelő kész megoldás létezik, annak teljes költsége ismert, működése tesztelt, és **a megrendelő kifejezetten vállalja a költségeit**. A beszerzés/élesítés addig nyitott, feltételes feladat.
- Az MVP **már most készüljön későbbi átállásra**: egységes, fizetési megoldástól független prémium-hozzáférési logika, közös `paid_through` és fiókalapú jogosultság, ellenőrzött WooCommerce-rendelésfeldolgozás, cserélhető fizetési/előfizetési adapter. A meglévő manuális jogosultságok migrációja és a duplaterhelés/átfedés kezelése későbbi integrációs feltétel.
- **D09-MVP/01–02 ELFOGADVA (2026-10-16):** a manuális havi hozzáférés hiteles fizetéstől egy naptári hónap célhelyi napjának végéig tart, `Europe/Budapest` és hónapvégi igazítással; aktív hozzáférés előrevásárlásai hozzáadódnak, **eredeti havi fordulónapot megőrizve**, a lejárt jog új fizetéssel új sorozatot indít. **D09-MVP/03 ELFOGADVA (2026-10-16):** lejárat mindig látható a PWA-ban, az utolsó 7 napban kiemelt figyelmeztetéssel és újravásárlással, automatikus e-mail/push nélkül; a meglévő webes fiókoldal esetleges átalakítása D01 szerint külön scope. **2026-10-16-án megerősítve:** kártyacsere, automatikus újrapróbálkozás, recurring lemondás és automatikus megújulási értesítés csak egy később kiválasztott és jóváhagyott kész integrációhoz specifikálandó.

**Specifikációs hatás:** a V1.3 F08–F09 eredeti automatikus megújulás/lemondás követelménye az MVP-ben nem kötelező; feltételes későbbi cél, a specifikáció következő kiadásában átvezetendő. A D09 üzleti irány lezárt, a kész megoldás költség- és megvalósíthatósági vizsgálata és megrendelői döntés nyitott.

**D12 – Környezet és fiókkezelés – ELFOGADOTT IRÁNY, RÉSZFELADATOK NYITVA (2026. október 15.)**

**Felhasználói pontosítás (2026-10-16):** a fiókkezelés teljes felülete a PWA `/app/` scope-jában marad. Natív WordPress/WooCommerce fiókműveletekre épülő saját React-űrlapok szükségesek; a felhasználót nem irányítjuk ki webes Fiókom oldalra. Az app miatt új publikus WP-oldal, fiókoldal-kijelölés vagy globális webes regisztrációs beállítás nem változtatható. Ez az MF04-re kötelező elfogadási feltétel.


Eredeti kérdés: Mi a végleges domain, hol lesz a staging tesztkörnyezet, és alkalmas-e a tárhely a PWA-ra? Hogyan regisztrálhat új ügyfél?

**Jóváhagyott megoldás és a projektgazda által megerősített kiinduló tények:**

- A PWA az **éles WordPress-weboldallal azonos domainen, az `/app/` útvonalon** működjön, a meglévő WordPress/WooCommerce-fiókrendszert használva; ne legyen külön appos felhasználó-adatbázis. Az éles kanonikus domain/www beállítás a telepítéskor ellenőrzendő.
- **A jelenlegi vásárlók vendégként, regisztrált fiók létrehozása nélkül vásárolnak.** A jelenlegi webshop általános vendégvásárlását nem tiltjuk le globálisan. Az app fiókhoz kötött funkcióihoz (prémium havi vásárlás és hozzáférés, digitális jegyek, saját adatok) bejelentkezés szükséges; a regisztráció és bejelentkezés konkrét WooCommerce/WordPress útvonalát, UX-ét, e-mailjeit és beállításait ellenőrizni és szükség szerint kialakítani kell. A havi prémiumterméket a webes checkouton sem lehet vendégként megvenni (D01/D09).
- **A tárhelyen már rendelkezésre áll egy tesztdomainen futó WordPress tesztpéldány**, és **a fejlesztő lokális fejlesztői környezetet is létrehozott**. A tesztpéldányon lehet végigpróbálni a PWA/plugin telepítését, frissítését, visszaállítását, belépést és checkoutot az éles oldal módosítása nélkül. A staging pontos címe és izolációs részletei nem szerepelnek itt, ellenőrizendők.
- **A tárhely PWA-kiszolgálásra alkalmas** (projektgazdai információ). Ez a PWA/appfájlok kiszolgálására vonatkozik, **nem bizonyítja a párhuzamos média-streaming kapacitást**.

**Nyitott, mérendő technikai feladatok:**

1. Mekkora párhuzamos audio-/videostream-forgalmat visel el a meglévő tárhely elfogadható akadás, válaszidő és erőforrásterhelés mellett? Reprezentatív tartalommal, mobilos és párhuzamos terheléses próbával mérjük a sávszélességet, PHP/HTTP kapcsolatszámot, memória/CPU/IO-terhelést, adatátviteli limiteket és a webshop egyidejű működését.
2. Eredmények és várható nézőszám, forgalom, szolgáltatási költség alapján **külön privát streaming/CDN szolgáltató szükséges-e**? Erről a **D10 média-döntésnél** kell dönteni; nem rendeljük meg automatikusan, és nem feltételezzük, hogy az alaptárhely elegendő. Prémium média jogosultságvédelmét bármely opciónál biztosítani kell.
3. Staging–éles eltérés, tesztadatok, biztonságos fizetési/e-mail sandbox és a telepítési/regressziós ellenőrzőlista véglegesítése; a meglévő webes vendégvásárlás ne sérüljön.
4. Regisztráció/fiók-UX vizsgálata a korábbi vendégvásárlók számára, és a régi vendégrendelések igazolt fiókhoz kapcsolásának külön kezelése (D08). A meglévő weboldal esetleges felületi átdolgozása a D01 szerint külön webmesteri munka vagy ajánlat.

**Státusz:** irány jóváhagyva; **tárhely PWA-szintű alkalmassága és a tesztkörnyezet rendelkezésre állása megerősítve**, de streamingkapacitás, regisztrációs folyamat és staging telepítési/terhelési eredmények még vizsgálandók. **A lenti második „D12 – Adatkezelés és megőrzés” önálló döntés; annak projekthatárát 2026-10-16-án külön jóváhagytuk, a jogi paraméterek továbbra is a megrendelő feladatai.**

**D13 – „Virág kérdezi” szavazás – ELFOGADVA, V1 KÖTELEZŐ FUNKCIÓ (2026. október 15.)**

Eredeti kérdés: Bekerüljön-e a „Virág kérdezi” szavazás az első verzióba?

**Döntés:** **Igen. A „Virág kérdezi” szavazás része az első éles verziónak és az MVP elfogadási feltételeinek.** Nem csupán prototípus-látványelem vagy későbbi opció.

**Javasolt megvalósítási minimum, az implementáció előtt ellenőrizendő részletszabályokkal:**
- Virág WordPress adminfelületen hozhat létre és kezelhet kérdéseket, válaszlehetőségeket és a szavazás nyitott/zárt állapotát; a megjelenítés az új PWA-ban történik.
- **D13/01 ELFOGADVA (2026-10-16):** bejelentkezett felhasználó **egy fiókkal szavazásonként egy végleges választ** adhat le. A PWA a beküldés **előtt megerősítést kér**; a sikeresen leadott választ utólag **nem lehet módosítani**. Lezárt szavazásra új választ nem lehet beküldeni. Szerveroldali egyedi (szavazás, felhasználó) korlát, jogosultsági és állapotellenőrzés védi a többszörös beküldést.
- **D13/03 ELFOGADVA (2026-10-16):** a PWA felhasználója **nem lát szavazási eredményeket**, se részeredményt, se lezárt összesítést, se eredménytörténetet. Kiválaszt egy választ, D13/01 szerint megerősíti, majd egyszerű **„Köszönjük a válaszodat!”** visszajelzést kap. **Virág a WordPress-adminban** bármikor megnézheti az egyes kérdések aktuális **összesített szavazatszámait/arányait**; felhasználók egyedi szavazatát az eredményfelület nem mutatja.
- Biztosítani kell a szavazat tárolását, az ismételt kérés/idempotencia és párhuzamos kattintás kezelését, valamint a mobilos üres, betöltés, hiba és lezárt állapotokat.
- **D13/02–04 PONTOSÍTVA ÉS ELFOGADVA (2026-10-16):** Virág sok aktív szavazást tarthat nyitva; a felhasználó dashboardra belépéskor egyszerre **egyetlen véletlenszerűen kiválasztott, számára még megválaszolatlan nyitott kérdést** lát. Az eredményösszesítések **csak Virág jogosult WordPress-adminfelületén** láthatók; a PWA nem mutat eredményeket. **D13/04:** a kérdések kizárólag kézzel nyithatók és zárhatók a WordPressben, határozatlan ideig maradhatnak nyitva, **nincs automatikus időzítés és új kérdés miatti e-mail/push**. A D13 minden MVP üzleti részletszabálya lezárt.

**D13/01 – Végleges, egyszer leadható szavazat – ELFOGADVA (2026. október 16.)**

Minden bejelentkezett WordPress-fiók szavazásonként egy választ adhat le, **megerősítő lépéssel még a végleges POST előtt**. A választás sikeres rögzítése után nincs felhasználói szerkesztés, felülírás vagy újraszavazás, még akkor sem, ha másik opciót választana. Azonos beküldés technikai újrapróbálása nem hoz létre második választ; eltérő opcióval történő ismételt beküldés a már leadott szavazatot nem változtathatja meg. Lezárt vagy még nem kézzel megnyitott szavazásra új válasz nem fogadható el (D13/04: nincs automatikus időablak). A PWA a sikeres végleges beküldés után egyszerű köszönő üzenetet mutat, eredmény vagy előzmény nélkül. A szerver ellenőrzi a bejelentkezést, a szavazás és opció érvényességét, a (poll_id, user_id) egyediséget és a párhuzamos kattintásokat.

**D13/02 – Sok tartósan nyitott szavazás; felhasználónként egy véletlen, megválaszolatlan dashboard-kérdés – PONTOSÍTOTT, ELFOGADVA (2026. október 16.)**

**Döntés:** Virág a WordPress-adminban **egyszerre több, akár nagy számú aktív szavazást** tarthat nyitva; nincs „legfeljebb egy aktív szavazás” üzleti korlát. A szavazások **határozatlan ideig nyitva maradnak**, amíg Virág/jogosult WordPress-admin kézzel le nem zárja őket. **D13/04 alapján nincs automatikus kezdési/lezárási időpont vagy ütemezett állapotváltás.** A piszkozat/nyitott/lezárt státusz szavazásonként külön működik. A D13/01 szerinti **egy végleges szavazat/fiók/szavazás** változatlan.

- **Eredmények – D13/03 felülírja a korábbi javaslatot:** a nyitott vagy lezárt szavazások **aktuális összesített eredményeit csak Virág/jogosult WordPress-admin** látja. A felhasználók egyáltalán nem látnak eredményszámot, százalékot, grafikont vagy korábbi válaszok/eredmények listáját. A végleges beküldés után csak köszönő visszajelzés következik.
- **Dashboard-kérdés kiválasztása – pontosított üzleti döntés:** amikor a bejelentkezett felhasználó belép a dashboardra, a rendszer a **nyitott/aktív ÉS az adott fiók által még meg nem válaszolt** szavazások közül **véletlenszerűen kiválaszt pontosan egyet**. Egyszerre **csak ez az egy kérdés** jelenik meg a számára. A már megválaszolt, lezárt vagy még kézzel meg nem nyitott kérdések **nem** választhatók. Ha nincs megfelelő kérdés, a dashboard nem jelenít meg új szavazásra felszólító kártyát (vagy egy egyszerű üres állapotot mutat). A kiválasztás fiókhoz kötött és szerveroldali jogosultság- és válaszellenőrzésen alapul; a fiókonkénti egy végleges válasz D13/01 szerint megmarad. **Nem készül kötelező, az összes aktív szavazást szavazásra kínáló felhasználói lista**. **D13/03 elfogadva:** nincs felhasználói eredménylista, eredménynavigáció vagy korábbi szavazatokból felépített eredményoldal. Az eredményösszesítés csak a WordPress-adminnak elérhető.
- **Tesztelendő:** két vagy sok párhuzamosan nyitott poll, a dashboardra lépéskor fiókonként **egyetlen véletlen, még megválaszolatlan és aktuálisan nyitott** kérdés; eltérő felhasználók eltérő jogosult kérdéseket kaphatnak; megválaszolt/lezárt/nem nyitott poll kiszűrése, minden kérdés megválaszolásakor üres állapot; új belépéskor új választható kérdés; fiókonként/pollonként egy végleges szavazat, manuális zárás, élő eredményaggregáció és jogosultsági/terhelési tesztek. **D13/03:** az aktuális összesített részeredmény a WordPress-adminnak elérhető, a felhasználónak nem; eredmény- és egyedi válaszadat nem kerülhet a PWA ügyfél-API-jába.

**D13/03 – Eredmény csak Virág WordPress-adminfelületén – ELFOGADVA (2026. október 16.)**

**Döntés:** A PWA-felhasználó nem látja sem saját szavazása előtt, sem utána az aktuális vagy végleges aggregált eredményeket. Nincs felhasználói „Korábbi válaszaim és eredmények” nézet, eredménylista, százalék vagy állásgrafikon. A felhasználói út: **egy dashboardon véletlenül kiválasztott megválaszolatlan kérdés → egy válasz kiválasztása → D13/01 szerinti megerősítés → „Köszönjük a válaszodat!” → kész.** A korábban megválaszolt kérdés nem jelenik meg ismét új szavazási feladatként.

**Virág/jogosult WordPress-admin** látja az egyes szavazások aktuális és a lezárás után végleges **összesített darabszámait, arányait és az összes válasz számát**, kérdésenként, a WordPress kezelőfelületén. Az összesítés frissül az új szavazatok alapján, nyitott állapotban is. Nem építünk felhasználói eredményoldalt, nem szükséges eredményláthatósági kapcsoló vagy push/e-mail eredményközlés. A felhasználói REST nem adhat eredményaggregátumot vagy idegen fiók egyedi válaszát; az adminösszesítés megfelelő WP jogosultsággal védett. Az eredmények adatkezelési határai D12 szerint érvényesek.

**Státusz:** D13/01–04 mind elfogadva. A P01/V1 szavazás üzleti szabályai lezártak; az implementáció, WordPress-admin, PWA és TP01 elfogadási tesztek végrehajtandók.

**D13/04 – Kézi nyitás és zárás, időzítés/értesítés nélkül – ELFOGADVA (2026. október 16.)**

**Döntés:** Virág vagy jogosult WordPress-admin a kérdéseket **kézzel rögzíti, nyitja meg és zárja le**. Egy kérdésnek nincs kötelező kezdési vagy zárási dátuma; **határozatlan ideig nyitva maradhat**, amíg Virág kézzel le nem zárja. **Automatikus/ütemezett megnyitás, automatikus/ütemezett lezárás, dátumhoz kapcsolt cron/Action Scheduler állapotváltás nem készül az MVP-ben.**

- **Állapotok:** `draft` (WordPressben előkészített, nem szavazható), `open` (Virág kézzel aktiválta, a fiók szavazhat, ha még nem tette meg), `closed` (Virág kézzel lezárta; nem fogad új választ). A lezárt kérdés **nem nyílik meg magától újra**, és nem nyílik meg automatikusan újra. Az esetleges kézi újranyitás működése nem része a jóváhagyott alapfunkciónak; ha később felmerül, külön pontosítandó, a korábbi végleges szavazatok védelmével.
- **Nincs új kérdésről automatikus e-mail, push vagy külön in-app kampány**, és nincs ilyen ütemezett küldő háttérfeladat. A D06 általános, manuális üzenetküldését ez nem tiltja, de a szavazás létrehozása/megnyitása nem vált ki küldést.
- A D13/02 szerinti dashboard a felhasználó **minden belépésekor** az éppen `open` és számára még megválaszolatlan kérdések közül szerveroldalon véletlenszerűen **egyet** választ; új kérdés csak ilyen dashboard-megnyitáskor kerül elé. Ha nincs ilyen, nem jelenik meg új szavazási feladat.
- A WordPress-admin a kérdés megnyitását és lezárását jogosultságellenőrzés és audit mellett végzi. A `draft` és `closed` státuszú kérdések nem szerepelhetnek a dashboard véletlen kiválasztásában, és a szerver sem fogadhat hozzájuk új szavazatot. Az eredmények Virág WordPress-adminfelületén megmaradnak (D13/03); felhasználónak csak köszönet jelenik meg.
- **Kötelező TP01 tesztek:** sok párhuzamos, tartósan nyitott kérdés; kézi `draft → open → closed` átmenet, kézi újranyitás nincs előírva; megnyitáskor nincs automatikus e-mail/push/kampány; sem időzítő, sem háttérfeladat nem nyit/zár kérdést; lezárt kérdés már nem választható és nem szavazható; dashboardra visszalépéskor a szerver aktuális nyitott, megválaszolatlan halmazból választ.

**D13 teljes státusz:** **D13/01 végleges szavazat, D13/02 egy véletlen megválaszolatlan dashboard-kérdés a sok nyitottból, D13/03 csak-admin eredmény és D13/04 kézi nyitás/zárás, értesítés nélkül – MIND ELFOGADVA.** Ez üzleti/specifikációs jóváhagyás, nem kész fejlesztés.

**Specifikációs hatás:** a V1.3 DOCX F01–F26 listájában ez nem szerepel; most új, önálló **P01 kötelező V1-követelményként** kell nyilvántartani. A következő üzleti specifikáció-verzióba átvezetendő, az eredeti DOCX történeti példánya változatlan.

**D10 – Média és streaming – ELFOGADOTT DÖNTÉSI ELJÁRÁS (2026. október 16.), SZOLGÁLTATÓ NYITOTT**

**Döntés:** A jelenlegi tárhely streamingkapacitását először **valós, dokumentált teszttel megmérjük**, a helyben történő kiszolgálás és a szóba jöhető külső streaming/CDN opciók **teljes költségét és ár/érték arányát** összehasonlítjuk, és csak ezután választunk. **Sem külső szolgáltató, sem a meglévő tárhely nem kapott még végleges jóváhagyást médiaforrásként.** A D12 szerinti PWA-kiszolgálási alkalmasság nem azonos az audio-/videostreaming kapacitásával.

**Mérési és összehasonlítási feladat:**
1. A tartalomgazdával becsülni kell az audio- és videóanyagok számát, méretét, bitrate-jét, formátumát, népszerűségét, csúcsban várt párhuzamos lejátszások számát és havi adatforgalmát. A feltételezett terhelési profil legyen dokumentált, ne kitalált kapacitásérték.
2. A meglévő tárhelyen, lehetőleg a rendelkezésre álló tesztdomaines környezetben, **az üzemeltetővel egyeztetett biztonságos korlátok között** kell reprezentatív, fokozatos párhuzamos audio- és videolejátszást mérni. Követendő: sikeres/hibás kérések, indítási késés, pufferelés/akadás, kiszolgált sávszélesség, kapcsolat- és erőforrásigény (CPU, memória, lemez/I/O), adatforgalmi korlát, mobilos HLS/range viselkedés és az ugyanott működő WooCommerce válaszideje. Az éles webshop működését nem veszélyeztethetjük kontrollálatlan terheléssel.
3. Össze kell vetni legalább a **meglévő tárhelyen megvalósítható védett kiszolgálás** és a **külső, jogosultságvédett streaming/CDN** megoldások költségeit (tárhely, forgalom, transzkódolás, licencek, beállítás/fejlesztés, üzemeltetés, támogatás), teljesítményét, méretezhetőségét és biztonsági korlátait.
4. A fejlesztő eredmény- és költségösszefoglalót készít a megrendelőnek; ez alapján külön döntés születik az éles médiakiszolgáló helyéről és az esetleges szolgáltatói költség vállalásáról.

**Választástól független minimum:** a prémium audio/video nem lehet közvetlen, nyilvános WordPress uploads URL-en jogosultságellenőrzés nélkül elérhető. A szerver minden lejátszási hozzáférést ellenőriz, a média/segment/kulcs hozzáférés jogosultsághoz kötött és rövid élettartamú vagy azzal egyenértékűen védett. A megoldás legyen cserélhető szolgáltatóadapterrel, hogy ne kössük előre a React-alkalmazást egy CDN-hez.

**Státusz:** a **mérés → költség/alkalmasság-összevetés → szolgáltatóválasztás** folyamata jóváhagyott. **Mérési eredmény, streamlimit, szolgáltató, szerződés és végleges költség még nincs igazolva vagy kiválasztva.** A médiamodul éles kiadása előtt a kiválasztott megoldást jogosultsági, mobil lejátszási és terhelési teszten igazolni kell (M7/T03/T06/T30/G4).

**D11 – Chat – ELFOGADOTT V1 IRÁNY (2026. október 16.)**

Megválaszolandó eredeti kérdés: Megfelel-e a Better Messages ingyenes REST/AJAX megoldása, vagy szükséges a fizetős WebSocket változat?

**Jóváhagyott döntés:** a V1-hez az **ingyenes Better Messages REST/AJAX-integrációval indulunk**, **az aktív chatképernyőn körülbelül 10 másodperces üzenetfrissítéssel**. Az alkalmazás a háttérben és a chatképernyőről távozás után ne kérdezgesse feleslegesen folyamatosan a szervert; visszatéréskor azonnal frissítsen. A cél aszinkron szöveges üzenetváltás a szülők és Virág között, nem feltétlenül azonnali WebSocket kézbesítés.

**Kötelező staging-integrációs próba:** az ingyenes változat tényleges API- és licenclehetőségei, kétirányú szövegküldés és fogadás, saját beszélgetés/jogosultság, idegen thread és szülő–szülő kommunikáció tiltása, olvasottság, mobilos működés, hibakezelés, retry és duplikált üzenet elleni védelem. A rendszer csak sikeres megfelelőségi próba után fogadható el V1 chatként.

**Fizetős WebSocket:** nem MVP-kötelező és **nincs beszerzésre jóváhagyva**. Csak igazolt használhatósági vagy teljesítménybeli szükség esetén, kompatibilitás- és költségfelmérés, majd **külön megrendelői költségjóváhagyás** után kerülhet be. Ha az ingyenes integráció nem elegendő, annak hiányosságát és a lehetséges alternatívákat külön döntésre kell hozni; saját, költséges chatfejlesztés nem automatikus következmény.

**Státusz:** megvalósítási irány jóváhagyva; a tényleges teszt eredménye még nyitott. A chat adatmegőrzési paraméterei a külön, projektscope szerint már elfogadott D12 értelmében a megrendelő/adatkezelő külső feladatai; új törlési alrendszer nem része a fejlesztésnek.

A média és a chat végleges megoldása később is lezárható, de a megvalósíthatósági próbájukat már az elején érdemes elvégezni.

**2. Elfogadott modulszabályok és végrehajtandó feladatok**

**D02 – Jegyek és bérletek érvényessége – ELFOGADOTT DÖNTÉS (2026. október 16.)**

**Döntés:**
- **Családi jegy:** a hitelesen sikeres WooCommerce-fizetés időpontjától érvényes, **3 naptári hónapig**, az így számított helyi lejárati nap végéig. Nem a rendelés létrehozásának idejétől.
- **8 alkalmas bérlet:** a megvásárlás nem indítja el a **8 naptári hónapos** időszakot; az első **ténylegesen sikeres, szerveroldalon rögzített beváltás** indítja. Az első használatig a bérlet a jelenlegi V1 szabály szerint `unactivated`, nincs kiszámított használat alapú lejárati dátuma. A QR megnyitása vagy csak ellenőrzése nem számít első beváltásnak. A 8 alkalom limit külön érvényes.
- **Lejárat:** mindkét terméktípusnál a cél nap **végéig, a `Europe/Budapest` időzóna szerint**. Technikailag `expires_at` = az ezt követő helyi nap 00:00-ja UTC-re konvertálva, **kizárólagos felső határ**; a szerver akkor tekinti érvényesnek, ha `now < expires_at`.
- **Hónapvége:** naptári hónapokat adunk a kezdő helyi dátumhoz; ha a céldátum napja nem létezik (például 31-e), a célhónap utolsó napjára igazítjuk. Példák: **január 31-i jegyvásárlás → április 30. nap végéig**; **január 31-i első bérletbeváltás → szeptember 30. nap végéig**. Szökőévek és téli/nyári időszámítás szerint is tesztelendő.
- **Konfigurálhatóság:** az időtartam (alapértelmezés: jegy 3, bérlet 8 naptári hónap) és az aktiválási szabály **a WordPressben karbantartható terméktípus-szabályhoz / termékleképezéshez tartozzon**. Ne legyenek a PWA-kliensbe beégetett fix számok. A rendeléstételhez mentett szabálypillanatkép biztosítja, hogy egy későbbi admin módosítás ne változtassa meg visszamenőleg a már megvett jegy/bérlet lejáratát. Érvénytelen termékkonfigurációt az admin/backend utasítson el.
- A szabály a **családi jegyre és 8 alkalmas bérletre** vonatkozik; az eseményjegyek és a D09 szerinti manuálisan megvásárolható prémium-hozzáférés eltérő időszabályait nem írja felül.

**Státusz:** a D02 üzleti döntés lezárt. A tényleges szerveroldali hónapszámítás és a WordPressben kezelhető termékszabályok megvalósítása/tesztelése M2–M3 és T11/T12 feladat; nem állítjuk, hogy a funkció már elkészült.

**D03 – Beváltás és alkalomlevonás – ELFOGADOTT DÖNTÉS (2026. október 16.)**

**Döntés:** Az egyszeri beléptetés és a visszatérés kezelése **egységesen vonatkozik a családi jegyre, a többalkalmas bérletre és a külön áras eseményjegyre is**.

- Egy jogosultságot egy **konkrét eseményen/foglalkozási alkalmon legfeljebb egyszer** lehet érdemben beváltani. Az első sikeres belépés a típusának megfelelő állapotváltást eredményezi: családi jegynél a jegy felhasználása, bérletnél pontosan egy alkalom levonása, külön áras eseményjegynél az **adott eseményre szóló jegy** felhasználása.
- Ha a család **ugyanarra a konkrét foglalkozásra visszatér**, a beléptető az előző belépés tényét és időpontját mutatja („már belépett – visszatérés”), és **egyik terméktípusnál sem végez újabb beváltást, levonást vagy új jogosultság-felhasználást**. A jogosultságellenőrzés továbbra is szükséges; az ismételt próbálkozás nem jelenhet meg új sikeres beváltásként.
- **Nincs általános napi limit**: ugyanazon napon **másik, külön eseményazonosítójú foglalkozás** a meglévő termékszabályok szerint látogatható, ha van rá felhasználható jogosultság és a szükséges foglalás teljesül. A bérletből itt újabb egy alkalom levonható. A már elhasznált, egyszeri családi jegy másik eseményre **nem** válik újra használhatóvá; a külön áras eseményjegy **csak a hozzá rendelt eseményen** érvényes, nem használható át másik programra.
- A szerver minden jegy/bérlet/eseményjegy beváltását tranzakciósan, egyedi `entitlement_id + event_id` kulccsal és idempotens művelettel védi. Párhuzamos ellenőrzés/beváltás nem okozhat duplázást; a QR puszta megnyitása vagy a staff `inspect` művelet nem beváltás.
- Az újra belépés **felhasználói/staff kijelzési szabály**, nem egy második redemption tranzakció. A beléptető felület jól elkülöníti az első sikeres beváltást, az ugyanazon eseményre történő visszatérést és a tényleges tiltó okokat (lejárt, másik esemény, rossz foglalás).

**Státusz:** a D03 üzleti döntés lezárt; az adatmodell, a staff API, a felület és a családi jegy/bérlet/külön eseményjegy regreszsziós tesztje az MF07–MF08 / M3–M4 megvalósítás része. A D05 időablak-/foglalásszabályait ez nem írja felül.

**D04 – Családmodell – ELFOGADOTT V1 DÖNTÉS (2026. október 16.)**

**Döntés:** Az első verzióban **egy WordPress/WooCommerce ügyfélfiók egy családot képvisel**. A család egy önálló belső `family_id` azonosítót kap, amelyhez a jegyek, bérletek, eseményjegyek és foglalások kapcsolódnak. A felhasználói hozzáférés és a vásárláshoz kapcsolódó tulajdonosi jog a V1-ben az egyetlen jogosult fióké.

- **Nincs automatikus családi fiókösszekapcsolás:** két szülő külön WordPress-fiókja nem fér hozzá magától ugyanahhoz a családi jegy-/foglalásállományhoz; közös többfiókos családadminisztráció nem V1-funkció.
- **Nincs ügyféloldali jegy-/bérletátruházás**, és nem épül több család egy fiókból történő önkiszolgáló kezelése. Ha több család vásárlása, jogosultság áthelyezése vagy családi fiókhelyzet javítása szükséges, azt Virág/jogosult munkatárs **kézi, ellenőrzött ügyintézéssel** rendezi. Ez nem jelent automatikus tömeges vásárlást, kéretlen családegyesítést vagy publikus átadási API-t; a kézi korrekció részleteit az admin jogosultsági és naplózási szabályok szerint kell megvalósítani.
- **Egy család egy konkrét eseményre legfeljebb egy aktív családi foglalással/foglalt kapacitásegységgel rendelkezhet.** A foglaláskor mindig a szerver által, a bejelentkezett fiókból feloldott `family_id` számít, nem egy kliens által beküldött családazonosító.
- **Későbbi bővíthetőség:** a család mint külön entitás és a jegyek/foglalások `family_id` kapcsolata maradjon elkülönítve a WordPress `user_id`-tól. V1-ben minden családnak egy fióktulajdonosa van. A későbbi, külön jóváhagyandó több szülős megoldáshoz külön családtag-/fióktagsági kapcsolattábla és jogosultságmodell csatlakoztatható, a meglévő családazonosítók és jogok tömeges átírása nélkül; **ezt a közös családhozzáférési funkciót most nem fejlesztjük le**.
- A családtagok részletes személyes adatainak gyűjtése, közös szülői felhasználómenedzsmentje nem szükséges V1-ben; a korábbi vendégvásárlások fiókhoz igazolása külön D08 kérdés, önmagában e-mail-egyezés alapján nincs automatikus hozzárendelés.

**Státusz:** üzleti döntés lezárva. A `family_id`-alapú hozzáférés, foglalási egyediség, manuális korrekció jogosultság- és auditkövetelménye és a későbbi tagság lehetőségének fenntartása implementációs/tesztelési feladat az MF07–MF08 modulokban. A D05 foglalási időablakai és a D07 visszatérítési szabályai szintén elfogadottak; implementációjuk és műszaki igazolásuk még feladat. A D08 legacy átvezetés külön nyitott döntés.

**D05 – Foglalási és beléptetési szabályok – ELFOGADOTT V1 DÖNTÉS (2026. október 16.)**

**Döntés:**
- **Alapdíjas, korlátozott létszámú esemény:** a saját aktív foglalás **a program kezdetéig**, azaz a szerveren rögzített kezdési időpontot megelőzően lemondható; lemondás esetén pontosan egy családi kapacitásegység szabadul fel. Ismételt lemondás nem szabadíthat fel újabb férőhelyet. A családi jegy/bérlet önmagában nem foglal helyet és a foglalás lemondása nem használja el.
- **Külön áras esemény fizetés alatti helyfenntartása:** a helyet a vásárlás megkezdésekor létrejövő ellenőrzött foglalási `hold` **15 percig** fenntartjuk, szerveridővel. A korlát minden értékesítési csatornára vonatkozik (PWA, webes kosár/pénztár, rendelésfizetés). Lejáratkor, ha még nincs igazolt és kapacitással egyeztetett fizetés, a hely ismét elérhetővé válhat.
- **Késő fizetési visszaigazolás:** a lejárt helyfenntartás után érkező sikeres fizetés **sohasem lépheti túl az esemény kapacitását**. Ugyanazon adatbázis-tranzakcióban újra vizsgáljuk, hogy van-e még szabad hely. Ha van, megerősíthető a vásárlás/jegy és foglalás; ha nincs, **nem állítunk ki érvényes belépési jogosultságot**, a rendelés `paid_capacity_conflict` állapotba kerül, és pénzügyi/ügyfélszolgálati rendezést (visszatérítés vagy más megoldás) igényel. A pénzügyi rendezésre az elfogadott D07 visszatérítési szabályai vonatkoznak.
- **Beléptetés:** a staff alapértelmezésben a foglalkozás kezdete **előtt 2 órával** kezdhet, és a foglalkozás **vége után 2 óráig** végezhet ellenőrzést/beváltást. A valós eseményadatokból szerveroldalon számolt időablak **WordPress adminból eseményenként módosítható**; az alapbeállítás további egyedi beavatkozás nélkül használható. Az ellenőrzés és az új beváltás a D03 szerinti egyszeriséget és családi/event jogosultságokat tiszteletben tartja.
- **Várólista:** **nem készül az első verzióban**. Betelt foglalkozásnál az alkalmazás világosan jelzi, hogy nincs foglalható hely; a kapacitásversenyt és a többcsatornás fizetést szerveroldali tranzakció védi.

**Megvalósítási/tesztelési szabály:** a WordPressben beállítható kivételes eseményablak, a kezdési határpillanat, a 15 perces holdlejárat, a dupla visszaigazolás, az utolsó helyért folyó párhuzamos vásárlás, valamint a lejárt hold utáni fizetés elutasítása/feloldása kötelezően tesztelendő. A D05 üzleti szabályai lezártak; **a teszteredmények, valamint az elfogadott D07 szerinti integráció igazolása és az admineljárás kidolgozása még végrehajtandó feladatok**.

**D07 – Visszatérítés és chargeback – ELFOGADOTT V1 DÖNTÉS (2026. október 16.)**

**Döntés:** A visszatérítés elsődleges ügyintézési helye a **meglévő WooCommerce**, a tényleges pénzmozgást a meglévő **Barion fizetési bővítmény** kezeli, a számlázási/helyesbítési folyamat a **Billingóban** marad. **Nem fejlesztünk saját Barion refund rendszert vagy új fizetési alrendszert.**

- **Egyértelmű teljes visszatérítés, fel nem használt jogosultság:** ha az adott, beazonosítható WooCommerce-rendeléstételre a teljes visszatérítés ténylegesen **sikeresen rögzítve / visszaigazolva** történt, a hozzá tartozó **még fel nem használt** családi jegy, bérlet vagy külön áras eseményjegy visszavonható. Csak az érintett rendeléstétel és az abból származó jog változhat, más termék nem.
- **Külön áras eseményjegy:** az egyértelműen visszatérített, még fel nem használt eseményjegy **aktív foglalása egyszer, kapacitásvédett tranzakcióban** felszabadítható, ha a hely még releváns. Nem szabad duplán felszabadítani a helyet vagy túlfoglalást okozni.
- **Már használt jegy/bérlet, részben felhasznált bérlet, részleges/összegalapú vagy többtermékes rendelés visszatérítése:** **nem** jár automatikus teljes jogosultság-visszavonással vagy alkalom-visszaadással. Virág/jogosult ügyintéző rendeléstételenként megvizsgálja és indoklással, jogosultságellenőrzéssel, naplózott kézi korrekcióval dönt. A korábbi sikeres belépési események **auditja változatlanul megmarad**.
- **Közvetlenül a Barion felületén végzett refund, chargeback, vitatott vagy visszaterhelt fizetés:** nem tételezzük fel, hogy a WooCommerce automatikusan értesül róla. Külön **kézi egyeztetési/reconciliation folyamat** szükséges a Barion, WooCommerce és Billingo állapota között. Kockázat esetén a még fel nem használt érintett hozzáférés ideiglenesen felfüggeszthető, de bizonytalan adat alapján nem történhet végleges automatikus törlés vagy alkalom-visszaadás.
- A **D05 szerinti `paid_capacity_conflict`** esetben nincs kiállított belépési jog; a ténylegesen megfizetett, de nem teljesíthető rendelés pénzügyi rendezése a WooCommerce/Barion/Billingo ellenőrzött folyamatában történjen, külön ügyintézési állapottal.
- **Kötelező staging/sandbox próba:** **WooCommerce → Barion → Billingo** teljes és részleges refund; siker, hiba, újrapróbálkozás, állapot- és rendeléstétel-megfeleltetés, helyesbítő bizonylat, egyértelmű/használt jog, többtermékes rendelés, eseményhely egyszeres felszabadítása, valamint a Barionban közvetlenül indított refund/chargeback **szinkronizációs képességének külön vizsgálata**.
- A helyben feltárt **Barion Payment Gateway for WooCommerce 3.10.2** deklarál `refunds` képességet; ez **nem bizonyítja**, hogy az éles beállításokkal a teljes/részleges refund és a Billingo-szinkron már működik. Tényleges sandbox-bizonyíték szükséges. Az esetleges működési hiány nem jogosít automatikus egyedi fizetési fejlesztésre; külön egyeztetés kell.

**Státusz:** üzleti szabály lezárva; a WooCommerce/Barion/Billingo integráció tényleges megfelelősége, a chargeback-értesítés és az egyeztetési admineljárás részletes tesztelése **nyitott műszaki/üzemeltetési feladat** (M0/M3/M5/M9, T08/T18/T20/T25/T30).

**D06 – Pushértesítések és címzettcsoportok – ELFOGADOTT V1 DÖNTÉS (2026. október 16.)**

**Döntés:** az alkalmazáson belüli értesítési előzmény **független** az operációs rendszer pushengedélyétől, az eszköz meglététől és a tényleges pushkézbesítéstől. A WordPressben Virág által elküldött értesítési kampány minden kijelölt címzettjéhez **pontosan egy fiókszintű értesítési rekord (receipt)** tartozik, push nélkül is.

- **Értesítési előzmény:** minden bejelentkezett felhasználó a **neki címzett** értesítéseket láthatja az alkalmazásban, akkor is, ha nem telepítette a PWA-t vagy nem engedélyezte a push-t. Több eszköz ugyanazt a fiókszintű listát és „ÚJ” jelölést látja. Az új jelölés az előző panelmegnyitáshoz / szerveroldali cursorhoz viszonyít.
- **Push mint külön szállítás:** ha az adott felhasználó/eszköz önként engedélyezte, megkíséreljük a push elküldését. A pushküldés és az eszköz/provider státusza **külön** nyilvántartás; pusztán a szolgáltatói átvételt nem állítjuk tényleges telefonos megjelenítésnek vagy olvasásnak. A sikertelen push **nem tünteti el** az appbeli rekordot.
- **Címzés:** Virág a **WordPress-adminban** indíthat kézi kampányt **egy konkrét felhasználónak, egy adminisztrált címzettcsoportnak vagy minden felhasználónak**. A kezdeti csoportokat Virág határozza meg, a konkrét csoportlista még rögzítendő. Küldéskor egyedi címzettpillanatkép készül; későbbi csoporttagság-változás nem írja át a múltbeli előzményeket. Az adminisztrációhoz nem kell külön mobiladmin.
- **365 napos előzmény:** az alkalmazás a **megelőző 365 nap címzett értesítéseit jeleníti meg**, fiókonként, szerveridővel számolva. **A mögöttes rekordok tényleges törlési/megőrzési idejét, jogalapját, tájékoztatását és az esetleges érintetti eljárást a D12 elfogadott projekthatára szerint a megrendelő adatkezelője határozza meg; külön GDPR-alrendszer nem része a fejlesztésnek.** A 365 nap nem általános adatmegőrzési szabály, nem jelent önmagában adatbázis-törlési felhatalmazást.
- **Pushengedély bekérése:** **nem** az alkalmazás első megnyitásakor ugrik fel automatikusan. Csak jól érthető, **a felhasználó által indított** műveletből kérjük az OS/böngésző engedélyét; elutasítás után nem ismételjük automatikusan. Az appbeli értesítések ehhez nem kötöttek.
- **Nyitott implementációs/adatkezelési feladatok:** Virág kezdeti csoportnevei/tagsági szabályai; WordPress-admin küldési előnézet; eszköz- és fiókváltás; opt-in/opt-out; jogosultság, több eszköz és hibás push végpont; D12 szerinti adatvédelmi szabályok és megőrzés.

**Státusz:** a D06 funkcionális döntés lezárt; az admin/címzettcsoportok konkrét beállítása, push-tesztje és a D12 adatkezelési projekthatár lezárt, a megrendelő jogi/megőrzési paraméterei külső feladatok.

**3. Nyitott végrehajtási részletek és külön elfogadott adatkezelési projekthatár**

A D09-MVP/01 időtartam, /02 eredeti fordulónapot őrző előrevásárlás és /03 kizárólag PWA-beli, utolsó 7 napos lejárati figyelmeztetés **mind elfogadott**; a D10 streaming-szolgáltatóválasztás továbbra is nyitott, de a D13 szavazási részletszabályai már mind elfogadottak. Az elfogadott D06 kezdeti csoportlistája még rögzítendő; a technikai próbák nem új üzleti döntések.

**D08 – Régi jegyek, bérletek és vendégrendelések átvezetése – ELFOGADOTT FOKOZATOS ÁTÁLLÁS (2026. október 16.)**

**Döntés:** **Nem kell az összes régi papírjegyet és papírbérletet digitalizálni az első verzió indulásához.** A meglévő, érvényes papíros jogosultságok a megszokott, ellenőrzött helyszíni rendben tovább használhatók, miközben az **átállást követően az új digitális jegy- és bérletfolyamatba tartozó vásárlásokat** az új alkalmazás kezeli. A két működés átmenetileg párhuzamos. A D01 szerinti régi WooCommerce-termékek megtartását ez önmagában nem tiltja vagy írja át; a régi SKU-k új digitális jogosultsághoz rendelését termékenként kell ellenőrizni.

- **Régi papírjogok:** nincs kötelező tömeges QR-import vagy minden régi papírbérlet digitalizálása. A régi jegyek/bérletek elfogadásának és felhasználásuk adminisztrációjának világos, a helyszíni munkatársakkal egyeztetett átmeneti eljárása legyen. Az első éles kiadásig a teljes régi készlet bevitele nem G3-kapu.
- **Opcionális, ellenőrzött egyedi átvezetés:** digitális, beváltható jogosultság **csak igazolt** fel nem használt jegyből, illetve ellenőrzött első-használati dátumú és maradék-alkalomszámú bérletből keletkezhet. Ha adatok hiányoznak/ellentmondásosak, `legacy_review_required` és **nincs aktív digitális QR**, amíg Virág vagy jogosult munkatárs nem igazolja. Átvezetés naplózottan, duplikáció- és kettős felhasználás elleni kontrollal történik; az átvett papírjog további papíros használatának szabályát az ügyintéző egyezteti.
- **Korábbi vendégrendelések:** az új WordPress-fiókhoz történő kapcsolás csak **tulajdonosi igazolással** vagy jogosult munkatárs ellenőrzött, auditált hozzárendelésével történhet. **Az e-mail-cím egyezése önmagában nem elegendő**, a régi rendelés fizetettsége önmagában nem bizonyítja, hogy van még felhasználható jegy.
- **Új vásárlások:** a kijelölt átállási időponttól a digitális jogosultságkezelésbe bevont jegy-/bérlettermékek új vásárlásai már az új WooCommerce–Ringató Core folyamatba kerülnek, közös web/PWA kereskedelmi szabályokkal. Ugyanazon vásárlásból nem készülhet párhuzamos új papíros és digitális, kétszer beváltható jogosultság.
- **Átállási időpont és ügyféltájékoztatás:** konkrét nap **még nincs jóváhagyva**. A fejlesztő, Virág és a helyszíni munkatársak a pilot/élesítés előtt meghatározzák, mely termékekre mikor indul az új digitális folyamat, hogyan azonosítható egy régi papírbérlet és hol történik a helyszíni nyilvántartása. Vevői és staff tájékoztatás kötelező.
- **V1 kiadási kapu:** igazolt új digitális vásárlás/QR/beváltás, a régi papíros jogok zavartalan elfogadása, kettős felhasználás elleni eljárás, és csak a **ténylegesen átvett** tételeknél adatellenőrzés/importteszt. **A teljes történeti állomány digitalizálása nem indulási feltétel**; a későbbi teljes migráció külön egyeztethető.

**Státusz:** üzleti irány jóváhagyva; a konkrét átállási dátum, termékkör, helyszíni eljárás és az opcionális átvétel részletes kontrolljai végrehajtandó feladatok. A D12 adatkezelési projekthatár külön elfogadott, a tényleges megőrzési paraméterek a megrendelő külső feladatai.

**D12 – Adatkezelés és megőrzés – ELFOGADOTT PROJEKTSCOPE (2026. október 16.); A JOGI PARAMÉTEREK KÜLSŐ FELELŐSSÉG**

**Üzleti döntés:** A Ringató PWA projekt **nem vállal jogi tanácsadást, adatkezelési tájékoztató vagy hozzájárulási szövegek jogi elkészítését/felülvizsgálatát**, és **nem fejleszt külön, átfogó anonimizálási, tömeges adattörlési vagy GDPR-ügyintézési alrendszert**. A meglévő WordPress/WooCommerce/Better Messages/Billingo és azok támogatott adatvédelmi funkcióit használjuk újra. A működéshez szükséges adatállapot-, session-, push-eszköz-leválasztási, jogosultsági és egyéb **funkcionális** törlések/korrekciók megmaradnak, valamint az eredetileg szükséges hozzáférés- és adatbiztonsági követelmények sem tűnnek el.

- **Beállítható értékek:** ahol a fejlesztés ténylegesen kezel saját megőrzési/megjelenítési időablakot vagy életciklust, lehetőség szerint **adatkategóriánként konfigurálható WordPress-beállítást** biztosítunk, dokumentált alapértékkel. A D06 szerinti **365 nap az app értesítéslista megjelenítési ablaka**, nem automatikus fizikai adattörlési határidő. A jegy és bérlet funkcionális lejárata szintén nem azonos a személyes adatok megőrzési idejével.
- **„Törvényi” alapérték:** **csak akkor** adunk jogszabályhoz kötött alapértelmezést, ha az az adott adatkategóriára valóban **egyértelműen és ellenőrzötten alkalmazható**, és a megrendelő/adatkezelési felelős megadta vagy jóváhagyta a hivatkozást. **Nincs a GDPR-ban minden adatra egységes megőrzési szám**. Ha ilyen alapérték nem határozható meg, a konfiguráció nem állíthat be ellenőrizetlen „jogi” időtartamot: a megrendelő választja ki/dokumentálja a megfelelő időt vagy a megőrzés felülvizsgálati eljárását. Önkényes automatikus törlés nincs.
- **Külső felelősség:** a megrendelő saját adatkezelési/jogi felelőse köteles ellenőrizni az adatkezelési jogalapot, tájékoztatást, megőrzési/törlési időket, érintetti kérelmek teljesíthetőségét és a szükséges hozzájárulási folyamatot. A funkciók korlátozott projektscope-ja **nem jelenti az adatkezelő jogi kötelezettségeinek megszűnését**. Ha a meglévő eszközökkel nem teljesíthető kötelező adatvédelmi funkció, azt hiányként jelezzük és **külön megbízás/scope-döntés** tárgyává tesszük, nem tekintjük csendben késznek.
- **Nincs új automatikus anonimizálási/törlési motor.** Nem távolítunk el kötelező üzleti auditot vagy számlázási adatot felületi kérésre; az adatkezelő által előírt jogszerű megőrzés és érintetti kérelemkezelés külön vizsgálandó. A technikai hozzáférésvédelem, adatminimalizálás, privacy-by-design és a meglévő WP-adatvédelmi funkciók **nem kerülnek kikapcsolásra**.
- **Technikai átadási ellenőrzés:** dokumentáljuk, mely új adatok keletkeznek (chat, szavazat, értesítések, profil/QR/audit), melyik meglévő rendszer tárolja őket, milyen kapcsolódó beállítások léteznek, és hol hiányzik az adatkezelői döntés. Ez **technikai adatleltár**, nem jogi vélemény és nem vállalás külön export-/erase-integráció fejlesztésére.

**Státusz:** a **projekthatár jóváhagyott**, a megrendelő által megadandó/jóváhagyandó tényleges megőrzési idők és kötelező adatvédelmi követelmények **külön külső feladatok**. Az éles indulás előtt az adatkezelő felelősségi körében kell rendezni őket; ez nem automatikus saját fejlesztésre szóló megrendelés.

**Automatikus előfizetés részletszabályai – ELHALASZTVA, ELFOGADOTT DÖNTÉS (2026. október 16.)**

**Jóváhagyott döntés:** a sikertelen **automatikus** terhelés utáni újrapróbálkozások száma/ütemezése, a fizetési eszköz cseréje, az automatikus megújulási értesítések, a recurring előfizetés lemondása és hasonló életciklus-folyamatok **nem az MVP követelményei**. Ezeket **csak akkor specifikáljuk részletesen**, amikor a D09 szerint ténylegesen kiválasztandó, kész WooCommerce-kompatibilis előfizetési integráció funkcióit, licencét és költségeit megismertük, a megrendelő vállalta a költséget, és a későbbi bevezetésről külön döntöttünk. A kész megoldások ár/érték-felmérése továbbra is elvégzendő, de nem blokkolja a manuális MVP-t. Saját Barion recurring bridge nem fejlesztési feladat.

**Az MVP változatlanul kötelező része:** bejelentkezve megvásárolható egyszeri WooCommerce/Barion havi prémiumtermék weben és PWA-ban, hiteles fizetésből szerveroldali hozzáférés és `paid_through`, hozzáférés kizárólag a kifizetett időszak végéig, új időszak önálló megvásárlása; nincs ismétlődő terhelés, automatikus retry, kártyacsere vagy „előfizetés lemondása” gomb. Az UI ne sugalljon aktív automatikus előfizetést.

**D09-MVP / 01 – A manuális havi hozzáférés időtartama – ELFOGADVA (2026. október 16.)**

**Döntés:** egy **újonnan, aktív prémiumidőszak nélkül** megvásárolt havi hozzáférés a **hitelesen sikeres WooCommerce/Barion fizetés pillanatától** használható. A fizetés `Europe/Budapest` szerinti **helyi dátumához pontosan egy naptári hónapot** adunk. Ha az eredeti hónap napja a célhónapban nem létezik, a célhónap utolsó létező napját használjuk (**hónapvégi clamp**). A hozzáférés **a kiszámolt lejárati nap végéig** él magyar helyi idő szerint, nem 30 × 24 óráig és nem az eredeti fizetési óra-percig.

**Technikai határ:** az adatbázisban `paid_through` a lejárati napot **követő helyi nap 00:00** pillanata UTC-re konvertálva, **kizárólagos felső határ**. Hozzáférés akkor van, ha a szerver `now < paid_through` feltételt teljesíti, és nincs egyéb jogosultsági tiltás. Nem fix 30 napot, 24 órás egységeket vagy kliensoldali időszámítást használunk. A megbízható `paid_at` és a rendeléstétel feldolgozása idempotens; minden új jogosultság a fizetett order itemhez kötött. A `Europe/Budapest` DST-átállásait és szökőévet tesztelni kell.

**Példa (nem szökőév):** január 31-én 10:00-kor sikeres fizetés → február 28. **helyi nap végéig** használható; `paid_through` március 1. 00:00 magyar helyi idő, UTC-ként tárolva. Február 29-i cél vagy októberi óraátállás ugyanígy helyi naptárral számolandó.

**Az időtartam és előrevásárlás külön elfogadott:** a /01 határozza meg az egy hónap fogalmát; az **elfogadott /02** a már aktív jogosultságot az eredeti naptári fordulónaphoz igazított, felhalmozódó hónapokkal hosszabbítja. A lejáratról küldött külön értesítés **D09-MVP/03** továbbra is nyitott. A D02 jegy-/bérletszabályok nem változnak.

**D09-MVP / 02 – Előre újravásárlás és időszakok összeadása – ELFOGADVA (2026. október 16.)**

**Döntés:** ha az ügyfélnek a hiteles fizetéskor még aktív manuális prémiumjoga van, minden újonnan **sikeresen kifizetett havi rendeléstétel további egy naptári hónappal hosszabbítja meg** a meglévő kifizetett jogosultságot, **az eredeti havi fordulónap megőrzésével**. Az új vásárlás nem indít a fizetési dátumon átfedő időszakot, és nem veszik el a már kifizetett idő.

- **Eredeti fordulónap (anchor):** az új folyamatos hozzáférési sorozatot megkezdő első hiteles `paid_at` `Europe/Budapest` szerinti helyi **napját** (például 31.) megőrizzük. Minden hosszabbítás **az eredeti kezdő helyi dátumhoz a teljes, eddig kifizetett hónapszám hozzáadásával** számolja a lejárati dátumot, a célhónap végére igazítva, ha ott nincs megfelelő nap. **Nem az előző, esetleg lerövidült februári 28/29. naphoz adunk újabb hónapot.**
- **Példa, nem szökőév:** első fizetés január 31. → február 28. **végéig**; új fizetés február 20-án, amíg még aktív → március 31. **végéig**; további előrevásárlás → április 30. **végéig**. Február 28. nem írhatja felül az eredeti **31-i fordulónapot**.
- **Lejárt hozzáférés:** ha az előző időszak a következő sikeres fizetéskor **már lejárt** (`paid_at >= paid_through`, illetve nincs aktív jogosultság), az új, önálló hónap **a fizetés dátumától** indul és **új fordulónapot** hoz létre; a régi, már lejárt hónapokhoz nem adódik hozzá.
- **Több vásárlás, duplikáció, verseny:** minden igazolt és jogosult WooCommerce-rendeléstétel pontosan egyszer adhat **egy** hónapot. Azonos rendeléstétel ismételt callbackje, háttérjobja vagy kétszeri feldolgozása nem hosszabbíthat újra; párhuzamos eltérő vásárlások tranzakciósan, forrás-azonosítóval, zárolással és egyeztethető időszaktörténettel dolgozandók fel. A sikertelen vagy még függő fizetés nem ad időt. Késve beérkező webhooknál a tényleges hiteles fizetési idő és az eddig jóváírt sorozat ellenőrzése szükséges, nem pusztán a callback beérkezési sorrendjét követjük.
- **Technikai lejárat:** az így számolt célhelyi nap **végéig** tart az elérés; a `paid_through` az azt **követő magyar helyi nap 00:00-ja** UTC-re konvertálva (**kizárólagos felső határ**). `Europe/Budapest`, szökőév, hónapvég és DST változatlanul érvényesek. A kliens csak a szerver által megállapított állapotot/lejáratot mutatja.
- **Refund/chargeback:** a **D07 elfogadott** szabályai érvényesek; nincs automatikus, kontrollálatlan visszadátumozás vagy már felhasznált hónap visszavonása. Csak egyértelmű, teljes és **még fel nem használt** időszak automatikus korrekciója engedhető meg, egyébként auditált kézi ügyintézés.
- **A D09-MVP/03 lejárati figyelmeztetés módja továbbra is NYITOTT**. A D09-MVP/02 elfogadása nem jelent automatikus megújítást vagy terhelést.

**Státusz:** az eredeti havi fordulónapot megőrző, felhalmozódó manuális újravásárlás **jóváhagyott MVP üzleti szabály**. Megvalósítási és tesztkapu M6/MF09, T08–T09.

**D09-MVP / 03 – Lejárati tájékoztatás – ELFOGADVA (2026. október 16.)**

**Döntés:** az MVP-ben a manuálisan megvásárolt prémium-hozzáférés **pontos lejárati helyi dátuma a PWA-ban mindig látható**; a lejáratig hátralévő **utolsó 7 napban kiemelt, alkalmazáson belüli figyelmeztetés** és egyértelmű **„Újravásárlás”** lehetőség jelenik meg. A figyelmeztetés nem külön üzenetkampány vagy küldési folyamat, hanem a PWA szerveradatból megjelenített állapota.

- **Nincs automatikus lejárati e-mail és nincs automatikus lejárati push** az MVP-ben; sem 3 nappal a lejárat előtt, sem más ütemezéssel. Nincs reminder-job, új WP e-mail-sablon vagy D06 push-kampány erre a célra. Más üzleti események meglévő, jóváhagyott e-mail/push folyamatait ez nem tiltja.
- A PWA a szerver által számolt **`paid_through` (UTC kizárólagos határ)** alapján a tényleges `Europe/Budapest` **helyi lejárati napot** és az aktív/lejárt státuszt mutatja. Az **utolsó hét napban** fokozottan kiemeli a közelgő lejáratot; a végső, határpillanat utáni állapot „lejárt”, újravásárlási lehetőséggel. A React önállóan nem számol hozzá további hónapokat.
- **Előrevásárlás után** a D09-MVP/02 szerint meghosszabbított új `paid_through` lesz az egyetlen irányadó; a korábbi dátumra mutató figyelmeztetés megszűnik, és a következő hét napos időszakig nem jelenik meg újra. Többszörös fizetési callback sem okozhat tévesen új figyelmeztetést.
- A lejárati státusz minden belépéskor és releváns hozzáférésváltozáskor frissítendő; időközbeni státuszváltozásnál ne maradjon elavult kiemelés. Az egyszeri vásárlást **nem** nevezzük automatikusan megújuló előfizetésnek. A meglévő webes fiókoldal esetleges módosítása a korábban elfogadott **D01 szerint külön felmérés/scope**, nem e döntésben jóváhagyott webes UI-fejlesztés.

**Státusz:** **D09-MVP/01, /02 és /03 mindhárom üzleti részletszabálya ELFOGADVA**. A D09-MVP funkcionális döntéssora lezárt; az M6/MF09 implementáció és T08–T09 elfogadási tesztek, az aktuális prémiumtermék ára/leképezése és a meglévő webes fiókélmény ellenőrzése végrehajtandó. Az automatikus recurring integráció beszerzése/szabályai továbbra is feltételes későbbi döntések.
