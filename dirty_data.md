**Beschrijving:** Schrijf een Python-script (`scripts/generate_dirty_data.py`) dat een fictieve retail-dataset genereert van exact 100.000 rijen. Sla deze op als `data/raw_returns.csv`.

**De Verborgen Baseline (De "Trap"):** Bouw in de generatie-logica in dat de defectkans afhankelijk is van een interactie tussen `shift_type` en `location`:

- `Night` + `Amsterdam`: 55%
- `Night` (anders): 25%
- `Amsterdam` (anders): 20%
- anders: 5%

Dit is de patroonherkenning die de studenten moeten vinden.

**Checklist (De Vervuiling):**

- Gebruik de Faker library voor realistische namen, UUIDs en datums.
- Injecteer in ~30% van de `price` kolom string-waardes met een komma als decimaal (bijv. "€ 1200,50").
- Injecteer in ~20% van de `order_date` kolom afwijkende formats (DD/MM/YYYY ipv YYYY-MM-DD).
- Injecteer in ~10% van de categorische kolommen verborgen NaN's (gebruik de exacte strings: "null", "N/A", " ").
- **Cruciaal:** Overschrijf in de target variabele (`is_defect`) ongeveer 40% van de '1' waardes (de daadwerkelijke defecten) met een lege `NaN` waarde. (Studenten die `dropna()` gebruiken, verpesten zo hun model).
- column location met keuze uit meerdere plekken

**Definition of Done:** Het script draait lokaal zonder errors en genereert een CSV van exact 100.000 rijen die voldoet aan bovenstaande vervuilingseisen.