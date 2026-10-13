**1. Az érdemi implementálás elején eldöntendő kérdések**

**D01 – Termékkínálat**

Megválaszolandó kérdés: A régi Online Ringató termékek csak az appból tűnnek el, vagy a webshopból is? Hol jelennek meg az új előfizetés- és eseménytermékek?

A terv javaslata: A RINGI04/05/06 termékeket csak a PWA-ból zárjuk ki; a webshop marad változatlan. Az új apptermékek legyenek rejtve a WooCommerce nyilvános katalógusában, de elérhetők az appból.

**D09 – Előfizetés**

Megválaszolandó kérdés: Van bizonyított Barion–WooCommerce Subscriptions integráció, vagy saját összekötő bővítményt kell fejleszteni? Ki biztosítja a Subscriptions licencet és a Barion ismétlődő terhelési jogosultságát?

A terv javaslata: Először kész integrációt vizsgáljunk sandboxpróbával. Ha nincs megfelelő megoldás, saját bridge szükséges.

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

A terv javaslata: Ezeket a Subscriptions–Barion integráció részeként kell konkretizálni. Sikertelen megújítás nem hosszabbítja meg automatikusan a hozzáférést; lemondáskor a már kifizetett időszak végéig megmarad a hozzáférés.
