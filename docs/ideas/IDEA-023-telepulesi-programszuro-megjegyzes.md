---
id: "IDEA-023"
title: "Település szerinti programszűrés megjegyzett választással"
area: "Programlista és személyre szabás"
lane: "mvp-review"
status: "elemzett"
moscow: "Should"
effort_size: "S"
effort_min_days: 1
effort_max_days: 3
user_value: 5
operations_value: 3
revenue_value: 3
communication_value: 4
risk: "alacsony"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF04","MF05","MF08"]
created: "2026-11-03"
updated: "2026-11-03"
origin: "Szabad szöveges fejlesztési ötlet – 2026-11-03"
communication_angle: "Csak a neked érdekes települések Ringató-programjai, egy megjegyzett választással."
---

# Település szerinti programszűrés megjegyzett választással

## Eredeti felvetés

> új ötlet, a user állíthassa be az app-ba, hogy mely település programjai érdeklik vagy legyen valami szűrés a program listába ami megjegyzi az utolsó beállítást

## Megoldandó probléma

Ha több település programjai szerepelnek a listán, a család minden látogatáskor újra kénytelen átnézni vagy kiszűrni a számára nem releváns helyszíneket. Az állandó lakóhely vagy pontos tartózkodási hely megadása helyett jobb a kifejezett, szabadon módosítható településválasztás. A kért funkció lehet egyszerű programlista-UX-javítás, de a külön fiókszintű érdeklődési profil és a célzott értesítés már eltérő scope.

## Megoldási változatok

- **A – Programlista-szűrő, utolsó választás megjegyzésével (elsőként ajánlott):** az `/app/events` listában „Összes település” alapértelmezett opció és az elérhető eseményhelyszínekből képzett településválasztó. Az utolsó választást az adott eszköz/böngésző csak nem érzékeny preferenciaként tárolja; visszatéréskor visszaállítja. A lista idő- és foglalási szabályai változatlanok, és látható „Szűrő törlése / Összes település” lehetőség van. Nem kér helyadat-engedélyt.
- **B – Több kedvelt település és fiókszintű szinkron (második ütem):** a bejelentkezett felhasználó egy vagy több települést jelölhet meg az alkalmazás beállításaiban vagy a lista szűrőjén. A választás WordPress `user_meta` / saját felhasználói preferencia API mögött menthető, ugyanazzal a beállítással több készüléken; az A módból átálláskor konfliktuskezelés kell. A profilfelület csak alternatív beállítási hely, **nem új kötelező profilnavigáció**.
- **C – Érdeklődési kör alapú programajánlás / értesítés:** a B szerint mentett települések új programjai a főoldalon külön jelenhetnek meg, illetve külön, kifejezetten engedélyezett értesítésekhez szolgálhatnak szűrőként. Ez a D06/MF13 meglévő, WordPressből szerkesztett címzettcsoportokat és pushopt-int nem írhatja felül; önálló adatkezelési és üzleti döntés szükséges.

## Technikai hatás, előzetes hipotézis

- MF05 `/app/events` meglévő WordPress-esemény olvasó nézetének felhasználói szűrője; MF08 foglalási, férőhely-, lejárati és vásárlási üzleti logikája változatlan. A településlista csak az **aktuálisan publikálható** programok normalizált helyszín-/településadataiból képződjön, ne kódban rögzített lista legyen. A WordPressben a helyszínadat pontosságát és a hiányzó település mezőket ellenőrizni kell.
- A változatban egyszerű lokális preferencia-kulcs, amely nem tartalmaz gyermek-, cím-, GPS- vagy rendelési adatot. Ha a választott településhez már nincs elérhető esemény, az üres lista mellett jelenjen meg a visszaállítási lehetőség; a felhasználó ne higgye azt, hogy az összes program megszűnt. Böngészőadat-törlés vagy más készülék esetén az A szűrő újra alapértelmezésű.
- Több helyszín ugyanazon településen egy szűrési csoport; településnevek írásmódja, homonim települések és időszakos helyszínek kezelése stabil településazonosítóval vagy megbízható, ellenőrzött normalizálással javasolt. Nem lehet kizárólag szabad szöveg-részlet egyezés.
- B változathoz hitelesített felhasználói preferencia endpoint és hozzáférésvédelem szükséges; jogosultságokból/termékadatokból nem vezetünk le érdeklődési települést, és nem használunk automatikus geolokációt.
- A szűrő feliratai, üres állapotai és magyarázó szövegei a projekt szabálya szerint WordPress ACF Free-ből szerkeszthetők, a dinamikus településnevek és eseményadatok pedig az esemény-adatforrásból jönnek. A kliens cache és logout működését vizsgálni kell: helyi preferenciát nem szabad privát fiókadatként vagy rejtett célozásként kezelni.

## Kockázatok és függőségek

- A WordPress eseményadatokban a település lehet hiányzó, következetlenül írt vagy nem külön mező; a szűrő megvalósíthatóságát a tényleges adattérképezés igazolja.
- Lokális preferencia az eszközön másik felhasználóra is érvényes lehet; ez az A változatnál csak akkor elfogadható, ha a szűrő nem érzékeny adat és egyszerűen törölhető. Fiókhoz kötött személyes preferencia esetén B változat és auth szükséges.
- A túl szigorú vagy megjegyzett szűrő eltüntetheti az új/alkalmi más települési foglalkozásokat; mindig legyen feltűnő aktív szűrő és egykattintásos „Összes program” visszaállítás.
- A C változat értesítése ne jelentse a D06 manuális csoporttagság vagy a pushengedély automatikus módosítását. Nincs szükség GPS-hozzáférésre, és nem vezetünk be lakcím-alapú személyes profilozást.

## Példa elfogadási feltétel

- A felhasználó az `/app/events` listán kiválaszt egy települést: csak az adott településhez tartozó megfelelő státuszú programok jelennek meg; ugyanott több külön foglalkozási helyszín mind szerepel.
- Az A változatban lapfrissítés, navigáció, appbezárás/újranyitás után ugyanazon böngészőben az utolsó szűrés visszaáll; privát/böngészőadat-törlés esetén az „Összes település” állapot biztonságos fallback.
- Az aktív településszűrő egyértelműen látszik; üres eredmény mellett is elérhető a „Szűrő törlése” gomb; a választó kezeli az új települést, a megszűnt helyszínt és a hiányos településadatokat.
- A szűrés nem változtatja az esemény részletének URL-jét, foglalhatóságát, tényleges férőhelyét, check-in állapotát vagy jogosultságát; közvetlen eseménymélylink továbbra is működik.
- B esetén a felhasználó csak saját mentett településeit módosíthatja/olvashatja, és a változtatás több eszközön tükröződik; C esetén csak külön jóváhagyott opt-in alapján indul értesítés.
- Mobil, tablet, képernyőolvasó és billentyűzetes navigáció, valamint offline/hiba/üres állapot ellenőrzött.

## Előzetes ráfordítás és értékelés

- **Besorolás: `mvp-review`, MoSCoW: Should, állapot: elemzett.** A megjegyzett programszűrő alapvető, kicsi UX-javítási jelölt, de **nem automatikusan jóváhagyott MVP-bővítés**.
- **S (1–3 AI-val támogatott fejlesztői munkanap)** kizárólag az A változat nagyon előzetes hipotézise, feltételezve, hogy az eseményeknél már megbízható településadat szerepel. Ha ezt strukturálni kell, illetve B/C verzió készül, külön, nagyobb becslés indokolt. Privát fejlesztői kód közvetlen auditja nélkül a bizonyosság alacsony; nem árajánlat vagy szállítási határidő.
- Szubjektív értékhipotézisek 1–5: felhasználó 5, üzemeltetés 3, bevétel 3, kommunikáció 4. Kockázat alacsony **az A változatnál**, adatminőségtől függően. RICE nem pontozható tényleges reach/impact/confidence/effort adatok nélkül.
- **Ajánlás:** először A (egy település + emlékező szűrő); ha a használat vagy családi visszajelzés több preferált települést igényel, B. Nem javasolt rögtön felhasználóprofil- és értesítési modulba bővíteni.

## Virágnak szóló rövid ajánlat

A családok a programlistában egyszer kiválaszthatják, melyik település foglalkozásai érdeklik őket. Az alkalmazás megjegyzi a választást, így legközelebb már a számukra releváns programok jelennek meg; az összes foglalkozás egyetlen érintéssel újra látható. Nem kell hozzá lakcímet megadni vagy a telefon helyadatait engedélyezni.

## Negyedéves kommunikációs lehetőség

„A hozzád közeli Ringató-programok egy helyen” helyett pontosabban: „Válaszd ki a településed, és legközelebb is a neked érdekes programokkal kezdünk!” Kizárólag megvalósítás után használható terméküzenet; nem vállalt kampány vagy szállítási dátum.

## Következő ellenőrzendő lépés

A jelenlegi `/app/events` esemény-API és WordPress helyszín-/település mezőinek tényleges ellenőrzése; az A szűrési UX próbája 2–3 településsel és hiányos adatsorral; az aktív szűrő/ürítés/újranyitás kipróbálása. Megfelelőség esetén külön MVP-prioritás- és scope-jóváhagyás, majd React módosítás és kiadási tesztek.

## Kapcsolódás a fejlesztéshez

**Duplikáció:** az IDEA-021 Virág által válogatott külső kulturális programajánlója helyszín-, dátum- és kategóriaszűrést is tartalmaz, de nem azonos az MF05/MF08 saját Ringató-foglalkozások érdeklődési településszűrőjével. A két szűrő később közös UI-mintát használhat, de nem egy közös jogosultsági vagy tartalomforrás. A korábbi IDEA-009/022 az anonim és autentikált kezdőélményről szólnak, nem programlista-szűrésről.

**MF05** saját események listázása és WordPressből olvasott adatok; **MF08** eseményfoglalás, férőhely és beléptetési üzleti szabályok érintetlenek. **MF04** csak a B változat többeszközös fiókpreferenciájánál lehetséges függőség. **D04/D05/D06** és a jóváhagyott MVP változatlanok; a katalógus publikálása nem implementációs megrendelés.
