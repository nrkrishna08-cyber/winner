# Horse Backing Rules (Streamlit) — v9

## Fix: 'Total runners missing' even when entered ✅
This version:
- Trims spaces in Race values (so **R1** and **R1␠** are treated the same)
- Auto-fills **TotalRunners** within each race if you entered it on only one row (ffill/bfill)
- Detects if TotalRunners is inconsistent within a race

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
