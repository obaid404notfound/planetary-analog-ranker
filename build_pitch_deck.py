"""
Generate SubZero 7-Slide Pitch Deck for NASA Space Apps Challenge 2026.
Creates SubZero_NASA_Pitch_Deck.pptx strictly adhering to NASA's 7-slide rule.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme colors
    BG_COLOR = RGBColor(11, 19, 43)        # #0B132B Dark Navy Space
    CARD_BG = RGBColor(18, 28, 52)         # #121C34 Dark Card
    CARD_BORDER = RGBColor(34, 52, 88)     # #223458 Slate Border
    ACCENT_BLUE = RGBColor(10, 132, 255)   # #0A84FF Electric Blue
    ACCENT_CYAN = RGBColor(0, 245, 212)    # #00F5D4 Cyan / Mint
    ACCENT_ORANGE = RGBColor(255, 90, 31)  # #FF5A1F Mars Orange
    TEXT_TITLE = RGBColor(245, 245, 247)   # Crisp White
    TEXT_MUTED = RGBColor(150, 165, 185)   # Muted Blue-Gray
    TEXT_BODY = RGBColor(220, 226, 238)    # Body text soft white

    app_dir = os.path.dirname(os.path.abspath(__file__))
    patch_path = os.path.join(app_dir, "assets", "mission_patch.jpg")
    screenshot_path = os.path.join(app_dir, "assets", "dashboard_screenshot.jpg")

    def add_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, tag_text, title_text, subtitle_text=""):
        # Category Tag
        tag_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.45), Inches(11.5), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = ACCENT_CYAN

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.8), Inches(11.5), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(27)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_TITLE

        # Subtitle
        if subtitle_text:
            sub_box = slide.shapes.add_textbox(Inches(0.9), Inches(1.45), Inches(11.5), Inches(0.35))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle_text
            p_sub.font.size = Pt(13)
            p_sub.font.color.rgb = TEXT_MUTED

    def add_footer(slide, current_idx, total=7):
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(6.85), Inches(11.533), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(25, 38, 65)
        line.line.fill.background()

        f_box = slide.shapes.add_textbox(Inches(0.9), Inches(6.95), Inches(8), Inches(0.35))
        tf_f = f_box.text_frame
        tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
        p_f = tf_f.paragraphs[0]
        p_f.text = "SubZero  |  NASA Space Apps Challenge 2026"
        p_f.font.size = Pt(10)
        p_f.font.color.rgb = TEXT_MUTED

        r_box = slide.shapes.add_textbox(Inches(10.0), Inches(6.95), Inches(2.433), Inches(0.35))
        tf_r = r_box.text_frame
        tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
        p_r = tf_r.paragraphs[0]
        p_r.alignment = PP_ALIGN.RIGHT
        p_r.text = f"Slide {current_idx} of {total}"
        p_r.font.size = Pt(10)
        p_r.font.bold = True
        p_r.font.color.rgb = ACCENT_BLUE

    def add_card(slide, left, top, width, height, bg=CARD_BG, border=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = border
        card.line.width = Pt(1)
        return card

    # =========================================================
    # SLIDE 1: TITLE & TEAM
    # =========================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1)

    # Patch Card on Left
    s1_patch_card = add_card(s1, Inches(1.0), Inches(1.3), Inches(4.5), Inches(5.0))
    if os.path.exists(patch_path):
        s1.shapes.add_picture(patch_path, Inches(1.35), Inches(1.65), Inches(3.8), Inches(3.8))
        caption_box = s1.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(4.5), Inches(0.4))
        p = caption_box.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = "OFFICIAL PROJECT MISSION INSIGNIA"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN

    # Title & Metadata on Right
    s1_text_card = add_card(s1, Inches(5.8), Inches(1.3), Inches(6.533), Inches(5.0))

    t_box = s1.shapes.add_textbox(Inches(6.15), Inches(1.55), Inches(5.8), Inches(4.5))
    tf = t_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p0 = tf.paragraphs[0]
    p0.text = "NASA SPACE APPS CHALLENGE 2026"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_CYAN

    p1 = tf.add_paragraph()
    p1.space_before = Pt(8)
    p1.text = "SUBZERO"
    p1.font.size = Pt(38)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_TITLE

    p2 = tf.add_paragraph()
    p2.text = "Planetary Analog Ranker & Portfolio Optimizer"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_BLUE

    p3 = tf.add_paragraph()
    p3.space_before = Pt(14)
    p3.text = "A scientific decision-support engine matching Earth testing terrains to Artemis Lunar South Pole & Mars surface environments."
    p3.font.size = Pt(13)
    p3.font.color.rgb = TEXT_BODY

    p4 = tf.add_paragraph()
    p4.space_before = Pt(20)
    p4.text = "TEAM INFORMATION & LINKS:"
    p4.font.size = Pt(10)
    p4.font.bold = True
    p4.font.color.rgb = ACCENT_CYAN

    p5 = tf.add_paragraph()
    p5.space_before = Pt(4)
    p5.text = "• Team Name: SubZero"
    p5.font.size = Pt(12)
    p5.font.color.rgb = TEXT_BODY

    p6 = tf.add_paragraph()
    p6.text = "• Live Application: https://subzero.streamlit.app/"
    p6.font.size = Pt(12)
    p6.font.color.rgb = ACCENT_CYAN

    p7 = tf.add_paragraph()
    p7.text = "• Open-Source Code: github.com/obaid404notfound/planetary-analog-ranker"
    p7.font.size = Pt(12)
    p7.font.color.rgb = TEXT_MUTED

    add_footer(s1, 1)

    # =========================================================
    # SLIDE 2: THE PROBLEM
    # =========================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "Challenge Context & Critical Bottleneck", "Why Planetary Analog Selection Fails Today",
               "Hardware failure on the Moon or Mars is catastrophic. Testing on Earth is essential, but flawed.")

    # 3 Comparison Columns
    col_w = Inches(3.64)
    card_y = Inches(1.95)
    card_h = Inches(3.4)

    # Col 1: Polar Deep Freeze
    add_card(s2, Inches(0.9), card_y, col_w, card_h)
    tb1 = s2.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(3.24), Inches(3.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0
    p = tf1.paragraphs[0]
    p.text = "POLAR DEEP-FREEZE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p_ex = tf1.add_paragraph()
    p_ex.text = "e.g., Concordia Station, McMurdo"
    p_ex.font.size = Pt(10)
    p_ex.font.color.rgb = TEXT_MUTED

    p = tf1.add_paragraph()
    p.space_before = Pt(10)
    p.text = "✓ Cryogenic cold (-80°C cold traps)\n✓ Low grazing polar illumination\n✓ Extreme isolation & crew confinement"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(120, 220, 160)

    p = tf1.add_paragraph()
    p.space_before = Pt(10)
    p.text = "✗ Missing basaltic rock & regolith\n✗ Missing volcanic lava tubes\n✗ Thick ice cover masks terrain"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(255, 130, 130)

    # Col 2: Volcanic Terrains
    add_card(s2, Inches(4.84), card_y, col_w, card_h)
    tb2 = s2.shapes.add_textbox(Inches(5.04), Inches(2.1), Inches(3.24), Inches(3.0))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
    p = tf2.paragraphs[0]
    p.text = "VOLCANIC BASALT"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE
    p_ex = tf2.add_paragraph()
    p_ex.text = "e.g., Askja (Iceland), Mauna Kea"
    p_ex.font.size = Pt(10)
    p_ex.font.color.rgb = TEXT_MUTED

    p = tf2.add_paragraph()
    p.space_before = Pt(10)
    p.text = "✓ Authentic basaltic mineral regolith\n✓ Underground lava tube caverns\n✓ Cratered rover mobility obstacles"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(120, 220, 160)

    p = tf2.add_paragraph()
    p.space_before = Pt(10)
    p.text = "✗ Above-freezing summer temperatures\n✗ High atmospheric humidity & rain\n✗ Standard 24-hr day/night cycle"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(255, 130, 130)

    # Col 3: Hyper-Arid Deserts
    add_card(s2, Inches(8.78), card_y, col_w, card_h)
    tb3 = s2.shapes.add_textbox(Inches(8.98), Inches(2.1), Inches(3.24), Inches(3.0))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_top = tf3.margin_right = tf3.margin_bottom = 0
    p = tf3.paragraphs[0]
    p.text = "HYPER-ARID DESERTS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p_ex = tf3.add_paragraph()
    p_ex.text = "e.g., Atacama Desert, Namib"
    p_ex.font.size = Pt(10)
    p_ex.font.color.rgb = TEXT_MUTED

    p = tf3.add_paragraph()
    p.space_before = Pt(10)
    p.text = "✓ Extreme aridity & zero precipitation\n✓ High UV radiation flux\n✓ Oxidized perchlorates & dust"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(120, 220, 160)

    p = tf3.add_paragraph()
    p.space_before = Pt(10)
    p.text = "✗ Zero cryogenic freeze conditions\n✗ Standard Earth gravitational pull\n✗ High daytime surface heat"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(255, 130, 130)

    # Summary Takeaway Banner
    add_card(s2, Inches(0.9), Inches(5.5), Inches(11.52), Inches(1.15))
    tb_bot = s2.shapes.add_textbox(Inches(1.15), Inches(5.6), Inches(11.0), Inches(0.95))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_top = tf_bot.margin_right = tf_bot.margin_bottom = 0
    p = tf_bot.paragraphs[0]
    p.text = "THE CORE BOTTLENECK:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    p = tf_bot.add_paragraph()
    p.text = "No single Earth site replicates all target environments. Missions have historically selected analog test sites based on subjective habit rather than empirical data—leaving dangerous hardware vulnerabilities undiscovered until launch."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_BODY

    add_footer(s2, 2)

    # =========================================================
    # SLIDE 3: OUR SOLUTION
    # =========================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "SubZero Solution & Software Platform", "Empirical Planetary Analog Evaluation Engine",
               "Transforms subjective expedition planning into a quantitative, multi-criteria decision pipeline.")

    # Left Column: Solution Highlights
    add_card(s3, Inches(0.9), Inches(1.95), Inches(5.1), Inches(4.7))
    tb_s3 = s3.shapes.add_textbox(Inches(1.15), Inches(2.15), Inches(4.6), Inches(4.3))
    tf_s3 = tb_s3.text_frame
    tf_s3.word_wrap = True
    tf_s3.margin_left = tf_s3.margin_top = tf_s3.margin_right = tf_s3.margin_bottom = 0

    features = [
        ("8 Multi-Criteria Dimensions", "Scores slope roughness, cryogenic cold, UV radiation, regolith chemistry, diurnal swing, pressure, aridity, and darkness.", ACCENT_CYAN),
        ("Submodular Portfolio Finder", "Greedy coverage optimization selects complementary 2–3 site teams to achieve 100% test requirements.", ACCENT_BLUE),
        ("Dirichlet Stability Verification", "Runs 1,000 Monte Carlo noise trials to prove site rankings withstand subjective weight shifts.", ACCENT_ORANGE),
        ("100% Open & Accessible", "Streamlit Cloud web app ingesting NASA satellite data with zero proprietary software dependencies.", RGBColor(120, 220, 160)),
    ]

    for i, (title, desc, color) in enumerate(features):
        p_t = tf_s3.paragraphs[0] if i == 0 else tf_s3.add_paragraph()
        if i > 0:
            p_t.space_before = Pt(12)
        p_t.text = f"▶  {title}"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = color

        p_d = tf_s3.add_paragraph()
        p_d.space_before = Pt(2)
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_BODY

    # Right Column: App Screenshot
    add_card(s3, Inches(6.25), Inches(1.95), Inches(6.18), Inches(4.7))
    if os.path.exists(screenshot_path):
        s3.shapes.add_picture(screenshot_path, Inches(6.4), Inches(2.1), Inches(5.88), Inches(3.95))
        cap_box = s3.shapes.add_textbox(Inches(6.4), Inches(6.15), Inches(5.88), Inches(0.35))
        p_c = cap_box.text_frame.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER
        p_c.text = "SubZero Live Dashboard: World Analog Map & Scientific Leaderboard"
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = ACCENT_CYAN

    add_footer(s3, 3)

    # =========================================================
    # SLIDE 4: HOW IT WORKS / USER EXPERIENCE
    # =========================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "Workflow & User Experience", "Four Steps From Target to Optimal Test Portfolio",
               "An intuitive decision workflow designed for flight mission planners, rover engineers, and scientists.")

    steps = [
        ("STEP 01", "Mission Setup",
         "Select target body (Moon South Pole vs. Mars) and choose operational mission presets (Rover Mobility, ISRU Drilling, or Human Habitat).",
         ACCENT_CYAN),
        ("STEP 02", "Empirical Ranking",
         "SubZero scores 15 global candidate sites using min-max normalized physical metrics, automatically detecting statistical ties within 2%.",
         ACCENT_BLUE),
        ("STEP 03", "Radar Profile Alignment",
         "Interactive side-by-side radar charts align Earth analog sites against measured planetary data (LRO Diviner, LOLA, Curiosity REMS).",
         ACCENT_ORANGE),
        ("STEP 04", "Portfolio Optimization",
         "Submodular greedy solver outputs the optimal 2–3 site pairing that eliminates test blindspots and spotlights remaining gaps.",
         RGBColor(120, 220, 160)),
    ]

    card_w = Inches(2.7)
    card_gap = Inches(0.24)
    start_x = Inches(0.9)

    for i, (num, heading, body, color) in enumerate(steps):
        cx = start_x + i * (card_w + card_gap)
        add_card(s4, cx, Inches(2.0), card_w, Inches(4.65))

        tb = s4.shapes.add_textbox(cx + Inches(0.18), Inches(2.2), card_w - Inches(0.36), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = num
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = color

        p = tf.add_paragraph()
        p.space_before = Pt(4)
        p.text = heading
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = TEXT_TITLE

        p = tf.add_paragraph()
        p.space_before = Pt(12)
        p.text = body
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_BODY

    add_footer(s4, 4)

    # =========================================================
    # SLIDE 5: NASA & SPACE AGENCY DATA USED
    # =========================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "Open Science Ingestion Pipeline", "Powered by Real NASA Earth & Planetary Data",
               "Ingests open space agency datasets—zero runtime API calls, reproducible offline data pipeline.")

    # 4 Data Cards in 2x2 Grid
    gw = Inches(5.64)
    gh = Inches(2.25)
    x1 = Inches(0.9)
    x2 = Inches(6.78)
    y1 = Inches(2.0)
    y2 = Inches(4.45)

    datasets = [
        (x1, y1, "NASA SRTM & ASTER GDEM", "Terrain Roughness & Elevation Variance",
         "Provides 30m digital elevation data across all candidate sites. SubZero calculates slope steepness and surface roughness to simulate rover trafficability on hazardous lunar/Martian regolith.", ACCENT_CYAN),
        (x2, y1, "NASA POWER & CERES Radiometry", "Solar Irradiance & UV Exposure",
         "Supplies satellite-derived surface solar flux and UV radiation index data. Evaluates photovoltaic power generation testing and spacesuit polymer photodegradation.", ACCENT_BLUE),
        (x1, y2, "NASA LRO (Diviner, LOLA, CRaTER)", "Artemis Lunar South Pole Baselines",
         "Calibrates planetary ground truth: -246°C cryogenic cold traps, low grazing polar illumination, and steep 12° Shackleton Crater crater rim topologies for Artemis landing simulation.", ACCENT_ORANGE),
        (x2, y2, "Curiosity REMS & MOLA Mars Data", "Martian Atmospheric & Thermal Swings",
         "Ingests Rover Environmental Monitoring Station diurnal temperature swings (90°C range), low surface atmospheric pressure, and Martian soil chemistry models.", RGBColor(120, 220, 160)),
    ]

    for (x, y, dname, dsub, ddesc, dcol) in datasets:
        add_card(s5, x, y, gw, gh)
        tb = s5.shapes.add_textbox(x + Inches(0.22), y + Inches(0.2), gw - Inches(0.44), gh - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = dname
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = dcol

        p = tf.add_paragraph()
        p.space_before = Pt(2)
        p.text = dsub
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_TITLE

        p = tf.add_paragraph()
        p.space_before = Pt(6)
        p.text = ddesc
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_BODY

    add_footer(s5, 5)

    # =========================================================
    # SLIDE 6: IMPACT & RELEVANCE
    # =========================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "Value to Spaceflight & Exploration", "De-Risking Human & Robotic Planetary Missions",
               "SubZero delivers immediate scientific and economic impact for agencies, commercial space, and academia.")

    col3_w = Inches(3.64)
    c3_y = Inches(2.0)
    c3_h = Inches(4.65)

    impacts = [
        ("MISSION SAFETY", "Preventing Catastrophic Failure",
         "Hardware tested against mismatched Earth terrain will fail on the Moon. SubZero guarantees that life-support systems, rovers, and spacesuits are tested against empirical extreme physics before launch.",
         "✓ Tested against authentic cryogenic cold\n✓ Validated against rover terrain hazards\n✓ Protects astronaut lives & payloads",
         ACCENT_CYAN),
        ("ECONOMIC ROI", "Saving Millions in Testing Budgets",
         "Field expeditions to Antarctica or the Arctic cost millions of dollars. SubZero's portfolio optimizer eliminates redundant expeditions and pinpoints minimal-cost site pairings.",
         "✓ Eliminates redundant expedition spend\n✓ 2-site portfolio achieves 88%+ coverage\n✓ Ingests accessibility & airport logistics",
         ACCENT_BLUE),
        ("OPEN SCIENCE", "Democratizing Mission Architecture",
         "Replaces closed, proprietary decision-making with transparent, reproducible open science accessible to emerging space nations, researchers, and university cubesat teams.",
         "✓ 100% open-source Python stack\n✓ Transparent mathematical formulas\n✓ Zero vendor lock-in or paid APIs",
         RGBColor(120, 220, 160)),
    ]

    for i, (tag, title, desc, bullets, color) in enumerate(impacts):
        cx = Inches(0.9) + i * (col3_w + Inches(0.3))
        add_card(s6, cx, c3_y, col3_w, c3_h)

        tb = s6.shapes.add_textbox(cx + Inches(0.22), c3_y + Inches(0.22), col3_w - Inches(0.44), c3_h - Inches(0.44))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = tag
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = color

        p = tf.add_paragraph()
        p.space_before = Pt(4)
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = TEXT_TITLE

        p = tf.add_paragraph()
        p.space_before = Pt(10)
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_BODY

        p = tf.add_paragraph()
        p.space_before = Pt(14)
        p.text = bullets
        p.font.size = Pt(10.5)
        p.font.color.rgb = color

    add_footer(s6, 6)

    # =========================================================
    # SLIDE 7: FUTURE ROADMAP & THANKS
    # =========================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "Future Vision & Verification", "Roadmap, Open Access & Acknowledgments",
               "SubZero is live, validated with 18 automated tests, and ready for deployment.")

    # Left: Roadmap
    add_card(s7, Inches(0.9), Inches(2.0), Inches(5.6), Inches(4.65))
    tb_r = s7.shapes.add_textbox(Inches(1.15), Inches(2.2), Inches(5.1), Inches(4.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0

    p = tf_r.paragraphs[0]
    p.text = "FUTURE DEVELOPMENT ROADMAP"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    roadmap_items = [
        ("Outer Planet Analogs", "Expand catalog to evaluate icy moons—including Europa sub-ice analog testing (Lake Vostok) and Titan cryo-lake environments.", ACCENT_BLUE),
        ("Live NASA PDS API Sync", "Automate direct connection to NASA Planetary Data System for live ingestion of new rover and orbiter data streams.", ACCENT_CYAN),
        ("Soil Assay & Electrostatic Dust", "Ingest perchlorate chemical assays and electrostatic dust levitation modeling for lunar dust mitigation testing.", ACCENT_ORANGE),
    ]

    for title, desc, color in roadmap_items:
        p_t = tf_r.add_paragraph()
        p_t.space_before = Pt(12)
        p_t.text = f"▶  {title}"
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = color

        p_d = tf_r.add_paragraph()
        p_d.space_before = Pt(2)
        p_d.text = desc
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = TEXT_BODY

    # Right: Links & Gratitude
    add_card(s7, Inches(6.8), Inches(2.0), Inches(5.633), Inches(4.65))
    tb_l = s7.shapes.add_textbox(Inches(7.05), Inches(2.2), Inches(5.133), Inches(4.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0

    p = tf_l.paragraphs[0]
    p.text = "PROJECT LINKS & ACCESS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    p = tf_l.add_paragraph()
    p.space_before = Pt(10)
    p.text = "Live Streamlit Web App:\nhttps://subzero.streamlit.app/"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    p = tf_l.add_paragraph()
    p.space_before = Pt(8)
    p.text = "GitHub Open Source Repository:\ngithub.com/obaid404notfound/planetary-analog-ranker"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    p = tf_l.add_paragraph()
    p.space_before = Pt(8)
    p.text = "Automated Test Suite:\n18/18 Unit & UI Integration Tests Passing"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(120, 220, 160)

    p = tf_l.add_paragraph()
    p.space_before = Pt(18)
    p.text = "SPECIAL THANKS:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE

    p = tf_l.add_paragraph()
    p.space_before = Pt(4)
    p.text = "Thank you to the NASA Space Apps Challenge 2026 organizers, evaluators, and the open planetary science community for making these datasets universally accessible."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_BODY

    add_footer(s7, 7)

    # Save output
    out_path = os.path.join(app_dir, "SubZero_NASA_Pitch_Deck.pptx")
    prs.save(out_path)
    print(f"Successfully generated PowerPoint deck: {out_path}")

if __name__ == "__main__":
    create_deck()
