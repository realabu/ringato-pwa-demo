# Dev Status mérési szabályok

Az óránkénti `dev-status.yml` két teljes Git-checkoutból olvas, ha a privát forrásrepo hitelesítése elérhető: elsődleges a
`nmarton/ringato-dev` alapértelmezett ága, terv és demó a `realabu/ringato-pwa-demo/main`.
A JSON mindkettő pontos commitját közli; a bizonyítéklinkek ezekhez kötöttek.
A fejlesztői repó kódját a generátor nem futtatja. Hibás vagy hiányzó checkout
esetén nem készül új mérés: a korábbi ellenőrzött pillanatkép eredeti mérési idejével
és feltűnő hozzáférési hibaüzenettel marad látható. Nincs nullával helyettesített
adat vagy mesterségesen friss mérési idő. Három óra után elavultságjelzés is látszik.

## Mit mérünk?

- Fizikai UTF-8 sorok (kommentek és üres sorok is), mellettük nem üres sorok.
- Alkalmazásforrás: `ringato-pwa/src`, két HTML belépő/offline oldal,
  `wordpress-plugins` PHP és `wordpress-local/mu-plugins` PHP.
- Külön: tesztkód, generált DTO/tartalomséma, fejlesztési eszközök és demó.
  Függőség, lockfile, média, font, képernyőkép és dokumentáció nincs a fő összegben.
- Modul = forrást tartalmazó közvetlen `src/features` alkönyvtár; réteg = Core `src`
  közvetlen alkönyvtár. Egyik sem jelenti, hogy az összes üzleti funkció elkészült.
- Saját plugin = PHP `Plugin Name` fejléc és verzió a forrásban.
- Implementált opciókulcs = a saját pluginban literálként az `add_option` vagy
  `update_option` hívásnak átadott különböző kulcs. Ez nem végrehajtási audit.
- Éles pluginleltár és tényleges WP-beállításváltozás ismeretlen (`null`),
  nem nulla. A helyi telepítési jelentés külön bizonyíték, nem élő környezeti mérés.

## Mérföldkövek és aktivitás

A kiadási és tesztjelentések együtt bizonyítanak helyi implementációs átadást.
A régebbi MF01–MF04 esetén a terv explicit „ellenőrzésre kész” állapota is
alátámasztás. Az újabb kiadások implementáltságot/ellenőrzésre kész állapotot
rögzítő szövege számít. Commitcím és létező üres funkcióváz nem elég.
A 2026-10-18-i audit MF01–MF06 átadását találta; a terv 4/14-et mond, ezért
az eltérés látható marad. Fizikai mobilos és távoli/éles elfogadás nincs igazolva.

A kódesemények a teljes elsőszülői Git-történet szűrt forrásdiffjei; a törlések
is látszanak, a kizárólag dokumentációs és formázási commitok nem.
A commit címe változatlanul forrásidézet; nem a generátor funkcionális minősítése.
A `progress_fingerprint` segédjel a forrás és a kész mérföldkőhalmaz változásához;
a ChatGPT-figyelés tartalmi diffellenőrzése dönti el, történt-e érdemi előrelépés.
A dashboard címe: https://realabu.github.io/ringato-pwa-demo/dev-status/ ; a PWA gyökere megmarad.

A Pages generálás nem küld értesítést és nem ír automatikus commitot.
A meglévő óránkénti ChatGPT-feladat külön kezeli az utoljára feldolgozott változást
és az egyszer már jelzett 12 órás inaktivitási ciklust. Hiányzó hozzáférés/előzmény
nem indok stagnálási értesítésre.

## Ellenőrzött kiindulás (2026-10-18)

Fejlesztői SHA: `960319f6c0e66836068cd12cec20023f15a69a20`.

| Kategória | Fájl | Fizikai sor | Nem üres sor |
|---|---:|---:|---:|
| React PWA | 37 | 3798 | 3751 |
| Saját WP pluginek | 12 | 638 | 623 |
| Helyi MU-plugin | 1 | 28 | 27 |
| **Fő összeg** | **50** | **4464** | **4401** |
| Tesztek, külön | 16 | 2658 | 2642 |
| Generált kód, külön | 2 | 566 | 564 |
| Eszközök, külön | 10 | 599 | 598 |
| Demó, külön | 5 | 312 | — |

7 funkciókönyvtár, 9 Core-réteg, 2 saját plugin, 4 implementált opciókulcs.
A reprodukálható fájlonkénti leltár a publikált `status.json` része.

```sh
python3 -m unittest discover -s scripts -p 'test_dev_status.py'
python3 scripts/dev_status.py --dev-repo /path/to/ringato-dev
```

GitHub cron: minden óra 17. perce UTC szerint, késés lehetséges.
A fejlesztői repó **privát**. A dashboard repóban a `RINGATO_DEV_READ_TOKEN`
Actions secret szükséges, amelynek a `nmarton/ringato-dev` tartalmához olvasási joga van.
A GitHub App/installation token kizárólag ehhez a repóhoz tartozó read-only tartalomjoggal
előnyös; a sima dashboard `GITHUB_TOKEN` nem lát át a másik privát repóba.
A munkamenet szélesebb személyes OAuth-tokenjét nem másoljuk Actions-secretbe.
A helyi, hitelesített auditból származó `baseline.json` publikálható mérési leltárt
őriz (forráskód és titkok nélkül). Hozzáférési hiba esetén a generátor az utolsó
publikált, schema 2 pillanatkép és e baseline közül az újabbat tartja meg.
A `refresh.source_access=false` egyértelműen jelzi, hogy az óránkénti mérés nem sikerült.
Az értesítő ezt nem értelmezheti 12 órás inaktivitásként.
