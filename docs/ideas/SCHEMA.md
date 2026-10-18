# Ötletlap struktúra és besorolás

Minden `docs/ideas/IDEA-XXX-*.md` az alábbi JSON-kompatibilis YAML-frontmattert követi. Egysoros `kulcs: JSON-érték` mezők; stringek JSON-idézőjelben, tömbök JSON-szintaxissal, `null` szó szerint. A Python standard könyvtár validálja, nem kell PyYAML.

| Mező | Kötelező érték |
|---|---|
| `id` | `IDEA-001` formátum; globálisan egyedi |
| `title`, `area`, `origin`, `communication_angle` | Nem üres string |
| `lane` | `mvp-review`, `later-feature`, `research`, `business-experiment` |
| `status` | `ötlet`, `elemzett`, `döntésre kész`, `elfogadott`, `fejlesztés alatt`, `elkészült`, `elvetett` |
| `moscow` | Must / Should / Could / Won't now |
| `effort_size` | S / M / L / XL |
| `effort_min_days`, `effort_max_days` | Pozitív egész, min ≤ max |
| `user_value`, `operations_value`, `revenue_value`, `communication_value` | 1–5 egész, hipotézis |
| `risk`, `estimate_confidence` | alacsony / közepes / magas |
| `rice_reach`, `rice_impact`, `rice_confidence`, `rice_effort` | Mind `null`, vagy mind pozitív szám |
| `related_milestones` | Nem üres JSON stringtömb, például `["MF07","MF08"]` |
| `created`, `updated` | ISO YYYY-MM-DD; updated ≥ created |

Kötelező Markdown-fejezetek: Eredeti felvetés; Megoldandó probléma; Megoldási változatok; Technikai hatás, előzetes hipotézis; Kockázatok és függőségek; Példa elfogadási feltétel; Előzetes ráfordítás és értékelés; Virágnak szóló rövid ajánlat; Negyedéves kommunikációs lehetőség; Következő ellenőrzendő lépés; Kapcsolódás a fejlesztéshez.

A RICE-számítás `reach*impact*confidence/effort`. Az `mvp-review` és `Should` **nem** módosítja a jóváhagyott mérföldköveket, az ügyfélszerződést vagy a prioritási döntéseket. A fontos változásokat külön döntési naplóban kell rögzíteni.
