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

**D11 – Chat**

Megválaszolandó kérdés: Megfelel-e a Better Messages ingyenes REST/AJAX megoldása, vagy szükséges a fizetős WebSocket változat?

A terv javaslata: Korai integrációs próba az ingyenes megoldással; aktív chatképernyőn 10 másodperces frissítés. A WebSocket opcionális.

A média és a chat végleges megoldása később is lezárható, de a megvalósíthatósági próbájukat már az elején érdemes elvégezni.

**2. Az érintett modul implementálása előtt lezárandó kérdések**

**D02 – Jegyek és bérletek érvényessége**

Megválaszolandó kérdés: Pontosan mikortól számít az érvényesség, és a lejárati nap mely időpontjáig tart? Hogyan kezeljük a hónapvégi dátumokat?

A terv javaslata: A jegy érvényessége a hiteles sikeres fizetéstől, a bérleté az első sikeres beváltástól számítson. Budapesti idő szerint a cél nap végéig tartson; ha a célhónapban nincs megfelelő nap, annak utolsó napját használjuk.

**D03 – Beváltás és alkalomlevonás**

Megválaszolandó kérdés: Ugyanazon programon lehet-e több alkalmat levonni egy bérletből? Van-e napi korlát? Hogyan kezeljük, ha valaki kilép, majd visszatér?

A terv javaslata: Egy jegy/bérlet egy konkrét eseményen egyszer váltható be. Visszatéréskor csak a korábbi belépést ellenőrizzük, új alkalmat nem vonunk le. Külön eseményen új alkalom használható.

**D04 – Családmodell**

Megválaszolandó kérdés: Egy fiók egy családot jelent? Használhat két szülő külön fiókot ugyanahhoz a családhoz? Lehet jegyet átadni vagy más családnak vásárolni?

A terv javaslata: V1-ben egy fiók egy család, nincs jegyátruházás, és eseményenként legfeljebb egy családi foglalás lehet. Több család kezelése kézi ügyintézéssel történjen.

**D05 – Foglalási és beléptetési szabályok**

Megválaszolandó kérdés: Meddig mondható le egy foglalás? Mennyi ideig tartjuk fenn a helyet fizetés közben? Mikortól és meddig engedélyezett a beléptetés? Kell-e várólista?

A terv javaslata: Nincs várólista. Az alapdíjas foglalás a program kezdetéig lemondható. Fizetés közben 15 percig tartjuk fenn a helyet. A beléptetés a kezdés előtt 2 órától a befejezés után 2 óráig engedélyezett, eseményenként módosítható beállítással.

**D07 – Visszatérítés és chargeback**

Megválaszolandó kérdés: Mi történik részleges visszatérítés, már használt jegy/bérlet vagy banki visszaterhelés esetén? Mikor vonjuk vissza a jogosultságot, szabadítjuk fel a helyet vagy adunk vissza alkalmat?

A terv javaslata: A fel nem használt jogosultságot visszavonjuk; külön áras eseménynél a hely felszabadul. A használt és részleges visszatérítési esetek kézi ellenőrzést igényelnek. Nincs automatikus alkalom-visszaadás.

**D06 – Pushértesítések és címzettcsoportok**

Megválaszolandó kérdés: Az előzményben minden megcímzett értesítés látszik, vagy csak a ténylegesen kézbesített push? Milyen címzettcsoportok lesznek, és milyen hozzájárulással kezeljük őket?

A terv javaslata: Minden címzett fiókjában legyen appbeli előzmény, a push kézbesítése külön állapotként szerepeljen. Egy fiókhoz egy közös előzmény tartozzon, 365 napos megőrzéssel. A kezdeti csoportokat Virág határozza meg.

**D08 – Régi jegyek, bérletek és vendégrendelések átvezetése**

Megválaszolandó kérdés: Honnan tudjuk a papírbérletek maradék alkalmait, első használatát és a régi jegyek beváltását? Hogyan rendelünk korábbi vendégvásárlást egy felhasználói fiókhoz? Mi lesz az átállás időpontja?

A terv javaslata: Csak igazolt adatokból keletkezzen aktív digitális jogosultság. A bizonytalan esetek kézi ellenőrzésre kerüljenek, aktív QR nélkül. A vendégrendelés hozzárendelése igazolt folyamatban történjen; önmagában az e-mail-cím egyezése nem elegendő.

**D12 – Adatkezelés és megőrzés**

Megválaszolandó kérdés: Meddig őrizzük meg a chatüzeneteket, auditnaplókat és egyéb adatokat? Milyen hozzájárulási szövegek, exportálási és törlési folyamatok szükségesek?

A terv javaslata: Az egyes adattípusokra külön megőrzési szabály készüljön, adatkezelési felelőssel egyeztetve. A pushelőzmény 365 napja nem általános adatmegőrzési idő.

**Az előfizetési modul további részletei**

Megválaszolandó kérdés: Sikertelen terhelés után mikor és hányszor próbálkozunk újra? Hogyan értesítjük az ügyfelet, és hogyan cserélhet fizetési eszközt?

D09 után **csak feltételes, későbbi automatikus előfizetési integrációhoz** döntendők el: az újrapróbálkozások, kártyacsere, értesítés, lemondás. A manuális havi MVP-ben nincs automatikus terhelés, így sikertelen automatikus renewal vagy kártyacsere folyamat sincs; a felhasználó maga vesz újabb hozzáférési időszakot. A már kifizetett időszak végéig tartó hozzáférés, a lejárat és az ismételt vásárlás kezelése az MVP része.
