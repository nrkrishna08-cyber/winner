import streamlit as st
import pandas as pd

st.set_page_config(page_title="Horse Backing Rules", page_icon="🏇", layout="wide")
st.title("🏇 Horse Backing Rules (One Race at a Time)")

# -------------------------
# Constants / Rules
# -------------------------
ALLOWED_COUNTRIES = ["Australia", "New Zealand", "South Africa", "France"]
ALLOWED_COUNTRIES_NORM = {c.strip().lower() for c in ALLOWED_COUNTRIES}

TRACK_TYPES = ["Turf", "All Weather", "Synthetic"]
TURF_ONLY_TRACK_NORM = "turf"

ODDS_MIN_DEFAULT = 1.4
ODDS_MAX_DEFAULT = 2.0

DEFAULT_ALLOWED_JOCKEYS = [
    "James Macdonald",
    "Ryan Malony",
    "Hugh Bowman",
    "Boris Thornton",
    "Damian Thornton",
    "Nash Rawiller",
    "Cambell Rawiller",
    "Jett Stanley",
    "Craig Newitt",
    "John Allen",
    "Jason Collet",
    "Warren Kennedy",
]

DEFAULT_VENUES = [
    "Randwick",
    "Flemington",
    "Caulfield",
    "Moonee Valley",
]

# TotalRunners is a user input column (per race)
COLUMNS = ["Race", "TotalRunners", "Jockey", "Odds", "Venue", "TrackType", "Country", "Reviewed"]

def norm(s: str) -> str:
    return str(s).strip().lower()

def do_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# -------------------------
# Start EMPTY table (no defaults)
# -------------------------
empty_df = pd.DataFrame(columns=COLUMNS)

# -------------------------
# Session state init
# -------------------------
if "data" not in st.session_state:
    st.session_state.data = empty_df.copy()

if "allowed_jockeys" not in st.session_state or not st.session_state.get("allowed_jockeys"):
    st.session_state.allowed_jockeys = DEFAULT_ALLOWED_JOCKEYS.copy()

if "venues" not in st.session_state or not st.session_state.get("venues"):
    st.session_state.venues = DEFAULT_VENUES.copy()

if "race_idx" not in st.session_state:
    st.session_state.race_idx = 0

if "editor_key" not in st.session_state:
    st.session_state.editor_key = 0

def add_blank_row():
    row = {
        "Race": "",
        "TotalRunners": None,
        "Jockey": st.session_state.allowed_jockeys[0] if st.session_state.allowed_jockeys else "",
        "Odds": None,
        "Venue": st.session_state.venues[0] if st.session_state.venues else "",
        "TrackType": "Turf",
        "Country": "Australia",
        "Reviewed": "No",
    }
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([row])], ignore_index=True)

def reset_table():
    st.session_state.data = empty_df.copy()
    st.session_state.race_idx = 0
    st.session_state.editor_key += 1
    for k in ["race_select"]:
        if k in st.session_state:
            del st.session_state[k]

def reset_all():
    reset_table()
    st.session_state.allowed_jockeys = DEFAULT_ALLOWED_JOCKEYS.copy()
    st.session_state.venues = DEFAULT_VENUES.copy()

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:
    st.header("Data")
    if st.button("➕ Add runner row", use_container_width=True):
        add_blank_row()
        do_rerun()

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Reset table", use_container_width=True):
            reset_table()
            do_rerun()
    with c2:
        if st.button("Reset ALL", use_container_width=True):
            reset_all()
            do_rerun()

    st.divider()
    st.header("Jockey list (dropdown)")
    add_j = st.text_input("Add jockey name")
    c3, c4 = st.columns(2)
    with c3:
        if st.button("Add jockey", use_container_width=True):
            name = add_j.strip()
            if name and name not in st.session_state.allowed_jockeys:
                st.session_state.allowed_jockeys.append(name)
            do_rerun()
    with c4:
        if st.button("Restore default jockeys", use_container_width=True):
            st.session_state.allowed_jockeys = DEFAULT_ALLOWED_JOCKEYS.copy()
            do_rerun()

    remove_j = st.multiselect("Remove jockey(s)", options=st.session_state.allowed_jockeys, key="remove_jockeys")
    if st.button("Remove selected jockeys", use_container_width=True):
        st.session_state.allowed_jockeys = [j for j in st.session_state.allowed_jockeys if j not in remove_j]
        if not st.session_state.allowed_jockeys:
            st.session_state.allowed_jockeys = DEFAULT_ALLOWED_JOCKEYS.copy()
        do_rerun()

    allowed_jockeys_norm = {norm(x) for x in st.session_state.allowed_jockeys}

    st.divider()
    st.header("Venue list (dropdown)")
    add_v = st.text_input("Add venue name")
    c5, c6 = st.columns(2)
    with c5:
        if st.button("Add venue", use_container_width=True):
            name = add_v.strip()
            if name and name not in st.session_state.venues:
                st.session_state.venues.append(name)
            do_rerun()
    with c6:
        if st.button("Restore default venues", use_container_width=True):
            st.session_state.venues = DEFAULT_VENUES.copy()
            do_rerun()

    remove_v = st.multiselect("Remove venue(s)", options=st.session_state.venues, key="remove_venues")
    if st.button("Remove selected venues", use_container_width=True):
        st.session_state.venues = [v for v in st.session_state.venues if v not in remove_v]
        if not st.session_state.venues:
            st.session_state.venues = DEFAULT_VENUES.copy()
        do_rerun()

    st.divider()
    st.header("Rules")
    max_runners = st.number_input("Max runners allowed", min_value=1, max_value=30, value=10, step=1)

    blocked_venues_raw = st.text_area(
        "Blocked venues (one per line)",
        value="Happy Valley\nGreyville\nFairview",
        height=110,
    )
    blocked_venues = {norm(x) for x in blocked_venues_raw.splitlines() if x.strip()}

    odds_min, odds_max = st.slider(
        "Odds range for GOOD horse",
        1.0, 10.0,
        (ODDS_MIN_DEFAULT, ODDS_MAX_DEFAULT),
        0.05
    )

st.info(
    "Hard rules: Country must be Australia / New Zealand / South Africa / France. "
    "TrackType must be Turf only. If Total runners in the race > 10 => NO BACK."
)

# -------------------------
# Data editor (input table)
# -------------------------
st.subheader("Input table (you fill this)")
st.caption("Tip: **TotalRunners** = total horses in the race. You can enter it on one row only — the app will auto-fill it for the whole race.")

edited = st.data_editor(
    st.session_state.data,
    key=f"data_editor_{st.session_state.editor_key}",
    use_container_width=True,
    num_rows="dynamic",
    column_config={
        "Race": st.column_config.TextColumn(required=True, help="Race identifier (e.g., R1)"),
        "TotalRunners": st.column_config.NumberColumn(
            "TotalRunners",
            required=True,
            min_value=1,
            step=1,
            help="Total number of runners in the race (e.g., 12). If > 10, NO BACK.",
        ),
        "Jockey": st.column_config.SelectboxColumn("Jockey", options=st.session_state.allowed_jockeys, required=True),
        "Odds": st.column_config.NumberColumn(required=True, min_value=1.0, step=0.05),
        "Venue": st.column_config.SelectboxColumn("Venue", options=st.session_state.venues, required=True),
        "TrackType": st.column_config.SelectboxColumn("TrackType", options=TRACK_TYPES, required=True),
        "Country": st.column_config.SelectboxColumn("Country", options=ALLOWED_COUNTRIES, required=True),
        "Reviewed": st.column_config.SelectboxColumn("Reviewed", options=["Yes", "No"], required=True),
    },
)
st.session_state.data = edited.copy()

df = st.session_state.data.copy()

if df.empty:
    st.warning("Your table is empty. Click **Add runner row** (sidebar) and start entering your race runners.")
    st.stop()

# -------------------------
# Robust cleaning (fixes 'Total runners missing' caused by spaces or partial entry)
# -------------------------
df["Race"] = df["Race"].astype(str).str.strip()  # ✅ trims spaces so R1 and 'R1 ' become the same race
df["Odds"] = pd.to_numeric(df["Odds"], errors="coerce")
df["TotalRunners"] = pd.to_numeric(df["TotalRunners"], errors="coerce")

# ✅ Auto-fill TotalRunners within each race if user entered it on only one row
df["TotalRunners"] = df.groupby("Race")["TotalRunners"].transform(lambda s: s.ffill().bfill())

# Race list
races = sorted([r for r in df["Race"].dropna().unique().tolist() if str(r).strip() != ""])
if not races:
    st.warning("No Race values found. Fill in the **Race** column (e.g., R1) for at least one runner.")
    st.stop()

# Navigation
st.session_state.race_idx = max(0, min(st.session_state.race_idx, len(races) - 1))
nav1, nav2, nav3 = st.columns([1, 2, 1])

with nav1:
    prev_disabled = st.session_state.race_idx <= 0
    if st.button("⬅️ Previous", use_container_width=True, disabled=prev_disabled):
        st.session_state.race_idx -= 1
        do_rerun()

with nav3:
    next_disabled = st.session_state.race_idx >= len(races) - 1
    if st.button("Next ➡️", use_container_width=True, disabled=next_disabled):
        st.session_state.race_idx += 1
        do_rerun()

with nav2:
    selected_race = st.selectbox("Select race", races, index=st.session_state.race_idx, key="race_select")
    st.session_state.race_idx = races.index(selected_race)

race_df = df[df["Race"] == selected_race].copy()

# Total runners for the selected race (after autofill)
total_runners_vals = race_df["TotalRunners"].dropna().unique().tolist()
total_runners = int(total_runners_vals[0]) if len(total_runners_vals) > 0 else None
rows_entered = int(len(race_df))

# Good horse by odds
race_df["Good"] = race_df["Odds"].between(odds_min, odds_max, inclusive="both")

# Race summary values
race_country = str(race_df["Country"].iloc[0])
race_track = str(race_df["TrackType"].iloc[0])
race_venue = str(race_df["Venue"].iloc[0])
reviewed_all = bool((race_df["Reviewed"].astype(str).str.strip() == "Yes").all())
good_horses = int(race_df["Good"].sum())

# Detect inconsistent TotalRunners values (if user entered different numbers on different rows)
inconsistent_total_runners = len(total_runners_vals) > 1

# Race decision
if total_runners is None:
    final, reason = "❌ NO BACK", "TotalRunners is missing for this race (enter it in any row of this race)"
elif inconsistent_total_runners:
    final, reason = "❌ NO BACK", f"TotalRunners is inconsistent in this race: {total_runners_vals} (make them the same)"
elif norm(race_country) not in ALLOWED_COUNTRIES_NORM:
    final, reason = "❌ NO BACK", f"Country not allowed: {race_country}"
elif norm(race_track) != TURF_ONLY_TRACK_NORM:
    final, reason = "❌ NO BACK", f"Not a Turf race: {race_track}"
elif total_runners > max_runners:
    final, reason = "❌ NO BACK", f"Total runners {total_runners} > {max_runners}"
elif norm(race_venue) in blocked_venues:
    final, reason = "❌ NO BACK", f"Blocked venue: {race_venue}"
elif not reviewed_all:
    final, reason = "❌ NO BACK", "Not reviewed all runners"
elif good_horses == 0:
    final, reason = "❌ NO BACK", f"No good horses (Odds must be {odds_min}–{odds_max})"
elif good_horses > 1:
    final, reason = "❌ NO BACK", f"{good_horses} good horses in race (other good horses exist)"
else:
    final, reason = "✅ BACK", "Pass all rules (single good horse)"

# FINAL RESULT (clear)
st.subheader("Final result (selected race)")
if final.startswith("✅"):
    st.success(f"{selected_race}: {final} — {reason}")
else:
    st.error(f"{selected_race}: {final} — {reason}")

# Runner-level decisions
race_df["Jockey allowed"] = race_df["Jockey"].astype(str).apply(
    lambda j: "Yes" if norm(j) in allowed_jockeys_norm else "No"
)

race_df["Other good horses in race"] = race_df.apply(
    lambda r: max(good_horses - (1 if r["Good"] else 0), 0),
    axis=1
)

race_df["Decision"] = race_df.apply(
    lambda r: "✅ BACK"
    if (final == "✅ BACK" and bool(r["Good"]) and norm(r["Jockey"]) in allowed_jockeys_norm)
    else "❌ NO BACK",
    axis=1
)

st.subheader("Race details")
st.write(
    f"**Country:** {race_country}  |  **Venue:** {race_venue}  |  **Track:** {race_track}  |  "
    f"**Total runners (race):** {total_runners}  |  **Rows entered:** {rows_entered}  |  "
    f"**Reviewed all:** {'Yes' if reviewed_all else 'No'}  |  **Good horses:** {good_horses}"
)

st.subheader("Runners (this race)")
race_df_display = race_df.reset_index(drop=True).copy()
race_df_display.insert(0, "Runner #", race_df_display.index + 1)

st.dataframe(
    race_df_display[[
        "Runner #", "TotalRunners", "Jockey", "Odds", "Venue", "TrackType", "Country", "Reviewed",
        "Good", "Jockey allowed", "Other good horses in race", "Decision"
    ]],
    use_container_width=True,
    hide_index=True
)

st.subheader("Pick(s) to BACK")
picks = race_df_display[race_df_display["Decision"] == "✅ BACK"][["Runner #", "Jockey", "Odds", "Venue", "Country", "TrackType"]]
if len(picks) == 0:
    st.write("No picks for this race.")
else:
    st.dataframe(picks, use_container_width=True, hide_index=True)

# Optional debug help (collapsed)
with st.expander("Debug (why TotalRunners might look missing)", expanded=False):
    st.write("TotalRunners values found for this race:", total_runners_vals)
    st.write("Tip: If you had Race values like 'R1 ' (extra space), this version auto-fixes it by trimming spaces.")
