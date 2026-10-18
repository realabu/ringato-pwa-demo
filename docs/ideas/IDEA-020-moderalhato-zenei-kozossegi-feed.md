---
id: "IDEA-020"
title: "Moderált közösségi feed zenei élményekhez"
area: "Közösség"
lane: "later-feature"
status: "elemzett"
moscow: "Could"
effort_size: "XL"
effort_min_days: 26
effort_max_days: 60
user_value: 4
operations_value: 1
revenue_value: 3
communication_value: 5
risk: "magas"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF04","MF12","MF13"]
created: "2026-10-19"
updated: "2026-10-19"
origin: "Szabad szöveges ötlet – 2026-10-19"
communication_angle: "„A hét közös zenés pillanata” – elsőként csak kifejezetten engedélyezett, szerkesztett történetekkel."
---

# Moderált közösségi feed zenei élményekhez

## Eredeti felvetés

> közösségi felület, például egy közös feed ahova zene élményeket lehetne postolni. Ezt is be lehet építeni a gamificationbe a használatát.

## Megoldandó probléma

A foglalkozáson túli közösségi élmények megosztása növelhetné az összetartozást, de egy közös hírfolyam nyilvánosabb és moderációigényesebb, mint az MVP személyes üzenetküldése. A gyermekes közösségben az adatvédelmi és biztonsági alapbeállítás különösen fontos.

## Megoldási változatok

- A – Virág által publikált közösségi élményposztok, családoktól kizárólag privát javaslatfogadással; hozzászólás és képfeltöltés nélkül (ajánlott első pilot).
- B – Bejelentkezett felnőttek előmoderált, szöveges zenei élményposztjai, jelentés, visszavonás, szabályzat, opcionális becenév és időben rendezett feed.
- C – Követhető témák, reakciók, képfeltöltés és önkéntes, alacsony súlyú aktivitásjelvény az IDEA-007-ben; moderációs és gyermekadat-védelmi eredmény után.

## Technikai hatás, előzetes hipotézis

- Saját WordPress CPT/kompatibilis moderálható tartalomstruktúra, szerzői jogosultság, draft/pending/published/rejected státusz és spamkorlát; ACF Free a szerkesztői szövegekhez.
- A D11/MF12 Better Messages privát üzenetfunkció nem alakítható automatikusan publikus közösségi feeddé. Feed API, médiafájl-jogosultság és moderátori queue külön fejlesztés.
- Minden beküldéshez kifejezett szabályelfogadás, „jelentem”, tiltás és szerkesztői levétel; a gyermekeket azonosító helyszín/fotó/adat alapból tiltandó vagy külön ellenőrzendő.

## Kockázatok és függőségek

- Gyermekfotók, valódi nevek, lokáció és megosztott érzékeny családi történetek; a posztoló szülő nem feltétlenül jogosult minden képen szereplő gyermek adatát publikálni.
- Folyamatos moderációs kötelezettség, zaklatás, spam, konfliktus és platformfelelősség; közösségkezelő kapacitás nélkül nem indítható nyílt feed.
- Játékos pontozás a gyakori posztolásért spamet és túlmegosztást ösztönözhet; önmagában a posztok száma alapján ne adjunk kupont.

## Példa elfogadási feltétel

- Beküldött poszt alapértelmezetten nem nyilvános, csak jogosult moderátor hagyhatja jóvá; a visszavont poszt nem tér vissza cache-ből.
- Jelentés és tiltás működik, sértő vagy gyermekadatot közlő tartalom gyorsan elrejthető; idegen fiók nem szerkeszthet más posztot.
- A feed és a meglévő privát üzenetfolyam szigorúan elkülönül; gamification csak külön opt-in és spamvédelmi szabály után.

## Előzetes ráfordítás és értékelés

- Besorolás: later-feature; státusz: elemzett, nem elfogadott; MoSCoW: Could. Nem vállalt MVP-hiba vagy alapvető UX-scope.
- XL (26–60 AI-val támogatott fejlesztői munkanap) kizárólag a B változat prototípusának durva, alacsony bizonyosságú hipotézise, nem árajánlat vagy határidő. A privát fejlesztői forrás közvetlen auditja nem történt meg.
- Szubjektív értékhipotézisek (1–5): ügyfél 4, üzemeltetés 1, bevétel 3, kommunikáció 5. Kockázat: magas.
- RICE-pontszám nincs: Reach, Impact, Confidence és Effort megalapozott bemenetei hiányoznak. A C változat, külső szolgáltató, pedagógiai tartalom, fizikai előállítás, marketing és üzemeltetés külön becslendő.

## Virágnak szóló rövid ajánlat

Lehetne egy inspiráló közös tér, ahol a családok zenei pillanatokat osztanak meg. Elsőként a Virág által gondozott, biztonságos feedet próbálnánk ki, nem moderálatlan közösségi oldalt.

## Negyedéves kommunikációs lehetőség

„A hét közös zenés pillanata” – elsőként csak kifejezetten engedélyezett, szerkesztett történetekkel. Kommunikációs hipotézis, nem jóváhagyott publikáció, megrendelés vagy vállalt dátum.

## Következő ellenőrzendő lépés

Virággal tisztázni, tud-e moderátori kapacitást biztosítani, elfogadható-e képek nélküli pilot, és milyen közösségi szabályzatot hagy jóvá az adatkezelő.

## Kapcsolódás a fejlesztéshez

IDEA-007 önkéntes közösségi jutalmazás külön szabály; IDEA-021 Virág által szerkesztett kulturális ajánlók más tartalomfajta. MF12 privát üzenet funkcióját nem változtatja át nyilvános feeddé.

A vállalt MF01–MF14 és a jóváhagyott D-döntések változatlanok. Új gyermekadat, új integráció, külső költség és szerkesztői/marketingközlés csak külön emberi jóváhagyás után. A PWA szerkesztői tartalmai WordPressből, ACF Free mezőkből kezelendők.
