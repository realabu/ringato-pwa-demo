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
- Nyitott részletszabályok: pontos havi időszak és újravásárláskor időszak-összeadás, lejárati tájékoztatás, webes fiókoldalon megjelenítés, a kész ajánlat(ok) árai és jóváhagyása. **A manuális MVP-hez nem szükséges kártyacsere, automatikus újrapróbálkozás vagy előfizetés-lemondás**; az automatikus opcióhoz majd igen.

**Specifikációs hatás:** a V1.3 F08–F09 eredeti automatikus megújulás/lemondás követelménye az MVP-ben nem kötelező; feltételes későbbi cél, a specifikáció következő kiadásában átvezetendő. A D09 üzleti irány lezárt, a kész megoldás költség- és megvalósíthatósági vizsgálata és megrendelői döntés nyitott.

**D12 – Környezet és fiókkezelés – ELFOGADOTT IRÁNY, RÉSZFELADATOK NYITVA (2026. október 15.)**

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

**Státusz:** irány jóváhagyva; **tárhely PWA-szintű alkalmassága és a tesztkörnyezet rendelkezésre állása megerősítve**, de streamingkapacitás, regisztrációs folyamat és staging telepítési/terhelési eredmények még vizsgálandók. **A lenti második „D12 – Adatkezelés és megőrzés” önálló, továbbra is nyitott döntés, nem része ennek a jóváhagyásnak.**

**D13 – „Virág kérdezi” szavazás – ELFOGADVA, V1 KÖTELEZŐ FUNKCIÓ (2026. október 15.)**

Eredeti kérdés: Bekerüljön-e a „Virág kérdezi” szavazás az első verzióba?

**Döntés:** **Igen. A „Virág kérdezi” szavazás része az első éles verziónak és az MVP elfogadási feltételeinek.** Nem csupán prototípus-látványelem vagy későbbi opció.

**Javasolt megvalósítási minimum, az implementáció előtt ellenőrizendő részletszabályokkal:**
- Virág WordPress adminfelületen hozhat létre és kezelhet kérdéseket, válaszlehetőségeket és a szavazás nyitott/zárt állapotát; a megjelenítés az új PWA-ban történik.
- Bejelentkezett felhasználók szavazhatnak; ajánlott kezdeti szabály: **egy fiók egy válasz egy szavazáson**, szerveroldali egyediséggel és jogosultság-ellenőrzéssel. A lezárt szavazás nem fogad új választ.
- Az alkalmazás megjeleníti, hogy a felhasználó szavazott-e, és szükség esetén összesített eredményeket mutat; az eredmények láthatósága kezdeti javaslat szerint WordPress adminban állítható.
- Biztosítani kell a szavazat tárolását, az ismételt kérés/idempotencia és párhuzamos kattintás kezelését, valamint a mobilos üres, betöltés, hiba és lezárt állapotokat.
- **Nem üzletileg jóváhagyott részletszabály még:** lehet-e válaszát módosítani; egyszerre hány szavazás lehet aktív; pontos eredményláthatóság, időzítés és az esetleges értesítés. Ezeket egyszerű alapértelmezéssel, Virággal/fejlesztővel a modul implementálása előtt egyeztetni kell, a V1-bekerülés ténye nem nyitott.

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

**Státusz:** megvalósítási irány jóváhagyva; a tényleges teszt eredménye még nyitott. A chat adatmegőrzési kérdése a külön D12 adatkezelési döntés része.

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
- **365 napos előzmény:** az alkalmazás a **megelőző 365 nap címzett értesítéseit jeleníti meg**, fiókonként, szerveridővel számolva. **A mögöttes adatbázisrekordok tényleges törlési/megőrzési határideje, exportálása, hozzájárulási szövege és a kommunikáció jogalapja továbbra is a külön D12 adatkezelési döntésben tisztázandó.** A 365 nap nem általános adatmegőrzési szabály, nem jelent önmagában adatbázis-törlési felhatalmazást.
- **Pushengedély bekérése:** **nem** az alkalmazás első megnyitásakor ugrik fel automatikusan. Csak jól érthető, **a felhasználó által indított** műveletből kérjük az OS/böngésző engedélyét; elutasítás után nem ismételjük automatikusan. Az appbeli értesítések ehhez nem kötöttek.
- **Nyitott implementációs/adatkezelési feladatok:** Virág kezdeti csoportnevei/tagsági szabályai; WordPress-admin küldési előnézet; eszköz- és fiókváltás; opt-in/opt-out; jogosultság, több eszköz és hibás push végpont; D12 szerinti adatvédelmi szabályok és megőrzés.

**Státusz:** a D06 funkcionális döntés lezárt; az admin/címzettcsoportok konkrét beállítása, push-tesztje és a külön D12 adatkezelési kérdés nyitott.

**3. Továbbra is nyitott üzleti és adatkezelési kérdések**

A D09 manuális prémium időszak-/újravásárlási/lejárati részletei, a D10 szolgáltatóválasztás és a D13 szavazási részletszabályai a fenti fejezetek szerint szintén nyitottak. Az elfogadott D06 kezdeti csoportlistája még rögzítendő; a technikai próbák nem új üzleti döntések.

**D08 – Régi jegyek, bérletek és vendégrendelések átvezetése**

Megválaszolandó kérdés: Honnan tudjuk a papírbérletek maradék alkalmait, első használatát és a régi jegyek beváltását? Hogyan rendelünk korábbi vendégvásárlást egy felhasználói fiókhoz? Mi lesz az átállás időpontja?

A terv javaslata: Csak igazolt adatokból keletkezzen aktív digitális jogosultság. A bizonytalan esetek kézi ellenőrzésre kerüljenek, aktív QR nélkül. A vendégrendelés hozzárendelése igazolt folyamatban történjen; önmagában az e-mail-cím egyezése nem elegendő.

**D12 – Adatkezelés és megőrzés**

Megválaszolandó kérdés: Meddig őrizzük meg a chatüzeneteket, auditnaplókat és egyéb adatokat? Milyen hozzájárulási szövegek, exportálási és törlési folyamatok szükségesek?

A terv javaslata: Az egyes adattípusokra külön megőrzési szabály készüljön, adatkezelési felelőssel egyeztetve. A pushelőzmény 365 napja nem általános adatmegőrzési idő.

**Az előfizetési modul további részletei**

Megválaszolandó kérdés: Sikertelen terhelés után mikor és hányszor próbálkozunk újra? Hogyan értesítjük az ügyfelet, és hogyan cserélhet fizetési eszközt?

D09 után **csak feltételes, későbbi automatikus előfizetési integrációhoz** döntendők el: az újrapróbálkozások, kártyacsere, értesítés, lemondás. A manuális havi MVP-ben nincs automatikus terhelés, így sikertelen automatikus renewal vagy kártyacsere folyamat sincs; a felhasználó maga vesz újabb hozzáférési időszakot. A már kifizetett időszak végéig tartó hozzáférés, a lejárat és az ismételt vásárlás kezelése az MVP része.
