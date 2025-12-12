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

## Reset
- **Reset table**: resets runners data + race selection
- **Reset ALL**: also restores the default jockey whitelist

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
