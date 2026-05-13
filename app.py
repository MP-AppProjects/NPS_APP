import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from modules.filters import render_filters
from modules.impact_map import render_impact_map, compute_nps
from modules.whatif import render_whatif
from modules.drivers import render_drivers
from modules.ranking import render_ranking
from modules.export import render_export

# ---------- Page config ----------
st.set_page_config(
    page_title="Panel Analityczny rNPS · mBank 2026",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
    [data-testid="stMetricValue"] { font-size: 1.5rem; font-weight: 700; }
    [data-testid="stMetricDelta"] { font-size: 0.85rem; }
    .main-header {
        background: linear-gradient(90deg, #c0392b 0%, #e74c3c 100%);
        padding: 18px 28px;
        border-radius: 10px;
        color: white;
        margin-bottom: 16px;
    }
    .main-header h1 { margin: 0; font-size: 1.6rem; font-weight: 700; }
    .main-header p { margin: 4px 0 0 0; opacity: 0.85; font-size: 0.9rem; }
    div[data-testid="metric-container"] {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 12px 16px;
    }
    .stTabs [data-baseweb="tab"] { font-size: 0.9rem; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ---------- Load data ----------
@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    df_resp = pd.read_csv(os.path.join(base, "data", "respondents.csv"))
    df_driv = pd.read_csv(os.path.join(base, "data", "drivers.csv"))
    df_rank = pd.read_csv(os.path.join(base, "data", "monthly_ranking.csv"))
    return df_resp, df_driv, df_rank

df_respondents, df_drivers, df_ranking = load_data()

# ---------- Header ----------
st.markdown("""
<div class="main-header">
    <h1>🏦 Panel Analityczny rNPS · mBank 2026</h1>
    <p>Relacyjne badanie NPS · Benchmark konkurencyjny · Drivery · Symulator „Co-jeśli"</p>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar filters ----------
df_filtered, df_ranking_filtered, filters = render_filters(df_respondents, df_ranking)

# ---------- Global KPIs ----------
nps_mbank = compute_nps(df_filtered[df_filtered["bank"] == "mBank"])
n_resp = len(df_filtered[df_filtered["bank"] == "mBank"])

# Latest ranking position
banks_in_filter = filters["banks"]
latest_month = sorted(df_ranking["miesiac"].unique())[-1]
ranking_latest = df_ranking[df_ranking["miesiac"] == latest_month].sort_values("nps", ascending=False)
ranking_latest = ranking_latest.reset_index(drop=True)
mbank_pos = ranking_latest[ranking_latest["bank"] == "mBank"].index
mbank_rank = int(mbank_pos[0]) + 1 if len(mbank_pos) > 0 else "–"
total_banks = len(ranking_latest)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("rNPS mBank (filtered)", f"{nps_mbank:.1f}")
k2.metric("Respondenci mBank", f"{n_resp:,}")
k3.metric("Pozycja w rankingu", f"{mbank_rank} / {total_banks}", help=f"Ranking za {latest_month}")
k4.metric("Banki w benchmarku", len(banks_in_filter))
k5.metric("Okres analizy", f"{filters['months'][0]} – {filters['months'][-1]}" if filters['months'] else "–")

st.markdown("---")

# ---------- Main tabs ----------
tab_map, tab_whatif, tab_drivers, tab_ranking_tab, tab_export = st.tabs([
    "\U0001f5fa\ufe0f Mapa wp\u0142yw \u00d7 incydencja",
    "\U0001f52e Symulator Co-je\u015bli",
    "\U0001f4ca Ranking driver\u00f3w",
    "\U0001f4c8 Ranking NPS & trendy",
    "\U0001f4e4 Dane & eksport",
])

with tab_map:
    render_impact_map(df_filtered, df_drivers)

with tab_whatif:
    render_whatif(df_filtered, df_drivers)

with tab_drivers:
    render_drivers(df_drivers)

with tab_ranking_tab:
    render_ranking(df_respondents, df_ranking, filters)

with tab_export:
    render_export(df_respondents, df_drivers, df_ranking)
