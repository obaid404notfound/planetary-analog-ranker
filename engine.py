"""
Analog Ranker Hackathon - Core Engine
Implements:
1. Analog Score (weighted multi-criteria evaluation with normalization)
2. Analog Portfolio Finder (greedy submodular coverage optimization with gap analysis)
3. Rank Stability (Monte Carlo Dirichlet weight perturbation)
4. Radar Comparison (criterion-by-criterion target alignment)
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd


def normalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    """Normalize weight dictionary so all weights sum to 1.0."""
    total = sum(weights.values())
    if total <= 0:
        n = len(weights)
        return {k: 1.0 / n for k in weights}
    return {k: v / total for k, v in weights.items()}


def analog_score(df: pd.DataFrame, weights: Dict[str, float]) -> pd.Series:
    """
    Computes 0-100 Analog Score per site.
    AnalogScore = sum(Normalized_i * Weight_i)
    
    Formula from NASA Hackathon Guide:
    w = np.array([weights[c] for c in cols])
    w = w / w.sum()
    return df[cols].values @ w
    """
    cols = list(weights.keys())
    w = np.array([weights[c] for c in cols], dtype=float)
    w_sum = w.sum()
    if w_sum > 0:
        w = w / w_sum
    else:
        w = np.ones(len(cols)) / len(cols)
    
    scores = df[cols].values @ w
    return pd.Series(scores, index=df.index, name="analog_score")


def portfolio(
    df: pd.DataFrame, 
    weights: Dict[str, float], 
    k: int = 3, 
    thr: float = 70.0
) -> Tuple[List[any], Dict[str, float], List[str]]:
    """
    Analog Portfolio Finder (top pick).
    Greedy rule: pick the best site, then repeatedly add the site whose weighted
    improvement over what the chosen sites already cover is largest.
    
    Parameters:
        df: DataFrame with sites and criterion score columns (0-100)
        weights: Dictionary of criterion weights
        k: Number of sites to select (2 or 3)
        thr: Threshold below which a criterion is flagged as still missing
        
    Returns:
        chosen: List of site IDs / indices chosen
        covered: Dict mapping each criterion to max coverage score achieved
        missing: List of criteria whose coverage remains below thr
    """
    cols = list(weights.keys())
    w = np.array([weights[c] for c in cols], dtype=float)
    w_sum = w.sum()
    norm_w = {c: weights[c] / w_sum if w_sum > 0 else 1.0 / len(cols) for c in cols}
    
    chosen: List[any] = []
    covered: Dict[str, float] = {c: 0.0 for c in cols}
    
    # In case k is greater than number of sites available
    max_k = min(k, len(df))
    
    for _ in range(max_k):
        def gain(i):
            row = df.loc[i]
            return sum(norm_w[c] * max(0.0, float(row[c]) - covered[c]) for c in cols)
        
        candidates = [i for i in df.index if i not in chosen]
        if not candidates:
            break
            
        best = max(candidates, key=gain)
        chosen.append(best)
        for c in cols:
            covered[c] = max(covered[c], float(df.loc[best, c]))
            
    # Gap report: any criterion whose best coverage stays below thr is listed as still missing
    missing = [c for c in cols if covered[c] < thr]
    
    return chosen, covered, missing


def rank_stability(
    df: pd.DataFrame, 
    cols: List[str], 
    num_runs: int = 1000, 
    top_n: int = 10,
    seed: int = 42
) -> pd.Series:
    """
    Rank stability analysis via Dirichlet weight perturbation.
    Draw about 1,000 random weight sets (Dirichlet keeps them summing to 1),
    rank the sites each time, and count how often each stays in the top N.
    
    rng = np.random.default_rng(42)
    W = rng.dirichlet(np.ones(len(cols)), size=1000)
    scores = df[cols].values @ W.T # sites x 1000
    ranks = (-scores).argsort(0).argsort(0) # 0 = best
    top10_rate = (ranks < 10).mean(axis=1) * 100 # % of runs in top 10
    """
    rng = np.random.default_rng(seed)
    # Dirichlet with concentration parameter alpha = 1.0 represents uniform sampling over the simplex
    W = rng.dirichlet(np.ones(len(cols)), size=num_runs)
    scores = df[cols].values @ W.T  # sites x num_runs
    ranks = (-scores).argsort(0).argsort(0)  # 0 = best rank
    
    effective_top_n = min(top_n, len(df))
    top_rate = (ranks < effective_top_n).mean(axis=1) * 100.0
    return pd.Series(top_rate, index=df.index, name=f"top_{effective_top_n}_rate")


def portfolio_value(df: pd.DataFrame, weights: Dict[str, float], chosen: List[any]) -> float:
    """Weighted coverage of a set of sites: best score per criterion, weighted and summed."""
    cols = list(weights.keys())
    w = np.array([weights[c] for c in cols], dtype=float)
    w = w / w.sum() if w.sum() > 0 else np.ones(len(cols)) / len(cols)
    best = df.loc[list(chosen), cols].values.max(axis=0)
    return float(best @ w)


def best_portfolio(
    df: pd.DataFrame,
    weights: Dict[str, float],
    k: int = 3,
    thr: float = 70.0,
) -> Tuple[List[any], Dict[str, float], List[str], float]:
    """
    True optimum: try every combination of k sites and keep the one with the highest
    weighted coverage. With ~15 sites and k <= 3 that is at most a few hundred
    combinations, so no approximation is needed.
    Returns (chosen, covered, missing, weighted_coverage), like `portfolio` plus the value.
    """
    from itertools import combinations

    cols = list(weights.keys())
    k = min(k, len(df))
    best_set, best_val = None, -1.0
    for combo in combinations(list(df.index), k):
        val = portfolio_value(df, weights, combo)
        if val > best_val + 1e-9:
            best_set, best_val = list(combo), val
    covered = {c: float(df.loc[best_set, c].max()) for c in cols}
    missing = [c for c in cols if covered[c] < thr]
    return best_set, covered, missing, best_val


def polar_score_from_latitude(latitude: float) -> float:
    """100 × (|latitude| / 80)², capped at 100.

    Polar / high-latitude score computed from latitude alone (0-100).
    score = 100 * (|lat| / 80)^2, capped at 100. The square keeps mid-latitudes low
    (45 deg -> 32) while the polar sites (75+ deg) land near the top, the way
    low-angle polar illumination does. Pure function of a measured quantity, so
    this criterion is reproducible rather than estimated.
    """
    return float(min(100.0, 100.0 * (abs(latitude) / 80.0) ** 2))


def rank_stability_local(
    df: pd.DataFrame,
    weights: Dict[str, float],
    concentration: float = 40.0,
    num_runs: int = 1000,
    top_n: int = 10,
    seed: int = 42,
) -> pd.Series:
    """
    Rank stability around a chosen weight profile.
    Weight sets are drawn from a Dirichlet centred on `weights` (alpha = weight * concentration),
    so the draws stay close to the chosen objective instead of covering every possible weighting.
    With concentration 40 a 25% weight typically moves by about +/- 7 points.
    """
    cols = list(weights.keys())
    w = np.array([weights[c] for c in cols], dtype=float)
    w = w / w.sum() if w.sum() > 0 else np.ones(len(cols)) / len(cols)
    alpha = np.maximum(w * concentration, 0.05)  # zero-weight criteria stay near zero
    rng = np.random.default_rng(seed)
    W = rng.dirichlet(alpha, size=num_runs)
    scores = df[cols].values @ W.T
    ranks = (-scores).argsort(0).argsort(0)
    effective_top_n = min(top_n, len(df))
    return pd.Series((ranks < effective_top_n).mean(axis=1) * 100.0, index=df.index, name=f"top_{effective_top_n}_rate")


def first_place_share(
    df: pd.DataFrame,
    weights: Dict[str, float],
    error: float = 5.0,
    num_runs: int = 1000,
    seed: int = 42,
) -> pd.Series:
    """
    How often each site ranks first when every criterion score may be wrong by up to
    +/- `error` points (uniform noise, clipped to 0-100). Returns a percentage per site.
    A leader that wins in well under 100% of trials is not a safe number one.
    """
    cols = list(weights.keys())
    w = np.array([weights[c] for c in cols], dtype=float)
    w = w / w.sum() if w.sum() > 0 else np.ones(len(cols)) / len(cols)
    rng = np.random.default_rng(seed)
    base = df[cols].values.astype(float)
    noise = rng.uniform(-error, error, size=(num_runs,) + base.shape)
    scores = np.clip(base[None, :, :] + noise, 0.0, 100.0) @ w  # runs x sites
    wins = np.bincount(scores.argmax(axis=1), minlength=len(df))
    return pd.Series(wins / num_runs * 100.0, index=df.index, name="first_place_share")


def overlapping_pairs(df: pd.DataFrame, cols: List[str], threshold: float = 0.8) -> List[Tuple[str, str, float]]:
    """Criterion pairs whose scores are strongly correlated across the sites (|r| >= threshold)."""
    corr = df[cols].astype(float).corr()
    pairs = []
    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            r = corr.loc[a, b]
            if pd.notna(r) and abs(r) >= threshold:
                pairs.append((a, b, float(r)))
    return sorted(pairs, key=lambda p: -abs(p[2]))


def deduplicated_weights(weights: Dict[str, float], pairs: List[Tuple[str, str, float]]) -> Dict[str, float]:
    """
    Stop counting the same thing twice: each criterion's weight is divided by
    (1 + number of criteria it rises and falls with), then all weights are rescaled to sum to 1.
    Only positive correlations count; opposites (such as isolation and accessibility) are left alone.
    """
    partners = {c: 0 for c in weights}
    for a, b, r in pairs:
        if r > 0 and a in partners and b in partners:
            partners[a] += 1
            partners[b] += 1
    return normalize_weights({c: weights[c] / (1 + partners[c]) for c in weights})


# --- Scores computed from measurements (see data/fetch_measured.py) ---

def cold_score(tmin_p1_c: float) -> float:
    """Coldest 1% of nights: +25 °C or warmer scores 0, −70 °C or colder scores 100."""
    return float(np.clip((25.0 - tmin_p1_c) / 95.0 * 100.0, 0.0, 100.0))


def aridity_score(precip_mm_yr: float) -> float:
    """Annual precipitation, log scale: 5 mm or less scores 100, 1,000 mm or more scores 0."""
    p = max(precip_mm_yr, 5.0)
    return float(np.clip(100.0 * (1.0 - np.log10(p / 5.0) / np.log10(1000.0 / 5.0)), 0.0, 100.0))


def relief_score(relief_std_m: float) -> float:
    """Spread of elevation in a 20 km window, log scale: flat scores 0, 600 m or more scores 100."""
    return float(np.clip(100.0 * np.log10(1.0 + relief_std_m) / np.log10(601.0), 0.0, 100.0))


def temperature_extremes_score(tmin_p1_c: float, diurnal_range_c: float) -> float:
    """Half coldest nights (as for cold), half mean daily swing (25 °C or more scores 100)."""
    swing = float(np.clip(diurnal_range_c / 25.0 * 100.0, 0.0, 100.0))
    return 0.5 * cold_score(tmin_p1_c) + 0.5 * swing


def _log_scale(value: float, low: float, high: float) -> float:
    """0 at `low` or below, 100 at `high` or above, logarithmic in between."""
    v = min(max(float(value), low), high)
    return float(100.0 * np.log10(v / low) / np.log10(high / low))


def uv_score(uv_index_mean: float) -> float:
    """All-day mean UV index, polar night counted as zero: 0 scores 0, 3 or more scores 100."""
    return float(np.clip(uv_index_mean / 3.0 * 100.0, 0.0, 100.0))


def isolation_score(town_km: float) -> float:
    """Distance to the nearest town or city, log scale: 5 km or less scores 0, 1,000 km or more scores 100."""
    return _log_scale(town_km, 5.0, 1000.0)


def accessibility_score(airport_km: float, road_km: float) -> float:
    """Starts at 100; loses up to 60 for distance to a commercial airport and up to 40 for distance to a road.

    Both penalties are on log scales: airport 20 km -> 0, 2,000 km -> 60; road 1 km -> 0, 300 km -> 40.
    """
    return float(100.0 - 0.6 * _log_scale(airport_km, 20.0, 2000.0) - 0.4 * _log_scale(road_km, 1.0, 300.0))


def volcanic_score(volcano_km: float, rock_type: str = "") -> float:
    """100 at a Holocene or Pleistocene volcano, halving every 40 km; non-basalt volcanoes count for three quarters.

    Not used for scoring: it only sees young volcanoes and misses ancient basalt (the Pilbara scores 0),
    so the volcanic criterion stays a hand estimate. Kept for comparison.
    """
    factor = 1.0 if "basalt" in str(rock_type).lower() else 0.75
    return float(100.0 * factor * 0.5 ** (max(0.0, volcano_km) / 40.0))


def crater_score(crater_km: float, crater_diameter_km: float = 0.0) -> float:
    """100 inside a confirmed impact structure, halving every 40 km beyond its rim.

    A small structure counts as 5 km in radius. A proxy for impact terrain, not a measure of crater density.
    """
    rim = max(float(crater_diameter_km or 0.0) / 2.0, 5.0)
    return float(100.0 * 0.5 ** (max(0.0, crater_km - rim) / 40.0))
