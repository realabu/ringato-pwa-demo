# 07 – Megvalósítás, tesztek, kiadás és döntések

## 1. Sorrendezett munkacsomagok

Ez implementációs backlog, nem most végrehajtott fejlesztés. Az alapmodulok a nyitott pénzügyi/üzleti döntésektől függetlenül elindíthatók; az érintett kapu nélkül a kapcsolódó funkció nem kiadható. Nincs vállalt naptári határidő vagy megalapozatlan költségbecslés.

| Csomag | Előfeltétel | Konkrét feladat és átadandó eredmény | Kész definíció |
|---|---|---|---|
| M0 – Döntések és integrációs próbák | Jelen terv | Éles leltár; D01–D13 lezárás szükség szerint; meglévő egyszeri Barion fizetés ellenőrzése; recurring kész megoldások ár/érték, teljes licenc/üzemeltetési költség és kompatibilitási feltárása (nem MVP-blokkoló); BM REST, CDN média, HPOS és cron próbák; OpenAPI 3.1/DTO | MVP-hez szükséges kapuk és negatív tesztek; G2 recurring jóváhagyás csak automatikus fázis előtt |
| M1 – Projekt és izoláció | M0 origin/auth | React/TS/Vite skeleton, app shell plugin, `/app/` routing, bootstrap/session, own SW, design token; CI/lint/build | Publikus oldal ugyanaz, `/app/` telepíthető, nonce/session működik |
| M2 – Core és olvasó adapterek | M1 | Core rétegek, migrációk, admin capability, event/catalog/order adapter, termékrule admin, média metadata, `/config/me/home` | HPOS saját rendeléshez hozzáférés és cross-user tiltás bizonyított |
| M3 – Jogosultság és staff | M2 + D02/D03/D07 | Order-item provisioning/outbox, családi jegy/bérlet/QR, atomikus checkin, audit és korrekció | Dupla callback és párhuzamos scan nem dupláz; dátumtesztek |
| M4 – Program és foglalás | M2/M3 + D04/D05 | Event config, inventory, alapdíjas reservation, paid hold minden checkout csatornára, ICS, late-payment handling | Utolsó hely konkurens tesztje és kapacitáskonfliktus visszajelzése |
| M5 – App vásárlás | M2/M4 + G1 | Terméktípus DTO-k, handoff, meglévő web kosár/pénztár, intent státusz, rendelés/jogosultság nézet | Simple/custom/variable/mixed cart útvonal, nincs kliensoldali paid flag |
| M6 – Havi prémium-hozzáférés (MVP) | M3/M5 + D09 | Bejelentkezve egyszeri WC/Barion havi termék mindkét csatornán; kifizetett hozzáférési időszak, lejárat, újravásárlás, ismételt vásárlás/idempotencia; fizetési módtól független adapter | Sikeres/failure/refund tesztek, paid-through helyes, nincs automatikus terhelés; web/PWA közös fiók |
| M7 – Média és preferenciák | M2 + CDN döntés | Privát stream, single/queue player, favorites, queue revision, prémium access, natív fullscreen | T03–T07/T06 eszközmátrix, signed segment/key védelem |
| M8 – Push és chat | M0 BM + M2 | Csoport/kampány WP admin, receipts/cursor, device/VAPID/jobs, PWA push; BM adapter + polling | Több eszköz, denied/unsupported, cross-thread tiltás, cursor verseny |
| M9 – Migráció és regresszió | M3–M8 + G3 | Papírjogok leltára, dry-run/claim/import, valós teszt tartalom, staging E2E/perf/security, backup/rollback próba | G5 és minden kötelező T teszt bizonyíték; hibás legacy jog nem kap QR-t |
| M10 – Élesítés és átadás | M9 + kapuk | Fokozatos feature flags, korlátozott ügyfélpilot, monitoring, staff oktatás, admin/runbook | Piloteredmény, napi egyeztetés, incidens/rollback felelős; release jegyzőkönyv |

M6 (manuális havi hozzáférés), M7 és M8 belső fejlesztése szerződéslezárás után egymástól részben független; ez ütemezési lehetőség, nem szükségszerű több-agent feladat. Az MVP automatikus megújulás nélkül élesíthető. **Külön, opcionális M6+ fázis:** kész és támogatott WCS/Barion vagy más megfelelő rendszer összköltség-összevetése, megrendelői jóváhagyása, sandbox, migráció és a megújulás/lemondás bevezetése; saját recurring bridge fejlesztés nincs a projektben.

### Későbbi fejlesztőnek átadandó minimum

Teljes OpenAPI és DB migration terv, plugin/npm lockfile, titokmentes `.env.example`, minimális tesztadat, feature flags, termékmapping, admin use case-ek, automata és valós eszközös tesztjegyzőkönyv, deploy/rollback/migráció runbook, staff használati leírás, médiafeltöltési/hozzáférési útmutató. A jelen csomag ezekhez az architektúrát és implementálási szabályokat adja.

## 2. Elfogadási tesztmátrix

A „kész” állapot tényleges backenddel és indokolt negatív esetekkel igazolandó. A prototípus helyi státusza nem bizonyíték. Automata tesztek elsősorban pénzügyi/jogosultsági/konkurencia invariánsokra; valós eszköz teszt a PWA, push és médialejátszás korlátaira.

| Teszt | Elfogadási feltétel és lényeges negatív eset |
|---|---|
| T01 – Fiók | WP login → app saját profil; logout/session expiry; A user nem olvashatja B order/QR/family adatát; lejárt nonce kontrollált újratöltés |
| T02 – Főoldal | Legkorábban lejáró, használható ticket/pass; used/expired/revoked kihagyás; unactivated pass utolsó; szerveridő/holmverseny |
| T03 – Médiatár | Audio/video és kategóriakeresés valós API; publikus metadata nem ad prémium forrást; jogosulatlan playback 403 |
| T04 – Single player | Egyedi média végén stop; nincs következő elem; loading/seek/error/retry/logout stop |
| T05 – Sor | Fel/le/remove, tetszőleges index, autoplay next és sorvégi stop; zárolt következőnél stop; másik eszköz revision conflict |
| T06 – Videó | 16:9 és 9:16 × portré és landscape iOS/Android; teljes képkocka, fullscreen/forgatás pozíció megmarad; play rejection használható |
| T07 – Kedvenc | Userenként elkülönül, több eszközön látszik, idempotens PUT/DELETE; törölt média biztonságos kezelése |
| T08 – Havi prémium MVP | Aktuális jóváhagyott árú manuálisan újravásárolható termék egyszeri Barion checkouttal, csak belépve; hiteles paid státusz ad hozzáférést, lejárat/újravásárlás és dupla callback biztonságos; nincs automatikus terhelés |
| T09 – Hozzáférési időszak | MVP-ben nincs automatikus renewal vagy lemondás; a már kifizetett prémium a paid-through végéig elérhető, utána nem; web/PWA azonos státusz, lejárat és újravásárlás felkínálva. A recurring cancel/renewal verseny csak M6+ teszt |
| T10 – Katalógus | Egységes web/PWA terméklista és élő ár/készlet; régi Online Ringató és új előfizetés/event termékek; opcionális alap-WC „csak webshopban” jelölés; ajándékutalvány konfigurátor; variable/custom fallback; előfizetés webes vásárlása csak belépve |
| T11 – Jegy | Fizetéstől 3 naptári hónap; jan31→apr30, szökőév, DST, napvége határ; egyetlen globális beváltás |
| T12 – Bérlet | 8 alkalom, first_used_at csak sikeres redeemnél; 8 naptári hónap; egy scan=egy decrement; remaining nem negatív; exhausted/expired tiltás |
| T13 – QR | Saját valid/unactivated joghoz QR; token TTL/revocation/owner; idegen token/lejárt screenshot tiltás; QR megnyitás nem aktivál bérletet |
| T14 – Egyszeriség | Két staff párhuzamosan ugyanazt a jegyet más programon váltja: csak egy siker; azonos key retry azonos redemption |
| T15 – Program | Részlet foglalás előtt/után elérhető; ICS UID/timezone/escaping és naptár import; hiányos/draft esemény nincs publikus appban |
| T16 – Rendszeres | Nincs kapacitás/foglalás gomb/API; családi ticket/pass beváltható, event ticket nem |
| T17 – Alapdíjas limitált | Foglalás kapacitást foglal, nem ad belépési jogot; reservation + ticket/pass kell; törölt foglalással redeem tiltás |
| T18 – Fizetős limitált | Hold+paid provisioning együtt jegy/foglalás; failed/cancelled nem végleges hely; webhook hold lejárta után full eseményre conflict és refund ügyintézés |
| T19 – Családi kapacitás | 1 family=1 hely; két párhuzamos user utolsó helyre csak egy siker; ugyanaz a family duplikáció tiltás; cancel retry nem szabadít kétszer |
| T20 – Előzmények | HPOS saját order/items jogosultság-státusz, helyes used/expired/legacy_review; nincs placeholder dupla lista; guest claim ellenőrzött |
| T21 – Push kampány | Csak megfelelő WP admin capability; egyéni/csoport/all deduplikáció, preview és kézi send; későbbi grouptagság nem módosít régi receiptet |
| T22 – Push előzmény | 365 nap cutoff, userenként egy receipt több device mellett; cursor snapshot közben érkező új receipt megmarad ÚJ; denied/410 endpoint rendben |
| T23 – Üzenet | BM saját parent–Virág thread, AJAX frissülés/read; más thread és parent-parent send tiltott; válaszvesztés nem dupla message; 200 result=false üzleti hiba |
| T24 – Staff | Capability+program scope; inspect read-only, redeem audit; rossz esemény/foglalás hiánya/timewindow tiltás; offline nem enged beléptetni |
| T25 – Admin | Eredeti WC/event admin megmarad; saját media/config/group/campaign UI, minimális role jog; kézi korrekció indok/audit; capacity invalid change tiltás |
| T26 – Scope | Nincs Kuponjaim, rövid olcsó médiacsomag vagy új Online appvásárlás; régi webes működés G1 jóváhagyása szerint változatlan |
| T27 – Oldalmegőrzés | Az alábbi publikus/shop/e-mail regressziós készlet teljesül |
| T28 – SW és offline | Scope csak /app/; idegen cache megmarad; auth/QR/media/private API nincs CacheStorage-ban; offline nincs mutáció; régi WP útvonal fallback nélkül |
| T29 – Kiadásbiztonság | Előző kliens/SW új API-val; update prompt nem szakítja meg checkout/redeem műveletet; rollback régi assetekkel működik |
| T30 – Biztonság és terhelés | Cross-user/CSRF/rate limit/SSRF/HTML sanitization; InnoDB tényleges párhuzamos foglalás és scan; cron outage/reconciliation |
| T31 – Migráció | Ismételt import nem dupláz; papírpass ismeretlen remaining nem aktiválódik; audit batch/cutoff; éles/staging személyes export nem publikus |
| P01 – Opcionális poll | Ha scope igen: egyszeri válasz DB unique, időablak, saját user, anonim aggregátum és admin eredményláthatóság |

### Oldalmegőrzési regressziós készlet

Kiinduló baseline ugyanazon staging backupból: főoldal, Rólam, Helyszínek, rendezvény/eseménynaptár, jegy/bérlet terméklista, simple termékrészlet, ajándékutalvány konfigurátor, kosár, checkout, account, meglévő URL-ek és mobilmenü. 375/711/1440px screenshot/DOM/asset ellenőrzés; dinamikus részek maszkolhatók, layout/kritikus CTA nem.

Checkout: korábbi webes kosár mellett app handoff; változatlan adó/címmező/szállítás/gateway; teszt-Barion siker/failure, Billingo sandbox számla/refund, meglévő SKU-alapú completed e-mail egyszer és változatlan tartalommal. Az új **manuális havi prémiumtermék** e-mailjéhez külön scoped adapter szükséges lehet, de nem globális theme e-mail csere. GiftRocket és legacy kombinált termék külön eset.

A jelenlegi helyi mail/cron/gateway inaktivitás miatt ezekhez dedikált staging konfiguráció és **tesztfiókok** kellenek. Éles merchant terhelést vagy ügyféllevelet tesztadat helyett nem használunk.

## 3. Döntési napló

A „javaslat” nem elfogadott üzleti döntés. A felelős a megvalósítás kezdetén pontos névvel kitöltendő; nincs most szükség minden kérdésre adott válaszra a dokumentáció használatához.

| ID | Döntés | Javasolt alap | Felelős / mikorra |
|---|---|---|---|
| D01 / G1 | **ELFOGADVA (2026-10-15):** egységes web/PWA termékkínálat | Régi Online Ringató megmaradhat; új app-előfizetés és eseménytermék weben is kapható, előfizetés csak bejelentkezve. Opcionális csak-webshop jelölés alap WooCommerce funkcióval vizsgálandó. Bejelentkezett felhasználó webes élménye feltárandó, de webes UI-módosítás külön scope | Üzleti döntés lezárva; technikai és scope-ellenőrzés M0/M5 alatt |
| D02 | Vásárlási idő és lejárat határa | Hiteles paid_at, Europe/Budapest célhónap utolsó napjára clamp, nap végéig; exclusive timestamp | Virág + backend, M3 előtt |
| D03 | Egy programon bérlet többször levonható? Napi korlát? | Egy entitlement/family/event egyszer; külön alkalom külön ID. Re-entry read-only | Virág, M3 előtt |
| D04 | Családi fiók és több jegy/átadás | V1 user=family, nincs átruházás, event max1/family; több család kézi ügyintézés | Üzleti tulajdonos, M4/M5 előtt |
| D05 | Foglalási és staff időablak, várólista, hold | Nincs várólista; alapdíjas lemondás startig; hold15m; staff start−2h/end+2h konfigurálható | Virág + backend, M4 előtt |
| D06 | „Kapott push” és címzettcsoport/consent | Receipt minden admin-címzettnek, transport külön; egy fiók egy lista,365nap; kezdeti csoportokat Virág adja | Virág + adatkezelési felelős, M8 előtt |
| D07 | Refund/chargeback/részleges és használt jegy szabály | Fel nem használt jog revocation; paid-event hely felszabadít; használt/összeg-only partial admin review; nincs automatikus visszaalkalom | Üzleti tulajdonos + pénzügy, M3/M6 előtt |
| D08 / G3 | Korábbi papírbérlet és vendégrendelés átvezetés | Bizonyított first-use/remaining/used; ismeretlen legacy review; igazolt claim; cutoff után automatikus | Virág + üzemeltető, M9 előtt |
| D09 / G2 | **ELFOGADOTT IRÁNY (2026-10-15):** manuális havi MVP, később feltételes automatikus megújulás | Kész kompatibilis opciók teljes licenc/tranzakció/üzemeltetési költségét és ár/értékét felmérjük; ha a megrendelő vállalja és teszt sikeres, automatikus módra váltunk. Addig egyszeri termék minden hónapban; nincs saját recurring bridge. Átállásra felkészített Core jogosultság | Üzleti irány lezárt; árajánlat, licenc, technikai igazolás, megrendelői döntés nyitott; recurring nem MVP-kapu |
| D10 / G4 | Média CDN és valódi tartalom | Privát signed HLS/audio/MP4, segmentvédelem; cover/ratio/hossz/felirat, volumenkalkuláció | Tartalomgazda + fejlesztő, M7 előtt |
| D11 / G4 | Better Messages free AJAX vagy WS | Free AJAX REST spike,10s aktív polling; websocket opcionális külön licenc/adapterpróba | Virág + fejlesztő, M0/M8 előtt |
| D12 | Domain, tárhely, cron, regisztráció, retention | Same-origin/app; meglévő WP login/account; valós cron; consent és audit/chat retention külön policy | Üzemeltető + adatkezelési felelős, M0/M1/M8 előtt |
| D13 | Prototípus „Virág kérdezi” része V1? | Opcionális P01, alap V1-scope-ban nincs, csak igen döntéssel | Üzleti tulajdonos, M0 előtt |

A D01 üzleti döntés alapján **nincs alapértelmezett PWA-specifikus termékszűrés vagy webes elrejtés**: az új előfizetés-/eseménytermékek és a régi Online Ringató termékek mindkét csatornán szerepelhetnek. A „csak webshopban” kivételt csak akkor vezetjük be, ha egyszerű WooCommerce-alapbeállítással megoldható. Külön tesztelendő a webes előfizetés szerveroldali, belépéshez kötött megvásárlása, az egységes fiók/jogosultság és a már belépett vásárló fiók-/előfizetésnézete. Az esetleges webes felületmódosítás a jelenlegi webmester vagy külön megbízás tárgya; nem automatikus PWA-feladat.

## 4. Kockázatok és kezelések

| Kockázat | Hatás | Kezelés |
|---|---|---|
| Barion gateway nem WCS-kompatibilis | Automatikus megújulás később nem indítható | Manuális havi termék működik; kész alternatívák költsége/kompatibilitása és megrendelői jóváhagyás szükséges; saját bridge nem MVP-feladat |
| Weboldal kódja témában hordoz domainlogikát | Pluginhook/e-mail/regresszió | Témát nem szerkesztjük; szűk adapter, baseline regresszió |
| Papírbérlet használata ismeretlen | Dupla belépési jog | Legacy review, leltár, cutoff, auditált import |
| Több fizetés utolsó helyre / késő callback | Túlfoglalás vagy fizetett teljesítési hiba | Tranzakciós hold minden csatornán, konfliktus/refund workflow |
| Cron/worker hiba | Renewal/push késés | Valós cron, queue lag riasztás, read-time expiry, reconciliation |
| Média publikus feltöltés / nem védett HLS segment | Prémium tartalom kiszivárgása | Privát storage, signed stream teljes lánc, provider teszt |
| PWA cache/session keveredés | Személyes adatszivárgás | NetworkOnly privát API, nincs user-state persistence, logout tisztítás |
| iOS push/autoplay/fullscreen eltérés | UX nem egyezik a demóval | Valós eszközös mátrix, feature detection és használható fallback |
| BM API/licenc/transport eltérés | Chat illesztés túl drága vagy nem működik | Korai spike, adapterhatár; ha alkalmatlan, külön saját text-chat ADR és becslés |
| `importing` termékek / HPOS maradványok | Téves katalógus/rendelés/migráció | Publish/purchasable szűrés, HPOS CRUD, éles leltár |

## 5. Kiadás és rollback

1. Staging: élesből származó, szükség szerint maszkolt adatok és külön sandbox titkok. Éles fizetés/SMTP nincs bekapcsolva a helyi mentés defaultjaiból.
2. Schema expand migráció és Core telepítés feature flags OFF állapotban; meglévő oldal baseline összevetés. Új `/app/` csak engedélyezett tesztfelhasználóknak.
3. App immutable build upload, shell release atomikusan vált; előző hash assetek megmaradnak. Szerver API kompatibilis előző klienssel.
4. Szűk staff pilot, tesztjegyek és külön esemény; utána kiválasztott ügyfélpilot. Valós számlázási/merchant engedély csak ellenőrzött éles konfigurációval.
5. Napi reconciliation és operációs metrikák: provisioning backlog/failed count, hold konfliktus, payment attempt uncertain, renewal failure, push queue lag/invalid endpoint, staff redeem error, auth/error rate.
6. Go/no-go: minden szükséges D/G lezárva, kötelező T01–T31 teljesült, súlyos nyitott hiba nincs, mentés-visszaállítás próbált, Virág és üzemeltető átadás kész.

Rollback nem az adatbázis vak visszatekerése. Új fizetések és beváltások után teljes DB restore elveszítené a valós kereskedelmi naplót. Első lépés feature flaggel appmutációk/új checkout indítás tiltása, előző frontend build és kompatibilis pluginverzió, az aktuális DB megtartásával. **Callback, reconciliation és már meglévő előfizetések biztonságos feldolgozása tovább szükséges.** Subscription plugint/gatewayt nem kapcsolunk ki úgy, hogy élő renewalokat magukra hagyjunk. Érintett recurring ütemezés felfüggesztéséről csak dedikált pénzügyi incidensfolyamat dönt.

DB helyreállítás csak külön incidens- és egyeztetési tervvel: backup utáni Barion/WC események visszajátszása, jogosultság/kapacitás/jegy audit összevetés. Plugin uninstall nem töröl own tables-t. Eredeti weboldal cache/cron/WAF konfigurációja kontrollált runbook szerint állítható vissza.

## 6. Mi ellenőrzött most és mi későbbi feladat?

Most ellenőrzött: DOCX V1.3 tartalom, prototípus kód és reprezentatív wallet/staff képernyők; helyi WP plugin/verzió/típus/termék/meta/count leltár; gateway támogatásdeklaráció; elsődleges technikai dokumentáció; jelen dokumentumok helyi linkjei és F/T megfeleltetése.

Későbbi bizonyíték: működő React build, OpenAPI contract, összes plugin/gateway/CDN/BM együttműködés, valódi fizetés/renewal/számlázás, konkurencia és jogosultsági teszt, mobil stream/push, éles tárhely/cron/WAF, legacy import. A terv nem állítja, hogy ezek már elkészültek vagy átmentek.
