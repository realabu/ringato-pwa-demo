---
id: "IDEA-023"
title: "Település szerinti programszűrés és megjegyzett választás"
area: "Programok és személyes preferenciák"
lane: "mvp-review"
status: "elemzett"
moscow: "Should"
effort_size: "M"
effort_min_days: 4
effort_max_days: 10
user_value: 5
operations_value: 3
revenue_value: 3
communication_value: 4
risk: "közepes"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF04","MF05","MF08"]
created: "2026-11-03"
updated: "2026-11-03"
origin: "Szabad szöveges fejlesztési ötlet – 2026-11-03"
communication_angle: "A közeledben érdekes Ringató-foglalkozások, újra és újra keresés nélkül"
---

# Település szerinti programszűrés és megjegyzett választás

## Eredeti felvetés

> új ötlet, a user állíthassa be az app-ba, hogy mely település programjai érdeklik vagy legyen valami szűrés a program listába ami megjegyzi az utolsó beállítást

## Megoldandó probléma

A több helyszínen tartott Ringató-foglalkozások közül a család jellemzően csak egy vagy néhány település programjai iránt érdeklődik. Ha a programlista mindig minden települést mutat, a releváns alkalmak megtalálása nehézkes, és ismételt szűrést igényel. A felhasználó által választott település nem azonos a GPS-helyzetével, a foglalkozás konkrét helyszínével vagy az eseményhez tartozó foglalási jogosultsággal.

## Megoldási változatok

- **A – Egyszerű településszűrő, utolsó érték megjegyzésével (elsőként javasolt).** A programlistán „Összes település” és az aktuálisan elérhető programok települései közül választható szűrő. A legutolsó beállítás az adott böngészőben / telepített PWA-ban megmarad visszalépés és alkalmazás-újranyitás után, biztonságos alapállapottal. Új fiókpreferencia-API nélkül is kipróbálható.
- **B – Fiókhoz kötött kedvenc települések (ajánlott hosszabb távú UX).** Bejelentkezett szülő több települést jelölhet meg, a választás WordPress-fiókhoz kötött privát preferenciaként tárolódik, és másik készüléken is azonosan látszik. A programlistán könnyen elérhető „Összes” mód, a kiválasztott városok egyértelmű megjelenítésével.
- **C – Érdeklődési terület és releváns programok.** Később opcionális környék-/régióválasztás, több helyszíncsoport vagy utazási távolság szerinti ajánló, új programokról külön engedélyezett értesítéssel. Nem történik automatikus GPS-lekérés és nincs automatikus pushfeliratkozás.

## Technikai hatás, előzetes hipotézis

- **Adatforrás-feltárás:** az MF05 `event` WordPress-adapterében ellenőrizni kell, szerepel-e normalizált, szerkesztő által ellenőrizhető településazonosító az esemény helyszínénél. A helyszín neve, utcacíme és település nem ugyanaz; hiányzó településadat nem jelölhető önkényesen.
- **Szűrés:** az aktív, a programlistában egyébként is látható eseményekből képezhető településlista. Településnév önmagában ütközhet, ezért stabil kulcs/azonosító és megfelelő megjelenítési név szükséges. Kezelendők az online/helyszín nélküli események, több helyszínnel rendelkező események, és a hiányos, visszavont vagy újonnan megjelent települések.
- **A változat:** az utolsó választás kezelhető lokális, személyes adatot nem tartalmazó UI-preferenciaként; nem tárolunk belőle program- vagy foglalási adatot, és nem bízzuk rá az API-jogosultságot. Kijelentkezés, fiókváltás és közös eszköz esetén kerülendő más felhasználó preferenciájának félreérthető átvétele; alapértelmezés „Összes település”.
- **B változat:** a fiókpreferenciát szerveroldalon, kizárólag a hiteles WP userhez kötve lehetne menteni; konfliktuskezelés több eszközön, idempotens frissítés és visszavonható választás. Az ACF Free a feliratok és szerkesztői szövegek forrása, nem a felhasználónkénti kiválasztott települések nyilvános tárolója.
- **MF05/MF08:** a lista UI-ja és szűrési logikája bővülhet; az események valós foglalhatóságát, kapacitását, időrendjét és D05-ös lemondási szabályait a szűrés nem változtathatja meg. Ha szűrő alatt nincs találat, legyen érthető üres állapot és egygombos „Összes program mutatása”.
- **Adatvédelem és akadálymentesség:** a településszűrő nem igényel pontos tartózkodási helyet vagy böngészős geolokációs engedélyt; címkés választómező, képernyőolvasó, billentyűzet és kis mobilképernyő támogatása szükséges.

## Kockázatok és függőségek

- A programok településadata nem feltétlenül szerepel önálló strukturált mezőben; a meglévő WordPress eseményadatok auditja nélkül nem ígérhető automatikusan megbízható szűrés.
- A megjegyzett szűrő elrejtheti az érdekes új programokat; a kiválasztás mindig legyen látványos, és egyszerűen visszaállítható „Összes” nézetre.
- A helyszín nélküli vagy online programokat ne rejtsük el váratlanul: legyen külön „Online / helyszín nélkül” választási lehetőség vagy dokumentált megjelenítési szabály.
- Lokális tárolás böngészőtörlésnél megszűnhet és fiókok között félreérthető lehet; a többeszközös preferencia új, külön szerverfejlesztés.
- A meglévő MF05 0.5.1 felületi döntés „keresőmezők nélkül” készült; a településválasztót ezért kifejezett felülvizsgálati UX-javaslatként kezeljük, nem vállalt alapkövetelményként.

## Példa elfogadási feltétel

- A programlistán kiválasztható egy elérhető település vagy az „Összes település” mód; a megjelenített találatok minden esetben az élő, szűrés nélkül is jogosultan látható programok részhalmazai.
- A változatban a választás listáról részletekre és vissza, frissítés, alkalmazás bezárása/újranyitása után megmarad ugyanazon készüléken; böngészőadat-törlés után korrekt alapállapot lép életbe.
- Ha a korábban kiválasztott település megszűnik vagy nincs benne aktuális program, ezt az UI érthetően jelzi, és egy kattintásra az összes program megjeleníthető.
- A kiválasztott település nem módosít árakat, jegyeket, jogosultságot vagy az MF08/D05 foglalási logikát; egy szűrésből megnyitott esemény URL-je közvetlenül is működik.
- B változat esetén másik saját eszköz ugyanazokat a fiókhoz mentett településeket mutatja; másik fiók nem láthatja, nem változtathatja a preferenciákat.
- 320–430 px-es mobilon, tableten és képernyőolvasóval kezelhető, a szűrő felirata és az üres állapot szövege WordPress ACF Free-ből szerkeszthető.

## Előzetes ráfordítás és értékelés

- **Besorolás: `mvp-review` / Should**, mert a jelenlegi programlista használhatóságához kapcsolódik, de nem igazolt technikai hiba és nem automatikusan jóváhagyott MVP-scope.
- **Ügyfélérték 5/5:** kevesebb ismételt keresés, gyorsabb programválasztás. **Üzemeltetés 3/5:** településadat-karbantartás szükséges. **Bevétel 3/5:** több releváns foglalás lehetséges, de nem bizonyított. **Kommunikáció 4/5:** személyesebb, helyi ajánlat.
- **M (4–10 AI-val támogatott fejlesztői munkanap)** nagyon durva becslés a B változat kezdeti prototípusára, alacsony bizonyossággal; az A változat ennél kisebb lehet, amennyiben a településadat már strukturált. Nem határidő és nem árajánlat.
- **Kockázat közepes** az adatminőség, szűrési UX és fiókadat-tárolás miatt. **RICE nincs számolva**, mert az elérés, hatás és tényleges ráfordítás adatai hiányoznak.

## Virágnak szóló rövid ajánlat

A családok gyorsabban megtalálhatnák az őket érdeklő települések Ringató-foglalkozásait. Az alkalmazás megjegyezhetné, melyik várost nézték utoljára, így legközelebb nem kell újrakezdeniük a keresést. Később akár több kedvenc települést is beállíthatnának.

## Negyedéves kommunikációs lehetőség

„Találd meg könnyebben a hozzád illő Ringató-foglalkozásokat!” – az egyszerű, megjegyzett településszűrő bevezetése után kommunikálható. Nem automatikus negyedéves szállítási vállalás.

## Következő ellenőrzendő lépés

1. Ellenőrizni, hogyan tárolja a meglévő WP `event` struktúra a települést és a helyszínt, és milyen adatminőségi hibák vannak.
2. Virággal tisztázni az online, többhelyszínes és település nélküli programok szűrési szabályát.
3. A változatot minimális, megjegyzett, „Összes” móddal könnyen felülírható településválasztóként UX-prototipizálni.
4. Használati visszajelzés alapján dönteni, szükséges-e több település és fiókhoz kötött többeszközös szinkron.

## Kapcsolódás a fejlesztéshez

- **MF05:** meglévő WordPress programlista és eseményadat-adapter, amely 0.5.1-ben keresőmezők nélkül, dátumcsoportos megjelenítéssel készült; új szűrő csak külön UX-döntéssel.
- **MF08:** programfoglalás, kapacitás és ár változatlan. A település szerinti szűrés csak megjelenítési preferencia, nem üzleti szabály vagy új foglalástípus.
- **MF04:** kizárólag a B változat fiókhoz mentett településválasztása esetén szükséges új, hozzáférésvédett user-meta/preferencia megoldás.
- **IDEA-021:** Virág külső kulturális programajánlója külön modul; ott helyszín szerinti szűrés már szerepel, de nem ugyanaz, mint a meglévő Ringató programlistájának megjegyzett preferenciája. **IDEA-012** országos vonzáskörzet-/kampánykutatás szintén más cél.
- **Döntési rend:** MF01–MF14 és D01–D13 nem változnak az ötlet rögzítésétől. Jelenleg nem történt tényleges React/WordPress kódmódosítás vagy staging telepítés; a privát forrás auditja a becslés pontosításához szükséges.
