# Ringató PWA – megvalósítási dokumentáció

**Tervverzió:** 1.0 · **Készült:** 2026. október 12. · **Alap:** Ringato_V1_3_specifikacio.docx és a jelenlegi prototípus.

A kiegészítő alkalmazás önálló React/TypeScript PWA. A meglévő WordPress/WooCommerce marad a felhasználók, termékek, rendelések és programok központi rendszere. Az eredeti publikus oldal megjelenése, útvonalai, témája és meglévő vásárlási folyamata változatlan marad. Új backendképességeket elkülönített bővítmények és saját táblák adnak hozzá.

Ez a csomag **terv**, nem működő alkalmazás. Nem telepítettünk bővítményt, nem módosítottunk témát, terméket, rendelést vagy WordPress-beállítást. A helyi példányt olvasási célból vizsgáltuk. A terv egyes üzleti szabályai ajánlott alapértékek; a döntési naplóban megjelölt kérdéseket az érintett megvalósítás előtt le kell zárni.

## Dokumentumok és olvasási sorrend

| Dokumentum | Mire használható |
|---|---|
| [01 – Feltárás és követelmények](01-feltaras-es-kovetelmenyek.md) | Ellenőrzött WordPress-állapot; V1.3 F01–F26 megfeleltetés; prototípus korlátai; terméktérkép |
| [02 – Architektúra](02-architektura.md) | Telepítés, komponensek, adatforrások, hitelesítés, elkülönítés, fizetési folyamatok |
| [03 – Bővítmények és függőségek](03-bovitmenyek-es-fuggosegek.md) | Megtartandó/új WP-bővítmények, saját fejlesztések, npm/Composer csomagok, infrastruktúra |
| [04 – Adatmodell és üzleti szabályok](04-adatmodell-es-uzleti-szabalyok.md) | Táblák, indexek, állapotgépek, konkurens foglalás és beváltás, jogosultságok, migráció |
| [05 – API-szerződés](05-api-szerzodes.md) | Tervezett végpontok, kérések/válaszok, hibák, verziózás, hozzáférési szabályok |
| [06 – React, PWA és UX](06-react-pwa-es-ux.md) | Útvonalak, modulok, lejátszás, push, service worker, mobil és offline viselkedés |
| [07 – Megvalósítás, tesztelés és döntések](07-megvalositas-tesztek-dontesek.md) | Sorrendezett munkacsomagok, elfogadási tesztek, kiadás, üzemeltetés, lezárandó kérdések |
| [08 – Forrásjegyzék](08-forrasjegyzek.md) | Helyi bizonyítékok és ellenőrzött elsődleges technikai dokumentáció |

## Fő javaslatok

1. **D12 által elfogadott irány:** a PWA a jelenlegi WordPressszel azonos HTTPS-originen az `/app/` útvonalon működjön, a meglévő WP/WC-fiókrendszerrel. Saját manifest és kizárólag `/app/` scope-ú service worker; a WordPress-oldalakon nincs PWA-regisztráció. A **jelenlegi vásárlók vendégként vásárolnak**; a PWA fiókhoz kötött funkcióihoz és a havi prémiumtermékhez bejelentkezés szükséges, miközben az általános vendégvásárlás megmarad.
2. A React buildet egy vékony **Ringató App Shell** bővítmény szolgálja ki. A **Ringató Core** bővítmény saját `ringato/v1` REST API-t, adminfelületet és üzleti szolgáltatásokat ad. A meglévő témába nem kerül új kód.
3. A V1 vásárlás a meglévő WooCommerce pénztárra történő biztonságos átadással működjön. A natív React pénztár későbbi, külön projekt; a Store API gateway-támogatása nem feltételezhető.
4. **D09 – elfogadott MVP:** havi, manuálisan újravásárolható prémium-hozzáférés a meglévő WooCommerce + egyszeri Barion fizetéssel. Az automatikus előfizetés **nem indulási feltétel**: kész, kompatibilis megoldások teljes költségét és ár/értékét fel kell mérni; csak megrendelői költségvállalással és sikeres teszttel vezethető be később. Saját recurring bridge fejlesztése nincs a projektkeretben; az architektúra átállásra készül.
5. A jegyek, bérletek, foglalások, push-előzmények és saját preferenciák külön, tranzakcióképes táblákba kerülnek. A rendelést és annak fizetési állapotát továbbra is WooCommerce CRUD-on keresztül olvassuk.
6. **D10 – elfogadott vizsgálati irány (2026-10-16):** a prémium média szerveroldali jogosultságellenőrzése és a teljes stream védelme kötelező. Először felmérjük a valós tartalom-/forgalmi igényt, megmérjük a meglévő tárhely párhuzamos audio/video kapacitását, majd összehasonlítjuk a helyi védett kiszolgálás és a külső streaming/CDN teljes költségét, teljesítményét és biztonságát. **A konkrét szolgáltató, mérési eredmény és ár még nyitott;** a WordPress publikus uploads mappa nem lehet korlátozás nélküli prémium médiatároló.
7. Better Messages REST-integráció staging próbával; a V1-hez AJAX/polling elegendő, a WebSocket külön opcionális licenc és illesztési vizsgálat.
8. **D13 (elfogadva, 2026-10-15):** a „Virág kérdezi” szavazás **kötelező V1-funkció**: WordPress adminban szerkeszthető kérdések/opciók, hitelesített PWA-szavazat, egyediségvédelem és jogosultság szerinti összesített eredmények. A korábbi opcionális P01 státusz megszűnt; TP01 elfogadási teszt kötelező.

## A megvalósítás indításának kapui

- **G1 / D01 – ELFOGADVA (2026-10-15):** Egységes WooCommerce-kínálat a weben és PWA-ban; régi Online Ringató termékek is maradhatnak, az új app-előfizetés és eseménytermékek weben is megvásárolhatók. App-előfizetést weben csak belépve lehet venni. Opcionális „csak webshopban” kivétel csak egyszerű WC-alapbeállítás esetén; a belépett webes fiókélményt fel kell mérni, webes átalakítása külön megbízás. A korábbi F26 online-értékesítés tiltása üzletileg felülírva; technikai ellenőrzés továbbra is szükséges.
- **G2 / D09 – ELFOGADOTT IRÁNY (2026-10-15):** MVP manuális havi egyszeri termékvásárlással; Barion recurring/WCS licenc **nem MVP-kapu**. Későbbi automatikus megújuláshoz: összehasonlított teljes költség, bizonyított kész integráció és kifejezett megrendelői vállalás. Saját fizetési bridge fejlesztés nélkül haladunk. A prémium-hozzáférési logika fizetési módtól független.
- **D13 / P01 – ELFOGADVA (2026-10-15):** „Virág kérdezi” szavazás kötelező az MVP-ben. A WordPress-admin, adatmodell, API és React modul, valamint a TP01 teszt az első verzió része; pontos válaszmódosítási/eredményláthatósági szabály implementálás előtt tisztázandó.
- **G3:** A papírjegyek/bérletek korábbi felhasználásának ellenőrzött átvezetése. A fizetett rendelés nem bizonyítja, hogy a belépés még felhasználható.
- **D12 – IRÁNY JÓVÁHAGYVA (2026-10-15):** a tárhely a projektgazda szerint PWA-kiszolgálásra alkalmas; **tesztdomaines WP példány és fejlesztői lokális környezet már létezik**, ezekkel vizsgáljuk a telepítést/rollbackot. A jelenlegi vendégvásárlásból az apphoz szükséges fiókregisztráció átmenetét stagingben teszteljük. **A streamkapacitás nincs igazolva**; párhuzamos audio/video terhelési mérés és a külön streaming-szolgáltató szükségességének D10 szerinti értékelése maradt nyitva.
- **D10 / G4 – MÓDSZER ELFOGADVA (2026-10-16), SZOLGÁLTATÓ NEM KIVÁLASZTVA:** a streamigény felmérése, kontrollált helyi terhelési tesztje és az elérhető külső privát streaming/CDN opciókkal való teljes költség- és minőség-összevetése végrehajtandó; eredmény alapján későbbi megrendelői jóváhagyás kell. A meglévő tárhely PWA-alkalmassága nem streaming-kapacitásmérés.
- **G4:** Better Messages API/licenc, védett médiakiszolgálás **mért párhuzamos kapacitással**, valós cron/reverse proxy és regisztrációs flow tesztje nyitott.
- **G5:** Stagingben igazolt weboldal-, webshop- és e-mail-regressziómentesség.

A háttérrendszer bővítése szükséges; a „változatlan oldal” a meglévő publikus felület és működés megőrzését jelenti. A WordPress teljes technikai változatlansága mellett a megadott API-alapú funkciók nem valósíthatók meg.
