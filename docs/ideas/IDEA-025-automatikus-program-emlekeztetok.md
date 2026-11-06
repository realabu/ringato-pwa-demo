---
id: "IDEA-025"
title: "Automatikus emlékeztetők a következő Ringató-programról"
area: "Értesítések és részvétel"
lane: "later-feature"
status: "elemzett"
moscow: "Should"
effort_size: "L"
effort_min_days: 11
effort_max_days: 25
user_value: 5
operations_value: 4
revenue_value: 3
communication_value: 4
risk: "magas"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF05","MF07","MF08","MF13"]
created: "2026-11-06"
updated: "2026-11-06"
origin: "Szabad szöveges felhasználói ötlet – 2026-11-06"
communication_angle: "„Holnap találkozunk a Ringatón!” – próbaüzenet a valóban jelentkezett családoknak, külön jóváhagyás után."
---

# Automatikus emlékeztetők a következő Ringató-programról

## Eredeti felvetés

> automatikus push üzenet küldés következő programról a jelentkezetteknek vagy szokásos résztvevőknek

## Megoldandó probléma

A foglalással rendelkező családok elfelejthetik a következő időpontot. A rendszeresen járó, de adott alkalomra nem jelentkezett családok megszólítása viszont nem tranzakciós emlékeztető, hanem személyre szabott ösztönzés: a címzetteket, a gyakoriságot és az értesítési jogosultságot külön kell meghatározni. A D06 ma kézzel indított adminpush-t ír elő; az eseményvezérelt automatikus küldés nem a jóváhagyott MVP része.

## Megoldási változatok

- **A** – Csak ténylegesen foglalt/jeggyel rendelkező, az eseményhez egyértelműen kötött résztvevőnek egyszeri, előre beállítható eseményemlékeztető, első lépésként kizárólag appbeli értesítéssel és külön opt-in kontrollal.
- **B** – A változat mellett időzített web push az erre külön feliratkozott eszközöknek, beállítható küldési idővel (például előző nap – szemléltető érték), módosítás/lemondás/törlés esetén ellenőrzött visszavonási vagy újratervezési szabállyal. Elsőként ezt csak szűk pilotban teszteljük.
- **C** – Szokásos résztvevőknek ajánló a korábbi részvétel és önként megadott érdeklődési település alapján, külön marketinghozzájárulással és gyakorisági plafonnal; a preferált program nem egyenlő foglalással.

## Technikai hatás, előzetes hipotézis

- MF08 foglalás- és eseményállapotából képzett szerveroldali címzetthalmaz, felhasználónként, eseményenként és értesítéstípusonként egyszeri, idempotens küldési kulccsal; felhasználói ellenőrzés nélkül, puszta QR-nézetből nem következtethető biztos részvétel.
- A szerverben a foglalás törlése, esemény áthelyezése/lemondása, fizetési hold lejárata, késő fizetés és státuszmódosulás újraellenőrzése a küldés pillanatában; ne menjen emlékeztető olyan eseményre, amelyre nincs jogosultság vagy érvényes foglalás.
- MF13 D06 infrastruktúra (fiókszintű inbox, jóváhagyott push-opt-in és címzettpillanatkép) újrahasznosítása; saját ütemező és határidő-feldolgozás, cron/Action Scheduler esetén tényleges megbízhatósági próba, időzóna Europe/Budapest és DST.
- Az „általában jár ide” célcsoport külön adatminimalizálási és jóváhagyási kapu: családi részvétel ne profilozzon gyermekeket, ne legyen automatikus kézi WP-csoporttagság átírás; opcionálisan IDEA-023 önként választott településszűrő használható.
- Minden új felirat, sablon és beállításszöveg WordPress/ACF Free szerkeszthető. A tényleges küldési logika, jogosultság és limit nem kerül ACF-tartalommezőbe.

## Kockázatok és függőségek

- Értesítési beleegyezés: az appbeli inbox nem azonos az OS pushengedéllyel; platformonkénti opt-in, visszavonás és tájékoztatás tisztázandó. Az automatikus ajánló különösen könnyen marketingüzenetnek minősülhet.
- Duplázott, már lemondott vagy hibás helyszínhez rendelt emlékeztető; cron-kimaradás és párhuzamos jobfutás. A push kézbesítése nem garantált, ezért az appbeli eseménynézet marad a hiteles információ.
- Rendszeres résztvevők kiválasztásánál túlzott profilozás, gyerekadatok és területi téves pozitívumok, értesítési fáradtság; dönteni kell a manuális csoport- és automatikus címzés kapcsolatáról.
- D09 prémiumlejárati automatikus e-mail/push és D13 szavazási értesítés továbbra is kizárt az MVP-ben; az ötlet nem kapcsolja be ezeket.

## Példa elfogadási feltétel

- Lemondott vagy áthelyezett eseményhez nem érkezik téves „holnap találkozunk” push; a küldés előtt a foglalás és az esemény friss státuszát ellenőrzi a szerver.
- Ugyanaz a címzett ugyanarra az eseményre ugyanazzal a szabállyal csak egyszer kap üzenetet, párhuzamos cron/retry mellett is; az üzenet saját eseményrészletre mutat, session nélkül biztonságos login után.
- Push csak aktív feliratkozás/megfelelő hozzájárulás mellett, opt-out után nincs új push; appbeli receipt és fiókhozzáférés a jóváhagyott D06 szerint.
- A rendszeres résztvevő marketingajánlása külön kapcsolható, nem tüntet fel foglalást, ha ilyen nincs. Tesztelt Europe/Budapest nyári/téli időváltás és cron-késés.

## Előzetes ráfordítás és értékelés

- **Besorolás:** later-feature; MoSCoW Should; státusz elemzett (nem elfogadott fejlesztési megrendelés).
- **Durva hipotézis:** L (11–25 AI-val támogatott munkanap) az első valós B-variáns prototípusára, a WordPress/PWA meglévő implementációjának auditja nélkül. Külső díj, marketing, üzemeltetés, licenc és teljes kiadás nincs benne. Becslési bizonyosság alacsony; nem ár vagy határidő.
- **Szubjektív értékhipotézis (1–5):** ügyfél 5, üzemeltetés 4, bevétel 3, kommunikáció 4. Kockázat: magas. RICE nincs, mert a reach, impact, confidence és effort megalapozott számai hiányoznak.

## Virágnak szóló rövid ajánlat

A jelentkezett családok egy kedves, automatikus emlékeztetőt kaphatnának a következő közös zenélésről. A rendszeres látogatóknak pedig később csak külön beleegyezéssel ajánlhatunk új alkalmakat. Így nem keverjük össze a meglévő foglalásról szóló tájékoztatást a marketinggel.

## Negyedéves kommunikációs lehetőség

„Holnap találkozunk a Ringatón!” – próbaüzenet a valóban jelentkezett családoknak, külön jóváhagyás után. Nem jóváhagyott kommunikáció, kampány vagy vállalt negyedéves szállítás.

## Következő ellenőrzendő lépés

Virággal eldönteni, mely részvételi állapot számít biztos jelentkezésnek; milyen nap/időpont jó; mely értesítés tranzakciós és mely marketing; célkör és opt-in szabály, majd pilot teszteseménnyel.

## Kapcsolódás a fejlesztéshez

D06/MF13 ma kézi küldés és kézi csoporttagság, automatikus eseménykiváltás nincs jóváhagyva. D05/MF08 foglalási státuszok és MF07 jegyek a hiteles adatforrások. IDEA-026 a Virág által szerkesztett időzített kampány; IDEA-023 település-preferencia legfeljebb későbbi marketingcélzás, nem foglalási bizonyíték.

A már elfogadott MF01–MF14 és D01–D13 döntések változatlanok. Új automatikus művelet, időzítés, személyesadat-kezelés, külső költség és TV/platformterjesztés csak külön megrendelői döntés után.
