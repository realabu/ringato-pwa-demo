---
id: "IDEA-024"
title: "Beléptetés után élő, látványos visszajelzés a család telefonján"
area: "Jegyek, bérletek és beléptetési UX"
lane: "mvp-review"
status: "elemzett"
moscow: "Should"
effort_size: "M"
effort_min_days: 4
effort_max_days: 10
user_value: 5
operations_value: 4
revenue_value: 2
communication_value: 5
risk: "közepes"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF06","MF07","MF08","MF14"]
created: "2026-11-04"
updated: "2026-11-04"
origin: "Szabad szöveges felhasználói ötlet – 2026-11-04"
communication_angle: "Egyértelmű, kedves fogadtatás: a beléptetés eredménye azonnal megjelenik a saját telefonon."
---

# Beléptetés után élő, látványos visszajelzés a család telefonján

## Eredeti felvetés

> új ötlet, amikor beolvassák és érvényesítik a felhasználó jegyét vagy bérletét legyen pollozás és valami kedves látványos nagy eltűnő üzenet hogy sikeres volt a beléptetés vagy hasznos jelzés a sikertelenségről pl, hogy nem megfelelő jegyet mutatott a rendezvényhez és próbáljon másikat.

## Megoldandó probléma

A beléptetést végző munkatárs a staff képernyőn látja a QR ellenőrzésének és beváltásának eredményét, de a család saját telefonján ez nem feltétlenül válik egyértelművé. Amikor a szülő a QR-t felmutatja, az alkalmazás egy barátságos, nagy, gyorsan észrevehető, automatikusan eltűnő visszajelzést adhatna az **igazolt belépésről**, illetve érthető segítséget a téves jegy kiválasztásához. Az ellenőrzés (inspect) önmagában nem azonos a tényleges beváltással (redeem).

Ez nem ugyanaz, mint az IDEA-003 staff-szkenner navigációja vagy az IDEA-001 önkiszolgáló kioszk. A jelenlegi D03 üzleti állapotok felhasználói, második eszközön látható visszajelzésének UX-kiegészítése.

## Megoldási változatok

- **A – Rögzített állapot frissítése, kis fejlesztési próba.** A saját jegy/bérlet QR-oldala látható állapotban rövid időközönként lekérdezi a jogosult, szerveroldalon tárolt legutóbbi check-in állapotot. A szerver által igazolt új beváltáskor nagy, animált, de akadálymentes „Sikeres beléptetés! Jó zenélést!” felirat és pipa jelenik meg rövid időre, utána az állapot és a beváltási történet frissül. Nincs külön push-szolgáltatás vagy háttérfolyamat.
- **B – Teljes, okhoz illő háromállapotú visszajelzés (ajánlott).** A sikeres **új beváltás** zöld, nagy, magától eltűnő pozitív jelzés; a **D03 szerinti, ugyanarra az eseményre történő visszatérés** semleges/kedves „Már beléptetek – visszatérés” jelzés, korábbi időponttal, *második levonás nélkül*; a **valóban sikertelen érvényesítés** külön, megérthető ok és következő lépés, például „Ez a jegy másik programhoz tartozik. Mutass egy ehhez az alkalomhoz érvényes jegyet!”. A hiba maradjon olvasható, amíg a szülő el nem olvasta, ne tűnjön el gyorsan. Hibajelzés csak akkor jelenhet meg automatikusan a szülőnél, ha a szerver azt a saját jogosultságához kötötten, biztonságosan és megfelelően azonosított beléptetési próbához kapcsolva adja vissza.
- **C – Finomabb élmény és többcsatornás visszajelzés.** B-re építve opcionális hang/haptikus jelzés, animációváltozatok és staff-oldali/ügyféloldali szinkron; esetleg SSE/WebSocket csak mért késleltetés és megvalósíthatósági teszt után. A saját telefon lezárt vagy háttérben lévő állapotára nem ígérünk állandó szinkront, és nincs automatikus új pushértesítés-jog.

**A megvalósítási döntésnél fontos:** az első A változat a létező, hiteles check-in tényt mutathatja, de a „rossz eseményhez tartozó jegy” hibája nem feltétlenül rekonstruálható pusztán a beváltási előzményből. A B változathoz szükséges lehet új, rövid életű, célzott scan-/inspect-eredménycsatorna szerveroldali adattal. Nem küldhetünk a szülőnek kitalált vagy másik család próbájából származó hibát.

## Technikai hatás, előzetes hipotézis

- **Felület:** az ügyfél saját `/app/wallet/:id` jegy- vagy bérlet-QR nézete; nem a staff telefonjának közvetlenül másolt állapota. Új kérés csak látható, aktív képernyőn, például 2–5 másodperces *tervezési* intervallummal, szerver- és mobilpróbán mért végső beállítással. Fókuszba visszatéréskor azonnali frissítés; kijelentkezéskor, háttérben vagy nézetváltáskor a polling leáll, nincs offline siker imitálása.
- **Szerveradat és jogosultság:** szerver által rögzített check-in eseményazonosító/státusz/idő és felhasználói jogosultság. A polling célzottan csak a kérdező család saját jogosultságának állapotát, felhasználói szintre szűrt (szükség esetén sanitizált) hibakódját olvashatja; QR titkos érték, másik ügyfél, staff token vagy személyes adat nem kerülhet válaszba. No-store és sessionhez kötött lekérés.
- **Új esemény kezelése:** az oldal a megnyitáskor elmenti az aktuális, szerver által adott utolsó eredményazonosítót; csak az ezután keletkező változás vált ki új animációt. Újratöltés, párhuzamos polling, újrafókusz vagy retry nem indíthat ismételt „új belépés” ünneplést; a szerver a D03 idempotens beváltást tartja fenn.
- **Siker, visszatérés, sikertelen próbálkozás:** D03 szerint a már egyszer beváltott azonos eseményre történő visszatérés **nem hiba, de nem új sikeres beváltás**. A „másik esemény jegye” / „lejárt” / „még nem érvényes” / „offline vagy hálózati hiba” különböző kategóriák; a kliens csak a szerver által igazolt okra adhat célzott javaslatot. A hálózati hiba nem azt jelenti, hogy a beléptetés sikertelen.
- **UX és tartalom:** nagy, jól kontrasztos visszajelző réteg vagy képernyőrész, fókuszkezeléssel, screen-reader live regionnel, `prefers-reduced-motion` szerinti animáció nélküli változattal; a sikerjelzés 2–4 másodperces *javasolt* megjelenése és a tartósan elérhető történet külön. Hiba ne legyen csak színnel jelölve, ne tűnjön el olvasás közben. Feliratok, üdvözlés és hibaszövegek WordPress ACF Free szerkesztői mezőiből, a szerverhibakód → típus leképezés kontrolláltan.
- **Hatókör:** MF07 check-in és wallet státusz, MF08 eseménykontextus; az üzleti beváltási szabály, beléptetési időablak, foglalás, QR-kibocsátás és jegylevonás nem változik. A staff-oldali explicit „Beváltás” lépés megmarad.

## Kockázatok és függőségek

- **Téves sikerjelzés:** a scan/inspect sikerét a felhasználó tényleges belépésnek értelmezheti, miközben az érvényesítés vagy beváltás még nem történt meg. Siker kizárólag rögzített, hiteles redeem után.
- **Hibaeredmény visszakötése:** egy sikertelen próbának nincs feltétlenül tartós check-in sora; az ügyféloldali célzott hibaüzenethez új szerveres, időben korlátos eredményrekord lehet szükséges, az adott jegyhez és családhoz kötve. Nem szabad másik esemény vagy fiók okát megjeleníteni.
- **D03 visszatérés:** korábban belépett család visszatérése nem vonhat le második alkalmat és nem lehet vörös „sikertelen” üzenet, sem félrevezető új siker.
- **Terhelés:** több telefon párhuzamos, állandó rövid pollingja terheli a WordPresst; láthatósághoz kötés, backoff, no-store és üzemeltetési terhelési próba kell; nincs böngésző-háttérben vagy minden jegyre folyamatos kérdezés.
- **Képernyő és adatvédelem:** a nagyméretű üzenet ne fedje el tartósan a QR-t, és idegen személyes adat vagy belépési előzmény ne villanjon fel a kioszk/staff kijelzőn. Akadálymentes animáció és hibaolvasás.
- **Eszközfüggőség:** szülő lezárt kijelzője, másik alkalmazásra váltása, gyenge hálózata esetén nem garantálható valós idejű értesítés; a staff-nál lévő hivatalos eredmény az irányadó.

## Példa elfogadási feltétel

- Sikeres QR inspect **önmagában** még nem mutat „Beléptél!” feliratot. A tényleges, szerveren rögzített redeem után, aktív ügyfél-QR oldalon egyszer megjelenik a nagy pozitív visszajelzés és az új beváltás bekerül az előzménybe.
- Az ugyanarra a foglalkozásra visszatérő család korrekt, semleges „Már beléptetek – visszatérés” jelzést kap, és nem történik új levonás (D03).
- Más eseményhez tartozó jegy scan-próbájánál csak a saját, azonosított próbáról származó szerveres hibakóddal jelenik meg célzott üzenet; nincs hamis siker vagy tetszőleges másik ügyfél hibájának megjelenítése.
- Polling leáll háttérben, bezárt nézetben és kijelentkezéskor, újranyitásnál egy friss lekérdezéssel folytatódik; offline és hálózati hiba nem jelenik meg beléptetési elutasításként.
- Egyazon redeem-eredmény nem okoz ismételt animációt retry, több tab vagy fókuszváltás után; a szerver által rögzített check-in/idempotencia független az UI-tól.
- A success overlay és a hiba hosszát, szövegét, kontrasztját, `prefers-reduced-motion` és screen-reader viselkedését fizikai Android/iPhone készüléken ellenőrzik; a hibát a felhasználó el tudja olvasni és javítani.
- Az eredmény-API nem enged idegen családi adatot vagy staff beléptetési státuszt lekérni; polling és WordPress terhelés mérve.

## Előzetes ráfordítás és értékelés

- **Besorolás:** `mvp-review`, MoSCoW **Should**, státusz **elemzett**; a közvetlen, szemléletes beléptetési visszajelzés alap UX javítás lehet, de **nem jóváhagyott MVP-scope-bővítés**.
- **Előzetes M méret (4–10 AI-val támogatott fejlesztői munkanap)** a B változatra vonatkozó, alacsony bizonyosságú nagyságrendi hipotézis. A tényleges szerveroldali hibakód- és pollingadat rendelkezésre állása audit nélkül nem ismert; más scope vagy szerveres eredménycsatorna esetén újra kell becsülni. Nem ár és nem szállítási határidő.
- **Szubjektív értékhipotézisek (1–5):** felhasználói 5; üzemeltetés 4; bevétel 2; kommunikáció 5. **Kockázat közepes.** RICE nincs kiszámolva bizonyított bemenetek nélkül.
- A változat kisebb próbaként külön vizsgálható, a B szerveroldali hibaszinchronizációt csak valódi igény és teljes jogosultsági megoldás után kell vállalni.

## Virágnak szóló rövid ajánlat

Amikor egy család belép a Ringató-foglalkozásra, a saját telefonján is azonnal egy kedves, nagy „Sikeres beléptetés – jó zenélést!” üzenet jelenhet meg. Ha rossz jegyet mutatnak, a rendszer nem egyszerűen piros hibát ad, hanem segít megérteni, melyik jogosultságot érdemes elővenni. A visszatérő családok külön, megnyugtató visszajelzést kapnak. Így gyorsabb és kellemesebb lehet az érkezés.

## Negyedéves kommunikációs lehetőség

„Üdv újra a Ringatón! – egyértelmű belépési visszajelzés a telefonodon” mint későbbi termékkommunikáció, kizárólag igazolt, működő mobilpróba után. Nem vállalt kampány vagy kiadási dátum.

## Következő ellenőrzendő lépés

1. A privát `nmarton/ringato-dev` MF07/Core check-in/wallet API és a staff inspect/redeem válaszainak ellenőrzése: a saját jegyoldal milyen szerveres check-in állapotváltozást tud biztonságosan megfigyelni?
2. Eldönteni, kell-e a valóban sikertelen scan/inspect próbákhoz új, rövid életű ügyféloldali eredményrekord, és miként köthető az a helyes családhoz és jegyhez.
3. UX-prototípus és telefonos próba: új beváltás, D03-visszatérés, rossz eseményjegy, lejárt jogosultság, hálózati hiba, több tab és háttérben lévő app.
4. Terhelési mérés és WordPress szerkeszthetőség igazolása után külön MVP-jóváhagyás, ha a megvalósítás aktuális fejlesztési körbe kerül.

## Kapcsolódás a fejlesztéshez

- **Duplikáció:** **IDEA-003** staff QR beléptetési UX (eseményválasztás, kézi kódmásolás) és **IDEA-001** önkiszolgáló beléptető kioszk (olvasóeszköz, státuszjelzés és létszám) rokon témák, de nem a *szülő saját telefonján* megjelenő, szerverre alapozott eredményjelzés. Ezért önálló IDEA-024. A kioszk későbbi státuszmodelljével esetleg újrahasznosítható megjelenítési elem.
- **D03/MF07:** már belépett család visszatérése sem hiba, sem új siker; az azonos eseményhez kötött check-in idempotens, nem új beváltás. **MF08/D05:** az eseményhez illeszkedő jegy, időablak és tényleges foglalás továbbra is szerveroldalon dől el.
- **MF06:** médiaélmény-komponensek nem adnak alapot a check-in státusz kitalálására; **MF14:** fizikai mobilpróba és regresszió. Az új UI-feliratokra a WordPress ACF Free kötelező szerkeszthetősége érvényes.
- **D11/MF12:** a meglévő üzenetküldési polling nem jogosít fel check-in státusz olvasására; attól független, célzott végpont és terhelési döntés kell.
- A jóváhagyott MF01–MF14 és D01–D13 szabályok változatlanok; az ötletlap publikálása nem kódmódosítás vagy fejlesztési jóváhagyás.
