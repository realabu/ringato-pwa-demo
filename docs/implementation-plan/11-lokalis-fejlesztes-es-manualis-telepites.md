# 11 – Lokális fejlesztés és manuális telepítés

**Munkarend:** elfogadott pontosítás, 2026-10-15. Fejlesztés és tesztek lokálisan; tesztszerveres és éles kitelepítés kézzel, verziózott csomagból. Nincs automatikus deploy.

**A dokumentum állapota:** telepítési terv és minden kiadáshoz kitöltendő útmutató. A React app, Ringató Core és App Shell még nincs implementálva; az alábbi saját plugin-/buildútvonalak tervezett csomagszerződések. Nem állítjuk, hogy már léteznek ZIP-ek, adminmenük vagy migrációs parancsok. Ezek pontos neve, verziója és kipróbált lépése az érintett mérföldkő átadási feltétele. A szerver dokumentumgyökerét és hozzáférését a telepítő adja meg.

## 1. Környezetek és felelősség

| Környezet | Mire használjuk? | Ki és hogyan módosítja? |
|---|---|---|
| Lokális WordPress + app | Fejlesztés; egység-, integrációs, E2E-, regressziós, konkurencia-, PWA- és eszköztesztek; csomagtelepítés/frissítés/rollback próbája | Fejlesztő, helyi forrásból és buildből |
| Tesztszerver | A lokálisan ellenőrzött csomag kézi fogadása; telepítés utáni rövid működésellenőrzés és bemutató | Telepítő/üzemeltető manuálisan; sandbox környezeti adatokkal |
| Éles | Azonos kiadási csomag, éles környezeti konfiguráció, fokozatos funkcióbekapcsolás | Telepítő/üzemeltető manuálisan, mentés és telepítési jegyzőkönyv mellett |

A fejlesztő átadja a csomagot, lokális teszteredményeket, változáslistát, függőségeket és lépésről lépésre telepítési/rollback-útmutatót. A telepítő kitölti a célkörnyezet adatait és rögzíti a végrehajtás eredményét. A tesztszerveren feltárt hiba javítása és tesztelése lokálisan történik; új csomagot kell készíteni, szerveren forráskódot szerkeszteni nem része a folyamatnak.

A célkörnyezeti ellenőrzés nem teljes fejlesztési tesztkör. A helyi siker nem bizonyítja a tárhely valós streamkapacitását, egressét, WAF-/cron-/cache-beállításait; ezek üzemeltetői igazolása vagy külön mérés szükséges az érintett funkció élesítéséhez.

## 2. Lokális környezet és tesztelési előfeltételek

A meglévő környezet: `wordpress-local/`, Compose-projektnév `ringatoviraggal-local`, WordPress és MariaDB konténer, tartós `wp_data`/`db_data` kötetek. Honlap: `http://localhost:8080`, admin: `http://localhost:8080/wp-admin/`. A részletes kiinduló állapot a projektgyökér `wordpress-local/README.md` fájljában található.

Indítás a projektgyökérből:

```bash
cd /home/admin/projects/ringatoviraggal/wordpress-local
DOCKER_CONFIG="$PWD/.docker" docker compose up -d
```

Leállítás adatmegtartással:

```bash
DOCKER_CONFIG="$PWD/.docker" docker compose down
```

A `down -v` törölné a tartós adatokat. A `setup.sh` régi XML-es kezdeti telepítő; nem a jelenlegi teljes mentés általános visszaállítója.

| Terület | Jelenlegi helyi állapot | A kapcsolódó mérföldkő teendője |
|---|---|---|
| Új saját pluginek | MF01–MF03 saját pluginek elkészültek, a 8081-es klónon telepítve; részletek a 11. szakaszban | MF01/MF03: csomagok másolása a konténer `wp-content/plugins/` alá, vagy külön pluginonként dokumentált fejlesztői bind mount. A teljes plugins mappa mountolása elfedné a meglévő bővítményeket. A pontos helyi parancs az első csomaghoz mellékelendő. |
| Levélküldés | A helyi mu-plugin tiltja; SMTP inaktív | MF04: lokális levélfogó és kizárólag helyi kézbesítést engedő konfiguráció kialakítása; a tiltás kontrollált illesztése. Regisztráció/reset levél így ellenőrizhető, ügyfélcímre küldés nélkül. Ez még nincs kész. |
| Cron | `DISABLE_WP_CRON=true` | Háttérjobokhoz dokumentált kézi WP-CLI/Action Scheduler futtatás, vagy lokális időzítő; a konkrét futtatási lépés és verzió az érintett kiadás része. A letiltott automatikus cron nem sikeres jobteszt. |
| Fizetés/számlázás | Barion és Billingo inaktív | MF07/MF09: kizárólag sandbox/teszt hitelesítőkkel aktiválni és próbálni. Külső callbackhoz szükség esetén ideiglenes HTTPS-alagút, csak a szükséges útvonalra. Hálózati elérés hiányában mockteszt külön jelölendő; nem bizonyítja a valós sandbox-integrációt. |
| Cache/WAF | Super Cache és Wordfence lokálisan inaktív | Lokálisan header-/útvonalteszt; szerveres cache/WAF szabályok külön telepítési beállítások. |
| Valós mobil, push, kamera, PWA | A port jelenleg `127.0.0.1` címhez kötött | Eszközteszthez dokumentált lokális HTTPS-elérés megbízható tanúsítvánnyal és szűk hálózati hozzáféréssel. A telefon `localhost` címe a telefonra mutat. A tesztelési proxy/tanúsítvány nem kerül az éles csomagba. |
| Importált adatok | Mentett rendelések, fiókok és integrációs beállítások is jelen lehetnek | Elkülönített tesztfiókok, szükség szerinti maszkolás; importált éles kulcsok nem használhatók tesztintegrációhoz. |

A lokális integrációs teszt az appot ugyanazon WP-originen `/app/` alatt használja. Vite külön portja fejlesztői eszköz lehet dokumentált proxyn keresztül; a végső auth/PWA/checkout teszt a csomagolt builddel és same-origin működéssel történik.

## 3. Kiadási csomag

Minden kézzel kitelepíthető növekményhez az alábbi szerkezetű csomag készüljön. A `<release>` és `<version>` helykitöltő; a konkrét kiadásban valódi azonosító szerepel.

```text
ringato-release-<release>/
  RELEASE.md                       # mérföldkő, változások, ismert korlátok
  INSTALL.md                       # ehhez a verzióhoz pontos, kipróbált műszaki lépések
  INSTALL-DOC.md                   # közérthető, lépésről lépésre telepítési útmutató
  ROLLBACK.md                      # kompatibilis visszaállítási lépések
  versions.json                    # build/API/schema/plugin verziók, minimumok
  checksums.sha256                 # átadott fájlok ellenőrzőösszege
  plugins/
    ringato-core-<version>.zip     # MF03-tól, ha érintett
    ringato-app-shell-<version>.zip
  config/
    settings.example.md            # környezeti mezők, titkok nélkül
    product-event-mapping.example.csv
  migrations/
    README.md                      # szükségesség, futtatás, ellenőrzés
  verification/
    local-test-results.md
    post-install-checklist.md
```

**Kötelező kétféle telepítési útmutató (2026-10-15):** minden kiadáshoz és mérföldkő-növekményhez a műszaki `INSTALL.md` mellé mindig készüljön és frissüljön egy **`INSTALL-DOC.md`** nevű, informatikai alapismeretekkel rendelkező személy számára is követhető változat. Mindkét dokumentum kerüljön be a verziózott kiadási csomagba, és ugyanannak a kiadásnak a tényleges telepítési lépéseit írja le.

Az `INSTALL-DOC.md` konkrét, számozott teendőket tartalmazzon: hova kell belépni; a WordPress melyik menüpontját és gombját kell használni; melyik ZIP-et kell feltölteni és milyen sorrendben; a szerveren melyik mappát kell megnyitni vagy létrehozni, és pontosan mely fájlokat hova kell másolni. Jelezze, ha egy mappát nem kell kézzel létrehozni. Térjen ki az előfeltételekre, mentésre, beállításokra, ellenőrzésre és visszaállításra is. A szakkifejezéseket röviden magyarázza el; a fejlesztői és üzemeltetői feladatokat külön, a megfelelő felelősnek továbbadható lépésekben adja meg. A parancsoknál szerepeljen a futtatás helye és a helykitöltők jelentése. Az útmutató ne feltételezzen fejlesztői tudást.

A ZIP-eknek közvetlenül a megfelelő `ringato-core/`, illetve `ringato-app-shell/` pluginmappát kell tartalmazniuk. A PHP runtime függőségek (`vendor/`, autoloader) a kész csomagban szerepelnek; Composer vagy Node nem előfeltétele a tárhelyes telepítésnek. A React production build az App Shell csomag része; ne külön fejlesztői forrásból épüljön szerveren.

Az MF01–MF03 tényleges buildparancsait, verzióit, lockfile-ját és csomagolóparancsát a 11. szakasz és a hivatkozott INSTALL.md rögzíti. A telepítő a lokálisan ellenőrzött kész csomagot kapja meg.

**Nem kerül a csomagba:** helyi `.env`, `wp-config.php`, teljes WordPress-adatbázis, `.wpress` mentés, Docker-környezet, helyi mu-plugin, tesztfelhasználók exportja, `node_modules`, éles/sandbox titkok és fejlesztői tanúsítványok. A tartalom- vagy régi jogosultságimport külön, ellenőrzött MF14 művelet.

## 4. Mit hova kell másolni?

Az alábbi célok a tényleges WordPress-gyökérhez relatívak. Egyedi `WP_CONTENT_DIR` esetén a telepítő a valódi content könyvtárat használja; a kiszolgáló abszolút útvonalát nem feltételezzük.

| Átadott elem | Célhely | Megjegyzés |
|---|---|---|
| Kibontott `ringato-core/` | `<WP_ROOT>/wp-content/plugins/ringato-core/` | Backend, REST, admin, migrációk és becsomagolt PHP-függőségek; MF03-tól. |
| Kibontott `ringato-app-shell/` | `<WP_ROOT>/wp-content/plugins/ringato-app-shell/` | `/app/` kiszolgálás, bootstrap és build; MF01-től. |
| App build | Tényleges: `ringato-app-shell/builds/<release>/` a pluginon belül | A csomag tartalmazza. Az MF01 igazolja a pontos belső elrendezést és aktív build váltását. Korábbi kliensekhez szükséges hash-elt assetek megmaradnak. |
| Manifest, SW, ikonok, offline oldal | A becsomagolt app buildben; publikus URL-ek `/app/` alatt | A plugin szolgálja ki. A manifest scope és SW scope kizárólag `/app/`. |
| Külső Better Messages plugin | A plugin saját szabványos `wp-content/plugins/` mappája | Csak MF12-höz, sikeres D11 próba után, a kiadásban megadott csomagból/verzióból. |
| Környezeti titkok | A tárhely védett konfigurációja / a konkrét integráció támogatott adminbeállítása | A kiadás megadja a pontos mezőt vagy konfigurációs kulcsot; nem publikus JSON/JS és nem forráskontroll. |
| Termék-, esemény- és jogmapping | A Core majdani adminfelülete vagy dokumentált importja | Célkörnyezeti azonosítókkal; helyi adatbázis átmásolása nélkül. |

**Az `/app/` URL, nem kötelező fizikai mappa a webgyökérben.** Nem másoljuk a Vite `index.html` fájlt a WordPress gyökerébe; az útvonalat az App Shell kezeli. Nem módosítjuk az eredeti témát, és nem írjuk felül a teljes `wp-content/`, `uploads/` vagy plugins könyvtárat.

Kézi módszerek: WP-admin plugin ZIP feltöltés/frissítés, vagy SFTP/tárhely fájlkezelő. A használt módszert a kiadási jegyzőkönyv rögzíti. Frissítéskor a kész pluginmappát az INSTALL.md szerint cseréljük, az elavult PHP-fájlok kezelésével; nem keverjük össze külön verziók fájljait. A régi appassetek megtartását a kiadási csomag és a Shell kezeli, nem a telepítőnek kell találomra fájlokat megőriznie.

## 5. WordPress-bővítmények

| Bővítmény | Telepítési teendő | Mikortól szükséges? |
|---|---|---|
| WooCommerce és meglévő esemény-/termékmegoldás | Meglévőt megtartani; a kiadási verziómátrix szerint ellenőrizni | MF05-től üzleti adatokhoz; Core függőségvizsgálata MF03-ban készül |
| Ringató App Shell | Saját kiadási ZIP felrakása és aktiválása | MF01 |
| Ringató Core | Saját kiadási ZIP felrakása és aktiválása | MF03 |
| Meglévő Barion gateway | Megtartani; helyileg sandbox konfigurációval aktiválni; szerveren környezet szerinti kulcsok | MF07/MF09 |
| Meglévő Billingo | Megtartani; sandbox/éles adatok és számlázási hatások ellenőrzése | Fizetési integráció |
| Better Messages | Új plugin; csak igazolt D11 megoldás és rögzített verzió/licenc után | MF12 |
| GiftRocket, CookieYes, SMTP, cache, WAF és egyéb meglévő pluginok | Megtartani, érintett integrációt/configot dokumentálni | A megfelelő modulnál; önálló frissítésük nem része automatikusan a PWA-kiadásnak |
| Action Scheduler | A meglévő WooCommerce által biztosított példány használata | Háttérjobok; külön plugin csak bizonyított szükség esetén |

Nem kell külön PWA-, JWT-, QR/jegy-, push SaaS- vagy általános booking plugint felrakni a tervezett saját modulok mellé. WooCommerce Subscriptions/recurring plugin nem MVP-előfeltétel; későbbi külön döntés és csomag.

A kiadás minden meglévő és új függőséghez pontosan rögzíti a **tesztelt verziót, minimumot, szükséges PHP-kiterjesztéseket, licencet és aktiválási sorrendet**. A mostani terv csomagnevei nem helyettesítik a későbbi kompatibilitási listát.

## 6. Mit kell beállítani?

A jelen táblázat beállítási leltár. A saját adminmezők és konfigurációs kulcsok pontos helyét az adott modul elkészültekor az INSTALL.md tartalmazza; most nem létező adminmenükre nem adunk kattintási utasítást.

| Beállítás | Lokális | Tesztszerver | Éles |
|---|---|---|---|
| Canonical origin és appútvonal | Helyi WP-origin + `/app/`; eszközteszthez helyi HTTPS | Tesztdomain HTTPS + `/app/` | WP kanonikus HTTPS-origin + `/app/` |
| WP/WC fiók | Regisztráció/reset tesztfiókkal és levélfogóval | Azonos támogatott fiókút, tesztlevelek | Jóváhagyott fiókút és kézbesítés; általános vendégvásárlás megmarad |
| Prémium vásárlási korlát | Termékszintű login-korlát tesztje | Céloldali mapping és korlát ellenőrzése | Weben és appból is szerveroldali login-korlát |
| Feature flag-ek | Csak elkészült/tesztelt modul | Kezdetben OFF vagy korlátozott tesztkör | Kezdetben OFF/pilot, majd fokozatos bekapcsolás |
| Termék/esemény mapping és árak | Helyi tesztazonosítók | Tesztszerver saját azonosítói | Éles azonosítók, jóváhagyott árak és szabályok |
| Barion/Billingo/SMTP | Sandbox és levélfogó | Sandbox és kizárólag tesztcímzettek | Meglévő éles konfiguráció megőrzése, új termékmapping ellenőrzése |
| Média | Engedélyezett tesztanyag, privát forrás tesztje | Elkülönített tesztforrás, ha szükséges | D10 szerinti igazolt privát kiszolgáló és hozzáférés |
| Push/VAPID | Helyi tesztkulcs, tesztböngésző | Külön tesztkulcs és címzettkör | Stabil éles kulcspár; privát kulcs backendben, nem kiadásonként cserélendő |
| Staff/admin jogosultság | Tesztrole és hozzárendelt tesztesemény | Tesztstaff, szűk capability | Nevesített staff/admin, esemény-hozzárendelés |
| Cron/jobs | Kézi vagy lokális ütemezett futtatás | Üzemeltető által beállított futtatás | Valós, monitorozott futtatás; meglévő webes cronfeladatok megőrzése |
| Cache/WAF | Privát header- és SW-tesztek | App/API/auth/checkout kivételek beállítása | Ugyanezen elvek az éles stackhez igazítva |

Cache-követelmények: személyes shell, `/app/bootstrap.json`, privát REST/BM és checkout/session válaszok `private,no-store`/cache-bypass; hash-elt statikus appassetek hosszú immutable cache; SW/manifest újraellenőrzést engedő policy. A rewrite a `/app/` mély útvonalait Shellre vezesse; `/wp-admin/`, webshop és régi WP-oldal nem kap appfallbacket. A konkrét Apache/Nginx/WAF szabály a tárhely stackjétől függ, az INSTALL.md a tényleges beállítást vagy tárhely-admin lépést tartalmazza.

A cron pontos parancsa és gyakorisága, pluginadmin mezők, migrációs indítás, valamint az aktív appbuild kiválasztása az implementáció során rögzítendő. Ezek nélkül az érintett modul nem tekinthető manuálisan telepíthetőnek.

## 7. Első kézi telepítés – tesztszerver, majd éles

1. **Kiadás ellenőrzése:** release-azonosító, ellenőrzőösszeg, lokális teszteredmények, plugin-/PHP-/DB-kompatibilitás, valamint az INSTALL.md és INSTALL-DOC.md megléte és egyezősége. Tényleges célkönyvtár, domain, telepítő és mentés helyének rögzítése.
2. **Mentés:** célkörnyezeti adatbázis, érintett pluginfájlok, konfiguráció és szükséges assetek mentése, visszaállítási lehetőség ellenőrzése. Kiinduló web/shop/fiók működés rögzítése.
3. **Előfeltételek:** meglévő WC/integrációk ellenőrzése; szükséges új külső plugin telepítése a kiadás verziólistája szerint. Tesztszerveren sandbox/levélizoláció ellenőrzése bármilyen fizetési vagy küldési művelet előtt.
4. **Saját pluginok másolása:** az MF01-only csomaghoz App Shell elegendő; MF03-tól Core, majd kompatibilis App Shell csomag telepítése. Hiányzó Core mellett a Shell a kiadásban definiált biztonságos korlátozott állapotot használja. Üzleti feature flag-ek kezdetben OFF.
5. **Aktiválás és migráció:** a kiadás szerinti sorrendben; MF03-tól Core schema/migráció ellenőrzése az appfunkciók bekapcsolása előtt. Rögzíteni a DB schema verziót és eredményt. A pluginbekapcsolás önmagában nem bizonyítja a migráció sikerét.
6. **Környezeti beállítások:** fiókút, termék/esemény mapping, titkok, staff, média/push és cron a telepített modulok szerint. Helyi ID-k és tesztkulcsok nem másolhatók vakon élesre.
7. **Útvonal/cache:** szükség esetén egyszeri rewrite-frissítés a kiadás leírása szerint; cache/WAF kivételek és HTTP-headerek ellenőrzése. Cacheürítés célzottan, idegen SW-cache törlése nélkül.
8. **Appbuild kiválasztása:** a csomagban megadott, teljesen feltöltött build aktiválása; hiányos feltöltésre nem váltunk. API–Shell–build kompatibilitás és régi assetek elérhetősége ellenőrzendő.
9. **Működésellenőrzés:** a 9. szakasz rövid listája. Hiba esetén funkció visszazárása/rollback és helyi javítás, új kiadás.
10. **Jegyzőkönyv:** telepített verziók, módosított beállítások titkok nélkül, migráció és ellenőrzés eredménye; engedélyezett modulok. Tesztszerveres siker után ugyanazt a csomagot, éles konfigurációval telepítjük manuálisan; éles környezetben is kell működésellenőrzés.

A másolás nem írja felül a cél WordPress-adatbázisát a helyi adatbázissal. A szükséges új termékek/események/adminadatok külön, dokumentált módon jönnek létre. Régi jogok importja kizárólag MF14/D08 szerint.

## 8. Kézi verziófrissítés és visszaállítás

**Frissítés:** változáslista és kompatibilitás ellenőrzése → célmentés → érintett új műveletek rövid felfüggesztése, ha szükséges → Core és bővítő, visszafelé kompatibilis sémamigráció → új Shell/build feltöltés → teljes build aktiválás → célzott cachekezelés → működésellenőrzés → flag-ek engedélyezése → jegyzőkönyv. Az INSTALL.md minden kiadáshoz megadja, hogy mely komponens cserélendő és milyen sorrendben; indokolt eltérést konkrétan leír.

Ha a fájlkezelő/SFTP nem tud atomikus mappacserét, dokumentált rövid karbantartási időszakban történjen a pluginfájlok cseréje. Folyamatban lévő fizetés, callback és staff beváltás kezelését a kiadásnak figyelembe kell vennie. Nem elég az összes új fájlt lassan a futó verzióra másolni.

**Appassetek:** a csomagoló/Shell megőrzi a még támogatott korábbi build hash-elt asseteit. A ZIP-frissítés után is elérhetők maradnak az előző kliens által kért URL-ek; ezt lokális frissítési teszt igazolja. Takarítás csak dokumentált támogatási ablak után történhet. Új SW nem tölt újra automatikusan checkout/beváltás közben.

**Rollback:** érintett új műveletek flaggel lezárása → előző kompatibilis frontend/build és szükség esetén plugin visszaállítása a kiadási utasítás szerint → aktuális DB megtartása → működésellenőrzés és pénzügyi/jogosultsági egyeztetés. Callbackok és helyreállító jobok biztonságos feldolgozása tovább szükséges. Plugin uninstall nem törölheti a saját üzleti táblákat.

Teljes DB-restore új vásárlások/beváltások után adatvesztést okozhat, ezért külön incidens- és egyeztetési tervhez kötött. Nem visszafordítható sémaváltozásnál az INSTALL/ROLLBACK pontosan rögzíti a kompatibilis visszaállítás vagy előrefelé javítás módját. Destruktív sématisztítás nem része az első váltásnak.

## 9. Telepítés utáni rövid ellenőrzőlista

Csak az adott kiadásban szereplő modulokra alkalmazandó; az eredményt környezetenként rögzíti a telepítő.

- [ ] A főoldal, meglévő webshop, kosár és fiókoldal működik; az általános vendégvásárlás megmaradt.
- [ ] `/app/` és egy mély link újratöltéssel megnyílik; a helyes release/API/schema verzió látszik a diagnosztikában.
- [ ] Belépés után a saját teszt/pilot fiók jelenik meg; kijelentkezés után nem látszik személyes adat.
- [ ] A manifest/SW scope `/app/`; nincs root scope-ra kiterjesztés, privát válasz nem lett cache-elve.
- [ ] A szükséges migrációk sikeresek, nincs váratlan PHP-/REST-hiba.
- [ ] Termék-/eseménymapping és feature flag-ek célkörnyezeti értékei helyesek; staff jogok szűkek.
- [ ] Fizetés/SMTP/Billingo/média/push a megfelelő környezetet használja; tesztszerver nem terhel és nem értesít éles ügyfelet.
- [ ] Háttérjob futtatás és hibajelzés rendben; stream és külső szolgáltató elérhető, ha a modul része.
- [ ] Korábbi kliens assetei még elérhetők; frissítésjelzés és a rollbackhoz szükséges csomag rendelkezésre áll.

Éles környezetben a lista nem jelent kötelező valódi fizetés, számlakiállítás vagy tömeges push indítást; ezekhez a release előre megadja a kockázatmentes ellenőrzési módot. Az alkalmazás puszta HTTP 200 válasza nem igazolja az üzleti integráció helyességét.

## 10. Kötelező kiadási és telepítési jegyzőkönyv

Minden MF-növekmény átadásakor kitöltendő; a távoli részek a későbbi kézi telepítéskor egészülnek ki.

| Mező | Kitöltendő adat |
|---|---|
| MF / release / dátum | Mérföldkő, egyedi buildazonosító, csomagellenőrzőösszeg |
| Komponensek | Core / Shell / app / API / schema verzió; külső pluginok tesztelt verziója |
| Lokális ellenőrzés | Futtatott tesztek, eredmény, eszközök, mock és valós sandbox külön jelölve |
| Másolási lista | Pontos ZIP/fájl és célmappa, telepítési módszer, csere/törlés/assetmegtartás |
| Aktiválás és konfiguráció | Pontos WP-admin lépések vagy támogatott kulcsok; környezeti eltérések, titokértékek nélkül |
| Adatváltozás | Migráció/parancs/indítási hely, schema előtte–utána, ellenőrzés; új mapping/tartalom |
| Rollback | Előző kompatibilis kiadás, lépések, adatbáziskorlátok, mentés helye |
| Célkörnyezet | Teszt/éles domain, WP-gyökér, telepítő neve és időpontja |
| Utóellenőrzés | Lista eredménye, engedélyezett flag-ek, észlelt hiba/teendő |

**Mérföldkőnkénti dokumentációs minimum:** MF01 csomag/build/Shell/SW és másolás; MF03 Core/schema/API; MF04 fiók/levél; MF05 mapping; MF07–MF09 fizetés/jog/foglalás/prémium; MF10 média; MF11 poll-admin; MF12 BM; MF13 push/cron; MF14 import és teljes átadás. MF02/MF06 az új asseteket/buildet és az esetleges konfigurációváltozást dokumentálja. Ha nincs új plugin, beállítás vagy migráció, azt a release kifejezetten jelzi.


## 11. MF01–MF03 tényleges megvalósítás – 2026-10-15

A korábbi szakaszok tervezett útvonalait e kiadásra az alábbi tényleges leltár pontosítja. Forrás a `ringato-dev/` gyökeréhez képest: `ringato-pwa/`, `wordpress-plugins/ringato-core/` és `wordpress-plugins/ringato-app-shell/`. A Docker `pwa` szolgáltatása is az új `ringato-dev/ringato-pwa/` alkalmazást futtatja (`http://localhost:5173/app/`), WP-proxyval. A korábbi `ringato-dev/pwa/` demómásolat megszűnt; a referencia a `ringato-pwa-demo/` alatt maradt.

**Ellenőrzött lokális WP:** `ringatoviraggal-dev-wordpress-1`, `http://localhost:8081` (WP 7.1.3 / PHP 8.3.35 / WC 11.1.2). A 8080-as eredeti példány változatlan. A két saját plugin már a klónon aktív. Minimum: WP 6.6 / PHP 8.1; MF03-hoz WC nem kötelező. A meglévő külső pluginokat nem frissítettük.

**Build és csomag:** a `ringato-dev/` gyökeréből `cd ringato-pwa && npm ci && npm run contracts && npm run lint && npm test && npm run release`. Node 24 / npm 11 / Python 3. A csomag helye `releases/ringato-release-<build>/`, ZIP-ek a `plugins/` alatt. A ZIP-ek a WP plugins könyvtárba kerülő mappát közvetlenül tartalmazzák. Kész build: `ringato-app-shell/builds/<build>/`; aktív alapérték a plugin `release.json` fájljában. Publikus hash-elt URL: `/app/builds/<build>/assets/<file>`. Bootstrap, manifest, worker, ikonok és offline lap a megfelelő `/app/` URL-en érhetők el. A korábbi támogatott buildmappák benne maradnak a csomagban; tiszta checkouton a csomagoló `--previous <elozo-shell.zip>` paramétere veszi át őket. Nincs új PHP runtime függőség, Composer vagy szerveres Node-telepítés.

**Lokális másolás:** a `ringato-dev/` gyökeréből `bash scripts/install-local.sh ringatoviraggal-dev-wordpress-1`. Core, utána Shell másolás és aktiválás a konténer `/var/www/html/wp-content/plugins/` alá. Csak a két saját plugin érintett. Távolra ugyanezeknek a ZIP-eknek a telepítése kézzel történik, mentés és célkörnyezeti ellenőrzés után.

**Migráció és konfiguráció:** schema 1 aktiváláskor/init során; hozzáadó admin capability-k és névterezett optionök, üzleti tábla/adatimport nélkül. Ellenőrzés az Eszközök → Ringató diagnosztika alatt. Nincs új secret, cron, termék/event mapping vagy bekapcsolható üzleti modul. `ringato_app_build` opcionális kézi override; `wp option delete ringato_app_build` visszaáll a csomag alapértelmezésére.

**Rollback:** `wp option update ringato_app_build <elozo-build>` a már feltöltött előző mappára, majd a PWA explicit frissítése. Korábbi assetek megmaradnak. Kompatibilis Core/Shell visszamásolható; schema 1 miatt DB-restore nem kell. A két plugin kikapcsolása visszaadja a WP-nek az app útvonalát. A buildváltás és SW-frissítés/visszaállítás böngészőteszttel ellenőrzött.

**Korlátok:** root WP-telepítés, közös origin és WP front-controller rewrite szükséges; `/app` kanonikus címe `/app/`. A célkörnyezeti HTTPS/WAF/cache és fizikai mobilos telepítés külön próba. A Girly Sunrise és az eredeti képek/logó jogai nem igazoltak, ezért nincsenek a csomagban. Nunito/Montserrat OFL-licencmásolattal szerepelnek. A klónon a WC myaccount permalink üresnek bizonyult; ennek támogatott konfigurálása MF04 technikai feladata, most nincs helyette új belépési backend.

Részletes, konkrét kiadási utasítás: [INSTALL.md](../../../ringato-dev/docs/releases/mf01-mf03/INSTALL.md), [közérthető INSTALL-DOC.md](../../../ringato-dev/docs/releases/mf01-mf03/INSTALL-DOC.md), [ROLLBACK.md](../../../ringato-dev/docs/releases/mf01-mf03/ROLLBACK.md), [ellenőrzések](../../../ringato-dev/docs/releases/mf01-mf03/local-test-results.md). Az MF01 build/Shell/SW, az MF02 UI/fontasset és az MF03 Core/API/schema változásait egy közös 0.3.0 növekmény adja át. Külső plugin- vagy üzleti konfigurációváltozás nincs.


## MF04 0.4.1 – PWA-n belüli fiókűrlapok

PWA/Core/Shell 0.4.1, API 1, schema 1, ACF-tartalom 3. A build/csomagolás és a két plugin manuális frissítése az MF01–MF03 rendjét követi. Új frontendűrlapok és `/app/auth/*` POST-adapterek szolgálják ki a fiókfolyamatot, natív WP/WC user/session/password műveletekkel.

**Nincs Fiókom oldal-létrehozás, WC-fiókoldal-kijelölés vagy globális regisztrációs opcióváltozás.** A regisztráció/belépés/reset/edit a `/app/account/*` útvonalakon marad. A korábbi hibás MF04 lokális aloldalát visszavonhatóan lomtárba helyeztük és az opciókat visszaállítottuk, felhasználók/rendelések megőrzésével. A read-only `configure-account.php` nem telepítési konfiguráció.

A `/app/auth/*` POST JSON + custom header, edithez nonce/cookie, no-store és CORS-tiltás szükséges. Az ACF hozzáadó migráció a Profil alatt hozza létre az új űrlapszövegeket. A resetlevél `/app/account/reset#...` linkje is az appot nyitja; a kulcs nem HTTP URL-paraméter. A helyi levélfogó nem telepíthető távoli szerverre. Célkörnyezeten külön SMTP/HTTPS/standalone mobilpróba szükséges.

[Telepítés](../../../ringato-dev/docs/releases/mf04/INSTALL.md), [közérthető útmutató](../../../ringato-dev/docs/releases/mf04/INSTALL-DOC.md), [visszaállítás](../../../ringato-dev/docs/releases/mf04/ROLLBACK.md), [tesztek](../../../ringato-dev/docs/releases/mf04/local-test-results.md).
