import streamlit as st
import pandas as pd

st.set_page_config(page_title="Horse Backing Rules", page_icon="🏇", layout="wide")
st.title("🏇 Horse Backing Rules (One Race at a Time)")

# -------------------------
# Constants / Rules
# -------------------------
ALLOWED_COUNTRIES = {"australia", "new zealand", "newzealand", "south africa", "france"}
TURF_ONLY_TRACK = "turf"
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

COLUMNS = ["Race", "Horse", "Jockey", "Odds", "Venue", "TrackType", "Country", "Reviewed"]

def norm(s: str) -> str:
    return str(s).strip().lower()

def do_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# -------------------------
# No default table: start EMPTY
# -------------------------
empty_df = pd.DataFrame(columns=COLUMNS)

# -------------------------
# Session state init
# -------------------------
if "data" not in st.session_state:
    st.session_state.data = empty_df.copy()

if "allowed_jockeys" not in st.session_state or not st.session_state.get("allowed_jockeys"):
    # Keep your default jockey whitelist (you can add more)
    st.session_state.allowed_jockeys = DEFAULT_ALLOWED_JOCKEYS.copy()

if "race_idx" not in st.session_state:
    st.session_state.race_idx = 0

if "editor_key" not in st.session_state:
    st.session_state.editor_key = 0

def add_blank_row():
    row = {c: "" for c in COLUMNS}
    row["Odds"] = None
    row["Reviewed"] = False
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

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:
    st.header("Data")
    if st.button("➕ Add blank runner row", use_container_width=True):
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

    st.caption("No default table: you build the race table each time. Reset ALL also restores the default jockey whitelist.")

    st.divider()
    st.header("Jockey whitelist")
    st.caption("Only these jockeys are allowed. Add/remove anytime.")

    add_j = st.text_input("Add allowed jockey name", key="add_jockey")
    c3, c4 = st.columns(2)
    with c3:
        if st.button("Add jockey", use_container_width=True):
            name = add_j.strip()
            if name and name not in st.session_state.allowed_jockeys:
                st.session_state.allowed_jockeys.append(name)
            do_rerun()
    with c4:
        if st.button("Restore default list", use_container_width=True):
            st.session_state.allowed_jockeys = DEFAULT_ALLOWED_JOCKEYS.copy()
            do_rerun()

    remove_j = st.multiselect("Remove jockey(s)", options=st.session_state.allowed_jockeys, key="remove_jockeys")
    if st.button("Remove selected", use_container_width=True):
        st.session_state.allowed_jockeys = [j for j in st.session_state.allowed_jockeys if j not in remove_j]
        if not st.session_state.allowed_jockeys:
            st.session_state.allowed_jockeys = DEFAULT_ALLOWED_JOCKEYS.copy()
        do_rerun()

    allowed_jockeys = {norm(x) for x in st.session_state.allowed_jockeys}

    st.divider()
    st.header("Race filters")
    max_runners = st.number_input("Max runners allowed", min_value=1, max_value=30, value=10, step=1)

    blocked_venues_raw = st.text_area(
        "Blocked venues (one per line)",
        value="Happy Valley\nGreyville\nFairview",
        height=110,
        key="blocked_venues"
    )
    blocked_venues = {norm(x) for x in blocked_venues_raw.splitlines() if x.strip()}

    st.divider()
    st.header("Good horse rule (Odds)")
    odds_min, odds_max = st.slider(
        "Odds range for GOOD horse",
        1.0, 10.0,
        (ODDS_MIN_DEFAULT, ODDS_MAX_DEFAULT),
        0.05
    )

st.info(
    "Hard rules: Countries allowed = Australia, New Zealand, South Africa, France. "
    "Turf only (NO All Weather). Max runners = 10."
)

# -------------------------
# Data editor
# -------------------------
with st.expander("Edit/Add runners data", expanded=True):
    edited = st.data_editor(
        st.session_state.data,
        key=f"data_editor_{st.session_state.editor_key}",
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Race": st.column_config.TextColumn(required=True, help="Race identifier (e.g., R1)"),
            "Horse": st.column_config.TextColumn(required=True),
            "Jockey": st.column_config.TextColumn(required=True),
            "Odds": st.column_config.NumberColumn(required=True, min_value=1.0, step=0.05),
            "Venue": st.column_config.TextColumn(required=True),
            "TrackType": st.column_config.TextColumn(required=True, help="Must be 'Turf'"),
            "Country": st.column_config.TextColumn(required=True, help="Australia / New Zealand / South Africa / France"),
            "Reviewed": st.column_config.CheckboxColumn("Reviewed?"),
        }
    )
    st.session_state.data = edited.copy()

df = st.session_state.data.copy()

# If empty, guide user
if df.empty:
    st.warning("Your table is empty. Click **Add blank runner row** (sidebar) and start entering your race runners.")
    st.stop()

# Coerce types
df["Odds"] = pd.to_numeric(df["Odds"], errors="coerce")

# -------------------------
# Race list + navigation
# -------------------------
races = sorted(df["Race"].astype(str).dropna().unique().tolist())
races = [r for r in races if r.strip() != ""]
if not races:
    st.warning("No Race values found. Fill in the **Race** column (e.g., R1) for at least one runner.")
    st.stop()

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
    selected_race = st.selectbox(
        "Select race",
        races,
        index=st.session_state.race_idx,
        key="race_select",
    )
    st.session_state.race_idx = races.index(selected_race)

race_df = df[df["Race"].astype(str) == selected_race].copy()

# Good horse by odds
race_df["Good"] = race_df["Odds"].between(odds_min, odds_max, inclusive="both")

# Race summary
race_country = str(race_df["Country"].iloc[0])
race_track = str(race_df["TrackType"].iloc[0])
race_venue = str(race_df["Venue"].iloc[0])
runners = int(len(race_df))
reviewed_all = bool(race_df["Reviewed"].fillna(False).all())
good_horses = int(race_df["Good"].sum())

# Race decision
if norm(race_country) not in ALLOWED_COUNTRIES:
    final, reason = "❌ NO BACK", f"Country not allowed: {race_country}"
elif norm(race_track) != TURF_ONLY_TRACK:
    final, reason = "❌ NO BACK", f"Not a Turf race: {race_track}"
elif runners > max_runners:
    final, reason = "❌ NO BACK", f"Runners {runners} > {max_runners}"
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

# Header
if final.startswith("✅"):
    st.success(f"{selected_race}: {final} — {reason}")
else:
    st.error(f"{selected_race}: {final} — {reason}")

# Runner-level decisions
race_df["Jockey allowed"] = race_df["Jockey"].astype(str).apply(
    lambda j: "Yes" if norm(j) in allowed_jockeys else "No"
)

race_df["Other good horses in race"] = race_df.apply(
    lambda r: max(good_horses - (1 if r["Good"] else 0), 0),
    axis=1
)

race_df["Horse decision"] = race_df.apply(
    lambda r: "✅ BACK"
    if (final == "✅ BACK" and bool(r["Good"]) and norm(r["Jockey"]) in allowed_jockeys)
    else "❌ NO BACK",
    axis=1
)

st.subheader("Race details")
st.write(
    f"**Country:** {race_country}  |  **Venue:** {race_venue}  |  **Track:** {race_track}  |  "
    f"**Runners:** {runners}  |  **Reviewed all:** {'Yes' if reviewed_all else 'No'}  |  "
    f"**Good horses:** {good_horses}"
)

st.subheader("Runners (this race)")
st.dataframe(
    race_df[["Horse", "Jockey", "Odds", "Good", "Jockey allowed", "Other good horses in race", "Horse decision", "Reviewed"]],
    use_container_width=True,
    hide_index=True
)
