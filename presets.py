"""
Analog Ranker Hackathon - Presets & Target Definitions
Contains criteria, baseline NASA weights, mission-objective weight profiles,
physical planetary target benchmarks, and tailored engineering gap mitigation advice
for both Moon South Pole and Mars exploration targets.
"""

from typing import Dict, Any

MOON_TARGET = "Moon South Pole"
MARS_TARGET = "Mars"

# --- Moon South Pole Configuration ---
MOON_CRITERIA_INFO: Dict[str, Dict[str, Any]] = {
    "Extreme cold and temperature range": {
        "baseline_weight": 15.0,
        "example_data": "MODIS LST, ERA5",
        "unit": "Min/Max Kelvin (K)",
        "description": "Permanently Shadowed Regions (PSRs) at lunar south pole reach ~25-50 K (-248°C to -223°C); analog captures extreme cryogenic thermal environments."
    },
    "Aridity / low humidity": {
        "baseline_weight": 15.0,
        "example_data": "MODIS, MERRA-2",
        "unit": "Precipitation (mm/yr)",
        "description": "Vacuum / hyper-arid conditions; absence of atmospheric moisture crucial for electrostatic dust behavior."
    },
    "High radiation / UV": {
        "baseline_weight": 10.0,
        "example_data": "OMI UV, altitude proxy",
        "unit": "UV Index / Elevation (m)",
        "description": "Lack of protective magnetosphere/atmosphere on Moon results in intense cosmic ray and solar radiation."
    },
    "Rocky / regolith-like surface": {
        "baseline_weight": 15.0,
        "example_data": "Landsat, Sentinel-2, ASTER",
        "unit": "Grain Size / Particle Texture",
        "description": "Anorthosite and basalt fragment regolith; abrasive particulate grain sizes affecting rover mobility and seals."
    },
    "Topographic complexity": {
        "baseline_weight": 15.0,
        "example_data": "SRTM, ASTER GDEM",
        "unit": "Slope Gradient (°)",
        "description": "Steep crater rims (Shackleton, Cabeus), rough boulder fields, severe slope navigation challenges."
    },
    "Isolation": {
        "baseline_weight": 10.0,
        "example_data": "WorldPop, OpenStreetMap",
        "unit": "Logistics Distance (km)",
        "description": "Remoteness from urban infrastructure for comms latency simulation, autonomous operations, and psychological isolation."
    },
    "Polar / high-latitude conditions": {
        "baseline_weight": 10.0,
        "example_data": "Latitude + illumination",
        "unit": "Latitude (°) / Solar Elevation",
        "description": "Low-angle incident sunlight, elongated shadows, polar diurnal cycles mimicking polar lunar lighting."
    },
    "Accessibility for testing": {
        "baseline_weight": 10.0,
        "example_data": "Roads, airports",
        "unit": "Transit Time (hours)",
        "description": "Feasibility of transporting heavy rover payloads, field crews, and scientific instrument packages."
    }
}

MOON_PRESETS: Dict[str, Dict[str, float]] = {
    "Balanced (NASA Baseline)": {
        "Extreme cold and temperature range": 15.0,
        "Aridity / low humidity": 15.0,
        "High radiation / UV": 10.0,
        "Rocky / regolith-like surface": 15.0,
        "Topographic complexity": 15.0,
        "Isolation": 10.0,
        "Polar / high-latitude conditions": 10.0,
        "Accessibility for testing": 10.0
    },
    "Rover mobility": {
        "Extreme cold and temperature range": 5.0,
        "Aridity / low humidity": 10.0,
        "High radiation / UV": 5.0,
        "Rocky / regolith-like surface": 30.0,
        "Topographic complexity": 30.0,
        "Isolation": 5.0,
        "Polar / high-latitude conditions": 5.0,
        "Accessibility for testing": 10.0
    },
    "Drilling and sampling": {
        "Extreme cold and temperature range": 15.0,
        "Aridity / low humidity": 10.0,
        "High radiation / UV": 5.0,
        "Rocky / regolith-like surface": 25.0,
        "Topographic complexity": 15.0,
        "Isolation": 5.0,
        "Polar / high-latitude conditions": 10.0,
        "Accessibility for testing": 15.0
    },
    "Habitat thermal testing": {
        "Extreme cold and temperature range": 35.0,
        "Aridity / low humidity": 25.0,
        "High radiation / UV": 10.0,
        "Rocky / regolith-like surface": 5.0,
        "Topographic complexity": 5.0,
        "Isolation": 15.0,
        "Polar / high-latitude conditions": 5.0,
        "Accessibility for testing": 0.0
    },
    "Astronaut training": {
        "Extreme cold and temperature range": 10.0,
        "Aridity / low humidity": 5.0,
        "High radiation / UV": 5.0,
        "Rocky / regolith-like surface": 15.0,
        "Topographic complexity": 15.0,
        "Isolation": 20.0,
        "Polar / high-latitude conditions": 15.0,
        "Accessibility for testing": 15.0
    }
}

# Physical Target Benchmark derived from LRO Diviner, LOLA, CRaTER
MOON_MEASURED_TARGET: Dict[str, float] = {
    "Extreme cold and temperature range": 98.0,
    "Aridity / low humidity": 100.0,
    "High radiation / UV": 95.0,
    "Rocky / regolith-like surface": 90.0,
    "Topographic complexity": 85.0,
    "Isolation": 100.0,
    "Polar / high-latitude conditions": 95.0,
    "Accessibility for testing": 10.0
}


# --- Mars Configuration ---
MARS_CRITERIA_INFO: Dict[str, Dict[str, Any]] = {
    "Extreme aridity": {
        "baseline_weight": 18.0,
        "example_data": "CHIRPS, soil moisture",
        "unit": "Precipitation (mm/yr)",
        "description": "Hyper-arid conditions analogous to Mars global desiccated surface and dry atmospheric column."
    },
    "Oxidized / iron-rich soils": {
        "baseline_weight": 15.0,
        "example_data": "ASTER, Landsat indices",
        "unit": "Ferric Oxide Index",
        "description": "Hematite, ferric oxides, and reddish mineral weathering matching Martian surface spectral features."
    },
    "Dust / fine particles": {
        "baseline_weight": 12.0,
        "example_data": "Aerosol data, dust maps",
        "unit": "Aerosol Optical Depth",
        "description": "Fine airborne dust, lofting potential, mechanical abrasion on solar arrays and mechanisms."
    },
    "Temperature extremes": {
        "baseline_weight": 12.0,
        "example_data": "MODIS LST",
        "unit": "Diurnal Range (Δ°C)",
        "description": "Wide diurnal temperature swings and sustained sub-zero thermal extremes."
    },
    "Volcanic / basaltic terrain": {
        "baseline_weight": 15.0,
        "example_data": "Geological maps, ASTER",
        "unit": "Mafic / Basalt Coverage (%)",
        "description": "Flood basalts, lava tubes, tephra, volcanic ash shields replicating Martian volcanism (Tharsis/Elysium)."
    },
    "Impact features / craters": {
        "baseline_weight": 10.0,
        "example_data": "Crater databases, DEM",
        "unit": "Crater Density / Breccia",
        "description": "Impact ejecta blankets, breccia, crater ramparts, and shatter topography."
    },
    "Salt / perchlorate-like chemistry": {
        "baseline_weight": 8.0,
        "example_data": "Soil chemistry proxies",
        "unit": "Perchlorate / Sulfate (wt%)",
        "description": "Evaporite chlorides, sulfates, perchlorates, nitrates matching Phoenix / Curiosity soil assays."
    },
    "Isolation and logistics": {
        "baseline_weight": 10.0,
        "example_data": "Population, infrastructure",
        "unit": "Distance to Hub (km)",
        "description": "Remoteness only: operational independence, mission delay testing, expedition survival testing. How easy the site is to reach is reported separately as the accessibility score."
    }
}

MARS_PRESETS: Dict[str, Dict[str, float]] = {
    "Balanced (NASA Baseline)": {
        "Extreme aridity": 18.0,
        "Oxidized / iron-rich soils": 15.0,
        "Dust / fine particles": 12.0,
        "Temperature extremes": 12.0,
        "Volcanic / basaltic terrain": 15.0,
        "Impact features / craters": 10.0,
        "Salt / perchlorate-like chemistry": 8.0,
        "Isolation and logistics": 10.0
    },
    "Rover mobility": {
        "Extreme aridity": 10.0,
        "Oxidized / iron-rich soils": 10.0,
        "Dust / fine particles": 15.0,
        "Temperature extremes": 5.0,
        "Volcanic / basaltic terrain": 30.0,
        "Impact features / craters": 20.0,
        "Salt / perchlorate-like chemistry": 0.0,
        "Isolation and logistics": 10.0
    },
    "Drilling and sampling": {
        "Extreme aridity": 10.0,
        "Oxidized / iron-rich soils": 20.0,
        "Dust / fine particles": 5.0,
        "Temperature extremes": 5.0,
        "Volcanic / basaltic terrain": 25.0,
        "Impact features / craters": 15.0,
        "Salt / perchlorate-like chemistry": 10.0,
        "Isolation and logistics": 10.0
    },
    "Habitat thermal testing": {
        "Extreme aridity": 25.0,
        "Oxidized / iron-rich soils": 5.0,
        "Dust / fine particles": 15.0,
        "Temperature extremes": 30.0,
        "Volcanic / basaltic terrain": 5.0,
        "Impact features / craters": 0.0,
        "Salt / perchlorate-like chemistry": 5.0,
        "Isolation and logistics": 15.0
    },
    "Astronaut training": {
        "Extreme aridity": 15.0,
        "Oxidized / iron-rich soils": 10.0,
        "Dust / fine particles": 15.0,
        "Temperature extremes": 10.0,
        "Volcanic / basaltic terrain": 15.0,
        "Impact features / craters": 15.0,
        "Salt / perchlorate-like chemistry": 5.0,
        "Isolation and logistics": 15.0
    }
}

# Physical Target Benchmark derived from MOLA, THEMIS, CRISM, REMS
MARS_MEASURED_TARGET: Dict[str, float] = {
    "Extreme aridity": 98.0,
    "Oxidized / iron-rich soils": 95.0,
    "Dust / fine particles": 90.0,
    "Temperature extremes": 85.0,
    "Volcanic / basaltic terrain": 80.0,
    "Impact features / craters": 75.0,
    "Salt / perchlorate-like chemistry": 85.0,
    "Isolation and logistics": 100.0
}


# --- Scientific Rationale for Presets ---
PRESET_RATIONALE: Dict[str, str] = {
    "Balanced (NASA Baseline)": (
        "Applies the baseline multi-criteria weights from the NASA Hackathon Guide. "
        "Balances geological surface fidelity, atmospheric/thermal physics, and operational logistics equally."
    ),
    "Rover mobility": (
        "Emphasizes terrain: topography plus rocky surface on the Moon (60% combined), volcanic plus impact terrain on Mars (50% combined). "
        "Rover drive systems face catastrophic risk from slope rollover, chassis high-centering, "
        "and abrasive wheel wear on sharp basalt rocks; thermal and chemical factors are secondary."
    ),
    "Drilling and sampling": (
        "Prioritizes rocky or basaltic substrate (25% on both targets), with accessibility weighted 15% on the Moon. "
        "Sub-surface drilling and core extraction require competent rock layers (basalt, breccia, permafrost) "
        "and road access to transport heavy hydraulic drill rigs and return intact core samples."
    ),
    "Habitat thermal testing": (
        "Focuses predominantly on Extreme cold / temperature range (30–35%) and Aridity (25%). "
        "Thermal insulation, environmental control, and seal integrity fail under extreme freeze-thaw "
        "cycling and hard vacuum/desiccation; terrain roughness is irrelevant for stationary habitats."
    ),
    "Astronaut training": (
        "Balances isolation (15–20%) with harsh surface conditions, and on the Moon accessibility (15%). "
        "Simulating crew psychology, communications latency, and space suit (EVA) mobility requires "
        "harsh isolation yet reliable medical evacuation logistics and representative visual lighting."
    )
}


# --- Tailored Engineering Recommendations for Uncovered Gaps ---
CRITERION_GAP_ADVICE: Dict[str, str] = {
    # Moon Criteria
    "Extreme cold and temperature range": (
        "Execute cryogenic thermal vacuum (TVAC) chamber testing (e.g. NASA Glenn VF-6) with liquid helium shrouds down to 40 K."
    ),
    "Aridity / low humidity": (
        "Subject mechanism seals and actuators to high-vacuum chamber runs (< 10⁻⁷ Torr) to evaluate electrostatic adhesion and outgassing."
    ),
    "High radiation / UV": (
        "Expose avionics and spacesuit polymers to particle accelerator beamlines (e.g. NASA Space Radiation Lab at Brookhaven)."
    ),
    "Rocky / regolith-like surface": (
        "Conduct wheel and drill bite tests in indoor simulant bins loaded with anorthositic lunar regolith simulant (LHS-1 / JSC-1A)."
    ),
    "Topographic complexity": (
        "Deploy rover chassis on variable-angle tilt tables and boulder obstacle courses in indoor mobility test arenas."
    ),
    "Isolation": (
        "Enforce simulated communications delay (1.3s Moon, up to 20m Mars) and crew confinement protocols at an isolation habitat (e.g. HERA)."
    ),
    "Polar / high-latitude conditions": (
        "Mount directional collimated low-angle LED solar lamps in darkened test facilities to evaluate shadow navigation and glare."
    ),
    "Accessibility for testing": (
        "Develop modular transport containers and remote air-drop deployment procedures to mitigate field access bottlenecks."
    ),
    
    # Mars Criteria
    "Extreme aridity": (
        "Utilize desiccated carbon dioxide environmental chambers with desiccated Mars soil simulant (MMS-1)."
    ),
    "Oxidized / iron-rich soils": (
        "Formulate synthetic ferric iron / hematite and jarosite chemical testbeds to evaluate corrosion and optical spectrometer calibration."
    ),
    "Dust / fine particles": (
        "Perform dust aerosolization in a low-pressure (0.6 kPa CO₂) wind tunnel to quantify solar panel obscuration and bearing wear."
    ),
    "Temperature extremes": (
        "Thermal cycle mechanisms in a CO₂ atmosphere chamber from -120°C to +20°C to stress-test battery life and actuator lubricants."
    ),
    "Volcanic / basaltic terrain": (
        "Supplement testing on basaltic lava fields (e.g. Hawaii PISCES or Iceland) or engineered basaltic slag obstacle courses."
    ),
    "Impact features / craters": (
        "Simulate impact crater rampart traversal at Barringer (Meteor) Crater or Ries Crater, or analyze projectile shatter blocks."
    ),
    "Salt / perchlorate-like chemistry": (
        "Prepare chemical test baths with magnesium/calcium perchlorates (0.5–1.0 wt%) to test seal corrosion and soil sample chemistry."
    ),
    "Isolation and logistics": (
        "Run strict autonomous mission control protocols with delayed comms simulation at remote field stations."
    )
}


# One-sentence versions of the rationale above, shown under the objective selector.
PRESET_SUMMARY: Dict[str, str] = {
    "Balanced (NASA Baseline)": "The baseline weights from the NASA challenge guide, with no single condition dominating.",
    "Rover mobility": "Favours rough terrain and rocky ground, where rovers are most at risk.",
    "Drilling and sampling": "Favours hard rocky ground and sites that heavy drill rigs can reach.",
    "Habitat thermal testing": "Favours extreme cold, large temperature swings and dry air; terrain matters little.",
    "Astronaut training": "Favours isolated sites with harsh conditions that crews can still reach and leave safely.",
}


# --- Resemblance versus practicality ---
# Accessibility says how easy a site is to work at, not how much it looks like the target.
# The app reports it separately for both targets (the Moon also keeps it in the guide's score).
ACCESS_CRITERION = "Accessibility for testing"

# Criteria whose scores are computed from measurements in data/measured.csv:
# criterion -> engine function, the measured columns it takes, the source, and how to show the raw value.
_CLIMATE = "ERA5 2019–2023"
_OSM = "OpenStreetMap"
ACCESS_SPEC: Dict[str, Any] = {
    "fn": "accessibility_score", "cols": ["airport_km", "road_km"], "source": _OSM,
    "raw": "{airport_km:.0f} km to a commercial airport; {road_km:.0f} km to a public road",
}
MEASURED_CRITERIA: Dict[str, Dict[str, Dict[str, Any]]] = {
    MOON_TARGET: {
        "Extreme cold and temperature range": {"fn": "cold_score", "cols": ["tmin_p1_c"], "source": _CLIMATE, "raw": "coldest 1% of nights {tmin_p1_c:.0f} °C"},
        "Aridity / low humidity": {"fn": "aridity_score", "cols": ["precip_mm_yr"], "source": _CLIMATE, "raw": "{precip_mm_yr:.0f} mm precipitation per year"},
        "High radiation / UV": {"fn": "uv_score", "cols": ["uv_index_mean"], "source": "NASA POWER (CERES) 2019–2023", "raw": "all-day mean UV index {uv_index_mean:.1f}; 95th percentile {uv_index_p95:.1f}"},
        "Topographic complexity": {"fn": "relief_score", "cols": ["relief_std_m"], "source": "NASA SRTM / ASTER GDEM 30 m", "raw": "elevation spread {relief_std_m:.0f} m within 20 km ({dem})"},
        "Isolation": {"fn": "isolation_score", "cols": ["town_km"], "source": _OSM, "raw": "{town_km:.0f} km to the nearest town or city"},
        "Polar / high-latitude conditions": {"fn": "polar_score_from_latitude", "cols": ["latitude"], "source": "Site latitude", "raw": "latitude {latitude:.1f}°"},
        ACCESS_CRITERION: ACCESS_SPEC,
    },
    MARS_TARGET: {
        "Extreme aridity": {"fn": "aridity_score", "cols": ["precip_mm_yr"], "source": _CLIMATE, "raw": "{precip_mm_yr:.0f} mm precipitation per year"},
        "Temperature extremes": {"fn": "temperature_extremes_score", "cols": ["tmin_p1_c", "diurnal_range_c"], "source": _CLIMATE, "raw": "coldest 1% of nights {tmin_p1_c:.0f} °C; daily swing {diurnal_range_c:.0f} °C"},
        "Impact features / craters": {"fn": "crater_score", "cols": ["crater_km", "crater_diameter_km"], "source": "Wikidata impact structures", "raw": "{crater_km:.0f} km to {crater_name}"},
        "Isolation and logistics": {"fn": "isolation_score", "cols": ["town_km"], "source": _OSM, "raw": "{town_km:.0f} km to the nearest town or city"},
    },
}

# Search limits: a distance equal to its limit means "nothing found within this many km".
SEARCH_LIMIT_KM: Dict[str, float] = {"town_km": 1500.0, "airport_km": 3000.0}

# A second, independent source for the climate values, used only as a cross-check (NASA POWER / MERRA-2).
CROSS_CHECK: Dict[str, Dict[str, str]] = {
    "Coldest nights (°C)": {"main": "tmin_p1_c", "other": "power_tmin_p1_c"},
    "Precipitation (mm/yr)": {"main": "precip_mm_yr", "other": "power_precip_mm_yr"},
    "Daily temperature swing (°C)": {"main": "diurnal_range_c", "other": "power_diurnal_range_c"},
}
