---
id: "IDEA-027"
title: "Főoldali Virág-fotó forgatása időzített programajánlóként"
area: "Főoldal és marketing UX"
lane: "later-feature"
status: "elemzett"
moscow: "Should"
effort_size: "M"
effort_min_days: 4
effort_max_days: 10
user_value: 4
operations_value: 5
revenue_value: 4
communication_value: 5
risk: "közepes"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF02","MF05","MF08"]
created: "2026-11-06"
updated: "2026-11-06"
origin: "Szabad szöveges felhasználói ötlet – 2026-11-06"
communication_angle: "„A héten ezt ajánlom nektek!” – Virág saját képes meghívója a következő foglalkozásra."
---

# Főoldali Virág-fotó forgatása időzített programajánlóként

## Eredeti felvetés

> nyitólapon lévő Virág fotó rotálása, cserélhetősége időzítetten egy-egy program promótálására, esetleg opcionális navigáció hozzárendelés

## Megoldandó probléma

A főoldal Virágot bemutató hangsúlyos képe jelenleg tartalomként kezelhető, de az ütemezett váltás és programhoz kötött cselekvési lehetőség külön UX. Az a cél, hogy Virág WordPressből kampányképeket készítsen elő, amelyek megadott időablakban látszanak, és opcionálisan egy valós, publikált Ringató-program részletére mutatnak, React-telepítés nélkül.

## Megoldási változatok

- **A** – Egyetlen főoldali fotó gyors WordPressből történő cseréje, opcionális programrészletre vezető hivatkozással; a már vállalt ACF Free szerkesztési elvek lehető legkisebb bővítése.
- **B** – Több előre jóváhagyott kép és címsor, kezdő/záró időablak, visszaeső alapértelmezett Virág-fotó, valamint opcionális belső program-CTA. A képek váltása időzített, az aktív promó automatikusan kiválasztódik az aktuális szerveridő alapján; ajánlott első megoldás.
- **C** – Több aktív kreatív forgatása (karusszel / rotáció), kézi előre-hátra léptetés és akár mért megjelenítés, programkampányokkal; külön UX-teszt után, mert az automatikus animáció figyelemelterelő lehet.

## Technikai hatás, előzetes hipotézis

- ACF Free kompatibilis, WordPress `ringato_content` szerkesztői kép-/szövegmezők, dátum és kapcsolt eseményazonosító, hozzáadó tartalommigrációval. ACF Free-ben nincs Repeater/Flexible Content/Options Page: több kreatívhoz külön WP CPT bejegyzések vagy előre rögzített Group mezők, nem fizetős ACF-komponens.
- A kép önálló publikus szerkesztői tartalom, nem engedhet jogosulatlan műveletet. Opcionális navigáció csak engedélyezett, valódi `/app/events/:id` útvonalra vagy kifejezetten jóváhagyott HTTPS címre; törölt/nem publikált programnál a CTA automatikusan eltűnik, miközben fallback képfelület marad.
- Az ütemezés Europe/Budapest időzóna szerint történjen, több aktív promó ütközésére előre meghatározott sorrend (prioritás vagy időpont), lejárat után alapértelmezett kép; cache-frissítés, szerkesztett értékek megőrzése és több eszköz konzisztenciája.
- Képek reszponzív méretezése, alt szöveg, képjogok, mobilos fókusz és visszafogott animáció; autoplay karusszel esetén megállítás/szüneteltetés és reduced motion támogatás. A profil és a személyes widgetek alatt nem jelenhet meg üres vagy vibráló overlay.

## Kockázatok és függőségek

- Időzített váltásnál hibás időzóna, lejárt kampány, ACF szerkesztési ütközés vagy cache miatt régi program promóciója látszhat.
- Mozgó hero / autoscroll figyelemzavaró, teljesítmény- és akadálymentességi problémák mobilon; lehet, hogy egyetlen időzített kép jobb, mint a karusszel.
- Külső promóciós hivatkozás, nem érvényes foglalási információ, szerzői képfelhasználás és gyermekfotó; publikálás előtti szerkesztői jóváhagyás szükséges.

## Példa elfogadási feltétel

- Virág WordPressben új képet, szöveget és dátumablakot állít be; az alkalmazás új frontend build nélkül az aktív promót jeleníti meg és visszaesik az eredeti Virág-fotóra kampány nélkül.
- Ha a kép egy konkrét programhoz kapcsolódik, a CTA az adott publikált esemény részletére visz; hiányzó/lejárt eseménynél nincs halott link, nincs téves foglalási jogosultság.
- Átfedő ütemezés és nyári/téli időváltás determinisztikus, a képcache legkésőbb a dokumentált frissítési határon érvényesül.
- Mobilon nincs erőszakos, megállíthatatlan mozgás; képernyőolvasóhoz jóváhagyott alt és CTA-label tartozik, a kattintható kép fókuszálható.

## Előzetes ráfordítás és értékelés

- **Besorolás:** later-feature; MoSCoW Should; státusz elemzett (nem elfogadott fejlesztési megrendelés).
- **Durva hipotézis:** M (4–10 AI-val támogatott munkanap) az első valós B-variáns prototípusára, a WordPress/PWA meglévő implementációjának auditja nélkül. Külső díj, marketing, üzemeltetés, licenc és teljes kiadás nincs benne. Becslési bizonyosság alacsony; nem ár vagy határidő.
- **Szubjektív értékhipotézis (1–5):** ügyfél 4, üzemeltetés 5, bevétel 4, kommunikáció 5. Kockázat: közepes. RICE nincs, mert a reach, impact, confidence és effort megalapozott számai hiányoznak.

## Virágnak szóló rövid ajánlat

Virág a főoldal kedves, személyes fotóját időnként egy-egy következő program ajánlására is felhasználhatná. Előre beállíthatna képet, üzenetet és időszakot a WordPressben; az app magától a megfelelő képet mutatná, és szükség esetén a részletes programhoz vezetne.

## Negyedéves kommunikációs lehetőség

„A héten ezt ajánlom nektek!” – Virág saját képes meghívója a következő foglalkozásra. Nem jóváhagyott kommunikáció, kampány vagy vállalt negyedéves szállítás.

## Következő ellenőrzendő lépés

Elsőként ellenőrizni a főoldali kép jelenlegi ACF-sémáját és a programlinket; egy időzített, egyetlen kreatívval kezdett prototípus és akadálymentességi ellenőrzés javasolt.

## Kapcsolódás a fejlesztéshez

MF02/MF05 főoldal és kötelező ACF Free szerkesztés: az alapfotó szerkeszthetősége részben már specifikált, a többes ütemezés és link új későbbi funkció. MF08 programrészlet hivatkozás; IDEA-021 kulturális ajánló nem ugyanaz, mint a saját főoldali kreatív időzítése.

A már elfogadott MF01–MF14 és D01–D13 döntések változatlanok. Új automatikus művelet, időzítés, személyesadat-kezelés, külső költség és TV/platformterjesztés csak külön megrendelői döntés után.
