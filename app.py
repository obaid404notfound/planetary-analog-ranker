"""
Planetary Analog Ranker
A Streamlit decision-support tool that ranks Earth sites as analogs for the lunar
South Pole and Mars, finds complementary 2-3 site test portfolios, and checks how
stable the ranking is when the criterion weights change.
"""

from typing import Dict, List, Tuple
import html
import math
import os
import textwrap

import folium
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_folium import st_folium

import engine
from engine import (
    analog_score, best_portfolio, deduplicated_weights, first_place_share, normalize_weights,
    overlapping_pairs, portfolio, rank_stability, rank_stability_local,
)
from presets import (
    MOON_TARGET, MARS_TARGET,
    MOON_CRITERIA_INFO, MARS_CRITERIA_INFO,
    MOON_PRESETS, MARS_PRESETS,
    MOON_MEASURED_TARGET, MARS_MEASURED_TARGET,
    PRESET_RATIONALE, PRESET_SUMMARY, CRITERION_GAP_ADVICE,
    ACCESS_CRITERION, ACCESS_SPEC, CROSS_CHECK, MEASURED_CRITERIA, SEARCH_LIMIT_KM,
)
from data.site_details import SITE_METADATA, SITE_PHYSICAL_MEASUREMENTS


# ---------------------------------------------------------
# Page configuration and styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Planetary Analog Ranker",
    page_icon=":material/public:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# The app follows the viewer's light/dark setting. One palette per mode, used
# everywhere (page, map, charts, cards).
try:
    DARK = st.context.theme.type == "dark"
except Exception:
    DARK = False

if DARK:
    PAL = dict(
        bg="#000000", side="#161617", card="#1C1C1E", fill="#2C2C2E", fill_hover="#3A3A3C",
        ink="#F5F5F7", muted="#98989D", line="#38383A", seg="#2C2C2E", seg_on="#636366",
        seg_hover="rgba(255, 255, 255, 0.08)", accent="#0A84FF", accent_hover="#409CFF",
        accent_rgb="10, 132, 255", header="rgba(0, 0, 0, 0.72)", shadow="rgba(0, 0, 0, 0.5)",
    )
    SITE_COLORS = ["#0A84FF", "#E8590C", "#2A9D63"]  # portfolio pick 1, 2, 3
else:
    PAL = dict(
        bg="#F5F5F7", side="#FFFFFF", card="#FFFFFF", fill="#F5F5F7", fill_hover="#EDEDF0",
        ink="#1D1D1F", muted="#6E6E73", line="#E5E5EA", seg="#E8E8ED", seg_on="#FFFFFF",
        seg_hover="rgba(255, 255, 255, 0.5)", accent="#0071E3", accent_hover="#0077ED",
        accent_rgb="0, 113, 227", header="rgba(245, 245, 247, 0.72)", shadow="rgba(0, 0, 0, 0.09)",
    )
    SITE_COLORS = ["#0071E3", "#F56300", "#30A46C"]  # portfolio pick 1, 2, 3

ACCENT = PAL["accent"]
INK = PAL["ink"]
MUTED = PAL["muted"]
GRID = PAL["line"]
CARD = PAL["card"]
TARGET_GREY = "#86868B"
FONT = "-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', Roboto, 'Noto Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif"
BASELINE_PRESET = "Balanced (NASA Baseline)"
SCORE_ERROR = 5.0      # assumed worst-case error on any single criterion score, in points
CONTENDER_SHARE = 10.0  # a site that takes first place in at least this % of noisy trials is a contender
OVERLAP_R = 0.8         # criteria correlated at least this strongly count as overlapping

# Colours reach the stylesheet below as CSS variables.
st.markdown(
    "<style>:root {"
    + " ".join(f"--{k.replace('_', '-')}: {v};" for k, v in PAL.items())
    + "}</style>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
        .stApp { background: var(--bg); }
        .block-container { padding-top: 3.4rem; padding-bottom: 3rem; max-width: 1320px; }
        [data-testid="stHeader"] {
            background: var(--header);
            backdrop-filter: saturate(180%) blur(20px); -webkit-backdrop-filter: saturate(180%) blur(20px);
        }
        [data-testid="stSidebar"] { background: var(--side); border-right: 1px solid var(--line); }
        [data-testid="stSidebar"] h3 { font-size: 0.95rem; font-weight: 600; letter-spacing: -0.01em; }

        /* Header */
        .eyebrow { font-size: 0.95rem; font-weight: 600; color: var(--muted); margin-bottom: 0.2rem; }
        .page-title {
            font-size: 3rem; font-weight: 700; line-height: 1.07; letter-spacing: -0.022em;
            color: var(--ink); margin: 0; padding: 0;
        }
        .page-sub { color: var(--muted); font-size: 1.3rem; line-height: 1.3; letter-spacing: -0.005em; margin: 0.55rem 0 1.4rem 0; }
        .notice { color: var(--muted); font-size: 0.82rem; line-height: 1.45; margin: 0.9rem 0 0.4rem 0; }

        /* Summary tiles */
        .tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 14px; }
        .tile { background: var(--card); border-radius: 18px; padding: 18px 20px 20px 20px; }
        .tile-label { font-size: 0.8rem; font-weight: 500; color: var(--muted); }
        .tile-value { font-size: 1.55rem; font-weight: 600; letter-spacing: -0.02em; color: var(--ink); margin-top: 0.3rem; line-height: 1.15; }
        .tile-value small { font-size: 0.95rem; font-weight: 500; color: var(--muted); letter-spacing: 0; }

        /* Cards (containers created with a key starting with "card") */
        [class*="st-key-card"] {
            background: var(--card); border: none !important; border-radius: 18px; padding: 1.15rem 1.3rem;
        }
        .card-label { font-size: 0.78rem; font-weight: 500; color: var(--muted); }
        .card-title { font-size: 1.12rem; font-weight: 600; letter-spacing: -0.015em; color: var(--ink); margin: 0.15rem 0 0.15rem 0; }
        .card-meta { font-size: 0.86rem; color: var(--muted); margin-bottom: 0.35rem; }
        .swatch { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 8px; }
        h4 { font-weight: 600 !important; letter-spacing: -0.02em !important; }

        /* Tabs as a segmented control */
        [role="tablist"] {
            background: var(--seg); border-radius: 10px; padding: 3px; gap: 0;
            width: fit-content; border: none !important; box-shadow: none !important;
        }
        [data-testid="stTab"] {
            height: auto; padding: 6px 20px; border-radius: 8px; border: none !important;
            font-size: 0.88rem; font-weight: 500; color: var(--ink) !important; background: transparent;
        }
        [data-testid="stTab"] p { font-size: 0.88rem; font-weight: 500; }
        [data-testid="stTab"][aria-selected="true"] { background: var(--seg-on); box-shadow: 0 1px 4px rgba(0, 0, 0, 0.14); }
        [data-testid="stTab"] .react-aria-SelectionIndicator { display: none !important; }
        [data-testid="stTabPanel"] { padding-top: 1.4rem; }

        /* Controls and surfaces */
        [data-testid="stExpander"] details { background: var(--card); border: none; border-radius: 14px; }
        [data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; }
        [data-testid="stCustomComponentV1"], iframe[title*="folium"] { border-radius: 18px; }
        [data-testid="stAlert"] { border-radius: 14px; }
        .stButton button, .stDownloadButton button {
            border: none; border-radius: 980px; padding: 0.42rem 1.15rem; font-weight: 500;
            background: var(--accent); color: #FFF;
        }
        .stButton button:hover, .stDownloadButton button:hover { background: var(--accent-hover); color: #FFF; }
        .stButton button:disabled { background: var(--fill); color: var(--muted); }
        [data-testid="stSidebar"] .stButton button:not(:disabled) { background: var(--fill); color: var(--accent); }
        hr { border-color: var(--line) !important; }
        .footer { color: var(--muted); font-size: 0.75rem; }
        /* ---------- Motion ---------- */
        @keyframes rise { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: none; } }
        @keyframes fade { from { opacity: 0; } to { opacity: 1; } }
        .eyebrow, .page-title, .page-sub, .tile, .notice, [class*="st-key-card"] {
            animation: rise 0.7s cubic-bezier(0.2, 0.8, 0.2, 1) backwards;
        }
        .page-title { animation-delay: 0.05s; }
        .page-sub { animation-delay: 0.12s; }
        .tile:nth-child(1) { animation-delay: 0.18s; }
        .tile:nth-child(2) { animation-delay: 0.25s; }
        .tile:nth-child(3) { animation-delay: 0.32s; }
        .tile:nth-child(4) { animation-delay: 0.39s; }
        .notice { animation-name: fade; animation-delay: 0.5s; }
        [data-testid="stTabPanel"] { animation: fade 0.45s ease backwards; }

        /* Cards lift slightly under the pointer */
        .tile, [class*="st-key-card"] {
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
            transition: transform 0.35s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.35s cubic-bezier(0.2, 0.8, 0.2, 1);
        }
        .tile:hover, [class*="st-key-card_top"]:hover, [class*="st-key-card_pick"]:hover, [class*="st-key-card_gap"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 14px 34px var(--shadow);
        }

        /* ---------- Buttons ---------- */
        .stButton button, .stDownloadButton button {
            transition: transform 0.18s ease, box-shadow 0.25s ease, background 0.25s ease, color 0.25s ease;
            box-shadow: 0 1px 2px rgba(var(--accent-rgb), 0.25);
            letter-spacing: -0.005em;
        }
        .stButton button:hover:not(:disabled), .stDownloadButton button:hover {
            box-shadow: 0 6px 18px rgba(var(--accent-rgb), 0.32); transform: translateY(-1px);
        }
        .stButton button:active:not(:disabled), .stDownloadButton button:active { transform: scale(0.96); box-shadow: none; }
        .stButton button:disabled { box-shadow: none; }
        .stButton button:focus-visible, .stDownloadButton button:focus-visible {
            outline: none; box-shadow: 0 0 0 4px rgba(var(--accent-rgb), 0.3);
        }
        [data-testid="stSidebar"] .stButton button:not(:disabled) { background: rgba(var(--accent-rgb), 0.1); box-shadow: none; }
        [data-testid="stSidebar"] .stButton button:hover:not(:disabled) {
            background: rgba(var(--accent-rgb), 0.16); color: var(--accent); box-shadow: none; transform: none;
        }

        /* ---------- Sliders: thick rounded track, white knob ---------- */
        [data-testid="stSlider"] [role="group"] > div > div:first-child { height: 6px; border-radius: 3px; }
        [data-testid="stSlider"] div[data-rac][style*="position: absolute"] {
            width: 24px !important; height: 24px !important; border-radius: 50% !important;
            background: #FFF !important; border: none !important;
            box-shadow: 0 0 0 0.5px rgba(0, 0, 0, 0.06), 0 2px 6px rgba(0, 0, 0, 0.22) !important;
            transition: box-shadow 0.2s ease; cursor: grab;
        }
        [data-testid="stSlider"] div[data-rac][style*="position: absolute"]:hover {
            box-shadow: 0 0 0 0.5px rgba(0, 0, 0, 0.06), 0 2px 6px rgba(0, 0, 0, 0.22), 0 0 0 8px rgba(var(--accent-rgb), 0.12) !important;
        }
        [data-testid="stSlider"] div[data-rac][style*="position: absolute"]:active {
            cursor: grabbing;
            box-shadow: 0 0 0 0.5px rgba(0, 0, 0, 0.06), 0 3px 10px rgba(0, 0, 0, 0.28), 0 0 0 10px rgba(var(--accent-rgb), 0.16) !important;
        }
        [data-testid="stSliderThumbValue"] p { color: var(--accent); font-weight: 600; font-variant-numeric: tabular-nums; }
        [data-testid="stSliderTickBar"] { display: none; }
        [data-testid="stSlider"] [role="group"] { margin-top: 0.85rem; }
        [data-testid="stSidebar"] [data-testid="stSlider"] label p { font-size: 0.84rem; color: var(--ink); }

        /* ---------- Sidebar radios as segmented controls ---------- */
        [data-testid="stSidebar"] [data-testid="stElementContainer"]:has(> [data-testid="stRadio"]),
        [data-testid="stSidebar"] [data-testid="stRadio"] { width: 100% !important; }
        [data-testid="stSidebar"] [data-testid="stRadioGroup"] {
            display: flex; flex-direction: row; flex-wrap: nowrap; gap: 0;
            background: var(--seg); border-radius: 10px; padding: 3px; width: 100% !important; box-sizing: border-box;
        }
        [data-testid="stSidebar"] [data-testid="stRadioGroup"] > div {
            flex: 1 1 0; border-radius: 8px; margin: 0;
            transition: background 0.25s ease, box-shadow 0.25s ease;
        }
        [data-testid="stSidebar"] [data-testid="stRadioGroup"] > div[data-selected="true"] {
            background: var(--seg-on); box-shadow: 0 1px 4px rgba(0, 0, 0, 0.14);
        }
        [data-testid="stSidebar"] [data-testid="stRadioOption"] {
            width: 100%; margin: 0; padding: 5px 6px; justify-content: center; cursor: pointer;
        }
        [data-testid="stSidebar"] [data-testid="stRadioOption"] > div { justify-content: center; gap: 0; }
        [data-testid="stSidebar"] [data-testid="stRadioOption"] > div > div:first-child { display: none; }
        [data-testid="stSidebar"] [data-testid="stRadioOption"] p { font-size: 0.84rem; font-weight: 500; white-space: nowrap; }

        /* ---------- Other controls ---------- */
        [data-testid="stSelectbox"] [role="group"] {
            background: var(--fill); border: 1px solid transparent; border-radius: 10px;
            transition: background 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }
        [data-testid="stSelectbox"] [role="group"]:hover { background: var(--fill-hover); }
        [data-testid="stSelectbox"] [role="group"]:focus-within {
            background: var(--card); border-color: var(--accent); box-shadow: 0 0 0 4px rgba(var(--accent-rgb), 0.18);
        }
        [data-testid="stTab"] { transition: background 0.25s ease, box-shadow 0.25s ease, color 0.2s ease; }
        [data-testid="stTab"]:not([aria-selected="true"]):hover { background: var(--seg-hover); }
        [data-testid="stExpander"] details { transition: box-shadow 0.3s ease; }
        [data-testid="stExpander"] details:hover { box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06); }
        [data-testid="stExpander"] summary { font-weight: 500; }

        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after { animation: none !important; transition: none !important; }
        }

        /* ---------- Hero and summary tiles ---------- */
        .hero-grid { display: grid; grid-template-columns: minmax(0, 1.7fr) minmax(0, 1fr) minmax(0, 1fr); gap: 14px; }
        @media (max-width: 900px) { .hero-grid { grid-template-columns: 1fr; } }
        .tile { display: flex; flex-direction: column; }
        .tile.hero { flex-direction: row; align-items: center; justify-content: space-between; gap: 20px; padding: 22px 26px; }
        .hero-name { font-size: 2.1rem; font-weight: 700; letter-spacing: -0.025em; line-height: 1.1; color: var(--ink); margin-top: 0.3rem; }
        .hero-meta, .tile-sub { font-size: 0.86rem; color: var(--muted); margin-top: 0.45rem; }
        .tile-sub { margin-top: auto; padding-top: 0.6rem; }
        @property --p { syntax: "<number>"; initial-value: 0; inherits: false; }
        @keyframes ring { from { --p: 0; } }
        .ring {
            position: relative; width: 112px; height: 112px; flex: none; border-radius: 50%;
            background: conic-gradient(var(--accent) calc(var(--p) * 1%), var(--seg) 0);
            -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 10px), #000 calc(100% - 9px));
            mask: radial-gradient(farthest-side, transparent calc(100% - 10px), #000 calc(100% - 9px));
            animation: ring 1.1s cubic-bezier(0.2, 0.8, 0.2, 1) 0.2s backwards;
        }
        .ring-wrap { position: relative; width: 112px; height: 112px; flex: none; }
        .ring-text { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .ring-num { font-size: 1.7rem; font-weight: 700; letter-spacing: -0.03em; color: var(--ink); line-height: 1; }
        .ring-cap { font-size: 0.7rem; color: var(--muted); margin-top: 3px; }

        /* Numbers count up when they change (falls back to plain text in older browsers) */
        @property --t { syntax: "<integer>"; initial-value: 0; inherits: false; }
        @keyframes countup { from { --t: 0; } }
        .num { font-variant-numeric: tabular-nums; }
        @supports (width: round(down, 1px, 1px)) {
            .num { animation: countup 1s cubic-bezier(0.2, 0.8, 0.2, 1) 0.15s backwards; }
            .num > span { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); }
            .num.dec { counter-reset: i round(down, var(--t) / 10) d calc(var(--t) - round(down, var(--t) / 10) * 10); }
            .num.dec::after { content: counter(i) "." counter(d); }
            .num.int { counter-reset: i var(--t); }
            .num.int::after { content: counter(i); }
        }

        /* ---------- Ranking list ---------- */
        .panel { background: var(--card); border-radius: 18px; padding: 6px; animation: rise 0.7s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; }
        .rank-list { height: 458px; overflow-y: auto; padding: 0 4px; scrollbar-width: thin; }
        .rank-row {
            display: grid; grid-template-columns: 28px minmax(0, 1.9fr) minmax(50px, 1fr) 38px; position: relative; align-items: center; gap: 12px;
            padding: 7px 10px; border-radius: 12px; transition: background 0.2s ease;
        }
        .rank-row + .rank-row::before { content: ""; position: absolute; top: 0; left: 50px; right: 10px; height: 1px; background: var(--line); }
        .rank-row:hover { background: var(--fill); }
        .rank-row:hover::before, .rank-row:hover + .rank-row::before { display: none; }
        .rank-badge {
            width: 26px; height: 26px; border-radius: 50%; background: var(--fill); color: var(--ink);
            font-size: 0.76rem; font-weight: 600; display: flex; align-items: center; justify-content: center;
        }
        .rank-row.top .rank-badge { background: var(--accent); color: #FFF; }
        .rank-name { font-size: 0.92rem; font-weight: 500; color: var(--ink); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; letter-spacing: -0.01em; }
        .rank-sub { font-size: 0.76rem; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .bar { height: 6px; border-radius: 3px; background: var(--seg); overflow: hidden; }
        .bar > span { display: block; height: 100%; border-radius: 3px; background: var(--accent); animation: grow 0.9s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; }
        .rank-row:not(.top) .bar > span { opacity: 0.55; }
        @keyframes grow { from { width: 0; } }
        .rank-score { font-size: 0.9rem; font-weight: 600; color: var(--ink); text-align: right; font-variant-numeric: tabular-nums; }

        /* ---------- Top-three cards ---------- */
        [class*="st-key-card_top"] { height: 100%; }
        .card-score { display: flex; align-items: center; gap: 10px; margin: 0.5rem 0 0.7rem 0; }
        .card-score .bar { flex: 1; }
        .card-score b { font-size: 0.95rem; font-weight: 600; color: var(--ink); font-variant-numeric: tabular-nums; }
        .card-body {
            font-size: 0.9rem; line-height: 1.5; color: var(--ink); min-height: 4.5em;
            display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;
        }
        [class*="st-key-card"] [data-testid="stExpander"] details { background: var(--fill); }
        [class*="st-key-card"] [data-testid="stExpander"] p, [class*="st-key-card"] [data-testid="stExpander"] li { font-size: 0.88rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
@st.cache_data
def load_datasets() -> Tuple[pd.DataFrame, pd.DataFrame]:
    app_dir = os.path.dirname(os.path.abspath(__file__))
    moon = pd.read_csv(os.path.join(app_dir, "data", "moon_sites.csv"), encoding="utf-8")
    mars = pd.read_csv(os.path.join(app_dir, "data", "mars_sites.csv"), encoding="utf-8")
    return moon, mars


@st.cache_data
def load_measured() -> pd.DataFrame:
    """Real measurements per site (NASA POWER, SRTM/ASTER, OpenStreetMap, GVP, Wikidata), built by data/fetch_measured.py."""
    app_dir = os.path.dirname(os.path.abspath(__file__))
    return pd.read_csv(os.path.join(app_dir, "data", "measured.csv"), encoding="utf-8", keep_default_na=False).set_index("site_id")


def with_measured(df: pd.DataFrame, target_name: str) -> pd.DataFrame:
    """Replace the hand estimate with a score computed from measurements, where one exists."""
    out = df.copy()
    specs = dict(MEASURED_CRITERIA[target_name])
    specs.setdefault(ACCESS_CRITERION, ACCESS_SPEC)  # reported for Mars too, though not one of its criteria
    for c, spec in specs.items():
        fn = getattr(engine, spec["fn"])
        out[c] = out[c].astype(float)
        for i, sid in out["site_id"].items():
            if sid in MEASURED.index:
                out.at[i, c] = round(fn(*[MEASURED.at[sid, col] for col in spec["cols"]]))
    return out


def short_name(site_name: str) -> str:
    """'Atacama Desert (Yungay)' -> 'Atacama Desert'."""
    return site_name.split(" (")[0]


def short_criterion(criterion: str) -> str:
    """'Aridity / low humidity' -> 'Aridity'."""
    return criterion.split("/")[0].strip()


def lower_first(text: str) -> str:
    """Lower-case only the first letter, so acronyms such as UV survive mid-sentence."""
    return text[:1].lower() + text[1:]


def wrap_label(text: str, width: int = 18) -> str:
    return "<br>".join(textwrap.wrap(text, width=width))


def find_metadata(site_name: str):
    meta = SITE_METADATA.get(short_name(site_name))
    if meta:
        return meta
    for key, value in SITE_METADATA.items():
        if key.lower() in site_name.lower() or site_name.lower() in key.lower():
            return value
    return None


def measurement(site_id: str, criterion: str) -> str:
    """Raw measured value when the criterion is computed from data, otherwise the site note."""
    spec = MEASURED_CRITERIA[target].get(criterion) or (ACCESS_SPEC if criterion == ACCESS_CRITERION else None)
    if use_measured and spec and site_id in MEASURED.index:
        row = MEASURED.loc[site_id].to_dict()
        text = spec["raw"].format(**row)
        # A distance equal to its search limit means nothing was found within that range.
        for col, limit in SEARCH_LIMIT_KM.items():
            if col in spec["cols"] and float(row[col]) >= limit:
                text = text.replace(f"{limit:.0f} km to", f"more than {limit:,.0f} km to")
        return text + f" ({spec['source']})"
    return SITE_PHYSICAL_MEASUREMENTS.get(site_id, {}).get(criterion, "")


moon_raw_df, mars_raw_df = load_datasets()
MEASURED = load_measured()


# ---------------------------------------------------------
# Appearance: Auto follows the device; Light and Dark force a mode.
# The choice is written where Streamlit keeps its own theme preference, then the page reloads.
# ---------------------------------------------------------
THEME_CHOICES = {"Auto": "System", "Light": "Light", "Dark": "Dark"}


def request_theme_change():
    st.query_params["theme"] = st.session_state.appearance.lower()
    st.session_state.apply_theme = True


if "appearance" not in st.session_state:
    st.session_state.appearance = st.query_params.get("theme", "auto").capitalize()
    if st.session_state.appearance not in THEME_CHOICES:
        st.session_state.appearance = "Auto"

if st.session_state.pop("apply_theme", False):
    st.html(
        "<script>(function () {"
        "var key = 'stActiveTheme-' + window.location.pathname + '-v2';"
        f"window.localStorage.setItem(key, JSON.stringify('{THEME_CHOICES[st.session_state.appearance]}'));"
        "window.location.reload();"
        "})();</script>",
        unsafe_allow_javascript=True,
    )
    st.stop()


# ---------------------------------------------------------
# Sidebar controls
# ---------------------------------------------------------
st.sidebar.radio(
    "Appearance",
    options=list(THEME_CHOICES.keys()),
    key="appearance",
    horizontal=True,
    on_change=request_theme_change,
    help="Auto follows your device setting. Light and Dark force that mode on this browser.",
)
st.sidebar.divider()
st.sidebar.markdown("### Mission setup")

target = st.sidebar.radio(
    "Target",
    options=[MOON_TARGET, MARS_TARGET],
    index=0,
    help="Sets the criteria, default weights and target profile.",
)

if target == MOON_TARGET:
    raw_df = moon_raw_df.copy()
    criteria_info = MOON_CRITERIA_INFO
    presets_dict = MOON_PRESETS
    measured_target_dict = MOON_MEASURED_TARGET
    target_subtitle = "Earth test sites for Artemis-era surface operations near the lunar South Pole"
else:
    raw_df = mars_raw_df.copy()
    criteria_info = MARS_CRITERIA_INFO
    presets_dict = MARS_PRESETS
    measured_target_dict = MARS_MEASURED_TARGET
    target_subtitle = "Earth test sites for Mars surface exploration"

criteria_list = list(criteria_info.keys())
measured_specs = MEASURED_CRITERIA[target]
hand_df = raw_df.copy()

score_source = st.sidebar.radio(
    "Score data",
    options=["Measured", "Estimates"],
    index=0,
    horizontal=True,
    help=(
        f"Measured: {len(measured_specs)} of {len(criteria_list)} criteria are computed from NASA and other open data "
        "(climate, elevation, maps, volcano and crater records); the rest are hand estimates. "
        "Estimates: every criterion uses the original hand estimate."
    ),
)
use_measured = score_source == "Measured"
if use_measured:
    raw_df = with_measured(raw_df, target)

# When the target changes, reset the preset and the sliders to that target's baseline.
if "prev_target" not in st.session_state:
    st.session_state.prev_target = target

if st.session_state.prev_target != target:
    st.session_state.prev_target = target
    st.session_state.preset_selector = BASELINE_PRESET
    for c, val in presets_dict[BASELINE_PRESET].items():
        st.session_state[f"slider_{target}_{c}"] = float(val)


def apply_preset():
    """Load the selected preset's weights into the sliders."""
    for c, val in presets_dict[st.session_state.preset_selector].items():
        st.session_state[f"slider_{target}_{c}"] = float(val)


selected_preset = st.sidebar.selectbox(
    "Test objective",
    options=list(presets_dict.keys()),
    index=0,
    key="preset_selector",
    on_change=apply_preset,
    help="Loads a weight profile for a specific kind of test campaign. You can still adjust the weights below.",
)
st.sidebar.caption(PRESET_SUMMARY.get(selected_preset, ""))

st.sidebar.divider()
st.sidebar.markdown("### Criterion weights")

raw_weights: Dict[str, float] = {}
for c in criteria_list:
    key = f"slider_{target}_{c}"
    if key not in st.session_state:
        st.session_state[key] = float(presets_dict[selected_preset].get(c, criteria_info[c]["baseline_weight"]))
    raw_weights[c] = st.sidebar.slider(
        label=c,
        min_value=0.0,
        max_value=50.0,
        step=1.0,
        key=key,
        format="%.0f",
        help=f"{criteria_info[c]['description']}\n\nPlanned data source: {criteria_info[c]['example_data']}",
    )

norm_weights = normalize_weights(raw_weights)
raw_total = sum(raw_weights.values())

preset_weights = presets_dict.get(selected_preset, {})
is_preset_modified = any(abs(raw_weights[c] - preset_weights.get(c, 0.0)) > 0.1 for c in criteria_list)
active_profile = "Custom weights" if is_preset_modified else selected_preset

if raw_total <= 0:
    st.sidebar.warning("All weights are zero, so every criterion is weighted equally.")
elif abs(raw_total - 100.0) > 0.5:
    st.sidebar.caption(f"Sliders total {raw_total:.0f}. They are rescaled to 100% before scoring.")
else:
    st.sidebar.caption("Sliders total 100%.")

st.sidebar.button(
    "Reset weights",
    help=f"Restore the “{selected_preset}” weights.",
    on_click=apply_preset,
    disabled=not is_preset_modified,
    width="stretch",
)

dedupe = st.sidebar.toggle(
    "Count overlapping criteria once",
    value=False,
    help=(
        "Some criteria rise and fall together across the sites, so the same condition is counted twice. "
        "When on, the weight of each such criterion is shared with its partners. Pairs are listed under Validation."
    ),
)

st.sidebar.divider()
st.sidebar.markdown("### Portfolio")
portfolio_k = st.sidebar.radio(
    "Sites in portfolio",
    options=[2, 3],
    index=0,
    horizontal=True,
    help="How many complementary sites to combine.",
)
gap_threshold = st.sidebar.slider(
    "Coverage threshold",
    min_value=60.0,
    max_value=95.0,
    value=85.0,
    step=5.0,
    format="%.0f",
    help="A criterion counts as a gap when no site in the portfolio scores at least this much on it.",
)


# ---------------------------------------------------------
# Scoring
# ---------------------------------------------------------
# The NASA worked-example row is a unit-test reference, not a real site.
eval_df = raw_df[raw_df["site_id"] != "worked_example"].copy().reset_index(drop=True)
hand_df = hand_df[hand_df["site_id"] != "worked_example"].copy().reset_index(drop=True)

# Criteria that move together across the sites; optionally stop counting them twice.
overlap_pairs = overlapping_pairs(eval_df, criteria_list, OVERLAP_R)
slider_weights = norm_weights
if dedupe:
    norm_weights = deduplicated_weights(norm_weights, overlap_pairs)

# Resemblance leaves accessibility out; accessibility is reported on its own for both targets.
match_cols = [c for c in criteria_list if c != ACCESS_CRITERION]
eval_df["match"] = analog_score(eval_df, {c: norm_weights[c] for c in match_cols}).round(1)
eval_df["access"] = eval_df[ACCESS_CRITERION].astype(float)
# How often each site comes first when every score may be off by up to SCORE_ERROR points.
eval_df["win_share"] = first_place_share(eval_df, norm_weights, error=SCORE_ERROR)

eval_df["score"] = analog_score(eval_df, norm_weights).round(1)
eval_df["rank"] = eval_df["score"].rank(ascending=False, method="min").astype(int)
rank_counts = eval_df["rank"].value_counts()
eval_df["display_rank"] = eval_df["rank"].apply(lambda r: f"{r} (tied)" if rank_counts[r] > 1 else str(r))
eval_df = eval_df.sort_values(by=["score", "site_name"], ascending=[False, True]).reset_index(drop=True)
n_sites = len(eval_df)
eval_df["too_close"] = (eval_df["win_share"] >= CONTENDER_SHARE) & (eval_df.index > 0)
n_close = int(eval_df["too_close"].sum())

chosen_indices, coverage_dict, missing_gaps = portfolio(
    eval_df, norm_weights, k=portfolio_k, thr=gap_threshold
)
chosen_sites = eval_df.loc[chosen_indices].copy()
opt_indices, opt_coverage, opt_missing, opt_value = best_portfolio(
    eval_df, norm_weights, k=portfolio_k, thr=gap_threshold
)
opt_sites = eval_df.loc[opt_indices].copy()
top_site = eval_df.iloc[0]
top_site_name = top_site["site_name"]


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
profile_label = "NASA baseline" if active_profile == BASELINE_PRESET else active_profile
top_meta = find_metadata(top_site["site_name"])
top_where = top_site["country"] + (" &middot; " + html.escape(top_meta["climate_zone"]) if top_meta else "")
st.html(
    '<div class="eyebrow">Planetary Analog Ranker</div>'
    f'<h1 class="page-title">{target} analog sites.</h1>'
    f'<p class="page-sub">{target_subtitle}</p>'
    '<div class="hero-grid">'
    '<div class="tile hero"><div>'
    '<div class="tile-label">Top-ranked site</div>'
    f'<div class="hero-name">{html.escape(short_name(top_site["site_name"]))}</div>'
    f'<div class="hero-meta">{top_where}</div></div>'
    f'<div class="ring-wrap" role="img" aria-label="Analog score {top_site["score"]:.1f} of 100">'
    f'<div class="ring" style="--p: {top_site["score"]:.1f};"></div>'
    '<div class="ring-text">'
    f'<div class="ring-num num dec" style="--t: {round(top_site["score"] * 10)};"><span>{top_site["score"]:.1f}</span></div>'
    '<div class="ring-cap">of 100</div></div></div></div>'
    '<div class="tile"><div class="tile-label">Weight profile</div>'
    f'<div class="tile-value">{html.escape(profile_label)}</div>'
    f'<div class="tile-sub">{len(criteria_list)} criteria, {n_sites} candidate sites</div></div>'
    f'<div class="tile"><div class="tile-label">Portfolio gaps</div>'
    f'<div class="tile-value"><span class="num int" style="--t: {len(missing_gaps)};"><span>{len(missing_gaps)}</span></span>'
    f' <small>of {len(criteria_list)} criteria</small></div>'
    f'<div class="tile-sub">Best {portfolio_k} sites together, threshold {gap_threshold:.0f}</div></div>'
    '</div>'
    f'<div class="notice">Prototype. {len(measured_specs) if use_measured else 0} of {len(criteria_list)} criteria are computed from NASA and other open '
    'data; the others are estimates compiled by hand from published analog-site literature. '
    'Sources and checks are under Validation.</div>'
)

with st.expander("How the scoring works"):
    st.markdown(
        f"""
No single place on Earth reproduces every condition of the Moon or Mars, so agencies test across
several sites. This tool scores each site, suggests which {portfolio_k} sites to combine, and checks
how much the ranking depends on the chosen weights.

**1. Analog score.** Each site has a 0–100 score on {len(criteria_list)} criteria (higher means a closer
match to {target}). The Analog Score is the weighted sum:

$$\\text{{AnalogScore}} = \\sum_{{i=1}}^{{N}} \\text{{Normalized}}_i \\times \\text{{Weight}}_i
\\qquad \\sum_{{i=1}}^{{N}} \\text{{Weight}}_i = 1$$

The default weights are the baseline from the NASA challenge guide. As a check, the guide's worked example
(scores 85, 90, 70, 80, 75, 60, 50, 80) gives 75.5, which is covered by a unit test.

**2. Test objectives.** Each objective loads a different weight profile:

- **Rover mobility.** {PRESET_RATIONALE['Rover mobility']}
- **Drilling and sampling.** {PRESET_RATIONALE['Drilling and sampling']}
- **Habitat thermal testing.** {PRESET_RATIONALE['Habitat thermal testing']}
- **Astronaut training.** {PRESET_RATIONALE['Astronaut training']}

**3. Portfolio finder.** A greedy search picks the best single site, then repeatedly adds the site
with the largest weighted improvement over what the chosen sites already cover:

$$\\text{{Gain}}(s) = \\sum_{{c}} w_c \\times \\max(0,\\ \\text{{Score}}_c(s) - \\text{{Covered}}_c)$$

Any criterion whose best score in the portfolio stays below the threshold ({gap_threshold:.0f}) is reported as a gap.
The greedy pick is what the challenge guide asks for, but it can miss the best pair or trio, so the app
also tries every combination of {portfolio_k} sites and shows the true best next to it.

**Isolation versus accessibility.** These two pull in opposite directions: a remote site is hard to reach.
Across the Moon sites they are almost mirror images (correlation about -0.9), so giving both a weight partly
cancels out. The chart under the ranking shows this trade-off directly.

**4. Rank stability.** The ranking is recomputed for 1,000 random weight sets (a Dirichlet distribution),
either close to the current weights or across all possible weightings. A site that stays near the top
in most draws does not depend on one particular choice of weights.

**Resemblance and accessibility.** Accessibility is about how easy a site is to work at, not how much it
looks like {target}. The app reports the two separately for both targets: resemblance is the analog score with
accessibility left out. The Moon's analog score still includes accessibility because the challenge guide does.

**Measured scores.** {len(measured_specs)} of the {len(criteria_list)} criteria are computed from open data instead
of estimated, using NASA POWER climate and UV data (2019–2023), NASA SRTM and ASTER elevation, OpenStreetMap
distances, the Smithsonian volcano database and Wikidata's list of impact structures. Each source and formula
is listed under Validation. Switch **Score data** to Estimates to see the original hand values.

**Too close to call.** Every score is shifted at random by up to {SCORE_ERROR:.0f} points, 1,000 times. A site
that takes first place in at least {CONTENDER_SHARE:.0f}% of those trials is marked too close to call.

**Limits.** The remaining scores are literature-based estimates on a relative 0–100 scale. Criteria are treated as
independent unless **Count overlapping criteria once** is on, and the greedy portfolio is a good approximation rather than a guaranteed optimum.
        """
    )

st.write("")

tab_map, tab_compare, tab_portfolio, tab_validation = st.tabs(
    ["Map and ranking", "Compare", "Portfolio", "Validation"]
)


# =========================================================
# TAB 1: Map and ranking
# =========================================================
with tab_map:
    col_map, col_table = st.columns([1.15, 0.85], gap="medium")

    with col_map:
        st.markdown(f"**{n_sites} candidate sites**, numbered by rank. Select a marker for details.")
        # Zoom chosen so the polar sites (often the top ranks) are visible without panning.
        m = folium.Map(location=[0.0, 10.0], zoom_start=1.0, zoom_snap=0.1, tiles=None)
        canvas = "World_Dark_Gray_Base" if DARK else "World_Light_Gray_Base"
        folium.TileLayer(
            tiles=f"https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/{canvas}/MapServer/tile/{{z}}/{{y}}/{{x}}",
            attr="Esri, HERE, Garmin, OpenStreetMap contributors",
            name="Map",
            max_zoom=16,
        ).add_to(m)
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri, Maxar, Earthstar Geographics",
            name="Satellite",
            max_zoom=17,
            show=False,
        ).add_to(m)
        folium.LayerControl(position="topright", collapsed=False).add_to(m)
        # Restyle the stock Leaflet controls, popups and tooltips to match the page.
        m.get_root().header.add_child(folium.Element(f"""
        <style>
            .leaflet-container {{ background: {PAL['fill']}; font-family: {FONT}; }}
            .leaflet-bar {{ border: none !important; border-radius: 12px !important; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,.16) !important; }}
            .leaflet-bar a {{ width: 34px !important; height: 34px !important; line-height: 34px !important; font-weight: 400;
                background: {CARD} !important; color: {INK} !important; border-bottom: 1px solid {GRID} !important; transition: background .2s; }}
            .leaflet-bar a:hover {{ background: {PAL['fill']} !important; }}
            .leaflet-bar a:last-child {{ border-bottom: none !important; }}
            .leaflet-control-layers {{ border: none !important; border-radius: 12px !important; background: {CARD} !important; color: {INK};
                box-shadow: 0 2px 12px rgba(0,0,0,.16) !important; padding: 8px 12px !important; font-size: 12px; font-weight: 500; }}
            .leaflet-control-layers label {{ margin: 2px 0; cursor: pointer; }}
            .leaflet-control-layers input {{ accent-color: {ACCENT}; }}
            .leaflet-control-attribution {{ font-size: 9px !important; background: transparent !important; color: {MUTED} !important; }}
            .leaflet-control-attribution a {{ color: {MUTED} !important; }}
            .leaflet-attribution-flag {{ display: none !important; }}
            .leaflet-popup-content-wrapper {{ border-radius: 16px !important; background: {CARD} !important; color: {INK} !important;
                box-shadow: 0 12px 40px rgba(0,0,0,.22) !important; }}
            .leaflet-popup-content {{ margin: 14px 16px !important; }}
            .leaflet-popup-tip {{ background: {CARD} !important; }}
            .leaflet-popup-close-button {{ color: {MUTED} !important; top: 6px !important; right: 6px !important; }}
            .leaflet-tooltip {{ border: none !important; border-radius: 8px !important; padding: 5px 10px !important;
                background: {CARD} !important; color: {INK} !important; font: 500 12px {FONT}; box-shadow: 0 4px 16px rgba(0,0,0,.18) !important; }}
            .leaflet-tooltip::before {{ display: none !important; }}
            .leaflet-marker-icon > div {{ transition: transform .2s cubic-bezier(.2,.8,.2,1); }}
            .leaflet-marker-icon:hover > div {{ transform: scale(1.18); }}
        </style>
        """))

        # Draw lower ranks first so the top sites sit on top where markers overlap.
        for _, row in eval_df.iloc[::-1].iterrows():
            rank = int(row["rank"])
            site_id = row["site_id"]
            is_top = rank <= 3
            fill, text_col, border = (ACCENT, "#FFFFFF", "#FFFFFF") if is_top else (CARD, INK, "#636366" if DARK else "#C7C7CC")
            size = 28 if is_top else 24

            ordered = sorted(criteria_list, key=lambda c: row[c], reverse=True)
            lines = []
            for c in ordered[:3]:
                note = measurement(site_id, c).split(";")[0]
                note_html = f"<br><span style='color:{MUTED};'>{note}</span>" if note else ""
                lines.append(f"<div style='margin-top:4px;'><b>{row[c]:.0f}</b> &nbsp;{short_criterion(c)}{note_html}</div>")
            weakest = ordered[-1]
            weak_note = measurement(site_id, weakest).split(";")[0]
            weak_note_html = f"<br><span style='color:{MUTED};'>{weak_note}</span>" if weak_note else ""

            popup_html = f"""
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; width: 250px; font-size: 12px; line-height: 1.4; color: {INK};">
                <div style="font-size: 14px; font-weight: 700;">{row['site_name']}</div>
                <div style="color: {MUTED};">{row['country']} &middot; {row['latitude']:.1f}°, {row['longitude']:.1f}°</div>
                <div style="margin: 6px 0; font-size: 13px;">
                    Rank <b>{row['display_rank']}</b> of {n_sites} &middot; Score <b>{row['score']:.1f}</b>
                </div>
                <div style="border-top: 1px solid {GRID}; padding-top: 5px;">
                    <span style="font-size: 10.5px; letter-spacing: .06em; text-transform: uppercase; color: {MUTED};">Strongest criteria</span>
                    {''.join(lines)}
                </div>
                <div style="border-top: 1px solid {GRID}; padding-top: 5px; margin-top: 6px;">
                    <span style="font-size: 10.5px; letter-spacing: .06em; text-transform: uppercase; color: {MUTED};">Weakest criterion</span>
                    <div style='margin-top:4px;'><b>{row[weakest]:.0f}</b> &nbsp;{short_criterion(weakest)}{weak_note_html}</div>
                </div>
            </div>
            """

            icon_html = (
                f"<div style='width:{size}px;height:{size}px;border-radius:50%;background:{fill};"
                f"border:2px solid {border};color:{text_col};font:600 12px/{size - 4}px -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Arial,sans-serif;"
                f"text-align:center;box-shadow:0 1px 4px rgba(0,0,0,.25);'>{rank}</div>"
            )
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=folium.Popup(popup_html, max_width=280),
                tooltip=f"{row['display_rank']}. {row['site_name']} ({row['score']:.1f})",
                icon=folium.DivIcon(html=icon_html, icon_size=(size, size), icon_anchor=(size // 2, size // 2)),
                z_index_offset=1000 - rank * 10,
            ).add_to(m)

        st_folium(m, width=None, height=470, returned_objects=[])
        st.caption("Filled markers are the top three sites under the current weights.")

    with col_table:
        st.markdown(f"**Ranking** under “{active_profile}”")
        rows_html = []
        for i, (_, r) in enumerate(eval_df.iterrows()):
            tied = "tied" in r["display_rank"]
            rows_html.append(
                f'<div class="rank-row{" top" if r["rank"] <= 3 else ""}">'
                f'<div class="rank-badge">{int(r["rank"])}</div>'
                f'<div><div class="rank-name" title="{html.escape(r["site_name"])}">{html.escape(short_name(r["site_name"]))}</div>'
                f'<div class="rank-sub">{html.escape(r["country"])}{" &middot; tied" if tied else ""}'
                f' &middot; access {r["access"]:.0f}'
                f'{" &middot; too close to call" if r["too_close"] else ""}</div></div>'
                f'<div class="bar"><span style="width: {r["score"]:.1f}%; animation-delay: {i * 35}ms;"></span></div>'
                f'<div class="rank-score">{r["score"]:.1f}</div></div>'
            )
        st.html(f'<div class="panel"><div class="rank-list">{"".join(rows_html)}</div></div>')
        lead_share = float(eval_df.iloc[0]["win_share"])
        close_text = (
            f" {n_close} other site{'s' if n_close != 1 else ''} take first place in at least "
            f"{CONTENDER_SHARE:.0f}% of trials and {'are' if n_close != 1 else 'is'} marked too close to call."
            if n_close else " No other site takes first place often enough to be a real contender."
        )
        st.caption(
            f"If any score could be off by up to {SCORE_ERROR:.0f} points, {short_name(top_site_name)} stays first in "
            f"{lead_share:.0f}% of 1,000 trials.{close_text}"
        )
        export_cols = ["rank", "site_name", "country", "latitude", "longitude", "score", "match", "access", "win_share"]
        export_df = eval_df[export_cols + [c for c in criteria_list if c != ACCESS_CRITERION] + [ACCESS_CRITERION]].rename(
            columns={"match": "resemblance", "access": "accessibility", "win_share": "first_place_share_pct"}
        )
        st.download_button(
            "Download ranking (CSV)",
            data=export_df.to_csv(index=False).encode("utf-8"),
            file_name=f"analog_ranking_{'moon' if target == MOON_TARGET else 'mars'}.csv",
            mime="text/csv",
        )

    st.divider()
    st.markdown("#### Resemblance versus accessibility")
    st.caption(
        f"Resemblance is how closely a site matches {target} (the analog score with accessibility left out). "
        "Accessibility is how easy it is to get crews and equipment there. Sites towards the top right offer both."
    )
    fig_trade = go.Figure(go.Scatter(
        x=eval_df["match"], y=eval_df["access"],
        mode="markers+text",
        text=eval_df["site_name"].map(short_name),
        textposition="top center",
        textfont=dict(size=10, color=MUTED),
        marker=dict(
            size=12, line=dict(color=CARD, width=2),
            color=[ACCENT if r <= 3 else TARGET_GREY for r in eval_df["rank"]],
        ),
        hovertemplate="%{text}<br>Resemblance %{x:.1f}<br>Accessibility %{y:.0f}<extra></extra>",
    ))
    fig_trade.update_layout(
        font=dict(family=FONT, color=INK), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=CARD,
        height=380, margin=dict(l=10, r=20, t=20, b=10), showlegend=False,
        xaxis=dict(title=f"Resemblance to {target} (0–100)", gridcolor=GRID, zeroline=False),
        yaxis=dict(title="Accessibility (0–100)", range=[0, 108], gridcolor=GRID, zeroline=False),
    )
    with st.container(border=True, key="card_tradeoff"):
        st.plotly_chart(fig_trade, width="stretch")

    st.divider()
    st.markdown("#### Top three sites")
    st.caption("Why each site scores well, and what it has been used for.")

    card_cols = st.columns(3, gap="medium")
    for i, (_, row) in enumerate(eval_df.head(3).iterrows()):
        meta = find_metadata(row["site_name"])
        with card_cols[i].container(border=True, key=f"card_top_{i}"):
            where = html.escape(row["country"]) + (" &middot; " + html.escape(meta["climate_zone"]) if meta else "")
            body = html.escape(meta["scientific_justification"]) if meta else "No detailed site notes yet."
            st.html(
                f'<div class="card-label">Rank {row["display_rank"]}{" &middot; too close to call" if row["too_close"] else ""}</div>'
                f'<div class="card-title">{html.escape(row["site_name"])}</div>'
                f'<div class="card-meta">{where}</div>'
                f'<div class="card-score"><div class="bar"><span style="width: {row["score"]:.1f}%;"></span></div>'
                f'<b>{row["score"]:.1f}</b></div>'
                f'<div class="card-body">{body}</div>'
            )
            if meta:
                with st.expander("More about this site"):
                    st.markdown(meta["scientific_justification"])
                    st.markdown(f"**Geology.** {meta['geology_type']}")
                    st.markdown("**Used for**")
                    for pm in meta["primary_missions"]:
                        st.markdown(f"- {pm}")


# =========================================================
# TAB 2: Compare
# =========================================================
with tab_compare:
    col_sel, col_bench = st.columns([1, 1], gap="medium")
    with col_sel:
        selected_site_name = st.selectbox("Earth site", options=eval_df["site_name"].tolist(), index=0)
    with col_bench:
        benchmark_choice = st.radio(
            "Compare against",
            options=["Perfect match (100 on every criterion)", f"Estimated {target} profile"],
            index=0,
            horizontal=True,
            help=(
                "A perfect match scores 100 on every resemblance criterion. The estimated profile places the "
                "target itself on the same 0–100 scales. Accessibility is left off this chart because it "
                "measures how easy a site is to work at, not how much it resembles the target."
            ),
        )

    site_row = eval_df[eval_df["site_name"] == selected_site_name].iloc[0]
    site_id = site_row["site_id"]
    use_estimated = benchmark_choice.startswith("Estimated")

    radar_col, breakdown_col = st.columns([1, 1], gap="medium")

    with radar_col:
        r_site = [float(site_row[c]) for c in match_cols]
        r_target = [float(measured_target_dict[c]) if use_estimated else 100.0 for c in match_cols]
        bench_label = f"Estimated {target} profile" if use_estimated else "Perfect match (100)"
        theta = [wrap_label(c, 15) for c in match_cols]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=r_target + r_target[:1],
            theta=theta + theta[:1],
            name=bench_label,
            mode="lines",
            line=dict(color=TARGET_GREY, width=2, dash="dash"),
            hovertemplate="%{theta}<br>%{r:.0f}<extra>" + bench_label + "</extra>",
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=r_site + r_site[:1],
            theta=theta + theta[:1],
            name=short_name(selected_site_name),
            mode="lines+markers",
            line=dict(color=SITE_COLORS[0], width=2),
            marker=dict(size=8, color=SITE_COLORS[0], line=dict(color=CARD, width=2)),
            fill="toself",
            fillcolor=f"rgba({PAL['accent_rgb']}, 0.14)",
            hovertemplate="%{theta}<br>%{r:.0f}<extra>" + short_name(selected_site_name) + "</extra>",
        ))
        fig_radar.update_layout(
            font=dict(family=FONT, color=INK), paper_bgcolor="rgba(0,0,0,0)",
            polar=dict(
                bgcolor=CARD,
                radialaxis=dict(
                    visible=True, range=[0, 100], tickvals=[25, 50, 75, 100],
                    tickfont=dict(size=10, color=MUTED), gridcolor=GRID, linecolor=GRID, angle=90,
                ),
                angularaxis=dict(tickfont=dict(size=11, color=INK), gridcolor=GRID, linecolor=GRID),
            ),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5),
            margin=dict(l=110, r=110, t=45, b=55),
            height=480,
        )
        with st.container(border=True, key="card_radar"):
            st.plotly_chart(fig_radar, width="stretch")

    with breakdown_col:
        st.markdown(
            f"""
            <div class="card-label">Rank {site_row['display_rank']} of {n_sites}</div>
            <div class="card-title">{selected_site_name}</div>
            <div class="card-meta">Analog score {site_row['score']:.1f} / 100 under “{active_profile}”
            &middot; resemblance {site_row['match']:.1f} &middot; accessibility {site_row['access']:.0f}</div>
            """,
            unsafe_allow_html=True,
        )
        breakdown = pd.DataFrame([
            {
                "Criterion": c,
                "Score": float(site_row[c]),
                "Weight (%)": norm_weights[c] * 100.0,
                "Points": float(site_row[c]) * norm_weights[c],
                "Basis": "Measured" if use_measured and c in measured_specs else "Estimate",
                "Ground observation": measurement(site_id, c) or "No site note yet",
            }
            for c in criteria_list
        ])
        st.dataframe(
            breakdown,
            width="stretch",
            hide_index=True,
            height=318,
            column_config={
                "Score": st.column_config.NumberColumn(format="%.0f", width="small"),
                "Weight (%)": st.column_config.NumberColumn(format="%.1f", width="small"),
                "Points": st.column_config.NumberColumn(
                    format="%.1f", width="small", help="Score × weight. The points add up to the analog score."
                ),
                "Ground observation": st.column_config.TextColumn(width="large"),
            },
        )

        strongest = max(criteria_list, key=lambda c: site_row[c])
        weakest = min(criteria_list, key=lambda c: site_row[c])
        col_s, col_w = st.columns(2)
        with col_s.container(border=True, key="card_strongest"):
            st.markdown(
                f"<div class='card-label'>Strongest criterion</div>"
                f"<div class='card-title'>{strongest}</div>"
                f"<div class='card-meta'>{site_row[strongest]:.0f} / 100</div>",
                unsafe_allow_html=True,
            )
        with col_w.container(border=True, key="card_weakest"):
            st.markdown(
                f"<div class='card-label'>Weakest criterion</div>"
                f"<div class='card-title'>{weakest}</div>"
                f"<div class='card-meta'>{site_row[weakest]:.0f} / 100</div>",
                unsafe_allow_html=True,
            )


# =========================================================
# TAB 3: Portfolio
# =========================================================
with tab_portfolio:
    st.markdown(
        f"The best {portfolio_k} sites to use together. The first pick is the top-ranked site; "
        "each later pick is the site that adds the most to what is already covered."
    )

    # Which chosen site supplies the best score on each criterion, and how the
    # weighted coverage grows with each pick.
    pick_names: List[str] = [short_name(n) for n in chosen_sites["site_name"]]
    pick_color = {name: SITE_COLORS[i] for i, name in enumerate(pick_names)}
    provider: Dict[str, str] = {}
    for c in criteria_list:
        for (_, p_site), name in zip(chosen_sites.iterrows(), pick_names):
            if float(p_site[c]) == coverage_dict[c]:
                provider[c] = name
                break

    running = {c: 0.0 for c in criteria_list}
    coverage_steps: List[float] = []
    for _, p_site in chosen_sites.iterrows():
        for c in criteria_list:
            running[c] = max(running[c], float(p_site[c]))
        coverage_steps.append(sum(norm_weights[c] * running[c] for c in criteria_list))

    col_sites, col_cov = st.columns([0.85, 1.15], gap="medium")

    with col_sites:
        st.markdown("#### Selected sites")
        for i, ((_, p_site), name) in enumerate(zip(chosen_sites.iterrows(), pick_names)):
            supplied = [lower_first(c) for c in criteria_list if provider.get(c) == name]
            gain = coverage_steps[i] - (coverage_steps[i - 1] if i else 0.0)
            gain_text = (
                f"Weighted coverage {coverage_steps[i]:.1f}"
                if i == 0 else
                f"Weighted coverage {coverage_steps[i]:.1f} (+{gain:.1f})"
            )
            with st.container(border=True, key=f"card_pick_{i}"):
                st.markdown(
                    f"""
                    <div class="card-label">Pick {i + 1} &middot; site rank {p_site['display_rank']} &middot; score {p_site['score']:.1f}</div>
                    <div class="card-title"><span class="swatch" style="background:{pick_color[name]};"></span>{p_site['site_name']}</div>
                    <div class="card-meta">{p_site['country']} &middot; {gain_text}</div>
                    """,
                    unsafe_allow_html=True,
                )
                if supplied:
                    st.markdown("Best in portfolio for " + "; ".join(supplied) + ".")
                else:
                    st.markdown("Adds no new best score; another site already covers each criterion at least as well.")
        st.caption(
            "Weighted coverage is the analog score of the portfolio as a whole, "
            "taking the best site for each criterion."
        )

    with col_cov:
        st.markdown("#### Coverage by criterion")
        cov_df = pd.DataFrame([
            {
                "Criterion": c,
                "Coverage": coverage_dict[c],
                "Best site": provider.get(c, pick_names[0]),
                "Label": f"{coverage_dict[c]:.0f}" + ("  below threshold" if coverage_dict[c] < gap_threshold else ""),
            }
            for c in criteria_list
        ])
        fig_cov = px.bar(
            cov_df,
            x="Coverage",
            y="Criterion",
            orientation="h",
            color="Best site",
            color_discrete_map=pick_color,
            category_orders={"Criterion": criteria_list, "Best site": pick_names},
            text="Label",
            range_x=[0, 100],
            height=430,
        )
        fig_cov.update_traces(
            textposition="inside", insidetextanchor="start", textangle=0, textfont=dict(color="#FFFFFF", size=12),
            marker_line_width=0, marker_cornerradius=5, width=0.62,
            hovertemplate="%{y}<br>Best score in portfolio: %{x:.0f}<extra>%{fullData.name}</extra>",
        )
        fig_cov.add_vline(
            x=gap_threshold, line_dash="dash", line_color=INK, line_width=1.5,
            annotation_text=f"Threshold {gap_threshold:.0f}", annotation_position="top",
            annotation_font=dict(size=11, color=INK),
        )
        fig_cov.update_layout(
            font=dict(family=FONT, color=INK), paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=30, b=70),
            xaxis=dict(title="Best score among the selected sites", gridcolor=GRID, zeroline=False),
            yaxis=dict(title=None),
            legend=dict(title="Supplied by  ", orientation="h", yanchor="top", y=-0.2, xanchor="left", x=0),
            plot_bgcolor=CARD,
            bargap=0.3,
        )
        with st.container(border=True, key="card_coverage"):
            st.plotly_chart(fig_cov, width="stretch")

    st.divider()
    st.markdown("#### Greedy pick versus the best possible combination")
    greedy_value = coverage_steps[-1]
    greedy_names = " + ".join(pick_names)
    opt_names = " + ".join(short_name(n) for n in opt_sites["site_name"])
    if set(opt_indices) == set(chosen_indices):
        st.success(
            f"The greedy pick ({greedy_names}) is also the best of all possible {portfolio_k}-site combinations "
            f"(weighted coverage {greedy_value:.1f})."
        )
    else:
        st.warning(
            f"**Greedy:** {greedy_names}, weighted coverage {greedy_value:.1f}, {len(missing_gaps)} gap(s).  \n"
            f"**Best combination:** {opt_names}, weighted coverage {opt_value:.1f}, {len(opt_missing)} gap(s).  \n"
            f"The best combination is {opt_value - greedy_value:.1f} points higher. Greedy picks the top site first "
            "and cannot back out of that choice."
        )
    st.caption("Best combination = every possible set of sites compared, so it is the true optimum for these weights.")

    st.divider()
    st.markdown("#### Gaps the portfolio does not cover")
    if missing_gaps:
        st.markdown(
            f"{len(missing_gaps)} of {len(criteria_list)} criteria stay below {gap_threshold:.0f} at every selected site. "
            "These conditions would need to be tested another way."
        )
        gap_cols = st.columns(min(len(missing_gaps), 3), gap="medium")
        for i, g in enumerate(missing_gaps):
            advice = CRITERION_GAP_ADVICE.get(g, "Test this condition in a laboratory chamber.")
            with gap_cols[i % len(gap_cols)].container(border=True, key=f"card_gap_{i}"):
                st.markdown(
                    f"""
                    <div class="card-label">Best in portfolio {coverage_dict[g]:.0f} / 100</div>
                    <div class="card-title">{g}</div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(f"**Why it matters.** {criteria_info[g]['description']}")
                st.markdown(f"**Suggested alternative.** {advice}")
    else:
        st.success(
            f"No gaps. Every criterion reaches at least {gap_threshold:.0f} at one of the {len(chosen_sites)} selected sites."
        )


# =========================================================
# TAB 4: Validation
# =========================================================
with tab_validation:
    st.markdown(
        "Two checks on the method: where three well-established analog sites land, "
        "and how much the ranking changes when the weights change."
    )

    col_calib, col_stab = st.columns([0.9, 1.1], gap="medium")

    with col_calib:
        st.markdown("#### Calibration against known analogs")
        st.caption(f"Scores and ranks under “{active_profile}”. They update with the weights.")

        calib_roles = {
            "mcmurdo": "Polar cold desert",
            "haughton": "Arctic impact crater",
            "atacama": "Hyper-arid desert",
        }
        calib_rows = [eval_df[eval_df["site_id"] == sid].iloc[0] for sid in calib_roles if (eval_df["site_id"] == sid).any()]
        calib_rows.sort(key=lambda r: r["rank"])

        st.dataframe(
            pd.DataFrame([
                {
                    "Site": short_name(r["site_name"]),
                    "Type": calib_roles[r["site_id"]],
                    "Score": r["score"],
                    f"Rank (of {n_sites})": r["display_rank"],
                }
                for r in calib_rows
            ]),
            width="stretch",
            hide_index=True,
            column_config={"Score": st.column_config.NumberColumn(format="%.1f")},
        )

        # Findings are generated from the live scores, so they stay true for any weights.
        top_third = math.ceil(n_sites / 3)
        high = [r for r in calib_rows if r["rank"] <= top_third]
        findings = []
        for r in calib_rows:
            ordered = sorted(criteria_list, key=lambda c: r[c], reverse=True)
            strengths = " and ".join(f"{lower_first(c)} ({r[c]:.0f})" for c in ordered[:2])
            sentence = f"**{short_name(r['site_name'])}** ranks {r['display_rank']} of {n_sites}. Strongest on {strengths}."
            if r["rank"] > top_third:
                # What costs this site the most points under the current weights.
                losses = sorted(criteria_list, key=lambda c: norm_weights[c] * (100.0 - r[c]), reverse=True)[:2]
                loss_text = " and ".join(f"{lower_first(c)} ({r[c]:.0f})" for c in losses)
                sentence += f" It lands lower mainly because of {loss_text}."
            else:
                weakest_c = ordered[-1]
                sentence += f" Weakest on {lower_first(weakest_c)} ({r[weakest_c]:.0f})."
            findings.append(f"- {sentence}")
        st.markdown("\n".join(findings))

        if len(high) == len(calib_rows):
            verdict = f"All {len(calib_rows)} known analogs land in the top third (top {top_third} of {n_sites}) under these weights."
        elif high:
            verdict = (
                f"{len(high)} of {len(calib_rows)} known analogs land in the top third (top {top_third} of {n_sites}) "
                "under these weights. A known analog that lands lower is a finding, not an error: each of these "
                f"sites is used for particular conditions, and the criteria above show where it differs from {target}."
            )
        else:
            verdict = (
                f"None of the known analogs land in the top third (top {top_third} of {n_sites}) under these weights. "
                "This weight profile favours conditions those sites are not known for."
            )
        st.info(verdict)
        st.caption(
            "Limit of this check: the team chose the hand estimates, so known analogs ranking high partly reflects "
            "the team's own judgement. The comparison with measured data below is the independent check."
        )

    with col_stab:
        st.markdown("#### Rank stability")
        stab_mode = st.radio(
            "Vary the weights",
            options=["Around the current weights", "Across all possible weightings"],
            index=0,
            horizontal=True,
            help=(
                "Around the current weights: 1,000 weight sets close to the sliders, which shows how robust "
                "this objective's ranking is. Across all possible weightings: 1,000 weight sets drawn uniformly, "
                "which ignores the sliders and shows which sites do well whatever the objective."
            ),
        )
        stab_local = stab_mode.startswith("Around")
        st.caption(
            f"Share of 1,000 weight sets near “{active_profile}” in which each site stays near the top."
            if stab_local else
            "Share of 1,000 random weight sets in which each site stays near the top. This view ignores the sliders."
        )
        stab_options = {"Top 3": 3, "Top 5": 5, "Top 10": 10}
        stab_choice = st.radio(
            "Count a site as stable when it ranks in the",
            options=list(stab_options.keys()),
            index=1,
            horizontal=True,
        )
        stab_top_n = stab_options[stab_choice]

        if stab_local:
            stability = rank_stability_local(eval_df, norm_weights, num_runs=1000, top_n=stab_top_n, seed=42)
        else:
            stability = rank_stability(eval_df, criteria_list, num_runs=1000, top_n=stab_top_n, seed=42)
        stab_df = pd.DataFrame({
            "Site": eval_df["site_name"].map(short_name),
            "Rate": stability.values,
        }).sort_values("Rate", ascending=True)

        fig_stab = go.Figure(go.Bar(
            x=stab_df["Rate"],
            y=stab_df["Site"],
            orientation="h",
            marker=dict(color=SITE_COLORS[0], cornerradius=4),
            width=0.62,
            text=[f"{v:.0f}%" for v in stab_df["Rate"]],
            textposition="outside",
            textfont=dict(color=INK, size=11),
            cliponaxis=False,
            hovertemplate="%{y}<br>In the " + stab_choice.lower() + " in %{x:.1f}% of weight sets<extra></extra>",
        ))
        fig_stab.update_layout(
            font=dict(family=FONT, color=INK), paper_bgcolor="rgba(0,0,0,0)",
            height=max(360, 26 * len(stab_df) + 70),
            margin=dict(l=10, r=40, t=10, b=10),
            xaxis=dict(
                title=f"Share of weight sets with the site in the {stab_choice.lower()} (%)",
                range=[0, 100], gridcolor=GRID, zeroline=False,
            ),
            yaxis=dict(title=None),
            plot_bgcolor=CARD,
            showlegend=False,
        )
        with st.container(border=True, key="card_stability"):
            st.plotly_chart(fig_stab, width="stretch")

        leaders = stab_df.sort_values("Rate", ascending=False).head(2)
        st.markdown(
            f"**{leaders.iloc[0]['Site']}** ({leaders.iloc[0]['Rate']:.0f}%) and "
            f"**{leaders.iloc[1]['Site']}** ({leaders.iloc[1]['Rate']:.0f}%) are the most stable "
f"{stab_choice.lower()} sites for {target}"
            + (f" when the weights move around “{active_profile}”. " if stab_local else ". ")
            + "Sites with a low share only rank well under particular weightings."
        )

    st.divider()
    col_meas, col_over = st.columns([1.1, 0.9], gap="medium")

    with col_meas:
        st.markdown("#### Hand estimates versus measured data")
        st.caption(
            "For each criterion that can be computed from open data, how well the original hand estimate "
            "orders the sites compared with the measurement (1.0 = identical order, 0 = unrelated)."
        )
        measured_scores = with_measured(hand_df, target)
        agree_rows = []
        for c, spec in measured_specs.items():
            agree_rows.append({
                "Criterion": short_criterion(c),
                "Source": spec["source"],
                "Agreement": float(hand_df[c].rank().corr(measured_scores[c].rank())),
                "Gap": float((hand_df[c] - measured_scores[c]).abs().mean()),
            })
        agree_df = pd.DataFrame(agree_rows)
        st.dataframe(
            agree_df, width="stretch", hide_index=True,
            column_config={
                "Agreement": st.column_config.NumberColumn(format="%.2f", help="Rank correlation between hand estimate and measured score."),
                "Gap": st.column_config.NumberColumn(format="%.0f pts", help="Average absolute difference between hand estimate and measured score, on the 0–100 scale."),
            },
        )
        strong = agree_df[agree_df["Agreement"] >= 0.8]
        weak = agree_df[agree_df["Agreement"] < 0.8]
        text = f"{len(strong)} of {len(agree_df)} measured criteria order the sites almost the same way as the hand estimates."
        if len(weak):
            text += " Weaker agreement on " + " and ".join(lower_first(c) for c in weak["Criterion"]) + ", where the estimates should be trusted less."
        st.markdown(text)
        st.caption(
            "Limits: ERA5 describes a grid cell of roughly 10–25 km, so a small dry or cold pocket (a dry valley, "
            "a summit) can look wetter or milder than it is. The crater score measures nearness to a confirmed "
            "impact structure, not how much of the terrain it covers. A low agreement is not always the "
            "measurement being right: it flags a criterion to look at."
        )

    with col_over:
        st.markdown("#### Overlapping criteria")
        st.caption(
            f"Pairs of criteria whose scores are strongly related across the {n_sites} sites "
            f"(correlation of {OVERLAP_R} or more, either direction)."
        )
        if overlap_pairs:
            st.dataframe(
                pd.DataFrame([
                    {
                        "Criteria": f"{short_criterion(a).split(' and ')[0]} + {short_criterion(b).split(' for ')[0]}",
                        "r": r,
                        "Effect": "Counted twice" if r > 0 else "Opposites",
                    }
                    for a, b, r in overlap_pairs
                ]),
                width="stretch", hide_index=True,
                column_config={"r": st.column_config.NumberColumn(format="%.2f", width="small", help="Correlation across the sites.")},
            )
            st.markdown(
                "Criteria that are counted twice get more influence than their weights suggest. "
                + ("**Count overlapping criteria once** is on, so their weights are shared."
                   if dedupe else "Turn on **Count overlapping criteria once** in the sidebar to share their weights.")
            )
        else:
            st.success("No pair of criteria is strongly related under the current score data.")

    st.divider()
    st.markdown("#### Two climate sources compared")
    st.caption(
        "The temperature and aridity scores use ERA5. NASA POWER (MERRA-2) gives the same quantities on a coarser "
        "grid of about 50 km, so it serves as an independent check. Agreement is the rank correlation across all "
        f"{len(MEASURED)} sites."
    )
    cross_rows = []
    for label, cols in CROSS_CHECK.items():
        a, b = MEASURED[cols["main"]].astype(float), MEASURED[cols["other"]].astype(float)
        worst = (a - b).abs().idxmax()
        worst_name = raw_df.loc[raw_df["site_id"] == worst, "site_name"]
        worst_name = short_name(worst_name.iloc[0]) if len(worst_name) else worst
        cross_rows.append({
            "Quantity": label,
            "Agreement": float(a.rank().corr(b.rank())),
            "Largest difference": f"{worst_name}: ERA5 {a[worst]:.0f}, NASA POWER {b[worst]:.0f}",
        })
    st.dataframe(
        pd.DataFrame(cross_rows), width="stretch", hide_index=True,
        column_config={"Agreement": st.column_config.NumberColumn(format="%.2f", width="small")},
    )
    st.caption(
        "The largest differences are at summits and basins that are smaller than a NASA POWER grid cell, "
        "which is why ERA5 is used for scoring and NASA POWER for UV and for this check."
    )

    st.divider()
    st.markdown("#### Data sources")
    st.markdown(
        f"{len(measured_specs)} of {len(criteria_list)} {target} criteria are computed from open data; "
        "`data/fetch_measured.py` rebuilds them from the original services and `data/measured.csv` holds the raw values. "
        "The rest are hand estimates, and the last column names the dataset that would replace each one."
    )
    provenance = pd.DataFrame([
        {
            "Criterion": c,
            "Now": "Measured" if c in measured_specs else "Hand estimate",
            "Source in use": measured_specs[c]["source"] if c in measured_specs else "Published analog-site literature",
            "How it is scored": (getattr(engine, measured_specs[c]["fn"]).__doc__ or "").strip().split("\n")[0] if c in measured_specs else "",
            "Planned dataset": criteria_info[c]["example_data"],
        }
        for c in criteria_list
    ])
    st.dataframe(provenance, width="stretch", hide_index=True)
    st.caption(
        "Target profiles come from mission data: LRO Diviner, LOLA and CRaTER for the Moon; "
        "MOLA, THEMIS, CRISM and Curiosity's REMS and RAD for Mars."
    )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.write("")
st.markdown(
    "<div class='footer'>Planetary Analog Ranker. Prototype built for the NASA Space Apps Challenge 2026. "
    "Not an official NASA product. Site scores combine open climate and elevation data with estimates from published literature.</div>",
    unsafe_allow_html=True,
)
