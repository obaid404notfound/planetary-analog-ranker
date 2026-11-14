"""
Builds data/measured.csv: real measurements for every candidate site.

All sources are open and need no account:

  ERA5 (Open-Meteo archive)      daily 2 m temperature min/max and precipitation, 2019-2023. Used for the
                                 temperature and aridity scores because its grid (about 10-25 km, corrected
                                 for site elevation) resolves summits and basins.
  NASA POWER (MERRA-2 + CERES)   UV index, surface solar radiation and humidity, 2019-2023, plus the same
                                 temperature and precipitation values (power_* columns) as a cross-check.
                                 Its grid is about 50 km, too coarse for summits and basins.
  NASA SRTM 30 m                 elevation on a 9 x 11 grid (about 20 km x 20 km) around the site;
  NASA/METI ASTER GDEM 30 m      used instead of SRTM poleward of 60 degrees, where SRTM has no data
  OpenStreetMap (Overpass)       distance to the nearest town or city, commercial airport and road
  Smithsonian GVP                distance to the nearest Holocene or Pleistocene volcano, and its rock type
  Wikidata                       distance to the nearest confirmed impact structure, and its diameter

Run from the project root:   python data/fetch_measured.py
Only the Python standard library is used. Responses are cached in data/.cache so a re-run is fast;
delete that folder to download everything again. The app reads the CSV and never calls these services.
"""

import csv
import hashlib
import json
import math
import os
import statistics
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, ".cache")
START, END = "2019-01-01", "2023-12-31"
YEARS = 5.0
GRID_ROWS, GRID_COLS, STEP_KM = 9, 11, 2.2
UA = "analog-ranker-data-build/1.0"
OVERPASS = "https://overpass-api.de/api/interpreter"
MAX_SEARCH_KM = 3000.0


# ----------------------------------------------------------------- helpers
def get_json(url: str, data: bytes = None, headers: dict = None, tries: int = 5, pause: float = 0.0):
    """GET (or POST when `data` is given) with an on-disk cache and retries."""
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.sha1((url + "|" + (data or b"").decode("utf-8")).encode("utf-8")).hexdigest()
    path = os.path.join(CACHE, key + ".json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, **(headers or {})})
            with urllib.request.urlopen(req, timeout=180) as resp:
                out = json.load(resp)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(out, f)
            time.sleep(pause)
            return out
        except Exception as exc:  # noqa: BLE001 - network errors of any kind are retried
            if attempt == tries - 1:
                raise
            print(f"   retry {attempt + 1} after {type(exc).__name__}", flush=True)
            time.sleep(8 * (attempt + 1))


def percentile(values, p):
    s = sorted(values)
    return s[min(len(s) - 1, max(0, int(round(p / 100.0 * (len(s) - 1)))))]


def km_between(lat1, lon1, lat2, lon2) -> float:
    """Great-circle distance in kilometres."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 6371.0 * 2 * math.asin(min(1.0, math.sqrt(a)))


# ----------------------------------------------------------------- climate
def climate_stats(tmax, tmin, precip) -> dict:
    days = [(a, b, c or 0.0) for a, b, c in zip(tmax, tmin, precip) if a is not None and b is not None]
    hi = [d[0] for d in days]
    lo = [d[1] for d in days]
    return {
        "precip_mm_yr": round(sum(d[2] for d in days) / YEARS, 1),
        "tmin_p1_c": round(percentile(lo, 1), 1),
        "tmax_p99_c": round(percentile(hi, 99), 1),
        "tmean_c": round(statistics.fmean((a + b) / 2 for a, b in zip(hi, lo)), 1),
        "diurnal_range_c": round(statistics.fmean(a - b for a, b in zip(hi, lo)), 1),
    }


def nasa_power(lat: float, lon: float) -> dict:
    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        "?parameters=T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,ALLSKY_SFC_UV_INDEX,ALLSKY_SFC_SW_DWN"
        f"&community=RE&longitude={lon}&latitude={lat}"
        f"&start={START.replace('-', '')}&end={END.replace('-', '')}&format=JSON"
    )
    p = get_json(url, pause=1.0)["properties"]["parameter"]
    dates = sorted(p["T2M_MAX"])
    val = lambda name, d: None if p[name][d] <= -900 else p[name][d]  # -999 marks missing
    stats = climate_stats([val("T2M_MAX", d) for d in dates], [val("T2M_MIN", d) for d in dates],
                          [val("PRECTOTCORR", d) for d in dates])
    out = {f"power_{k}": v for k, v in stats.items() if k in ("precip_mm_yr", "tmin_p1_c", "diurnal_range_c")}
    rh = [v for v in (val("RH2M", d) for d in dates) if v is not None]
    # UV and sunlight are missing during polar night; those days count as zero.
    uv = [val("ALLSKY_SFC_UV_INDEX", d) or 0.0 for d in dates]
    sw = [val("ALLSKY_SFC_SW_DWN", d) or 0.0 for d in dates]
    out.update({
        "rel_humidity_pct": round(statistics.fmean(rh), 1),
        "uv_index_mean": round(statistics.fmean(uv), 2),
        "uv_index_p95": round(percentile(uv, 95), 2),
        "solar_kwh_m2_day": round(statistics.fmean(sw), 2),
    })
    return out


def era5(lat: float, lon: float) -> dict:
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lon}&start_date={START}&end_date={END}"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=GMT"
    )
    d = get_json(url, pause=0.5)["daily"]
    return climate_stats(d["temperature_2m_max"], d["temperature_2m_min"], d["precipitation_sum"])


# ----------------------------------------------------------------- terrain
def relief(lat: float, lon: float) -> dict:
    dataset = "srtm30m" if abs(lat) < 56 else "aster30m"  # SRTM covers 56 S to 60 N
    dlat = STEP_KM / 111.0
    dlon = STEP_KM / (111.0 * max(0.05, math.cos(math.radians(lat))))
    pts = [
        (lat + (r - GRID_ROWS // 2) * dlat, lon + (c - GRID_COLS // 2) * dlon)
        for r in range(GRID_ROWS) for c in range(GRID_COLS)
    ]
    locs = "|".join(f"{a:.5f},{b:.5f}" for a, b in pts)
    res = get_json(f"https://api.opentopodata.org/v1/{dataset}?locations={locs}", pause=1.2)["results"]
    elev = [r["elevation"] for r in res if r["elevation"] is not None]
    return {
        "dem": "SRTM 30 m" if dataset == "srtm30m" else "ASTER GDEM 30 m",
        "elevation_m": round(statistics.fmean(elev)),
        "relief_std_m": round(statistics.pstdev(elev), 1),
        "relief_range_m": round(max(elev) - min(elev)),
    }


# ----------------------------------------------------------------- OpenStreetMap
def nearest_osm(lat: float, lon: float, selector: str, radii_km) -> float:
    """Distance to the nearest matching OpenStreetMap feature, widening the search until one is found."""
    for radius in radii_km:
        query = f"[out:json][timeout:120];({selector.format(r=int(radius * 1000), lat=lat, lon=lon)});out center;"
        body = urllib.parse.urlencode({"data": query}).encode("utf-8")
        elements = get_json(OVERPASS, data=body, pause=2.0).get("elements", [])
        dists = []
        for e in elements:
            la = e.get("lat", e.get("center", {}).get("lat"))
            lo = e.get("lon", e.get("center", {}).get("lon"))
            if la is not None:
                dists.append(km_between(lat, lon, la, lo))
        if dists:
            return round(min(dists), 1)
    return float(radii_km[-1])  # nothing within the widest search: recorded as that limit


def osm(lat: float, lon: float) -> dict:
    town = 'node["place"~"^(city|town)$"](around:{r},{lat},{lon});'
    airport = 'nwr["aeroway"="aerodrome"]["iata"](around:{r},{lat},{lon});'
    road = 'way["highway"~"^(motorway|trunk|primary|secondary|tertiary)$"](around:{r},{lat},{lon});'
    return {
        "town_km": nearest_osm(lat, lon, town, (50, 200, 600, 1500)),
        "airport_km": nearest_osm(lat, lon, airport, (100, 400, 1200, MAX_SEARCH_KM)),
        "road_km": nearest_osm(lat, lon, road, (5, 25, 100, 400, 1200)),
    }


# ----------------------------------------------------------------- volcanoes and craters
def load_volcanoes():
    # The Pleistocene layer does not record a rock type, so those volcanoes carry an empty one.
    layers = {
        "Smithsonian_VOTW_Holocene_Volcanoes": "Volcano_Name,Latitude,Longitude,Major_Rock_Type",
        "Smithsonian_VOTW_Pleistocene_Volcanoes": "Volcano_Name,Latitude,Longitude",
    }
    out = []
    for layer, props in layers.items():
        url = (
            "https://webservices.volcano.si.edu/geoserver/GVP-VOTW/ows?service=WFS&version=1.0.0"
            f"&request=GetFeature&typeName=GVP-VOTW:{layer}&outputFormat=application/json&propertyName={props}"
        )
        for f in get_json(url)["features"]:
            p = f["properties"]
            if p.get("Latitude") is None:
                continue
            out.append((p["Latitude"], p["Longitude"], p["Volcano_Name"], p.get("Major_Rock_Type") or "rock type not recorded"))
    return out


def load_craters():
    query = (
        "SELECT ?c ?cLabel ?coord ?diam WHERE { ?c wdt:P31/wdt:P279* wd:Q55818; wdt:P625 ?coord; wdt:P17 ?country. "
        "OPTIONAL { ?c wdt:P2386 ?diam } "
        'SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } }'
    )
    url = "https://query.wikidata.org/sparql?" + urllib.parse.urlencode({"query": query})
    rows = get_json(url, headers={"Accept": "application/sparql-results+json"})["results"]["bindings"]
    out = []
    for b in rows:
        coord = b["coord"]["value"]
        if not coord.startswith("Point("):  # coordinates on another body carry a globe prefix; skip them
            continue
        lon, lat = coord.replace("Point(", "").replace(")", "").split()
        diam = float(b["diam"]["value"]) if "diam" in b else 0.0
        out.append((float(lat), float(lon), b["cLabel"]["value"], diam))
    return out


def nearest(lat, lon, features):
    best = min(features, key=lambda f: km_between(lat, lon, f[0], f[1]))
    return round(km_between(lat, lon, best[0], best[1]), 1), best[2], best[3]


# ----------------------------------------------------------------- main
def main():
    sites = {}
    for name in ("moon_sites.csv", "mars_sites.csv"):
        with open(os.path.join(HERE, name), newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row["site_id"] != "worked_example":
                    sites[row["site_id"]] = (float(row["latitude"]), float(row["longitude"]))

    volcanoes = load_volcanoes()
    craters = load_craters()
    print(f"{len(volcanoes)} volcanoes, {len(craters)} impact structures loaded")

    rows = []
    for site_id, (lat, lon) in sorted(sites.items()):
        print(site_id, flush=True)
        row = {"site_id": site_id, "latitude": lat, "longitude": lon}
        row.update(era5(lat, lon))
        row.update(nasa_power(lat, lon))
        row.update(relief(lat, lon))
        row.update(osm(lat, lon))
        v_km, v_name, v_rock = nearest(lat, lon, volcanoes)
        c_km, c_name, c_diam = nearest(lat, lon, craters)
        row.update({
            "volcano_km": v_km, "volcano_name": v_name, "volcano_rock": v_rock,
            "crater_km": c_km, "crater_name": c_name, "crater_diameter_km": c_diam,
        })
        rows.append(row)
        print("  ", {k: v for k, v in row.items() if k not in ("site_id", "latitude", "longitude")})

    out = os.path.join(HERE, "measured.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {out} ({len(rows)} sites)")


if __name__ == "__main__":
    main()
