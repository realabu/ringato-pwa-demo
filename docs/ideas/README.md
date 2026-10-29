# Ringató – ötlettár és termékroadmap

Szabad szöveges ötletek feldolgozására létrehozott **közösen szerkeszthető, AI-kompatibilis termékötlettár**. A GitHubon lévő `IDEA-*.md` fájlok a hiteles források. A HTML és a `catalog.json` ezekből generálódik.

## Hogyan használja egy másik kolléga?

1. Kapjon GitHub-olvasási és szerkesztési hozzáférést a `realabu/ringato-pwa-demo` repositoryhoz.
2. Nyissa meg a repót tetszőleges AI-asszisztenssel (Codex, ChatGPT, Claude vagy hasonló).
3. Írja: **„Olvasd el az AGENTS.md és a docs/ideas/README.md fájlokat. Új ötletem: [szabad szöveg]. Keress duplikátumot, dolgozd ki változatokra, értékeld, majd frissítsd a repót és a HTML-katalógust.”**
4. Az AI meglévő ötletet bővít vagy új `IDEA-XXX-*.md` fájlt készít; validálás után **csak az IDEA Markdownot** közvetlenül a `main` ágba commitolja, ha van jogosultsága. Nem kell külön jóváhagyni az ötlet regisztrálását.
5. Ha több szerkesztő PR-ben dolgozik, a [külön ötletpublikáló workflow](../../.github/workflows/auto-publish-ideas.yml) a **nem draft, azonos repóbeli PR-ből** csak a validált `docs/ideas/IDEA-*.md` fájlokat másolja automatikusan a `main` ágba. A specifikációs, döntési és kódmódosítások a PR-ben maradnak, és csak külön jóváhagyással merge-ölhetők.
6. A `main` ágba került ötletlapok alapján a GitHub Pages generálja az aktuális HTML-katalógust. Automatikus PR-átvételnél a folyamat kifejezetten elindítja a Pages jobot, mert a GitHub Actions saját tokenes commitja önmagában nem indít push workflow-t.

**HTML-cím:** https://realabu.github.io/ringato-pwa-demo/ideas/

A folyamat másik beszélgetésből is megismételhető; nem kell ismerni az eredeti ChatGPT-beszélgetést.

## Szerkezet

- `AGENTS.md` – AI-munkafolyamat és védőszabályok.
- `docs/ideas/SCHEMA.md` – strukturált frontmatter és értékelés.
- `docs/ideas/TEMPLATE.md` – új ötlet mintája.
- `docs/ideas/IDEA-*.md` – ötletek eredeti megfogalmazással és kidolgozással.
- `docs/ideas/index.html` – kereső/szűrő/részletes vizualizáció.
- `scripts/build_ideas.py`, `scripts/test_build_ideas.py` – automatikus validálás és generálás.
- `.github/workflows/dev-status.yml` – a **meglévő** óránkénti és `main`-ra commitoláskor induló Pages publikálás.
- `.github/workflows/auto-publish-ideas.yml`, `scripts/promote_ideas.py` – az azonos repóbeli PR-k ötletlapjainak validált, csak-ötlet automatikus átvétele és a Pages workflow indítása.

## Üzleti módszertan

**Besorolás:** `mvp-review` = specifikációval összevetendő hiba vagy alapvető UX; `later-feature` = jövőbeli ajánlható fejlesztés; `research` = megvalósíthatósági kutatás; `business-experiment` = új üzleti modell próbája.

**MoSCoW:** backlogon belüli szállítási preferencia, nem szerződéses prioritás.

**RICE:** Reach × Impact × Confidence ÷ Effort. Ha nincs adat, **nincs pontszám**, a négy mező `null`. Ne kreálj számokat a rangsor kedvéért.

**Érték:** felhasználói, üzemeltetési, bevételi és kommunikációs dimenzió 1–5 skálán, szubjektív hipotézisként.

**Munka:** S=1–3, M=4–10, L=11–25, XL=26–60 AI-val támogatott fejlesztői munkanap csak előzetes nagyságrendi sávként. Külön teszt, integráció, szolgáltatói és operációs kockázatok a konkrét ajánlatban újrabecsülendők. Ez **nem árajánlat vagy határidő**.

**Sales és negyedéves roadmap:** rövid Virág-pitch és kommunikációs téma készül, de nem automatikusan elfogadott megrendelés, publikált hír vagy vállalt dátum.

## Helyi generálás

```sh
python3 -m unittest discover -s scripts -p 'test_build_ideas.py'
python3 scripts/build_ideas.py --output docs/ideas/catalog.json
python3 -m http.server 8000 --directory docs/ideas
# http://localhost:8000
```

A generált `catalog.json` nem kerül a Gitbe. A `main` ágra commitoláskor vagy a PR-ből automatikus ötletátvétel utáni `workflow_dispatch` indításkor a Pages-workflow újragenerálja és publikálja a katalógust. Az óránkénti ütemezés tartalék frissítés. Forkból vagy draft PR-ből nincs automatikus átvétel. Az automatizmus ütköző/érvénytelen ötletlapnál megáll, nem írja felül a `main` időközben módosult fájlját.

**Elővigyázatosság:** offline beléptetésnél duplikációvédelem, prémium médiánál szolgáltatói/licencvizsgálat, gyermekes felhasználói körnél adatminimalizálás szükséges. Titkot, ügyféllistát, éles QR-tokent ne tegyünk az ötlettárba.

**Első feltöltés:** 11 felhasználói ötlet, 2026. október 18. Az összes státusz „ötlet”, a RICE nem pontozott; a becslések alacsony bizonyosságúak.

## Bővítés – 2026. október 19.

A 2026-10-19-i tíz új szabad szöveges felvetésből **kilenc új ötletlap** (IDEA-013–021) készült, a látogatási sorozatokra és gyors bérletfelhasználásra épülő hűségjutalmazás pedig a meglévő **IDEA-007**-be került (a korábbi eredeti felvetés megtartásával). Az IDEA-012 országos lefedettségi kutatással együtt így **21 egyedi ötletlap** van.

A Zeneovi-részvételi és motivációs jelzéseket (IDEA-017) tudatosan külön kezeljük a potenciálisan érzékeny gyermekmegfigyelési naplótól (IDEA-018). Az IDEA-019 gyűjtőalbum ötlete önálló Ringató-arculatot feltételez, nem harmadik fél márkájának használatát. Az IDEA-021 napi AI-programkeresése **csak jóváhagyásra váró piszkozatot** hozhat létre, nem automatikusan publikált programot. Az új ötletek „elemzett” státusza nem fejlesztési megrendelés; a RICE mindenhol adat hiányában üres.

## Független ötletpublikálás – 2026. október 29.

Az **IDEA-022** (kijelentkezett PWA-nyitóoldal) már a `main` ágon van az IDEA-009 kapcsolódó hivatkozásának frissítésével. A fejlesztési specifikáció módosítása ettől **független, nyitott [PR #4](https://github.com/realabu/ringato-pwa-demo/pull/4)**, nem automatikus jóváhagyás. A katalógusban a lap `mvp-review` és `elemzett` státuszú.

**Következő azonosító:** mindig az aktuális `main` ágon lévő `IDEA-*.md` lapok legnagyobb száma +1; a sablonban nincs rögzített következő szám. A PR-alapú automatizmus nem automatikus specifikáció-merge és nem hirdetési/megrendelési jóváhagyás.
