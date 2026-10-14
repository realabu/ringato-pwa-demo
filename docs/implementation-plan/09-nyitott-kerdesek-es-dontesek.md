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

**D12 – Környezet és fiókkezelés**

Megválaszolandó kérdés: Mi a végleges domain, hol lesz a staging tesztkörnyezet, és alkalmas-e a tárhely az alkalmazás működtetésére? Hogyan regisztrálhat új ügyfél?

A terv javaslata: A PWA a meglévő weboldallal azonos domainen, az `/app/` útvonalon működjön, a meglévő WordPress/WooCommerce bejelentkezést és fiókkezelést használva. A regisztráció jelenlegi beállításait ellenőrizni kell.

**D13 – A V1 funkciói**

Megválaszolandó kérdés: Bekerül-e a „Virág kérdezi” szavazás az első verzióba?

A terv javaslata: Alapból kimarad; csak külön igen döntéssel kerül be.

**D10 – Média**

Megválaszolandó kérdés: Melyik privát tárhely/CDN szolgáltatja a tartalmakat? Mennyi audio- és videóanyaggal, várható forgalommal és költségkerettel számolunk?

A terv javaslata: Privát médiatároló, rövid életű, aláírt hozzáféréssel. A prémium tartalom ne a WordPress publikus feltöltési könyvtárába kerüljön.

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
