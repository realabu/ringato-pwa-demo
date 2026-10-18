---
id: "IDEA-012"
title: "Országos Ringató-lefedettség és célzott online kampány"
area: "Piackutatás és marketing"
lane: "business-experiment"
status: "elemzett"
moscow: "Could"
effort_size: "L"
effort_min_days: 11
effort_max_days: 25
user_value: 4
operations_value: 3
revenue_value: 5
communication_value: 5
risk: "magas"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF05","MF09","MF10"]
created: "2026-10-19"
updated: "2026-10-19"
origin: "Szabad szöveges ötlet – 2026-10-19"
communication_angle: "„A Ringató házhoz megy – online” az időben nehezen elérhető térségeknek (jóváhagyandó üzenet)"
---

# Országos Ringató-lefedettség és célzott online kampány

## Eredeti felvetés

> terkepezzuk fel az országban az összes ringato foglalkozást, készítsünk vonzaskorzetuk alapján elemzést, melyek a vak foltok, kinek kell sokat utazni es tegyünk javaslatot célzott reklám kampányra. A ringato házhoz megy online.

## Megoldandó probléma

Nem ismert, hogy Magyarország mely településeiről, milyen eljutási idővel érhető el rendszeres, **aktuálisan megtartott** Ringató foglalkozás, és hol lakhatnak olyan kisgyermekes családok, akiknek a helyszíni részvétel nehéz. A települések egyszerű számlálása félrevezető: a foglalkozás időpontja, közlekedési módja, gyakorisága és a potenciális célcsoport létszáma is számít. Az eredményből **nem automatikusan** következik az online vásárlási igény.

A cél belső piackutatás és az Online Ringató / Virággal PWA ismertségét vizsgáló, mérhető kísérlet; **nem országos foglalkozás-adminisztrációs funkció**, és nem a vállalt MVP bővítése. A helyszíni közösségi élményt nem állítjuk egyenértékűnek az online médiával: az online ajánlat alternatíva/kiegészítés az utazási nehézséggel érintetteknek.

## Megoldási változatok

- **A – Kézi, szűk területi pilot (elsőként javasolt).** Engedélyezett vagy kézzel jóváhagyott forrásból két-három eltérő jellegű mintatérség aktív helyszíneinek ellenőrzése; települési kiindulópontokhoz egyszerű távolság- és becsült autós elérési idősávok. KSH nyilvános aggregátumokból célcsoport-becslés, hiányosságok jelölése; belső térkép/táblázat, egy ellenőrzött kreatív és kis költésű marketingkísérlet **csak külön költség- és tartalomjóváhagyással**. Nincs új PWA-modul.
- **B – Országos, reprodukálható térinformatikai elemzés (analitikai ajánlott célállapot).** Jogosultan átvett, verziózott magyarországi helyszín- és alkalomlista, geokódolási minőségjelzés, aktív/szünetelő állapot és frissítés dátuma. Települési vagy rácscella-szintű eredet–cél útvonalidők; például 15/30/45 perces **állítható elemzési küszöbök**, nem tényként kezelt optimális vonzáskörzetek. Keresletproxy: 0–3 éves korú gyermekek vagy elérhető legjobb korcsoport-/születési aggregátum, évjárattal és bizonytalansággal. Rangsorolt vakfoltok térképen, célterület/kampánytábla exportja, kézi jóváhagyási kapu.
- **C – Kampányoptimalizált, rendszeresen ismételt üzleti kísérlet.** B-re épülő, külön jóváhagyandó geo-kampányok, lokális kreatívvariánsok, UTM-es landing / meglévő WooCommerce-ajánlat, aggregált tölcsérmérés és A/B-teszt. Kontrollterület vagy időszakos összehasonlítás a többlethatás becslésére; szabályozott frissítés és tanulságok. Hirdetésköltés, platformfiók, jogi megfelelés és operatív működtetés **külön projekt**; nincs automatikus kampányindítás.

A–B–C fokozatok: először az adatjog és adatminőség, utána a valóban problémás területek bizonyítása, végül a konverzió vizsgálata. Sikertelen pilotnál nincs automatikus továbblépés.

## Technikai hatás, előzetes hipotézis

- **Kiinduló forrás:** a központi Ringató honlapján már van országos foglalkozáskereső és térképes nézet. A honlapon több időpontban eltérő számlálók jelennek meg; ezért **nem tekinthető ellenőrzöttnek az „összes foglalkozás” listája**. Előbb az üzemeltetőtől kérendő engedélyezett, dátumozott export/licenc vagy együttműködés; ennek hiányában csak korlátozott, megengedett nyilvános/engedélyezett minta. Automatizált másolás/scraping nincs előzetes jogosultságtisztázás nélkül.
- **Források és ország-határ:** foglalkozásvezető, helyszín és heti alkalom külön azonosítandó, a duplikátumok, szünetek és változó órarend kezelendő. Magyarországi vizsgálatnál a külföldi helyszíneket külön szűrni kell. Forráshivatkozás, lekérés/ellenőrzés dátuma, frissesség és geokódolási pontosság minden sorhoz.
- **Módszer:** a légvonalbeli kör csak gyors előszűrés; az elsődleges elérhetőség az úthálózaton számolt *becsült utazási idő*. Ahol releváns, tömegközlekedés/gyalogos szakasz és foglalkozásnapi menetrend külön ellenőrzendő; az autós modell nem képviseli az autó nélküli családokat. A menetrend és az utazási idő napszakfüggő, az eredmény bizonytalan.
- **Célcsoport:** csak települési/régiós aggregált KSH és más jogszerű nyílt statisztika. A 0–14-es csoport **nem helyettesíti** az érintett 0–3 éves célcsoportot; ha részletes adat nincs, proxy és korlát kötelező. Fiókadat, gyermekazonosító, lakcím, pontos családi koordináta vagy különleges adat **nem kerül a térképre**.
- **Pontozás:** területi szükséglet ≈ megfelelő korú gyermekek becsült száma × nehéz elérhetőség aránya × adatbizonyosság (külön bizonytalansággal). Rangsor előtt érzékenységvizsgálat küszöbökre és közlekedési módokra. A „vakfolt” nem jelenti azt, hogy ott nincs helyi alternatíva, és nem bizonyítja a fizetési hajlandóságot.
- **Kampánykapcsolat:** meglévő webes/PWA ajánlat és WooCommerce-fizetés; az MF09 prémium manuális havi hozzáférésével és MF10 médiával konzisztens, pontos ígéret. Szerkesztői szöveg/CTA WordPress ACF Free-ből, ha PWA-n belüli tartalom jön létre; marketinghez önálló analitikai megoldás előnyben. Az MF05 programlistája Virág meglévő WP-eseményeit mutatja, nem országos adatbázist.
- **Független hivatkozási alapok a későbbi kutatáshoz (2026-10-19-i ellenőrzés):** https://ringato.hu/ és https://ringato.hu/hu/ (Ringató hivatalos kereső/térkép); https://www.ksh.gov.hu/stadat_files/nep/hu/nep0035.html (vármegyei korcsoportos adat, nem települési 0–3 proxy). Ezek nem jelentenek adatátvételi engedélyt.

## Kockázatok és függőségek

- **Adat-/védjegyjog:** a központi Ringató márkanév védjegy, és a honlap tartalmának felhasználási feltételei korlátozóak. Országos adatfelhasználás, márkaüzenet, kreatív és esetleges hivatalos együttműködés jogosultsága külön tisztázandó. Ne sugalljuk, hogy Virág minden helyszínt képvisel.
- **Adatminőség:** régiek, megszűnt vagy szünetelő alkalmak; sokszoros helyszínek; határon túli adatok; nem pontos címek; frissítés elmaradása. Hamis vakfolt vagy hibás régiós rangsor reklámpénzt pazarolhat.
- **Módszertani torzítás:** autóval nem rendelkező családok, valós busz-/vonatmenetrend, foglalkozások időpontjai, kistérségi célcsoportproxy és választási szabadság. Minden hőtérképhez forrás és bizonytalansági jelzés kell.
- **Marketing és adatvédelem:** csak felnőtt célközönség jogszerű földrajzi célzása; nincs gyermekek profilozása, lakcím alapú mikrocélzás vagy meglévő ügyfelek engedély nélküli összevezetése. Hirdetési platformok aktuális szabályai, hozzájárulás és mérőeszközök külön ellenőrizendők.
- **Üzlet:** a helyszíni Ringatóval való viszonyt pozitívan, kiegészítő lehetőségként kell megfogalmazni; az online termék tartalma, hozzáférése, ára és kreatívjai jóváhagyandók. Kampánykezelési munka és reklámkeret nem része a fejlesztési becslésnek.

## Példa elfogadási feltétel

- A mintaterület valamennyi *bevont* helyszínéhez forrás, jogos felhasználás, aktualitás, helyazonosítási bizonyosság és foglalkozásállapot tartozik; az ellenőrizetlen helyszín nem kap bizonyított elérhetőségi címkét.
- Az elemzés megismételhető ugyanazon bemeneti verzióból; táblázatosan és térképen külön megjelenik a település, becsült legközelebbi eljutási idő, célcsoportproxy, hiányzó adatok és a választott küszöb.
- Véletlen mintán manuálisan ellenőrizhető az útvonal és az aktív foglalkozás; eltérésnél a terület „ellenőrzendő” státuszt kap, nem biztos vakfolt-jelölést.
- A kiválasztott pilotrégiókhoz elkészül egy jóváhagyásra kész kreatívterv, költési plafon, becsült célterület és mérési terv (UTM, aggregált landinglátogatás, vásárlási esemény, költség/új vevő, kontroll vagy referencia).
- **Nem indul éles hirdetés és nincs külső díjfizetés emberi jóváhagyás nélkül.** Sikertelen/hiányos adatjog esetén az elemzés leáll vagy engedélyezett mintára szűkül.

## Előzetes ráfordítás és értékelés

- **Besorolás:** üzleti kísérlet, kutatási előfeltétellel; nem bug, nem már vállalt MVP-funkció. **MoSCoW: Could; állapot: elemzett, nem elfogadott.**
- **Hipotetikus felhasználói érték 4/5:** utazással terhelt családoknak relevánsabb tájékoztatás. **Üzemeltetés 3/5:** célzottabb tervezés, de rendszeres adatfrissítéssel. **Bevétel 5/5:** új, eddig el nem ért érdeklődők potenciális megszólítása, validálatlan. **Kommunikáció 5/5:** erős, könnyen érthető földrajzi történet, márkajogi kontroll mellett.
- **Ráfordítási sáv L (11–25 AI-val támogatott fejlesztői munkanap) – kizárólag B típusú, egyszeri analitikai prototípus durva hipotézise.** A kézi A pilot külön kisebb kutatási/marketingmunka; a C üzemelő frissítés és hirdetésmenedzsment külön felmérés. Adatbeszerzés, utazásiadat-licenc, hirdetési költés, kreatív és marketingüzemeltetés **nincs a sávban**. Megbízhatóság alacsony, privát fejlesztői forrás / pontos adatlicenc nem vizsgált.
- **Kockázat magas:** jogszerű országos hozzáférés és módszertani hibák. **RICE nincs kiszámolva:** reach/impact/confidence/effort mérhető, egységes bemenetei hiányoznak. Kampány előtt pilotadatokból újraértékelendő.
- **Döntési kapu:** A pilot bizonyított, engedélyezett adaton mutasson érdemi, célközönséggel fedett nehéz elérhetőségű területeket; ezt kövesse külön üzleti jóváhagyás, és csak azután országos rendszer vagy költés.

## Virágnak szóló rövid ajánlat

Egy térkép megmutathatja, hol érhető el könnyen a személyes Ringató – mi pedig azt keressük meg, hol jelent túl nagy utazást a családoknak. Itt lehet különösen értékes az általad kínált online zenei tartalom: otthon, a saját ritmusukban. Előbb kis mintán, ellenőrzött adatokkal megvizsgáljuk az ötletet, és csak bizonyított lehetőségnél ajánlunk célzott, mérhető hirdetést. Ez önálló marketingkísérlet, nem a jelenlegi alkalmazás kötelező fejlesztése.

## Negyedéves kommunikációs lehetőség

- **Kampányhipotézis:** „A Ringató házhoz megy – online.” A mondat és a márkahasználat publikálás előtt Virág és szükség szerint a jogosult márkatulajdonos jóváhagyását igényli.
- **Tartalomterv:** területi nehézség érzékeltetése megbélyegző „nincs itt semmi” üzenet nélkül; meglévő foglalkozások pozitív elismerése; az online médiatár konkrét, igazolt tartalmának bemutatása.
- **Szekvencia, nem vállalt negyedéves szállítás:** kutatási tanulság → jóváhagyott területi pilothirdetés → aggregált konverziós visszajelzés → döntés az új régiókról. Nincs automatikus marketingértesítés vagy hirdetési kötelezettség.

## Következő ellenőrzendő lépés

1. Az országos Ringató-adatok jogosult kezelőjének, export-lehetőségének, felhasználási és márkaengedélyeinek tisztázása; csak megengedett adatból indulunk.
2. Virággal egyeztetni, hogy az ajánlat melyik **már meglévő online termékre** és pontos célközönségre mutat, milyen pilotköltséget/marketingmunkát hajlandó külön jóváhagyni.
3. Mintaterületek és objektív „túl hosszú út” forgatókönyvek kiválasztása; célcsoport-statisztikák területi bontásának/évjáratának ellenőrzése; induló adatminőség-tábla.
4. Az A változat belső eredménye alapján dönteni, hogy érdemes-e B modellre, majd C kampányra külön ajánlatot adni.

## Kapcsolódás a fejlesztéshez

- **Átfedésvizsgálat (IDEA-001–011):** nincs duplikátum. **IDEA-010** helyi partnerajánlat és referral, nem országos vonzáskörzet-kutatás; legfeljebb későbbi kampányterület-szinergia. **IDEA-009** érdeklődői vendégmód, egy lehetséges landing-konverziós súrlódáshoz kapcsolódhat, de nem előfeltétel.
- **MF05:** Virág WordPressből olvasott programjai; az országos Ringató helyszínlistát **nem** tartalmazza. A külső elemzés nem módosítja az MF05 API-ját vagy eseménykezelését.
- **MF09 / D09 és MF10 / D10:** a kampány a ténylegesen elérhető manuális havi prémium-hozzáférést és védett online médiát ajánlhatja, nem ígér automatikus előfizetést vagy jogosulatlan felhasználást.
- **Scope és döntési rend:** MF01–MF14, D01–D13 és a meglévő MVP változatlan. Új kampány, országos adat-API, tracking és PWA marketingfelület csak későbbi, külön jóváhagyott munka; WordPressben szerkeszthető PWA-üzenetekre továbbra is ACF Free-szabály érvényes.
