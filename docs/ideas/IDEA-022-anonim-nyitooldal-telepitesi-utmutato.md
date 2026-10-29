---
id: "IDEA-022"
title: "Kijelentkezett PWA üdvözlőoldal és eszközfüggő telepítési útmutató"
area: "Belépés előtti UX és telepítés"
lane: "mvp-review"
status: "elemzett"
moscow: "Should"
effort_size: "M"
effort_min_days: 4
effort_max_days: 10
user_value: 5
operations_value: 4
revenue_value: 4
communication_value: 5
risk: "közepes"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF01","MF02","MF03","MF04","MF05"]
created: "2026-10-29"
updated: "2026-10-29"
origin: "Felhasználói észrevétel a teszt PWA-ról – 2026-10-29"
communication_angle: "Áttekinthető indulás: belépés, regisztráció és egyszerű telepítés"
---

# Kijelentkezett PWA üdvözlőoldal és eszközfüggő telepítési útmutató

## Eredeti felvetés

> észrevétel a fejlesztés kapcsán ma. a [https://www.teszt.ringatoviraggal.hu/app/](https://www.teszt.ringatoviraggal.hu/app/) oldalon elérhető kijelentkezett állapotú nézetben, igazából nem kellene látszania az app menüjének és nem kellene hogy bármelyik oldal vagy tartalom innen kezelhető legyen anonym usernek. egy szép nyitó lap kell ahonnan elindítható a login / regisztráció és elmagyarázza érthetően attól függően milyen eszközről jött a user, hogy mobilon hogyan tudja az app-ot telepíteni.

## Megoldandó probléma

A felhasználó a tesztkörnyezet kijelentkezett PWA-nézetében jelenleg az alkalmazás navigációjával találkozik; a kívánt élmény ezzel szemben egy tiszta belépési/telepítési képernyő. Ez **MVP-UX felülvizsgálat**, nem új prémium funkció vagy bizonyított jogosultsági incidens. A jelenlegi `06-react-pwa-es-ux.md` vendégként böngészhető appoldalakat említ, és az MF05 is publikus tartalmat ír le, tehát a változás korábbi, jóváhagyott irányt érint, külön jóváhagyást igényel.

## Megoldási változatok

- **A – Minimális, funkcionális védelem:** anonim állapotban csak bejelentkezés/regisztráció/jelszó-visszaállítás, minden egyéb appoldal auth-gate mögött; appmenü rejtve. Egyszerű telepítési szövegek képernyőtípus szerint.
- **B – Arculatos nyitóoldal és eszközfüggő útmutató (javasolt MVP UX):** saját, WordPress ACF Free mezőkből szerkeszthető üdvözlő/értékajánlat, két hangsúlyos CTA, iPhone/iPad, Android és desktop szerinti, valóban megvalósítható telepítési segítség; már telepített appban nincs ismételt install ajánlat. Mélylink, session- és logouttesztek.
- **C – Későbbi konverziós továbbfejlesztés:** opcionális rövid bemutató, eszközös lépésábrák, mért onboarding és A/B változatok; külön scope és adatkezelési döntés után. Nem azonos az IDEA-009 érdeklődői vendégmóddal.

## Technikai hatás, előzetes hipotézis

- **Auth-gate:** `/app/` anonim látogatónak üdvözlőoldal, `/app/*` belső route-ok belépési képernyőre vezetnek; csak auth, regisztráció, jelszó-visszaállítás és publikus install-információ érhető el. Bootstrap során ne villanjon fel a belépett menü, session-lejáratkor, logoutkor, több tabnál, frissítéskor és `standalone` módban az állapot konzisztens. Sikeres belépés után kizárólag validált, belső `/app/` célútvonalra lehessen visszatérni.
- **Biztonság:** vizuális menürejtés nem hozzáférésvédelem. A Core REST privát/mutációs végpontjain szerveroldali WP session/capability/tulajdonosi ellenőrzés továbbra is kötelező. A meglévő publikus WordPress tartalom és általános webes WooCommerce vendégcheckout változatlan; az appanonimitási korlátozás nem a teljes webhely nyilvános API-jának eltüntetése.
- **UI:** arculatnak megfelelő landing; WordPress `ringato_content` / ACF Free oldalanként szerkeszthető hero, bevezető, CTA, platformonkénti telepítési leírás, üres/hibaállapot és akadálymentes feliratok. Üzemszerű szerkesztői szöveg Reactbe nem égethető.
- **Eszközspecifikus install:** iOS/iPadOS Megosztás → Főképernyőhöz adás; az „Open as Web App” lehetőség, ha látszik. Android/Chrome saját install gomb csak valóban érkező `beforeinstallprompt` eseménnyel, egyébként menü → Telepítés/Főképernyőre. Desktopon Chrome/Edge vagy Mac Safari szerinti útmutató. Beépített böngészőben támogatott böngészőre váltást javasló fallback, már telepített appban nincs új telepítésre felhívás. Nem univerzális install API, és a telepítés nem belépési követelmény.
- **Telepítési források:** https://support.apple.com/guide/iphone/open-as-web-app-iphea86e5236/27/ios/27 ; https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable ; https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeinstallprompt_event .

## Kockázatok és függőségek

- A jelenlegi D12/MF05 vendégböngészési irányt kifejezetten módosítaná: **egyelőre felülvizsgálati javaslat**, nem csendben elfogadott scope-változtatás. Jóváhagyás után aktualizálandó a döntési napló, követelmények és tesztek.
- Egyetlen eszközdetektor alapján nem garantálható install gomb: OS/böngésző, in-app böngésző, telepítettség és támogatás eltér. Hamis install CTA és félrevezető útmutató kerülendő.
- PWA cache/manifest, logout, több tab és deep link kezelésnél regresszió lehet; WP/WC alap vendégvásárlást nem szabad érinteni.
- A megadott teszt URL közvetlen lekérése a vizsgálat során DNS/fetch okból nem sikerült; a hiba tényleges megjelenését a felhasználói beszámoló írja le. A privát implementációs forrás itt nem ellenőrzött.

## Példa elfogadási feltétel

- Kijelentkezve az `/app/` kizárólag az arculatos nyitóoldalt, login/regisztráció gombokat és telepítési segítséget mutatja; **app főmenü nem látszik**. Ugyanez igaz a telepített app újbóli indítására.
- Anonim közvetlen `/app/library`, `/app/events`, `/app/shop`, `/app/wallet`, `/app/media/:id`, `/app/messages`, `/app/staff/checkin`, illetve bármely más belső útvonal nem mutat appadatot és nem kínál appműveletet; nincs auth bootstrap alatti menüvillanás. Jogosulatlan REST olvasás és írás tiltott.
- Az auth, regisztráció, elfelejtett jelszó, helyes sessionvisszatérés és a logout teljes körben működik, a belépett menüt nem érinti.
- iPhone Safari: ténylegesen használható kézi telepítési instrukció; Android Chrome: elérhető prompt esetén működik az install CTA, máskor kézi útmutató; asztali vagy in-app böngésző: korrekt fallback; már telepítve nincs új install CTA.
- WordPressben a nyitóoldal és útmutató valamennyi szerkesztői mezője ACF Free-ből új frontend build nélkül módosítható, a jogosultsági szabály viszont nem szerkesztői tartalom.
- 320–430px, tablet, desktop, offline, képernyőolvasó és különböző sessionállapotok tesztelve; a normál webes vendégcheckout és a WP nyilvános oldal változatlan.

## Belépés utáni céloldal – 2026-10-29-i kiegészítő észrevétel

> észrevétel, hogy login után ne a profil-ra navigáljon hanem a nyitó oldalra.

- **Alapértelmezés:** a sikeres bejelentkezés után az alkalmazás **bejelentkezett főoldala** (`/app/`) jelenjen meg, ne a `/app/profile`. A bejelentkezésre szolgáló publikus üdvözlőoldal és az autentikált főoldal a session szerint külön nézet.
- **Kivétel:** ha a felhasználó egy védett belső mélylinket nyitott meg, és emiatt kellett belépnie, sikeres azonosítás után a biztonságosan ellenőrzött, alkalmazáson belüli eredeti célra térhet vissza. Külső vagy manipulált `returnTo`/redirect paraméter nem használható, nincs open redirect.
- **Profil:** csak a felhasználó kifejezett profilmenü-választására vagy érvényes profil-mélylinkre nyíljon meg; a regisztráció utáni első céloldal kérdése a tényleges onboarding-folyamat figyelembevételével ugyanezen UX-szabály szerint tesztelendő.
- **Elfogadás:** normál login → bejelentkezett főoldal; védett médiatár mélylink → sikeres login → az eredeti jogosult útvonal; lejárt/tiltott mélylink → biztonságos főoldali fallback; logout és új login → főoldal. Böngésző Back, frissítés, telepített PWA és több fül esetén nincs véletlen profilátirányítás.
- **Határ:** ez MF04 route-/post-login UX hibaészrevétel, az IDEA-022 nyitólapjához kapcsolódó kiegészítés, nem új termékfunkció. Az éles kódbeli okot a fejlesztői repóban kell ellenőrizni.

## Előzetes ráfordítás és értékelés

- **MVP-vizsgálat / Should**, nem automatikus vállalt scope. Ügyfél 5/5, üzemeltetés 4/5, bevétel 4/5, kommunikáció 5/5: kizárólag szubjektív értékhipotézisek.
- **M (4–10 AI-val támogatott fejlesztői munkanap)** csak a B változat előzetes, alacsony bizonyosságú munkasávja; nem vállalt szállítási idő vagy árajánlat. A privát forrás konkrét állapota és a tényleges integrációs ráfordítás nem ismert.
- Kockázat közepes; fontos regressziós és session/API tesztkapukkal. **RICE nincs**, mert nincs megalapozott reach, impact, confidence, effort bemenet.

## Virágnak szóló rövid ajánlat

Aki először nyitja meg a Ringató alkalmazást, ne egy bonyolult menüvel találkozzon, hanem egy barátságos, egyértelmű üdvözlőoldallal. Innen kényelmesen bejelentkezhet vagy regisztrálhat, és saját telefonján érthető segítséget kap ahhoz, hogy a Ringatót alkalmazásként is elérje.

## Negyedéves kommunikációs lehetőség

„A Ringató Virággal most már a telefonod főképernyőjéről is indulhat!” – csak sikeres PWA/telepítési és termékfelület-tesztek után kommunikálható; nincs automatikus indulási dátum.

## Következő ellenőrzendő lépés

A projektgazdai irány jóváhagyása a korábbi D12 vendégapp-UX felülírására; az elsődleges `nmarton/ringato-dev` React/Auth/Shell és tartalommodell vizsgálata; UI megvalósítás + automatizált teszt; verziózott kézi telepítési csomag és tényleges tesztoldali működésellenőrzés. Kapcsolódó feladat: https://github.com/realabu/ringato-pwa-demo/issues/2 .

## Kapcsolódás a fejlesztéshez

**MF01–MF05 / D12:** PWA manifest és install támogatás, layout és session, fiókfolyamat, publikus appkatalógus helyett bejelentkezés előtti üdvözlés. Kifejezett jóváhagyásig a meglévő döntési pontok nem tekinthetők módosítottnak. **IDEA-009:** későbbi választható guest mód; az anonim landing nem guest mód.

**Publikálási szabály:** az IDEA-lap automatikus `main`-ra kerülése csak a termékötlettár megjelenítését jelenti; a D12/MF04–MF05 megvalósítási szabályait kizárólag a külön jóváhagyott specifikációs PR módosíthatja. A fő WordPress-webhely, WooCommerce guest checkout és D01/D09 prémium vásárlási szabályok változatlanok.
