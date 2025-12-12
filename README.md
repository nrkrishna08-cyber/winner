# Horse Backing Rules (Streamlit)

## What changed
- ✅ Added **TotalRunners** column in the INPUT table (this is the real number of runners in the race)
- Rule enforced: **if TotalRunners > 10 => NO BACK**
- Final result is now shown clearly in a **Final result** section for the selected race
- Still: No horse name column, dropdowns for jockey/venue, Reviewed is Yes/No

## How to use
1. Click **Add runner row**
2. Fill:
   - Race (e.g., R1)
   - TotalRunners (e.g., 12)  ← same value for all rows in that race
   - Jockey, Odds, Venue, TrackType, Country, Reviewed
3. Select the race at the top and see:
   - Final result (BACK / NO BACK)
   - Pick(s) to BACK (if any)

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
