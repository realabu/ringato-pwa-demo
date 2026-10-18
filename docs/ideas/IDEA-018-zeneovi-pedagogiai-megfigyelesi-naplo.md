---
id: "IDEA-018"
title: "Zeneovi pedagógiai megfigyelési és fejlődési napló"
area: "Zeneovi és adatvédelem"
lane: "research"
status: "elemzett"
moscow: "Could"
effort_size: "XL"
effort_min_days: 26
effort_max_days: 60
user_value: 4
operations_value: 2
revenue_value: 2
communication_value: 3
risk: "magas"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF04","MF05","MF08"]
created: "2026-10-19"
updated: "2026-10-19"
origin: "Szabad szöveges ötlet – 2026-10-19"
communication_angle: "„Emlékek és pedagógiai tapasztalatok a foglalkozásokról” – csak a megfelelő jogosultsági és szakmai rendszer kialakítása után."
---

# Zeneovi pedagógiai megfigyelési és fejlődési napló

## Eredeti felvetés

> zene ovi hoz gyerek fejlődési napló vagy megfigyelés napló

## Megoldandó probléma

A Zeneovi pedagógusa számára hasznos lehet saját megfigyelések dokumentálása, de egy gyermekről szóló strukturált személyes napló magas kockázatú, és nem azonos a szülőknek szánt motivációs jelvényrendszerrel. Nem cél automatikusan fejlődést diagnosztizálni.

## Megoldási változatok

- A – Gyermekhez nem kötött csoportfoglalkozási napló: milyen zenéket, játékokat és gyakorlatokat végeztek, hozzáférés csak illetékes pedagógusnak.
- B – Minimalista, csak illetékes pedagógus által vezetett, időbélyegzett, leíró jellegű egyéni megfigyelési napló, explicit cél, szerepkör, adatkezelői szabály és hozzáférési napló mellett; csak előzetes adatvédelmi ellenőrzés után.
- C – Szülővel megosztható, jóváhagyásra váró összefoglaló és export, helyesbítési/törlési eljárással; tartalmi/szakmai és jogi döntés után.

## Technikai hatás, előzetes hipotézis

- A napló nem nyilvános ACF-tartalom: külön, védett szerveroldali gyermek- és megfigyelés-adatmodell, engedélyezett pedagógus-csoport-hozzárendelés, audit, adatmegőrzés és hozzáférés szükséges.
- Személyes gyermekprofil csak a megfelelő gondviselői jogosultság és a Zeneovi szervezeti/adatkezelői viszony tisztázása után; D04 MVP family_id önmagában nem felhatalmazás minden gyermekadat kezelésére.
- Válasszuk külön: szakmai megfigyelés, családi visszajelzés, esetleges szülői megosztás. Egészségügyi/diagnosztikus következtetések és automatizált gyermekminősítés kizárva.

## Kockázatok és függőségek

- Gyermekek különösen védendő személyes adatai, téves hozzáférés, adatmegőrzési és adatkezelői jogalap kérdései; a D12 projekthatár nem helyettesít új funkcióhoz szükséges adatvédelmi döntést.
- Kedvezőtlen vagy pontatlan megfogalmazás stigmatizálhat; javítható, dátumozott ténymegfigyelések és szakmai útmutató szükséges.
- Tanári munkaidő és adminterhelés meghaladhatja az értéket; valódi használói kutatás nélkül nagy a túlfejlesztés veszélye.

## Példa elfogadási feltétel

- A naplót alapból sem más szülő, sem nem érintett kolléga nem olvashatja; közvetlen API lekérés vagy manipulált család-/gyermekazonosító sem kerülheti meg a kontrollt.
- Minden bejegyzésnél szerző, idő, jogosultság és módosítási audit szerepel, hozzáférési/megőrzési eljárás dokumentált.
- A/ B/C fokozatban nincs automatikus diagnózis, gyermeki rangsor vagy megfigyelésekből táplált marketingcélzás; szülői megosztás csak szabályozottan.

## Előzetes ráfordítás és értékelés

- Besorolás: research; státusz: elemzett, nem elfogadott; MoSCoW: Could. Nem vállalt MVP-hiba vagy alapvető UX-scope.
- XL (26–60 AI-val támogatott fejlesztői munkanap) kizárólag a B változat prototípusának durva, alacsony bizonyosságú hipotézise, nem árajánlat vagy határidő. A privát fejlesztői forrás közvetlen auditja nem történt meg.
- Szubjektív értékhipotézisek (1–5): ügyfél 4, üzemeltetés 2, bevétel 2, kommunikáció 3. Kockázat: magas.
- RICE-pontszám nincs: Reach, Impact, Confidence és Effort megalapozott bemenetei hiányoznak. A C változat, külső szolgáltató, pedagógiai tartalom, fizikai előállítás, marketing és üzemeltetés külön becslendő.

## Virágnak szóló rövid ajánlat

Lehetőség nyílhat a Zeneoviban történt értékes pedagógiai megfigyelések megőrzésére, de csak biztonságos, egyszerű rendszerben és a gyermekek adatainak elsőbbségével. Kezdjük személyes adat nélküli csoportnaplóval.

## Negyedéves kommunikációs lehetőség

„Emlékek és pedagógiai tapasztalatok a foglalkozásokról” – csak a megfelelő jogosultsági és szakmai rendszer kialakítása után. Kommunikációs hipotézis, nem jóváhagyott publikáció, megrendelés vagy vállalt dátum.

## Következő ellenőrzendő lépés

Interjú pedagógusokkal; kideríteni, milyen megfigyelések ténylegesen szükségesek, ki a jogszerű adatkezelő és milyen minimális jogosultsági/adatmegőrzési szabály indokolt.

## Kapcsolódás a fejlesztéshez

Kapcsolódik IDEA-017 Zeneovi-modulhoz, de annál szigorúbb hozzáférésű, személyes adatokat érintő külön kutatási kapu. D04 egy fiók/egy family_id nem írható felül; MF04/05/08 új modulhoz csak lehetséges technikai támpont.

A vállalt MF01–MF14 és a jóváhagyott D-döntések változatlanok. Új gyermekadat, új integráció, külső költség és szerkesztői/marketingközlés csak külön emberi jóváhagyás után. A PWA szerkesztői tartalmai WordPressből, ACF Free mezőkből kezelendők.
