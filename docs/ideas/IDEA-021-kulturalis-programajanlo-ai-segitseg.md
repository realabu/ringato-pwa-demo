---
id: "IDEA-021"
title: "Kulturális programajánló és AI-támogatott szerkesztés"
area: "Helyi programok és tartalom"
lane: "later-feature"
status: "elemzett"
moscow: "Should"
effort_size: "L"
effort_min_days: 11
effort_max_days: 25
user_value: 5
operations_value: 3
revenue_value: 4
communication_value: 5
risk: "magas"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF05","MF08","MF13"]
created: "2026-10-19"
updated: "2026-10-19"
origin: "Szabad szöveges ötlet – 2026-10-19"
communication_angle: "„Virág kulturális tippjei a hétre” – városi és környékbeli családi programok, igazolt forrásokkal."
---

# Kulturális programajánló és AI-támogatott szerkesztés

## Eredeti felvetés

> egy témába illő program ajánló felület viragtol, ahol esetleg egyedi kedvezmény kódokat is tud közölni. De ide gyűjthetne a város es a környék kulturális javaslatait. Ehhez lehetne valami automata AI support is ami naponta keres ilyet es előkészíti jóváhagyásra a program publikálását. Lehetne több körben bővíteni naptár nézettel ami korábban akar csak egy szűrhető feed.

## Megoldandó probléma

Virág a saját foglalkozásain túl értékes, környékbeli családbarát kulturális programokat ajánlhatna. Ma nincs erre külön szerkesztett, ellenőrzött ajánlófelület, és az automatikus webes programkeresés hibás dátumot, félrevezető kedvezményt vagy szerzői jogi problémát is okozhat.

## Megoldási változatok

- A – Virág által WordPressből szerkeszthető, címkékkel és helyszínnel szűrhető kulturális ajánlófeed, saját Ringató-programoktól megkülönböztetve (első ajánlott pilot).
- B – Strukturált ajánlók eseménydátummal, célkorosztállyal, térséggel, lejárati dátummal és ellenőrzött kedvezménykóddal; mobil naptár/listanézet, ICS/hivatkozás, szerkesztői kiemelés.
- C – Napi automatikus AI-alapú forrásfigyelés engedélyezett forrásokból, adatkinyerés, duplikációellenőrzés és „ellenőrizendő” WordPress-piszkozat; Virág minden publikációt kézzel engedélyez.

## Technikai hatás, előzetes hipotézis

- Javasolt külön WordPress programajánló CPT és ACF Free kompatibilis adatmezők (cím, forrás-URL, helyszín, dátum, relevancia, életkor, kedvezmény, lejárat, állapot, ellenőrzés ideje), a PWA-n szűrhető szerkesztői feed.
- MF05/MF08 meglévő saját események, helyfoglalás és jegyár logikáját nem módosítjuk: a harmadik felek kulturális eseményei külső linkre vezetnek, nincs automatikus Ringató-foglalás vagy jegyjog.
- Az AI csak jóváhagyott forrásjegyzékből készíthet ellenőrzendő piszkozatot, bizonyíték/forrásdátum és bizalmi státusz mellett; nincs automatikus publikáció, kuponkód-generálás vagy jogosulatlan scraping.
- A napi figyelés megbízható ütemezése külön infrastruktúra/cron és forrásjogi jóváhagyás kérdése; először kézi kezelést és importálható szerkesztői listát tesztelünk.

## Kockázatok és függőségek

- Programok időpontja, férőhelye, ára és kedvezménye bármikor változhat; egyedi kedvezménykódot csak hivatalos partneri megállapodással, érvényességellenőrzéssel közölhetünk.
- Szerzői jog, forrásoldal felhasználási feltétele, AI hallucináció és késve frissülő esemény; minden ajánláshoz kattintható elsődleges forrás és utolsó ellenőrzési nap kell.
- Fizetett ajánló vagy barter jól látható reklámjelölést igényel; ne keverjük szerkesztői javaslattal, kapcsolódás IDEA-010 partnerekhez.
- Adatvédelmi szempontból ne építsünk rejtett helymeghatározásra vagy személyes gyermekprofilból számolt célzásra.

## Példa elfogadási feltétel

- A WordPressből publikált, dátumozott kulturális program önálló ajánlófeedben látható, kategória/hely/dátum alapján szűrhető; lejárt esemény nem szerepel jövőbeli programként.
- Minden elemhez forráslink, ellenőrzési dátum, és ha kuponos, ellenőrzött kód/feltétel/lejárat tartozik; fizetett elhelyezés egyértelmű.
- Az AI által talált javaslat sosem válik publikussá külön szerkesztői jóváhagyás nélkül; hibás/duplikált adat elvethető és visszakereshető.
- Naptárnézet esetén időzóna és többnapos esemény működik, de a külső ajánló nem aktiválja a Ringató belépőjét vagy foglalását.

## Előzetes ráfordítás és értékelés

- Besorolás: later-feature; státusz: elemzett, nem elfogadott; MoSCoW: Should. Nem vállalt MVP-hiba vagy alapvető UX-scope.
- L (11–25 AI-val támogatott fejlesztői munkanap) kizárólag a B változat prototípusának durva, alacsony bizonyosságú hipotézise, nem árajánlat vagy határidő. A privát fejlesztői forrás közvetlen auditja nem történt meg.
- Szubjektív értékhipotézisek (1–5): ügyfél 5, üzemeltetés 3, bevétel 4, kommunikáció 5. Kockázat: magas.
- RICE-pontszám nincs: Reach, Impact, Confidence és Effort megalapozott bemenetei hiányoznak. A C változat, külső szolgáltató, pedagógiai tartalom, fizikai előállítás, marketing és üzemeltetés külön becslendő.

## Virágnak szóló rövid ajánlat

Készíthetünk egy Virág által válogatott, családbarát helyi kulturális ajánlót. Előbb egyszerű szűrhető feedként indulhat, később naptárral és egy AI-asszisztenssel, amely napi javaslatokat készít – Virág jóváhagyása nélkül semmi nem jelenik meg.

## Negyedéves kommunikációs lehetőség

„Virág kulturális tippjei a hétre” – városi és környékbeli családi programok, igazolt forrásokkal. Kommunikációs hipotézis, nem jóváhagyott publikáció, megrendelés vagy vállalt dátum.

## Következő ellenőrzendő lépés

Virággal a célvárost és vonzáskörzetet, megbízható programforrásokat, első kategóriákat és szerkesztői jóváhagyási folyamatot tisztázni; 10 kézzel bevitt ajánlással pilot.

## Kapcsolódás a fejlesztéshez

IDEA-010 partnerajánlatok és fizetett reklám eltér a független szerkesztői kulturális programválogatástól, de közös reklámjelölési szabály lehet. IDEA-012 országos marketingelemzés nem azonos a helyi programajánlóval. MF05/MF08 saját programjai nem importálódnak automatikusan külső foglalássá.

A vállalt MF01–MF14 és a jóváhagyott D-döntések változatlanok. Új gyermekadat, új integráció, külső költség és szerkesztői/marketingközlés csak külön emberi jóváhagyás után. A PWA szerkesztői tartalmai WordPressből, ACF Free mezőkből kezelendők.
