# 12 – Kötelező WordPress tartalomkezelés

**Elfogadott követelmény: 2026-10-16. Minden jelenlegi és későbbi mérföldkőre kötelező.**

A PWA szerkesztői szövegei és blokkadatai nem lehetnek beégetve a React-kódba. A tartalom egyetlen szerkesztési helye a WordPress, az **Advanced Custom Fields ingyenes** bővítményével. A közös layout, menüfeliratok és cserélhető menüikonok ugyanúgy ide tartoznak, mint az egyes oldalak címei, kártyái, gombjai, tájékoztatói, üres/hibaállapotai és akadálymentes feliratai. Az adminban a blokkok oldalanként csoportosítva jelenjenek meg; a közös layout külön szerkeszthető egység.

A megjelenést a React/CSS sablonok adják. A kezdeti ACF-adatok a jelenlegi szövegekkel és ikonokkal egyeznek, így az átállás nem változtatja meg a PWA külsejét. A felhasználói, rendelési és jogosultsági adatok továbbra is saját hiteles adatforrásukból jönnek; szerkesztői mező nem módosíthat üzleti jogot vagy hitelesítési szabályt.

## Megvalósítás az MF01–MF03 alapokon

- A Core a `ringato_content` admin CPT 22 bejegyzésén regisztrál ACF Free Group, Text, Textarea, True/False és Image mezőket. Nincs Repeater, Flexible Content vagy Options Page függőség.
- A közös layout és minden oldal külön bejegyzés, a blokkok magyar címkéjű mezőcsoportok. A főoldali blokkok külön elrejthetők. A menüpont ikonjának karaktere vagy médiatárképe választható.
- A `content/pages.json` a verziózott szerveroldali mezőséma és az egyszeri kezdőadatok forrása. Idempotens, hozzáadó tartalommigráció; a már mentett vagy üresre törölt érték nem írható felül. Új mező esetén tartalommigráció-verzióemelés kötelező.
- `GET /wp-json/ringato/v1/content` publikus, csak engedélyezett mezőkből képzett, runtime validált DTO. Nincs publikus tartalomírás vagy személyes adat. React Query memóriából jelenít, fókuszkor és percenként frissít; a HTTP/REST válasz nem persistálható.
- Az offline tájékoztatót a Shell ACF-adatokból generálja; csak ennek a publikus HTML-nek a legutóbb online letöltött változata tárolható a saját statikus cache-ben. Offline nem várható el WP-lekérés.
- Kizárólag a CMS-kieséshez és telepítési hibához szükséges minimális technikai helyreállítási felirat maradhat kódban. Az üzemszerű UI nem használhat Reactbe másolt kezdőszöveget fallbackként.

## Minden következő mérföldkő kész-feltétele

1. Az új képernyő/blokk összes szerkesztői mezője szerepel az oldalhoz tartozó ACF-csoportban, magyar címkével, Free típusokkal.
2. A migráció hozzáadja a hiányzó kezdőadatokat és megőrzi a szerkesztett, üres és kikapcsolt értékeket.
3. Frissül a DTO, Zod-séma, OpenAPI és a frontend bekötése; szerkesztői szöveg nincs a React buildben.
4. WP-adminból mentett szöveg és menüikon új build nélkül megjelenik, oldalanként elkülönül, és a mentéshez WordPress szerkesztői jogosultság kell.
5. Az eredeti kezdőértékekkel a meglévő megjelenés mobilon és asztali nézetben is változatlan. Hiba, üres érték, offline működés és adatmegőrző újratelepítés ellenőrizve.
6. A kiadási csomag tartalmazza az ACF függőséget megnevező telepítési és tartalomszerkesztési útmutatót.

Kezelési és technikai leírás: [PWA tartalmak szerkesztése](../../../ringato-dev/docs/content-editing.md). Az ACF Free telepítése a [gyártó hivatalos forrásából](https://www.advancedcustomfields.com/resources/installation/) történjen.
