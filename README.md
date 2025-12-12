# Horse Backing Rules (Streamlit)

## What changed (your request)
- **No Horse name column** (removed completely)
- In the table:
  - **Jockey** is a dropdown (from your jockey list)
  - **Venue** is a dropdown (from your venue list)
  - **Reviewed** is dropdown **Yes/No** (not a checkbox)

## Start empty (no default table)
The table starts empty every time. Click **Add runner row** to begin.

## Rules
- Allowed countries: Australia, New Zealand, South Africa, France
- Turf only (no All Weather)
- Max runners: 10
- Blocked venues list
- Must review all runners (Reviewed must be Yes for all rows in the race)
- Good horse = odds between 1.4 and 2.0 (adjustable slider)
- If more than 1 good horse in the race => NO BACK
- Jockey must be in your whitelist (editable list)

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
