# Horse Backing Rules (Streamlit)

One-race-at-a-time, mobile-friendly BACK / NO BACK app.

## Rules implemented
- Allowed countries: Australia, New Zealand, South Africa, France
- Turf only (no All Weather)
- Max runners: 10
- Blocked venues list
- Must review all runners
- Good horse = odds between 1.4 and 2.0 (adjustable slider)
- If more than 1 good horse in the race => NO BACK
- Jockey must be in your whitelist (editable in the sidebar)

## Reset (button only)
Use the sidebar button **Reset (table + race)** to restore the default table and jump back to the first race.
Edits persist until you press reset.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
