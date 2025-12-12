# Horse Backing Rules (Streamlit) — v10

## Fix for StreamlitAPIException (data_editor type compatibilities) ✅
Streamlit checks dataframe dtypes against column_config. An empty dataframe must still have correct dtypes.
This version creates the empty table with:
- TotalRunners: Int64 (nullable int)
- Odds: float
- others: string

It also:
- trims spaces in Race
- auto-fills TotalRunners within each race

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
