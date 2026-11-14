"""
Analog Ranker Hackathon - Earth Analog Sites Detailed Metadata & Science Notes
Provides geographic coordinates, geological classifications, NASA/ESA operational history,
and physical ground measurements for candidate Earth analog sites.
"""

from typing import Dict, Any

SITE_METADATA: Dict[str, Dict[str, Any]] = {
    "McMurdo Dry Valleys": {
        "full_name": "McMurdo Dry Valleys (Taylor & Wright Valleys)",
        "country": "Antarctica",
        "latitude": -77.50,
        "longitude": 162.87,
        "elevation_m": 800,
        "climate_zone": "Polar hyper-arid desert",
        "geology_type": "Glacial till, sandstone bedrock, wind-scoured regolith, permafrost polygons",
        "analog_for": ["Moon South Pole", "Mars polar/cryogenic"],
        "is_calibration_site": True,
        "summary": "Coldest, driest desert on Earth with liquid water virtually absent. Wind-scoured regolith and permafrost closely mimic high-latitude lunar and Martian soil physics.",
        "scientific_justification": (
            "The Dry Valleys are maintained by powerful katabatic winds that evaporate all moisture, "
            "creating a hyper-arid, sub-zero environment. NASA Astrobiology and planetary science teams "
            "use McMurdo to test autonomous cryogenic drills and study endolithic organisms in sandstone rocks. "
            "Ranks exceptionally high for extreme cold and aridity, but receives a realistic logistics penalty "
            "due to extreme Antarctic isolation and treaty constraints."
        ),
        "primary_missions": ["NASA ASTEP IceBreaker drill", "Cryogenic core sample drills", "Astrobiology life-detection protocols"]
    },
    "Haughton Impact Crater": {
        "full_name": "Haughton Impact Structure, Devon Island",
        "country": "Canada (Nunavut)",
        "latitude": 75.38,
        "longitude": -89.67,
        "elevation_m": 250,
        "climate_zone": "High Arctic polar desert",
        "geology_type": "Complex impact crater (23 km dia), shatter cones, impact melt breccia, permafrost ground ice",
        "analog_for": ["Moon South Pole", "Mars impact terrains"],
        "is_calibration_site": True,
        "summary": "A 23-km diameter impact crater situated in the High Arctic. Features deep gullies, shatter cones, and ejecta blocks ideal for crater rim rover exploration.",
        "scientific_justification": (
            "Formed ~39 million years ago, Haughton Crater is the home of the NASA Haughton-Mars Project (HMP). "
            "Its combination of genuine meteorite impact features (hydrothermal paleovents, ejecta blocks, "
            "fractured dolomite target rock) with Arctic permafrost makes it an unequalled dual-analog for lunar "
            "impact basin exploration and Martian periglacial landscapes. Moderately isolated with seasonal airstrip access."
        ),
        "primary_missions": ["NASA Haughton-Mars Project (HMP)", "CSA rover testing", "Autonomous EVA traverse simulations"]
    },
    "Atacama Desert (Yungay)": {
        "full_name": "Atacama Hyperarid Core (Yungay / Peine)",
        "country": "Chile",
        "latitude": -24.06,
        "longitude": -69.87,
        "elevation_m": 1200,
        "climate_zone": "Subtropical hyperarid desert",
        "geology_type": "Evaporite nitrates, perchlorates, gypsum, volcanic cobbles, oxidised sands",
        "analog_for": ["Mars geochemical", "Moon hyperarid vacuum proxy"],
        "is_calibration_site": True,
        "summary": "The oldest and driest non-polar desert on Earth. Possesses chemical oxidants, UV radiation levels, and perchlorate soil salts directly analogous to Martian regolith.",
        "scientific_justification": (
            "Rainfall in the core has averaged <1 mm/year for over 2 million years. Atacama's soil chemistry—bearing "
            "perchlorates, nitrates, and extreme reactive oxygen species—served as the baseline testbed for the Viking, "
            "Phoenix, and Mars Science Laboratory (Curiosity) instrument packages. High solar UV flux tests coatings "
            "and materials degradation. High accessibility via Pan-American highway infrastructure."
        ),
        "primary_missions": ["Viking / Phoenix biology package calibration", "ESA ExoMars drill field trials", "Zoë autonomous rover"]
    },
    "Mauna Kea & Mauna Loa (HI-SEAS)": {
        "full_name": "HI-SEAS Habitat & Mauna Kea Basaltic Slopes",
        "country": "United States (Hawaii)",
        "latitude": 19.82,
        "longitude": -155.47,
        "elevation_m": 2500,
        "climate_zone": "Alpine volcanic desert",
        "geology_type": "Tholeiitic basalt, basaltic ash, volcanic tephra, active lava tubes",
        "analog_for": ["Moon lunar mare", "Mars volcanic shields / lava tubes"],
        "is_calibration_site": False,
        "summary": "Basaltic volcanic terrain with weathered ash mimicking lunar mare regolith, accompanied by extensive lava tube networks for subsurface habitat engineering.",
        "scientific_justification": (
            "Hawaii's shield volcanoes produce weathered basaltic tephra whose particle size distribution, mineralogy, "
            "and shear strength closely simulate lunar mare dust. The HI-SEAS habitat on Mauna Loa hosts long-duration "
            "human isolation analog missions, while Mauna Kea's basalt fields are frequently used for PISCES and NASA rover testing."
        ),
        "primary_missions": ["NASA HI-SEAS Isolation Campaigns", "PISCES Lunar Rover Field Trials", "Lava tube LiDAR mapping"]
    },
    "Askja Caldera & Holuhraun": {
        "full_name": "Askja Caldera & Holuhraun Lava Shield, Central Highlands",
        "country": "Iceland",
        "latitude": 65.03,
        "longitude": -16.75,
        "elevation_m": 1100,
        "climate_zone": "Sub-polar volcanic desert",
        "geology_type": "Holocene tholeiitic basalt, pumice tephra, collapse caldera, fresh aa lava flows",
        "analog_for": ["Moon Apollo heritage analog", "Mars volcanic basalt"],
        "is_calibration_site": False,
        "summary": "Historic Apollo astronaut lunar training site featuring extensive barren volcanic ash and basalt plains with no vegetation.",
        "scientific_justification": (
            "In 1965 and 1967, Apollo crews (including Neil Armstrong) trained here in field geology because its barren, "
            "cratered basaltic pumice landscapes were deemed the most lunar-like accessible environment on Earth. Today, "
            "the 2014-2015 Holuhraun basalt lava field provides pristine, unweathered basaltic textures for rover obstacle negotiation."
        ),
        "primary_missions": ["Apollo geology field training (Apollo 11, 15, 17)", "NASA GLEN rover trials", "Drone aerial survey calibration"]
    },
    "Concordia Station (Dome C)": {
        "full_name": "Concordia Research Station, Dome C",
        "country": "Antarctica (French-Italian)",
        "latitude": -75.10,
        "longitude": 123.33,
        "elevation_m": 3233,
        "climate_zone": "Polar continental deep-freeze",
        "geology_type": "Glacial ice plateau, packed firn, snow sastrugi, extreme altitude desert",
        "analog_for": ["Moon South Pole PSR thermal analog", "Crew extreme isolation"],
        "is_calibration_site": False,
        "summary": "High-altitude Antarctic plateau station enduring temperatures below -80°C and 9 months of total winter physical isolation.",
        "scientific_justification": (
            "Operating at an equivalent physiological altitude of 3,800m with temperatures plunging below -80°C, Concordia "
            "is ESA's premier human spaceflight simulation testbed. Replicates the cryogenic temperatures of Moon South Pole "
            "craters and tests habitat thermal insulation, life support reliability, and psychological confinement under 100 days of polar night."
        ),
        "primary_missions": ["ESA Human Spaceflight isolation studies", "Extreme cryogenic life-support testing", "Hypobaric hypoxia physiology"]
    },
    "Svalbard (AMASE & Ny-Ålesund)": {
        "full_name": "Svalbard Archipelago (AMASE Sites, Spitsbergen)",
        "country": "Norway",
        "latitude": 78.93,
        "longitude": 11.93,
        "elevation_m": 350,
        "climate_zone": "Arctic polar marine / permafrost",
        "geology_type": "Basaltic volcanism in sedimentary basins, glaciers, carbonate globules in basalt (ALH84001 analog)",
        "analog_for": ["Mars astrobiology & glaciers", "Moon high-latitude illumination"],
        "is_calibration_site": False,
        "summary": "Arctic test site featuring basaltic volcanic outcrops interacting with glaciers. Contains carbonate globules identical to those found in Martian meteorite ALH84001.",
        "scientific_justification": (
            "Site of the Arctic Mars Analog Svalbard Expedition (AMASE), supported by NASA and ESA. The Bockfjorden "
            "volcanic complex hosts primitive mantle xenoliths and carbonate deposits precipitated in cryogenic conditions, "
            "used to validate Raman spectrometers and CHEMCAM-like instruments for Mars rover missions."
        ),
        "primary_missions": ["ESA/NASA AMASE Expeditions", "ExoMars PanCam & Raman testing", "Polar rover autonomy"]
    },
    "Mojave Desert / Pisgah Crater (Desert RATS)": {
        "full_name": "Mojave Desert & Pisgah Volcanic Field",
        "country": "United States (California)",
        "latitude": 34.75,
        "longitude": -116.38,
        "elevation_m": 640,
        "climate_zone": "Arid continental desert",
        "geology_type": "Basaltic cinder cone, pahoehoe and aa basalt lava flows, alluvial fanglomerates",
        "analog_for": ["Moon rover mobility", "Mars rover mobility"],
        "is_calibration_site": False,
        "summary": "Accessible volcanic field with diverse lava morphologies and steep crater slopes, heavily utilized for NASA rover and spacesuit mobility tests.",
        "scientific_justification": (
            "Served as the primary testing grounds for NASA's Desert Research and Technology Studies (Desert RATS), "
            "testing pressurized lunar rovers (SEV), robotic assistants (Centaur), and space suit field walk protocols. "
            "Exceptional logistics, year-round road accessibility, and diverse terrain textures make it a top operational hub."
        ),
        "primary_missions": ["NASA Desert RATS field exercises", "Space Exploration Vehicle (SEV) tests", "Chariot rover mobility"]
    },
    "Teide Caldera (Las Cañadas)": {
        "full_name": "Las Cañadas Caldera & Mount Teide, Tenerife",
        "country": "Spain (Canary Islands)",
        "latitude": 28.27,
        "longitude": -16.64,
        "elevation_m": 2200,
        "climate_zone": "High-altitude volcanic alpine",
        "geology_type": "Phonolite & basaltic lava flows, pyroclastic pumice deposits, volcanic caldera wall",
        "analog_for": ["Mars volcanic plains & rover obstacle navigation"],
        "is_calibration_site": False,
        "summary": "High-altitude volcanic caldera featuring rugged basaltic and phonolitic blocky lava fields under clear skies and high UV.",
        "scientific_justification": (
            "Used by the European Space Agency (ESA) for ExoMars field trials (Seeker rover tests). Offers a wide range "
            "of obstacle types (pumice gravel, aa lava, smooth pahoehoe, cratered slopes) with high logistical convenience "
            "and immediate laboratory access."
        ),
        "primary_missions": ["ESA Seeker rover autonomous navigation", "ExoMars optical camera calibrations", "Field spectrometer trials"]
    },
    "Qaidam Basin (Yardang Field)": {
        "full_name": "Qaidam Basin Hyper-Arid Yardang Field, Qinghai",
        "country": "China (Tibetan Plateau)",
        "latitude": 37.85,
        "longitude": 93.40,
        "elevation_m": 2850,
        "climate_zone": "High-altitude hyper-arid plateau desert",
        "geology_type": "Wind-carved yardangs, evaporite playa salts, perchlorate-bearing silts, aeolian dunes",
        "analog_for": ["Mars aeolian yardangs & salt flats"],
        "is_calibration_site": False,
        "summary": "Earth's largest and highest hyperarid yardang field with strong UV radiation, perchlorate salts, and massive wind-carved landforms.",
        "scientific_justification": (
            "Located at ~3,000 meters altitude on the Tibetan Plateau, Qaidam Basin combines extreme solar UV radiation, "
            "hyper-aridity, and intense aeolian erosion. The yardang fields match the Medusae Fossae Formation on Mars, "
            "and its saline playa sediments contain sulfate and perchlorate minerals directly relevant to the Zhurong and Curiosity missions."
        ),
        "primary_missions": ["Tianwen-1 / Zhurong instrument calibration", "Wind-erosion rover mobility models", "Evaporite spectroscopy"]
    },
    "Danakil Depression": {
        "full_name": "Danakil Depression & Dallol Geothermal Field",
        "country": "Ethiopia",
        "latitude": 14.24,
        "longitude": 40.30,
        "elevation_m": -125,
        "climate_zone": "Hyper-arid hyper-thermal depression",
        "geology_type": "Volcanic basalt, hyper-acidic brine pools (pH < 1), hydro-saline evaporite chimneys, iron oxy-hydroxides",
        "analog_for": ["Mars early hydrothermal & acidic chemistry"],
        "is_calibration_site": False,
        "summary": "Poly-extreme depression below sea level featuring boiling acidic springs, iron precipitates, and hyper-saline salt formations.",
        "scientific_justification": (
            "Dallol represents an intersection of extreme heat (>45°C ambient), extreme acidity (pH ~0), and high salinity. "
            "Its bright yellow and red iron oxy-hydroxide chimneys match early Martian hydrothermal and acidic sulfate deposits, "
            "offering an unmatched geochemical stress test for instrument durability and biosignature detection."
        ),
        "primary_missions": ["Europlanet Danakil Planetary Analogue", "Acid-resistant materials validation", "Biosignature limit testing"]
    },
    "Namib Desert (Sossusvlei & Skeleton Coast)": {
        "full_name": "Namib Sand Sea & Skeleton Coast",
        "country": "Namibia",
        "latitude": -24.75,
        "longitude": 15.28,
        "elevation_m": 550,
        "climate_zone": "Hyper-arid coastal fog desert",
        "geology_type": "Linear and star dunes, hematite-coated quartz sands, salt pans, rocky deflation plains",
        "analog_for": ["Mars sand seas (ergs) & dune slipface mobility"],
        "is_calibration_site": False,
        "summary": "Ancient hyperarid sand sea where oxidized, iron-oxide coated red sands form towering dunes mimicking Martian sand seas.",
        "scientific_justification": (
            "The vivid orange-red color of Namib sands is caused by thin coatings of iron oxide (hematite) on quartz grains, "
            "a near-perfect visual and physical proxy for Martian dune fields (such as Bagnold Dunes). Crucial for testing "
            "rover wheel sinkage (slip ratio) on steep slipfaces."
        ),
        "primary_missions": ["Sand dune slope mobility testing", "Wind-blown particle abrasion studies", "Hyperarid soil ecology"]
    },
    "Rio Tinto": {
        "full_name": "Rio Tinto Acidic River Basin",
        "country": "Spain (Andalusia)",
        "latitude": 37.69,
        "longitude": -6.55,
        "elevation_m": 320,
        "climate_zone": "Mediterranean warm temperate",
        "geology_type": "Massive sulfide gossans, jarosite, goethite, hematite precipitate sediments",
        "analog_for": ["Mars Meridiani Planum geochemistry"],
        "is_calibration_site": False,
        "summary": "Intensely red acidic river system with high concentrations of dissolved ferric iron, jarosite, and sulfate minerals.",
        "scientific_justification": (
            "When the Opportunity rover discovered jarosite at Meridiani Planum, it confirmed Rio Tinto as a prime "
            "geochemical analog. The oxidation of iron sulfides produces an acidic, metal-rich environment where chemolithotrophic "
            "microbes thrive, providing a living model for past Martian groundwater chemistry."
        ),
        "primary_missions": ["MARTE (Mars Analog Research and Technology Experiment)", "Borehole robotic drill tests", "Spectroscopy ground-truthing"]
    },
    "Sudbury Impact Basin": {
        "full_name": "Sudbury Impact Structure, Ontario",
        "country": "Canada",
        "latitude": 46.60,
        "longitude": -81.20,
        "elevation_m": 310,
        "climate_zone": "Boreal continental",
        "geology_type": "Paleoproterozoic 1.85 Ga complex impact crater, shatter cones, fallback breccia (Onaping formation)",
        "analog_for": ["Moon impact crater geology & impactite sampling"],
        "is_calibration_site": False,
        "summary": "Ancient 1.85 billion-year-old giant impact crater exhibiting prominent shatter cones and impact melt sheets.",
        "scientific_justification": (
            "Apollo astronauts (including Apollo 16 and 17 crews) trained at Sudbury to learn how to identify shatter cones "
            "and impact breccia in the field. Provides textbook examples of shocked minerals, melt sheets, and impact-induced "
            "hydrothermal systems analogous to lunar highlands impact basins."
        ),
        "primary_missions": ["Apollo astronaut impact geology training", "Impact melt sheet sampling protocols", "Shocked quartz identification"]
    },
    "Pilbara Craton": {
        "full_name": "Pilbara Craton & North Pole Dome",
        "country": "Australia (Western Australia)",
        "latitude": -21.28,
        "longitude": 119.75,
        "elevation_m": 420,
        "climate_zone": "Arid sub-tropical outback",
        "geology_type": "3.5 Ga Archaean basaltic greenstone, fossilized stromatolites, banded iron formations (BIF), barite",
        "analog_for": ["Mars early astrobiology & Noachian crust"],
        "is_calibration_site": False,
        "summary": "Ancient 3.5-billion-year-old Archaean rock formation preserving Earth's earliest fossil life; premier analog for ancient habitable Mars.",
        "scientific_justification": (
            "NASA and ESA astrobiology leadership have conducted joint field campaigns in the Pilbara (Dresser Formation) "
            "to study the co-occurrence of early microbial biosignatures with hydrothermal silica deposits. These rocks are the "
            "closest earthly physical and temporal analog to Noachian-age Martian crust in Jezero Crater and Columbia Hills."
        ),
        "primary_missions": ["NASA/ESA Astrobiology Field Expedition", "Perseverance SHERLOC / PIXL ground-truthing", "Stromatolite Raman spectroscopy"]
    },
    "Wadi Rum": {
        "full_name": "Wadi Rum Protected Area ('Valley of the Moon')",
        "country": "Jordan",
        "latitude": 29.57,
        "longitude": 35.42,
        "elevation_m": 950,
        "climate_zone": "Hyper-arid desert plateau",
        "geology_type": "Dissected Paleozoic red sandstone, granite basement inselbergs, iron-oxide dunes, dry canyons",
        "analog_for": ["Mars rover autonomous navigation & desert canyons", "Moon topographic canyon mobility"],
        "is_calibration_site": False,
        "summary": "Vast hyperarid valley with vertical sandstone monoliths and fine red quartz sands, frequently used for robotic rover field tests.",
        "scientific_justification": (
            "Known as the 'Valley of the Moon' for its barren, dramatic topography. The European Space Agency (ESA) "
            "and Austrian Space Forum (OeWF) have conducted rover autonomy trials and Mars spacesuit simulations in Wadi Rum "
            "due to its complex obstacle geometry, steep slope slipfaces, and dry, high-friction sandstone substrates."
        ),
        "primary_missions": ["ESA Rover Autonomy Navigation Trials", "OeWF Mars Field Simulations", "Optical terrain-relative navigation testing"]
    }
}

# Ground Truth Measurements and Physical Observations per Site
SITE_PHYSICAL_MEASUREMENTS: Dict[str, Dict[str, str]] = {
    "mcmurdo": {
        "Extreme cold and temperature range": "Mean annual: -20°C; winter lows down to -50°C; wind chill -65°C",
        "Aridity / low humidity": "<10 mm/yr precipitation; relative humidity <0.1%; zero liquid surface water",
        "High radiation / UV": "Solar UV Index 6-8 (summer peak); enhanced seasonal UV during Antarctic ozone thinning",
        "Rocky / regolith-like surface": "Ferrar dolerite and sandstone scree, abrasive wind-scoured regolith, ventifacts",
        "Topographic complexity": "Slopes 15°–35°, steep valley walls, glacial moraines, frost-cracked polygons",
        "Isolation": "Over 1,500 km to civilian settlements; total winter freeze-in lockdown",
        "Polar / high-latitude conditions": "77.5°S latitude; 4 months continuous polar night, 4 months continuous daylight",
        "Accessibility for testing": "Military ski-equipped aircraft (LC-130 / C-17) only; strict Antarctic treaty permits",
        # Mars criteria
        "Extreme aridity": "Hyper-arid desiccated polar desert; sublimating ice only",
        "Oxidized / iron-rich soils": "Localized ferric oxidation (Blood Falls iron outflow), iron-varnished sandstones",
        "Dust / fine particles": "Aeolian silts, frost-shattered rock flour, windblown sand grains",
        "Temperature extremes": "Sustained -50°C to -10°C; extreme cryogenic thermal cycling",
        "Volcanic / basaltic terrain": "Ferrar dolerite sills and basaltic dykes; McMurdo Volcanic Group nearby",
        "Impact features / craters": "Glacial cirques and valley troughs; lacks genuine meteorite impact morphology",
        "Salt / perchlorate-like chemistry": "Don Juan Pond calcium chloride brine; sulfate and halite crusts",
        "Isolation and logistics": "Expedition logistics; requires deep-field polar field camp infrastructure"
    },
    "haughton": {
        "Extreme cold and temperature range": "Winter lows -45°C; brief summer thaw (0°C to 5°C); permafrost active layer",
        "Aridity / low humidity": "High Arctic polar desert; ~100 mm/yr water equivalent precipitation",
        "High radiation / UV": "Solar UV Index 3-5; low sun elevation angle",
        "Rocky / regolith-like surface": "Shatter cones, shocked dolomite impact breccia, hydrothermal paleovent deposits",
        "Topographic complexity": "23 km impact rim, 150m crater walls, incised meltwater gullies",
        "Isolation": "Devon Island is largest uninhabited island on Earth; no permanent roads or settlements",
        "Polar / high-latitude conditions": "75.4°N latitude; 24h continuous sunlight (summer), continuous polar night (winter)",
        "Accessibility for testing": "Unpaved dirt airstrip; chartered Twin Otter bush flights from Resolute Bay",
        # Mars criteria
        "Extreme aridity": "Desiccated polar ground with subterranean permafrost ice",
        "Oxidized / iron-rich soils": "Hydrothermal gossans, oxidized paleosols, iron-stained dolomites",
        "Dust / fine particles": "Fine periglacial rock flour and silt deposits",
        "Temperature extremes": "-45°C winter to +8°C summer diurnal flux",
        "Volcanic / basaltic terrain": "Sedimentary carbonate target rock with regional mafic dyke swarms",
        "Impact features / craters": "23-km complex meteorite impact crater, central uplift, polymict breccia",
        "Salt / perchlorate-like chemistry": "Hydrothermal sulfate deposits, gypsum veins, saline springs",
        "Isolation and logistics": "NASA HMP research station; seasonal summer expedition logistics only"
    },
    "atacama": {
        "Extreme cold and temperature range": "Night temps -5°C; daytime +25°C; diurnal range ~30°C",
        "Aridity / low humidity": "<1 mm/yr rainfall for >2 million years; core hyperarid desiccated soil",
        "High radiation / UV": "UV Index >15; highest natural solar irradiance on Earth (>1,200 W/m²)",
        "Rocky / regolith-like surface": "Nitrate/gypsum crust, desert pavement, volcanic pebbles, oxidized sand",
        "Topographic complexity": "Cordillera de la Sal ridges, alluvial fans, slope gradients 10°–25°",
        "Isolation": "Remote desert interior; uninhabited salt flats and volcanic aprons",
        "Polar / high-latitude conditions": "24.1°S subtropical; normal diurnal solar transit (lacks polar lighting)",
        "Accessibility for testing": "Paved Pan-American highway, 2h drive from Antofagasta airport",
        # Mars criteria
        "Extreme aridity": "Globally recognized gold standard for Martian hyper-aridity",
        "Oxidized / iron-rich soils": "Widespread hematite, goethite coatings, high reactive oxidants (H₂O₂ proxies)",
        "Dust / fine particles": "Fine desert dust, salt aerosol, windblown silts",
        "Temperature extremes": "30°C daily diurnal thermal fluctuation",
        "Volcanic / basaltic terrain": "Andean ignimbrites, andesitic/basaltic volcanic flows",
        "Impact features / craters": "Monturaqui impact crater (350m dia) within driving distance",
        "Salt / perchlorate-like chemistry": "Natural perchlorates (0.1–0.6 wt%), nitrates, and sulfates identical to Phoenix assays",
        "Isolation and logistics": "Excellent logistics with rapid emergency medical evacuation capability"
    },
    "maunakea": {
        "Extreme cold and temperature range": "Night freezing (-2°C to 4°C); day +15°C; subalpine diurnal cycle",
        "Aridity / low humidity": "Above trade-wind cloud inversion layer; humidity ~10–20%",
        "High radiation / UV": "Elevation 2,500m–4,200m; high solar UV Index (10–12)",
        "Rocky / regolith-like surface": "Weathered basaltic cinder, tephra, volcanic ash (lunar mare simulant base)",
        "Topographic complexity": "Steep cinder cones (20°–35°), blocky aa lava fields, lava tube caverns",
        "Isolation": "Restricted military and telescope reserve; simulated habitat isolation (HI-SEAS)",
        "Polar / high-latitude conditions": "19.8°N tropical latitude; normal high-elevation solar elevation",
        "Accessibility for testing": "Paved Daniel K. Inouye Highway; 45 min drive to Hilo International Airport",
        # Mars criteria
        "Extreme aridity": "Dry alpine mountain environment above the inversion layer",
        "Oxidized / iron-rich soils": "Weathered palagonite tephra, basaltic clays, ferric oxides",
        "Dust / fine particles": "Fine particulate basaltic dust matching JSC-Mars-1 simulant source",
        "Temperature extremes": "Mild diurnal swings (-2°C to 18°C)",
        "Volcanic / basaltic terrain": "Archetypal basaltic shield volcano, pahoehoe, aa lava, intact lava tube caves",
        "Impact features / craters": "Volcanic pit craters and cinder cones; no meteorite impact structures",
        "Salt / perchlorate-like chemistry": "Trace volcanic sublimates and secondary sulfate minerals",
        "Isolation and logistics": "Established research infrastructure, power, emergency access"
    },
    "askja": {
        "Extreme cold and temperature range": "Sub-polar alpine; winter -20°C, summer +5°C; freeze-thaw weathering",
        "Aridity / low humidity": "Rain shadow of Vatnajökull ice cap; arid volcanic pumice desert",
        "High radiation / UV": "Moderate UV Index 4–6; high latitude cloud cover",
        "Rocky / regolith-like surface": "Holuhraun fresh basaltic lava fields, jagged aa lava, pumice tephra",
        "Topographic complexity": "Caldera collapse scarps, crater explosion pits, rugged lava flow ridges",
        "Isolation": "Highland interior; unpopulated volcanic desert, impassable in winter",
        "Polar / high-latitude conditions": "65.0°N sub-arctic; low summer sun angles, extended twilight",
        "Accessibility for testing": "Seasonal 4WD gravel mountain tracks (F-roads); unbridged river crossings",
        # Mars criteria
        "Extreme aridity": "Volcanic rain-shadow desert, dry volcanic sands",
        "Oxidized / iron-rich soils": "Basaltic glass, palagonitized tephra, iron-rich tholeiitic sands",
        "Dust / fine particles": "Fine airborne volcanic ash, pumice powder",
        "Temperature extremes": "Sub-zero winters, active freeze-thaw cycles",
        "Volcanic / basaltic terrain": "Massive recent flood basalt (Holuhraun 2014-15), nested calderas",
        "Impact features / craters": "Volcanic explosion craters mimicking secondary impact morphologies",
        "Salt / perchlorate-like chemistry": "Fumarolic sulfur sublimates and hydrothermal alterations",
        "Isolation and logistics": "Rugged highland expedition logistics; seasonal summer testing only"
    },
    "concordia": {
        "Extreme cold and temperature range": "Winter lows plunge below -80°C; summer highs -25°C; cryogenic deep-freeze",
        "Aridity / low humidity": "Annual water equivalent <2 mm; absolute vapor pressure near zero",
        "High radiation / UV": "Elevation 3,233m; intense solar UV during 24h daylight summer",
        "Rocky / regolith-like surface": "Pure glacial ice and compacted firn snow; lacks exposed mineral rock",
        "Topographic complexity": "Extremely flat continental ice dome plateau (<0.5° slope)",
        "Isolation": "Most physically isolated habitat on Earth; 9 months zero-access winterover",
        "Polar / high-latitude conditions": "75.1°S latitude; 100 consecutive days of total polar night",
        "Accessibility for testing": "Ski-equipped Twin Otter or Basler BT-67 flights from coastal stations",
        # Mars criteria
        "Extreme aridity": "Cryogenic hyper-arid air column; moisture frozen out",
        "Oxidized / iron-rich soils": "Snow cover only; zero exposed mineral soils",
        "Dust / fine particles": "Cleanest air on Earth; lacks abrasive particulate dust",
        "Temperature extremes": "Extreme deep-freeze (-80°C) matching Martian winter polar caps",
        "Volcanic / basaltic terrain": "3,000 meters of ice overlying bedrock; no volcanic exposures",
        "Impact features / craters": "Featureless polar ice sheet",
        "Salt / perchlorate-like chemistry": "Trace atmospheric nitrates in snow cores",
        "Isolation and logistics": "Premier ESA human isolation testbed for deep-space mission crews"
    },
    "danakil": {
        "Extreme cold and temperature range": "Hottest inhabited place on Earth; temps consistently >45°C; poor cold match",
        "Aridity / low humidity": "Hyper-arid Rift depression; annual rainfall <50 mm",
        "High radiation / UV": "Intense tropical solar insolation; UV Index >12",
        "Rocky / regolith-like surface": "Hydrothermal salt chimneys, evaporite halite crusts, volcanic basalt",
        "Topographic complexity": "Rift valley scarps, volcanic fissure vents, Dallol uplifted salt dome",
        "Isolation": "Remote Afar Depression; harsh geopolitical and climatic environment",
        "Polar / high-latitude conditions": "14.2°N tropical latitude; direct overhead solar transit",
        "Accessibility for testing": "4WD desert expedition with armed convoy security",
        # Mars criteria
        "Extreme aridity": "Dessicated depression, ambient temp >45°C",
        "Oxidized / iron-rich soils": "Bright yellow and red iron oxy-hydroxides, hematite, ferric sulfate brines",
        "Dust / fine particles": "Fine salt dust, volcanic ash plumes",
        "Temperature extremes": "Extreme heat and wide daily thermal stress",
        "Volcanic / basaltic terrain": "Erta Ale active shield volcano, basaltic lava lakes, volcanic fissures",
        "Impact features / craters": "Volcanic phreatic explosion craters",
        "Salt / perchlorate-like chemistry": "Hyperacidic brine pools (pH ~0), magnesium and sodium salts",
        "Isolation and logistics": "Extreme logistics; harsh poly-extreme field testing campaign"
    },
    "pilbara": {
        "Extreme cold and temperature range": "Sub-tropical desert; summer >45°C, winter night lows down to 4°C",
        "Aridity / low humidity": "Annual rainfall <250 mm; high evaporation rate (>3,000 mm/yr)",
        "High radiation / UV": "High solar UV Index (11–14) across vast open outback",
        "Rocky / regolith-like surface": "Silicified cherts, banded iron formations, jagged rock pavements",
        "Topographic complexity": "Dissected plateaus, gorge walls, stony scree slopes (10°–25°)",
        "Isolation": "Remote Australian outback; hundreds of kilometers from major centers",
        "Polar / high-latitude conditions": "21.3°S sub-tropical; no polar day/night lighting cycles",
        "Accessibility for testing": "Mining haul roads and regional regional airstrips (Newman / Port Hedland)",
        # Mars criteria
        "Extreme aridity": "Hyperarid interior outback environment",
        "Oxidized / iron-rich soils": "3.5 Ga Banded Iron Formations (BIF), hematite, deep red oxidized crust",
        "Dust / fine particles": "Pervasive red dust, fine silica and iron oxide particulates",
        "Temperature extremes": "Wide outback diurnal swings (5°C to 45°C)",
        "Volcanic / basaltic terrain": "Ancient Archaean basaltic greenstones, komatiite lavas",
        "Impact features / craters": "Ancient bedrock fracture systems and regional impact structures",
        "Salt / perchlorate-like chemistry": "Hydrothermal barite, sulfate paleolakes, evaporite cherts",
        "Isolation and logistics": "Autonomous rover traverse testing with delayed comms simulation"
    },
    "wadirum": {
        "Extreme cold and temperature range": "Winter lows down to 0°C; summer highs +40°C; desert diurnal swings",
        "Aridity / low humidity": "<50 mm/yr precipitation; dry desert air column",
        "High radiation / UV": "High desert solar UV Index (10–12)",
        "Rocky / regolith-like surface": "Sandstone scree, fractured granite boulders, red sand plains",
        "Topographic complexity": "Towering vertical inselbergs (up to 1,750m), narrow desert gorges, steep talus",
        "Isolation": "Protected wilderness area; uninhabited sandstone labyrinths",
        "Polar / high-latitude conditions": "29.6°N latitude; standard desert sun angles",
        "Accessibility for testing": "Paved highway from Aqaba (1h drive) and King Hussein Airport",
        # Mars criteria
        "Extreme aridity": "Desiccated desert valley, minimal vegetation",
        "Oxidized / iron-rich soils": "Iron-oxide stained red sandstones, red quartz sands",
        "Dust / fine particles": "Fine aeolian red dust, windblown quartz particles",
        "Temperature extremes": "Daily temperature swings of ~25°C",
        "Volcanic / basaltic terrain": "Granitic basement with regional basaltic dyke intrusions",
        "Impact features / craters": "Wind-sculpted amphitheaters and canyon walls",
        "Salt / perchlorate-like chemistry": "Alkali playa flats, carbonate/sulfate coatings",
        "Isolation and logistics": "ESA / OeWF test site with immediate field support vehicle logistics"
    },
    "svalbard": {
        "Extreme cold and temperature range": "Mean annual about -4°C at Ny-Ålesund; winter lows near -30°C; continuous permafrost",
        "Aridity / low humidity": "Arctic semi-desert; roughly 200–450 mm/yr precipitation, mostly snow",
        "High radiation / UV": "Low sun elevation; summer UV Index 2–4",
        "Rocky / regolith-like surface": "Frost-shattered scree, patterned ground, basaltic volcanic rubble at Bockfjorden",
        "Topographic complexity": "Glacially carved fjord walls and alpine ridges rising to ~1,700 m",
        "Isolation": "Archipelago of ~2,500 residents, about 1,000 km from mainland Norway",
        "Polar / high-latitude conditions": "78.9°N latitude; ~4 months polar night and ~4 months midnight sun",
        "Accessibility for testing": "Scheduled flights to Longyearbyen; field sites reached by boat, helicopter or snowmobile",
        # Mars criteria
        "Extreme aridity": "Cold polar semi-desert; dry by Arctic standards but far wetter than Mars",
        "Oxidized / iron-rich soils": "Devonian Old Red Sandstone and iron-stained weathering crusts",
        "Dust / fine particles": "Glacial rock flour and periglacial silts; limited airborne dust",
        "Temperature extremes": "About -30°C in winter to +8°C in summer",
        "Volcanic / basaltic terrain": "Quaternary Sverrefjellet volcano and basaltic lavas of the Bockfjorden Volcanic Complex",
        "Impact features / craters": "No confirmed impact structure on land; glacial landforms only",
        "Salt / perchlorate-like chemistry": "Carbonate globules similar to those in ALH84001; Troll thermal spring deposits",
        "Isolation and logistics": "Ship- or helicopter-supported summer campaigns (AMASE) from Longyearbyen and Ny-Ålesund"
    },
    "pisgah": {
        "Extreme cold and temperature range": "Summer highs above 40°C; winter nights near 0°C; no sustained cold",
        "Aridity / low humidity": "Mojave Desert; roughly 100–130 mm/yr rainfall",
        "High radiation / UV": "Clear desert sky; summer UV Index 10–11",
        "Rocky / regolith-like surface": "Young basaltic lava flows (pahoehoe and aa), cinders and lava tubes",
        "Topographic complexity": "~100 m cinder cone, rough flow margins, collapsed tubes and pressure ridges",
        "Isolation": "Open desert a few km from Interstate 40; about 60 km east of Barstow",
        "Polar / high-latitude conditions": "34.8°N latitude; ordinary mid-latitude sun angles",
        "Accessibility for testing": "Paved highway plus short graded road; 2–3 h drive from Los Angeles",
        # Mars criteria
        "Extreme aridity": "Arid, not hyper-arid; roughly 100–130 mm/yr rainfall",
        "Oxidized / iron-rich soils": "Oxidized red cinders and weathered basalt; source region of Mojave Mars Simulant",
        "Dust / fine particles": "Playa silt and windblown sand; regular dust devils on nearby dry lakes",
        "Temperature extremes": "Diurnal swings of 15–20°C; seasonal range about 0°C to 45°C",
        "Volcanic / basaltic terrain": "Alkali basalt cinder cone with lava flows extending several km",
        "Impact features / craters": "Volcanic crater only; no impact structure",
        "Salt / perchlorate-like chemistry": "Evaporite playas nearby (Lavic and Bristol dry lakes) with chlorides and sulfates",
        "Isolation and logistics": "Excellent road logistics; low isolation"
    },
    "teide": {
        "Extreme cold and temperature range": "Mean annual about 10°C at 2,400 m; winter nights down to -10°C with frost and snow",
        "Aridity / low humidity": "Above the trade-wind inversion; roughly 350–450 mm/yr; humidity often below 30%",
        "High radiation / UV": "Caldera floor at ~2,100 m; summer UV Index 11–13",
        "Rocky / regolith-like surface": "Blocky basaltic to phonolitic lava flows, pumice fields and lapilli plains",
        "Topographic complexity": "16 km caldera with walls up to ~600 m; Teide summit at 3,715 m",
        "Isolation": "National park with no permanent settlement in the caldera; towns within 30 km",
        "Polar / high-latitude conditions": "28.3°N latitude; subtropical sun angles",
        "Accessibility for testing": "Paved roads into the caldera; about 1 h from two international airports",
        # Mars criteria
        "Extreme aridity": "Dry high-mountain desert; roughly 350–450 mm/yr, mostly in winter",
        "Oxidized / iron-rich soils": "Oxidized red scoria and hydrothermally altered deposits (Los Azulejos)",
        "Dust / fine particles": "Pumice lapilli and volcanic ash; periodic Saharan dust intrusions",
        "Temperature extremes": "Daily range of 10–15°C; frost through winter",
        "Volcanic / basaltic terrain": "Stratovolcano complex with basanite to phonolite lavas and historic eruptions",
        "Impact features / craters": "Volcanic collapse caldera; no impact structure",
        "Salt / perchlorate-like chemistry": "Fumarolic sulfur and sulfate deposits near the summit; limited evaporites",
        "Isolation and logistics": "Strong logistics; used for ESA and DLR rover field trials"
    },
    "qaidam": {
        "Extreme cold and temperature range": "Mean annual about 2–4°C; winter lows near -30°C; daily swings of 15–25°C",
        "Aridity / low humidity": "Western basin under 50 mm/yr (about 20 mm at Lenghu); evaporation over 2,500 mm/yr",
        "High radiation / UV": "Plateau basin at 2,800–3,200 m; summer UV Index 11+",
        "Rocky / regolith-like surface": "Wind-eroded yardangs, salt-cemented crusts and gravel desert (gobi)",
        "Topographic complexity": "Yardang fields with ridges tens of metres high; polygonal salt terrain; alluvial fans",
        "Isolation": "Sparsely populated plateau basin; nearest airport roughly 250 km away",
        "Polar / high-latitude conditions": "37.9°N latitude; mid-latitude sun angles",
        "Accessibility for testing": "National highways cross the basin; long overland drives to field sites",
        # Mars criteria
        "Extreme aridity": "Hyper-arid core; aridity index below 0.05 in the western basin",
        "Oxidized / iron-rich soils": "Red Neogene mudstones and iron-oxide-bearing playa sediments",
        "Dust / fine particles": "Major Asian dust source; frequent dust storms and active yardang abrasion",
        "Temperature extremes": "About -30°C to +35°C annual range; large daily swings",
        "Volcanic / basaltic terrain": "Sedimentary basin; essentially no young volcanic terrain",
        "Impact features / craters": "No confirmed impact structure; wind-eroded pits only",
        "Salt / perchlorate-like chemistry": "Thick halite, gypsum and Mg-sulfate deposits; natural perchlorate detected in soils",
        "Isolation and logistics": "Remote but road-accessible; Mars simulation base operating at Lenghu"
    },
    "namib": {
        "Extreme cold and temperature range": "Coastal 10–20°C year-round; inland summer highs above 40°C, winter nights near 0°C",
        "Aridity / low humidity": "Under 25 mm/yr at the coast, up to ~100 mm inland; coastal fog is the main moisture source",
        "High radiation / UV": "Clear inland skies; summer UV Index 11–13",
        "Rocky / regolith-like surface": "Quartz dune sand, gravel plains and gypsum crusts; limited bedrock exposure",
        "Topographic complexity": "Linear and star dunes up to ~300 m; granite inselbergs; Kuiseb canyon",
        "Isolation": "Protected dune sea with almost no settlement; Gobabeb research station inside the park",
        "Polar / high-latitude conditions": "24.8°S latitude; subtropical sun angles",
        "Accessibility for testing": "Gravel roads from Walvis Bay and Windhoek (4–5 h); deep sand needs 4WD",
        # Mars criteria
        "Extreme aridity": "Hyper-arid coastal desert, among the oldest on Earth",
        "Oxidized / iron-rich soils": "Dune sands coated with iron oxide (hematite), reddening inland",
        "Dust / fine particles": "Active saltating sand and dust plumes during easterly 'berg' winds",
        "Temperature extremes": "Moderate at the coast; 20–25°C daily swings inland",
        "Volcanic / basaltic terrain": "Little volcanic terrain in the dune sea; Etendeka flood basalts lie far to the north",
        "Impact features / craters": "Roter Kamm impact crater (2.5 km) in the southern Namib",
        "Salt / perchlorate-like chemistry": "Gypsum and halite crusts fed by fog and coastal salt pans",
        "Isolation and logistics": "Gobabeb supports field campaigns; long gravel-road supply lines"
    },
    "riotinto": {
        "Extreme aridity": "Mediterranean climate; roughly 600–700 mm/yr rainfall, so a poor aridity match",
        "Oxidized / iron-rich soils": "Acidic river (pH ~2.3) carrying several g/L of dissolved iron; goethite and hematite terraces",
        "Dust / fine particles": "Fine mine tailings and ochre sediments; little natural airborne dust",
        "Temperature extremes": "Mild winters (about 5°C) and hot summers (35–40°C); no deep cold",
        "Volcanic / basaltic terrain": "Iberian Pyrite Belt volcano-sedimentary massive sulfides; not basaltic plains",
        "Impact features / craters": "No impact structure; open-pit mines only",
        "Salt / perchlorate-like chemistry": "Jarosite, schwertmannite and seasonal iron-sulfate efflorescences, as at Meridiani Planum",
        "Isolation and logistics": "About 1 h by road from Huelva and Seville; low isolation"
    },
    "sudbury": {
        "Extreme cold and temperature range": "January mean about -13°C with lows near -30°C; warm summers (~25°C)",
        "Aridity / low humidity": "Humid continental climate; roughly 900 mm/yr precipitation",
        "High radiation / UV": "Low elevation (~300 m); summer UV Index 7–8",
        "Rocky / regolith-like surface": "Shatter cones, Sudbury Breccia and Onaping Formation impact breccia; glacially scoured outcrop",
        "Topographic complexity": "Eroded elliptical basin (~60 × 30 km) with low rocky ridges; modest relief",
        "Isolation": "City of about 165,000 inside the basin; minimal isolation",
        "Polar / high-latitude conditions": "46.6°N latitude; snow cover 4–5 months but ordinary sun angles",
        "Accessibility for testing": "Trans-Canada Highway, regional airport and rail; outcrops beside roads",
        # Mars criteria
        "Extreme aridity": "Humid, vegetated and lake-rich; a poor aridity match",
        "Oxidized / iron-rich soils": "Gossans and oxidized nickel–copper sulfide ores along the Sudbury Igneous Complex",
        "Dust / fine particles": "Vegetated terrain; little natural dust",
        "Temperature extremes": "About -30°C in winter to +30°C in summer",
        "Volcanic / basaltic terrain": "Impact melt sheet (norite to granophyre) rather than volcanic basalt",
        "Impact features / craters": "1.85-billion-year-old impact structure, originally ~200 km across; Apollo 16 and 17 crews trained here",
        "Salt / perchlorate-like chemistry": "No significant evaporites or perchlorate",
        "Isolation and logistics": "Excellent logistics; mining-city infrastructure"
    }
}
