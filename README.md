# Horse Backing Rules (Streamlit)

One-race-at-a-time, mobile-friendly BACK / NO BACK app.

## No default table (as requested)
This app starts with an **empty table** every time.
Use the sidebar button **Add blank runner row** to start entering:
Race, Horse, Jockey, Odds, Venue, TrackType, Country, Reviewed.

## Rules
- Allowed countries: Australia, New Zealand, South Africa, France
- Turf only (no All Weather)
- Max runners: 10
- Blocked venues list
- Must review all runners
- Good horse = odds between 1.4 and 2.0 (adjustable slider)
- If more than 1 good horse in the race => NO BACK
- Jockey must be in your whitelist (editable in the sidebar)

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
