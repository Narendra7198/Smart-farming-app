import streamlit as st
import pandas as pd
import pickle
import requests

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Smart Farming",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;900&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', sans-serif; color: #1a1a1a; }
.stApp { background: #f4faf4; overflow-x: hidden; }
p, span, li, div, label { color: #1a1a1a; }
img { max-width: 100% !important; height: auto !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a3a1a 0%, #2e7d32 60%, #388e3c 100%);
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label { color: white !important; }
[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 10px 16px;
    margin: 4px 0;
    display: block;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    border: 1px solid rgba(255,255,255,0.2);
    color: white !important;
}
[data-testid="stSidebar"] .stRadio label:hover { background: rgba(255,255,255,0.25); }

.hero {
    background: linear-gradient(120deg, #1b5e20 0%, #2e7d32 55%, #558b2f 100%);
    border-radius: 24px;
    padding: 44px 36px;
    text-align: center;
    margin-bottom: 28px;
    box-shadow: 0 10px 40px rgba(27,94,32,0.35);
}
.hero h1 { color: #ffffff !important; font-size: 2.6rem; font-weight: 900; margin: 0 0 10px 0; }
.hero p  { color: #e8f5e9 !important; font-size: 1.1rem; margin: 4px 0; }

.card {
    background: #ffffff;
    border-radius: 18px;
    padding: 24px;
    margin: 10px 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border-top: 4px solid #43a047;
}
.card h3 { color: #1b5e20 !important; margin-top: 0; font-size: 1.1rem; }
.card p  { color: #333333 !important; font-size: 0.92rem; line-height: 1.6; }
.card ul { color: #333333 !important; }
.card li { color: #333333 !important; margin-bottom: 4px; }
.card pre { color: #222222 !important; }

.result-box {
    background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #388e3c 100%);
    border-radius: 22px;
    padding: 36px 30px;
    text-align: center;
    margin: 20px 0;
    box-shadow: 0 8px 32px rgba(27,94,32,0.4);
}
.result-box .crop-emoji { font-size: 4rem; margin-bottom: 8px; display: block; }
.result-box .crop-name  { color: #ffffff !important; font-size: 2.4rem; font-weight: 900; }
.result-box .crop-sub   { color: #e8f5e9 !important; font-size: 1rem; margin-top: 6px; }

.tip {
    background: #ffffff;
    border-left: 5px solid #43a047;
    border-radius: 10px;
    padding: 12px 18px;
    margin: 7px 0;
    font-size: 0.93rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    color: #1a1a1a !important;
    line-height: 1.5;
}
.tip-red   { border-left-color: #e53935; background: #fff8f8; }
.tip-amber { border-left-color: #fb8c00; background: #fffaf3; }

.sec-head {
    background: linear-gradient(90deg, #2e7d32, #66bb6a);
    color: #ffffff !important;
    padding: 11px 20px;
    border-radius: 12px;
    font-size: 1.05rem;
    font-weight: 700;
    margin: 22px 0 14px 0;
}

[data-testid="metric-container"] {
    background: #ffffff;
    border-radius: 14px;
    padding: 14px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.07);
    border-top: 4px solid #66bb6a;
}
[data-testid="metric-container"] label { color: #555555 !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #1b5e20 !important; font-weight: 800; }

.stButton > button {
    background: linear-gradient(135deg, #2e7d32 0%, #43a047 100%);
    color: #ffffff !important;
    border-radius: 50px;
    padding: 14px 48px;
    font-size: 1.1rem;
    font-weight: 700;
    border: none;
    box-shadow: 0 5px 18px rgba(46,125,50,0.4);
    width: 100%;
    transition: all 0.3s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 9px 24px rgba(46,125,50,0.5);
}

.crop-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 14px;
    text-align: center;
    box-shadow: 0 3px 14px rgba(0,0,0,0.08);
    margin: 6px 0;
    border-bottom: 3px solid #66bb6a;
}
.crop-card b { color: #1b5e20 !important; font-size: 1.0rem; display: block; margin: 4px 0; }
.crop-card p { color: #444444 !important; font-size: 0.8rem; margin: 2px 0 0 0; }

.weather-strip {
    background: #ffffff;
    border-radius: 14px;
    padding: 14px 20px;
    margin: 12px 0;
    border: 2px solid #a5d6a7;
}
.weather-strip b { color: #1b5e20 !important; }

.stSlider label, .stSelectbox label,
.stNumberInput label, .stTextInput label {
    font-weight: 700 !important;
    color: #1b5e20 !important;
    font-size: 0.95rem !important;
}

[data-testid="stDataFrame"] { color: #1a1a1a !important; }

/* ── Selectbox / Dropdown — full fix ── */
[data-baseweb="select"] { color: #1a1a1a !important; }
[data-baseweb="select"] * { color: #1a1a1a !important; }
[data-baseweb="select"] div { color: #1a1a1a !important; background: #ffffff !important; }
[data-baseweb="select"] span { color: #1a1a1a !important; }
[data-baseweb="popover"] { color: #1a1a1a !important; }
[data-baseweb="popover"] * { color: #1a1a1a !important; }
[data-baseweb="popover"] li { color: #1a1a1a !important; background: #ffffff !important; }
[data-baseweb="popover"] li:hover { background: #e8f5e9 !important; color: #1b5e20 !important; }
[data-baseweb="menu"] { background: #ffffff !important; }
[data-baseweb="menu"] * { color: #1a1a1a !important; }
[data-baseweb="option"] { color: #1a1a1a !important; background: #ffffff !important; }
[data-baseweb="option"]:hover { background: #e8f5e9 !important; }
div[role="listbox"] { background: #ffffff !important; }
div[role="listbox"] * { color: #1a1a1a !important; }
div[role="option"] { color: #1a1a1a !important; background: #ffffff !important; }
div[role="option"]:hover { background: #e8f5e9 !important; color: #1b5e20 !important; }

.stAlert p { color: #1a1a1a !important; }
hr { border-color: #c8e6c9; margin: 14px 0; }

/* ════════════════════════════════════════
   MOBILE RESPONSIVE — 768px and below
   ════════════════════════════════════════ */
@media (max-width: 768px) {

    /* Hero banner — smaller on mobile */
    .hero { padding: 22px 14px !important; border-radius: 14px !important; margin-bottom: 14px !important; }
    .hero h1 { font-size: 1.55rem !important; }
    .hero p  { font-size: 0.86rem !important; }

    /* Cards — less padding */
    .card { padding: 14px !important; border-radius: 12px !important; }
    .card h3 { font-size: 0.98rem !important; }
    .card p, .card li { font-size: 0.84rem !important; }
    .card pre { font-size: 0.76rem !important; overflow-x: auto; }

    /* Result box — readable on small screen */
    .result-box { padding: 18px 12px !important; border-radius: 14px !important; }
    .result-box .crop-emoji { font-size: 2.6rem !important; }
    .result-box .crop-name  { font-size: 1.45rem !important; word-break: break-word; }
    .result-box .crop-sub   { font-size: 0.82rem !important; }

    /* Tips */
    .tip { padding: 10px 12px !important; font-size: 0.84rem !important; }

    /* Section header */
    .sec-head { padding: 8px 14px !important; font-size: 0.9rem !important; margin: 14px 0 10px 0 !important; }

    /* Predict button — big thumb-friendly */
    .stButton > button {
        font-size: 1rem !important;
        padding: 15px 20px !important;
        min-height: 54px !important;
        border-radius: 14px !important;
    }

    /* Metric cards — compact */
    [data-testid="metric-container"] { padding: 10px 8px !important; }
    [data-testid="metric-container"] label { font-size: 0.75rem !important; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] { font-size: 1rem !important; }

    /* Crop gallery cards */
    .crop-card { padding: 8px 5px !important; border-radius: 10px !important; }
    .crop-card b { font-size: 0.76rem !important; }
    .crop-card p { font-size: 0.66rem !important; }

    /* Weather strip */
    .weather-strip { padding: 10px 12px !important; }

    /* Input labels */
    .stSlider label, .stSelectbox label,
    .stNumberInput label, .stTextInput label {
        font-size: 0.85rem !important;
    }

    /* Slider handle — bigger for thumbs */
    [data-testid="stSlider"] [role="slider"] {
        width: 24px !important;
        height: 24px !important;
    }

    /* Dropdown options — taller for thumbs */
    div[role="option"] { min-height: 46px !important; padding: 12px !important; }
}

/* ════════════════════════════════════════
   SMALL PHONES — 480px and below
   ════════════════════════════════════════ */
@media (max-width: 480px) {
    .hero h1 { font-size: 1.3rem !important; }
    .hero p  { font-size: 0.8rem !important; }
    .result-box .crop-name { font-size: 1.25rem !important; }
    .result-box .crop-emoji { font-size: 2.2rem !important; }
    .sec-head { font-size: 0.85rem !important; }
    .tip { font-size: 0.82rem !important; }
    .card h3 { font-size: 0.92rem !important; }
}

/* ── Slider touch targets ── */
[data-testid="stSlider"] [role="slider"] {
    width: 22px !important;
    height: 22px !important;
    touch-action: none;
}

/* ── Selectbox / Dropdown — full visibility fix ── */
[data-baseweb="select"]           { color: #1a1a1a !important; }
[data-baseweb="select"] *         { color: #1a1a1a !important; }
[data-baseweb="select"] div       { color: #1a1a1a !important; background: #ffffff !important; }
[data-baseweb="select"] span      { color: #1a1a1a !important; }
[data-baseweb="popover"]          { color: #1a1a1a !important; }
[data-baseweb="popover"] *        { color: #1a1a1a !important; }
[data-baseweb="popover"] li       { color: #1a1a1a !important; background: #ffffff !important; }
[data-baseweb="popover"] li:hover { background: #e8f5e9 !important; color: #1b5e20 !important; }
[data-baseweb="menu"]             { background: #ffffff !important; }
[data-baseweb="menu"] *           { color: #1a1a1a !important; }
[data-baseweb="option"]           { color: #1a1a1a !important; background: #ffffff !important; min-height: 44px; }
[data-baseweb="option"]:hover     { background: #e8f5e9 !important; }
div[role="listbox"]               { background: #ffffff !important; }
div[role="listbox"] *             { color: #1a1a1a !important; }
div[role="option"]                { color: #1a1a1a !important; background: #ffffff !important; min-height: 44px; }
div[role="option"]:hover          { background: #e8f5e9 !important; color: #1b5e20 !important; }
</style>
""", unsafe_allow_html=True)

# ── CROP DATABASE ──────────────────────────────────────────────────────────────
CROP_INFO = {
    "rice":        {"emoji":"🌾","season":"Kharif (Jun–Nov)","water":"High","soil":"Clay / Loamy",
                    "desc":"Staple grain — largest cultivated crop in India",
                    "tips":["Maintain 5 cm standing water during early growth",
                            "Allow 21 days submergence after transplanting",
                            "Apply Zinc Sulfate 25 kg/ha to prevent deficiency"]},
    "maize":       {"emoji":"🌽","season":"Kharif + Rabi","water":"Medium","soil":"Sandy Loam",
                    "desc":"Corn — used in food, livestock feed, and industry",
                    "tips":["Plant in 4–5 rows for proper bee pollination",
                            "Apply top-dress nitrogen at knee-high stage",
                            "Spray Chlorpyrifos to control stem borer"]},
    "chickpea":    {"emoji":"🫘","season":"Rabi (Oct–Mar)","water":"Low","soil":"Sandy Loam",
                    "desc":"High-protein pulse — major source of dietary protein",
                    "tips":["Use wilt-resistant certified varieties",
                            "Treat seeds with Rhizobium culture before sowing",
                            "Avoid waterlogging — chickpea is highly sensitive"]},
    "kidneybeans": {"emoji":"🫘","season":"Kharif","water":"Medium","soil":"Loamy",
                    "desc":"Rajma — popular legume in northern hill regions",
                    "tips":["Install trellis or support sticks for climbing growth",
                            "Spray neem-based insecticide to control pod borer",
                            "Harvest when pods are fully dry and firm"]},
    "pigeonpeas":  {"emoji":"🌿","season":"Kharif (Jun–Oct)","water":"Low","soil":"Sandy / Loam",
                    "desc":"Arhar / Toor Dal — drought-tolerant pulse crop",
                    "tips":["Excellent for intercropping with cereals",
                            "Use Fusarium wilt-resistant varieties",
                            "Matures in 100–120 days after sowing"]},
    "mothbeans":   {"emoji":"🫘","season":"Kharif","water":"Very Low","soil":"Sandy",
                    "desc":"Drought-hardy pulse — suited to arid and semi-arid regions",
                    "tips":["Can produce yield with very little rainfall",
                            "Best choice for dry, arid growing conditions",
                            "Fixes atmospheric nitrogen, improving soil fertility"]},
    "mungbean":    {"emoji":"🌱","season":"Kharif + Zaid","water":"Low","soil":"Sandy Loam",
                    "desc":"Green gram — fast-maturing, short-duration pulse",
                    "tips":["Ready for harvest in just 60–65 days",
                            "Can give 2–3 harvests in a single season",
                            "Spray fungicide early to prevent powdery mildew"]},
    "blackgram":   {"emoji":"🫘","season":"Kharif","water":"Low-Medium","soil":"Clay Loam",
                    "desc":"Urad Dal — essential pulse in South Indian cuisine",
                    "tips":["Monitor regularly for yellow mosaic virus",
                            "Control whitefly to prevent virus spread",
                            "Apply fungicide during high-humidity periods"]},
    "lentil":      {"emoji":"🫘","season":"Rabi (Oct–Mar)","water":"Low","soil":"Sandy Loam",
                    "desc":"Masoor Dal — cool-season pulse, rich in protein",
                    "tips":["Grows best in cool, dry weather",
                            "Weed control is critical in the first 40 days",
                            "Spray Mancozeb to manage rust disease"]},
    "pomegranate": {"emoji":"🍎","season":"Perennial","water":"Low","soil":"Sandy / Loam",
                    "desc":"High-value fruit — grown in Maharashtra and Karnataka",
                    "tips":["Drip irrigation is the most efficient method",
                            "Apply copper-based spray to prevent bacterial blight",
                            "Bahar treatment regulates and improves flowering"]},
    "banana":      {"emoji":"🍌","season":"Year Round","water":"High","soil":"Loamy",
                    "desc":"India's number one fruit crop by production volume",
                    "tips":["Choose Panama wilt-resistant varieties",
                            "Use pseudo stem for compost after harvest",
                            "Cover developing bunches to improve fruit quality"]},
    "mango":       {"emoji":"🥭","season":"Summer (Mar–Jun)","water":"Low-Medium","soil":"Alluvial",
                    "desc":"National fruit of India — king of tropical fruits",
                    "tips":["Use Paclobutrazol to regulate off-season flowering",
                            "Apply Imidacloprid to control mango hoppers",
                            "Regular pruning improves canopy and yield"]},
    "grapes":      {"emoji":"🍇","season":"Rabi (Oct–Feb)","water":"Medium","soil":"Sandy Loam",
                    "desc":"High-value fruit crop — major export from Maharashtra",
                    "tips":["Follow a strict fungicide schedule for mildew control",
                            "Pruning is essential for good bunch development",
                            "Bunch thinning improves fruit size and quality"]},
    "watermelon":  {"emoji":"🍉","season":"Summer / Zaid","water":"Medium","soil":"Sandy",
                    "desc":"Popular summer fruit — high water content, heat tolerant",
                    "tips":["Direct sow seeds — does not transplant well",
                            "Requires adequate pollinators for fruit set",
                            "Use protein bait traps to manage fruit fly"]},
    "muskmelon":   {"emoji":"🍈","season":"Summer / Zaid","water":"Medium","soil":"Sandy",
                    "desc":"Sweet melon — widely grown across North India",
                    "tips":["Drip irrigation improves sweetness and quality",
                            "Spray sulfur-based fungicide to control powdery mildew",
                            "Crop is ready for harvest in 75–80 days"]},
    "apple":       {"emoji":"🍎","season":"Summer (Jun–Sep)","water":"Medium","soil":"Loamy",
                    "desc":"Temperate fruit — grown in Himachal, J&K, Uttarakhand",
                    "tips":["Requires sufficient chilling hours for proper fruit set",
                            "Protect against apple scab and fire blight",
                            "Fruit thinning produces larger, better-quality apples"]},
    "orange":      {"emoji":"🍊","season":"Winter (Nov–Jan)","water":"Medium","soil":"Sandy Loam",
                    "desc":"Citrus fruit — Nagpur orange is world-famous",
                    "tips":["Apply copper spray to prevent citrus canker",
                            "Control psyllid insects to prevent greening disease",
                            "Ensure well-drained soil — citrus is waterlogging sensitive"]},
    "papaya":      {"emoji":"🍈","season":"Year Round","water":"Medium","soil":"Sandy Loam",
                    "desc":"Fast-growing fruit crop with high return on investment",
                    "tips":["Control whitefly to prevent papaya ring spot virus",
                            "Maintain a male to female ratio of 1:10",
                            "First harvest ready within 9–10 months of planting"]},
    "coconut":     {"emoji":"🥥","season":"Perennial","water":"High","soil":"Sandy / Loam",
                    "desc":"Tree of life — major crop along Kerala and Karnataka coasts",
                    "tips":["Protect palms from rhinoceros beetle damage",
                            "Apply ferrous sulfate to soil for micronutrient correction",
                            "Practice intercropping to maximize income per hectare"]},
    "cotton":      {"emoji":"🤍","season":"Kharif (May–Nov)","water":"Medium","soil":"Black Cotton",
                    "desc":"White gold — India is the world's largest cotton producer",
                    "tips":["Bt cotton varieties provide excellent bollworm protection",
                            "Apply Imidacloprid to manage sucking pests",
                            "Avoid excessive nitrogen — causes vegetative overgrowth"]},
    "jute":        {"emoji":"🌿","season":"Kharif (Mar–Jun)","water":"High","soil":"Alluvial",
                    "desc":"Golden fibre — mainly grown in West Bengal and Assam",
                    "tips":["Crop reaches harvest maturity in about 120 days",
                            "Apply Mancozeb to prevent stem rot disease",
                            "Follow proper water retting process for fibre quality"]},
    "coffee":      {"emoji":"☕","season":"Perennial","water":"High","soil":"Red Laterite",
                    "desc":"Plantation crop — grown in the hills of Karnataka and Kerala",
                    "tips":["Always grow under shade trees for best quality beans",
                            "Protect plants from white stem borer infestation",
                            "Wet processing method produces superior quality coffee"]},
}

CROP_EMOJIS = {k: v["emoji"] for k, v in CROP_INFO.items()}

# ── WEATHER API ────────────────────────────────────────────────────────────────
def get_weather(city):
    try:
        api_key = "9b8ac5eb7dc15a8c413ed690b9793507"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        data = requests.get(url, timeout=5).json()
        if data.get("cod") != 200:
            return None
        return {
            "temp":     round(data["main"]["temp"], 1),
            "humidity": data["main"]["humidity"],
            "rainfall": round(data.get("rain", {}).get("1h", 0), 1),
            "desc":     data["weather"][0]["description"].title(),
            "city":     data["name"]
        }
    except Exception:
        return None

# ── LOAD MODEL ─────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    return pickle.load(open("Model/crop_model.pkl", "rb"))

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 AI Smart Farming")
    st.markdown("---")
    page = st.radio("Navigation", [
        "🏠 Home",
        "🌱 Crop Recommendation",
        "🦠 Disease Guide",
        "📊 Crop Information",
        "ℹ️ About"
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.82rem; color:#c8e6c9; line-height:1.9'>
    <b>22 Crops Supported:</b><br>
    🌾 Rice · Wheat · Maize<br>
    🫘 Chickpea · Lentil · Mung Bean<br>
    🍌 Banana · Mango · Apple<br>
    🍇 Grapes · Orange · Papaya<br>
    🤍 Cotton · Jute · Coffee<br>
    + 7 more crops
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; font-size:0.8rem; color:#a5d6a7'>
    🇮🇳 Built for Indian Farmers
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
if "Home" in page:
    st.markdown("""
    <div class="hero">
        <h1>🌾 AI Smart Farming</h1>
        <p>Smart technology to help you farm better and earn more</p>
        <p>Which crop should I grow? What disease is this? — Get instant answers.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="card">
        <h3>🌱 Smart Crop Recommendation</h3>
        <p>Enter your soil's N, P, K values and your city name — the AI recommends
        the best crop suited to your exact field conditions.</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="card">
        <h3>🦠 Disease Guide</h3>
        <p>Browse common diseases across 22 crops. View symptoms, treatment steps,
        and prevention tips — all clearly explained.</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="card">
        <h3>📊 Crop Information</h3>
        <p>Detailed profile for every crop — growing season, water requirement,
        best soil type, and expert farming tips.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 📈 System Overview")
        m1, m2 = st.columns(2)
        m1.metric("🌾 Crops Supported", "22", "Indian crops")
        m2.metric("🎯 Model Accuracy", "99.3%", "Random Forest")
        m3, m4 = st.columns(2)
        m3.metric("🌦️ Live Weather", "Real-time", "OpenWeatherMap API")
        m4.metric("⚡ Prediction Speed", "< 1 sec", "Instant result")
    with col_b:
        st.markdown("### 🚀 How to Use")
        for step, desc in [
            ("1️⃣ Crop Recommendation",
             "Go to Crop Recommendation → Enter your city and soil NPK → Click Predict"),
            ("2️⃣ Disease Guide",
             "Go to Disease Guide → Select your crop → View diseases and treatment"),
            ("3️⃣ Crop Information",
             "Go to Crop Information → Search any crop → Get full growing details"),
        ]:
            st.markdown(f'<div class="tip"><b>{step}</b><br>{desc}</div>',
                        unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🌿 All Supported Crops")
    crops_list = list(CROP_INFO.items())
    for row_start in range(0, len(crops_list), 7):
        row = crops_list[row_start:row_start + 7]
        cols = st.columns(len(row))
        for col, (name, info) in zip(cols, row):
            with col:
                st.markdown(f"""<div class="crop-card">
                <span style="font-size:2rem">{info['emoji']}</span>
                <b>{name.title()}</b>
                <p>{info['season']}</p>
                </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CROP RECOMMENDATION
# ══════════════════════════════════════════════════════════════════════════════
elif "Recommendation" in page:
    st.markdown("""
    <div class="hero">
        <h1>🌱 Crop Recommendation</h1>
        <p>Enter your soil and weather data — AI tells you the best crop to grow</p>
    </div>
    """, unsafe_allow_html=True)

    model = load_model()
    col_left, col_right = st.columns([1, 1.1], gap="large")

    with col_left:
        st.markdown('<div class="sec-head">🧪 Soil Nutrients</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            N = st.slider("🟢 Nitrogen (N)", 0, 200, 90,
                          help="Promotes leaf and stem growth — source: Urea")
        with c2:
            P = st.slider("🟡 Phosphorus (P)", 0, 200, 42,
                          help="Supports root development — source: DAP / SSP")
        with c3:
            K = st.slider("🔴 Potassium (K)", 0, 200, 43,
                          help="Improves disease resistance — source: MOP")

        ph = st.slider("⚗️ Soil pH", 0.0, 14.0, 6.5, step=0.1,
                       help="7 = neutral  |  below 7 = acidic  |  above 7 = alkaline")

        if ph < 5.5:
            st.markdown(
                '<div class="tip tip-red">⚠️ pH is too low (acidic) — apply agricultural lime to correct it</div>',
                unsafe_allow_html=True)
        elif ph > 8.5:
            st.markdown(
                '<div class="tip tip-amber">⚠️ pH is too high (alkaline) — apply sulfur or gypsum to lower it</div>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="tip">✅ Soil pH is in the normal range — suitable for most crops</div>',
                unsafe_allow_html=True)

        st.markdown('<div class="sec-head">🌦️ Weather Data</div>', unsafe_allow_html=True)
        city = st.text_input("📍 Enter your city name",
                             placeholder="e.g. Jaipur, Lucknow, Pune, Mumbai...")

        weather = None
        if city:
            with st.spinner("Fetching live weather data..."):
                weather = get_weather(city)
            if weather:
                st.markdown(f"""<div class="weather-strip">
                <b>🌤️ {weather['city']} — {weather['desc']}</b></div>""",
                            unsafe_allow_html=True)
                wc1, wc2, wc3 = st.columns(3)
                wc1.metric("🌡️ Temperature", f"{weather['temp']} °C")
                wc2.metric("💧 Humidity",    f"{weather['humidity']} %")
                wc3.metric("🌧️ Rainfall",    f"{weather['rainfall']} mm")
                temperature = weather["temp"]
                humidity    = weather["humidity"]
                rainfall    = weather["rainfall"]
            else:
                st.warning("City not found or no internet — please enter values manually")
                mc1, mc2, mc3 = st.columns(3)
                with mc1: temperature = st.number_input("🌡️ Temperature (°C)", 0.0, 50.0, 25.0)
                with mc2: humidity    = st.number_input("💧 Humidity (%)",      0.0,100.0, 70.0)
                with mc3: rainfall    = st.number_input("🌧️ Rainfall (mm)",     0.0,300.0,100.0)
        else:
            mc1, mc2, mc3 = st.columns(3)
            with mc1: temperature = st.number_input("🌡️ Temperature (°C)", 0.0, 50.0, 25.0)
            with mc2: humidity    = st.number_input("💧 Humidity (%)",      0.0,100.0, 70.0)
            with mc3: rainfall    = st.number_input("🌧️ Rainfall (mm)",     0.0,300.0,100.0)

        st.markdown("<br>", unsafe_allow_html=True)
        predict_btn = st.button("🚜 Predict Best Crop", use_container_width=True)

    with col_right:
        st.markdown('<div class="sec-head">🏆 AI Recommendation</div>', unsafe_allow_html=True)

        if predict_btn:
            sample = pd.DataFrame(
                [[N, P, K, temperature, humidity, ph, rainfall]],
                columns=["N","P","K","temperature","humidity","ph","rainfall"]
            )
            with st.spinner("AI is analyzing your field data..."):
                result = model.predict(sample)[0]
                info = CROP_INFO.get(result.lower(), {
                    "emoji":"🌾","season":"—","desc":"Crop information not available",
                    "water":"—","soil":"—","tips":[]
                })

            st.markdown(f"""
            <div class="result-box">
                <span class="crop-emoji">{info['emoji']}</span>
                <div class="crop-name">{result.upper()}</div>
                <div class="crop-sub">{info['desc']}</div>
            </div>""", unsafe_allow_html=True)

            dc1, dc2, dc3 = st.columns(3)
            dc1.metric("📅 Season",    info.get("season","—"))
            dc2.metric("💧 Water Need",info.get("water","—"))
            dc3.metric("🪨 Best Soil", info.get("soil","—"))

            if info.get("tips"):
                st.markdown('<div class="sec-head">💡 Key Farming Tips</div>',
                            unsafe_allow_html=True)
                for tip in info["tips"]:
                    st.markdown(f'<div class="tip">🌱 {tip}</div>', unsafe_allow_html=True)

            with st.expander("📋 View Your Input Summary"):
                summ = pd.DataFrame({
                    "Parameter":   ["Nitrogen","Phosphorus","Potassium","pH",
                                    "Temperature","Humidity","Rainfall"],
                    "Your Value":  [f"{N} kg/ha",f"{P} kg/ha",f"{K} kg/ha",
                                    str(ph),f"{temperature} °C",
                                    f"{humidity} %",f"{rainfall} mm"],
                    "Ideal Range": ["60–120","30–60","40–80","6.0–7.5",
                                    "18–35 °C","50–85 %","50–250 mm"]
                })
                st.dataframe(summ, use_container_width=True, hide_index=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:60px 20px;background:white;
                        border-radius:16px;border:2px dashed #a5d6a7;color:#888">
                <p style="font-size:3rem">🌾</p>
                <p style="font-size:1.1rem">Enter your soil and weather data<br>
                then click <b>Predict Best Crop</b></p>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🌿 NPK Quick Reference")
        ng, pg, kg_col = st.columns(3)
        with ng:
            st.markdown("""<div class="card">
            <h3>🟢 N — Nitrogen</h3>
            <p>Promotes green leaf growth and strong stems</p>
            <p><b>Source:</b> Urea (46% N)</p>
            <p><b>Deficiency sign:</b> Yellow leaves</p>
            </div>""", unsafe_allow_html=True)
        with pg:
            st.markdown("""<div class="card">
            <h3>🟡 P — Phosphorus</h3>
            <p>Strengthens roots and supports flowering</p>
            <p><b>Source:</b> DAP, SSP</p>
            <p><b>Deficiency sign:</b> Purple or reddish leaves</p>
            </div>""", unsafe_allow_html=True)
        with kg_col:
            st.markdown("""<div class="card">
            <h3>🔴 K — Potassium</h3>
            <p>Builds disease resistance and improves crop quality</p>
            <p><b>Source:</b> MOP (Muriate of Potash)</p>
            <p><b>Deficiency sign:</b> Browning of leaf edges</p>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DISEASE GUIDE
# ══════════════════════════════════════════════════════════════════════════════
elif "Disease" in page:
    st.markdown("""
    <div class="hero">
        <h1>🦠 Crop Disease Guide</h1>
        <p>Identify plant diseases — symptoms, treatment steps, and prevention tips</p>
    </div>
    """, unsafe_allow_html=True)

    DISEASE_DB = {
        "Rice": [
            {"name":"🟤 Blast Disease",
             "symptoms":"Diamond-shaped gray spots on leaves; brown lesions on the neck near the panicle",
             "treatment":["Spray Tricyclazole 75WP at 0.6 g per liter of water",
                          "Apply at boot leaf stage and again at heading stage",
                          "Avoid excess nitrogen fertilizer application"],
             "prevention":["Use blast-resistant varieties such as IR64 or Pusa Basmati",
                           "Treat seeds with Carbendazim 2 g per kg before sowing",
                           "Maintain 20 × 15 cm plant spacing for air circulation"]},
            {"name":"🟡 Bacterial Leaf Blight",
             "symptoms":"Leaf edges turn yellow then brown; leaves wilt and dry from the tips inward",
             "treatment":["Spray copper oxychloride at 3 g per liter",
                          "Increase potassium fertilizer application",
                          "Drain field water temporarily to reduce humidity"],
             "prevention":["Use certified disease-free seeds only",
                           "Avoid excessive nitrogen application",
                           "Maintain proper field drainage at all times"]},
            {"name":"🟤 Brown Spot",
             "symptoms":"Oval brown spots with a yellow halo on leaves and grains",
             "treatment":["Spray Edifenphos or Mancozeb fungicide",
                          "Apply potassium and silicon fertilizers to boost plant immunity"],
             "prevention":["Follow balanced NPK fertilization schedule",
                           "Treat seeds with Thiram 3 g per kg before planting"]},
        ],
        "Wheat": [
            {"name":"🟡 Yellow (Stripe) Rust",
             "symptoms":"Bright yellow stripes running along the leaf surface; powdery appearance",
             "treatment":["Spray Propiconazole 25 EC at 0.1% concentration — act immediately",
                          "Repeat spray after 14 days if infection persists",
                          "Apply potassium fertilizer to strengthen plant immunity"],
             "prevention":["Use rust-resistant varieties such as HD 2967 or PBW 550",
                           "Sow early in October–November to avoid peak rust season",
                           "Scout fields regularly during cool, humid weather"]},
            {"name":"🟠 Leaf Rust (Brown Rust)",
             "symptoms":"Orange-brown powdery pustules scattered on the upper leaf surface",
             "treatment":["Spray Tebuconazole or Propiconazole at first sign of infection",
                          "Apply at flag leaf stage for maximum protection"],
             "prevention":["Choose rust-resistant wheat varieties",
                           "Apply preventive fungicide spray at flag leaf emergence"]},
            {"name":"⚫ Loose Smut",
             "symptoms":"Entire grain replaced by a black powdery fungal mass",
             "treatment":["Treat seeds with Carboxin + Thiram (Vitavax) before sowing",
                          "Remove and destroy infected spikes before spores spread"],
             "prevention":["Always use certified smut-free seeds",
                           "Apply systemic fungicide seed treatment before every sowing"]},
        ],
        "Tomato": [
            {"name":"🟤 Early Blight",
             "symptoms":"Dark brown spots with concentric rings (target-board pattern) on lower leaves",
             "treatment":["Spray Chlorothalonil or Mancozeb every 7 days",
                          "Remove and destroy all infected lower leaves immediately",
                          "Apply copper-based fungicide as an alternative"],
             "prevention":["Maintain plant spacing of 45–60 cm for air circulation",
                           "Use drip irrigation — avoid wetting the foliage",
                           "Apply mulch around base to prevent soil splash on leaves"]},
            {"name":"💧 Late Blight",
             "symptoms":"Dark water-soaked spots on leaves and stems; white fungal growth; foul smell",
             "treatment":["Apply Metalaxyl + Mancozeb fungicide immediately — do not delay",
                          "Remove infected plants, seal in bags, and dispose safely",
                          "Continue spraying every 5 days during cool, wet weather"],
             "prevention":["Use blight-resistant varieties such as Arka Abha or Pusa Hybrid",
                           "Avoid waterlogging and overhead irrigation",
                           "Destroy all infected crop debris thoroughly after harvest"]},
            {"name":"🟡 Yellow Leaf Curl Virus (TYLCV)",
             "symptoms":"Leaves curl upward and turn yellow; plants become stunted and distorted",
             "treatment":["Remove and destroy all infected plants immediately",
                          "Spray Imidacloprid to control whitefly — the virus carrier",
                          "Install yellow sticky traps to reduce whitefly population"],
             "prevention":["Grow TYLCV-resistant tomato varieties",
                           "Use insect-proof nets to protect nursery seedlings",
                           "Keep field free of weeds — they serve as host plants for whitefly"]},
        ],
        "Potato": [
            {"name":"💀 Late Blight",
             "symptoms":"Dark brown spots on leaves, stems, and tubers; wet rot with foul odour",
             "treatment":["Apply Metalaxyl-M fungicide immediately — every day matters",
                          "Remove and safely destroy all infected plant material",
                          "Continue spraying every 5–7 days during humid weather"],
             "prevention":["Use certified, disease-free seed potatoes only",
                           "Improve field drainage before planting",
                           "Monitor daily during cool and wet conditions"]},
            {"name":"🟤 Early Blight",
             "symptoms":"Dark brown spots with concentric rings appearing on older leaves",
             "treatment":["Spray Chlorothalonil or Mancozeb fungicide",
                          "Remove infected leaves as soon as they appear",
                          "Apply copper fungicide as a backup option"],
             "prevention":["Practice crop rotation — avoid planting potato in the same field",
                           "Apply mulch to prevent infected soil from splashing onto leaves",
                           "Maintain proper plant spacing for adequate air movement"]},
        ],
        "Cotton": [
            {"name":"🪲 American Bollworm",
             "symptoms":"Holes in bolls, squares, and flowers; bolls fall off prematurely",
             "treatment":["Grow Bt cotton varieties for built-in bollworm resistance",
                          "Spray Emamectin Benzoate for chemical control",
                          "Use Spinosad spray in organic farming systems"],
             "prevention":["Install pheromone traps for early population detection",
                           "Monitor crop weekly from flowering stage onward",
                           "Apply neem oil spray as a preventive measure"]},
            {"name":"🟤 Alternaria Blight",
             "symptoms":"Brown circular spots with a yellow halo appearing on leaves",
             "treatment":["Spray Mancozeb at 2.5 g per liter of water",
                          "Remove and destroy all infected plant parts"],
             "prevention":["Rotate cotton with other crops to break the disease cycle",
                           "Use certified disease-free seeds for every sowing"]},
        ],
        "Maize": [
            {"name":"⬛ Fall Armyworm",
             "symptoms":"Holes in leaves and tassels; black frass (droppings) visible in the whorl",
             "treatment":["Spray Emamectin Benzoate 5% SG at 0.4 g per liter",
                          "Apply Chlorantraniliprole for severe infestations",
                          "Use neem oil and soap solution for organic control"],
             "prevention":["Sow early in June to avoid peak armyworm pressure",
                           "Inspect at least 5 plants per week from seedling stage",
                           "Place 2 pheromone traps per acre for monitoring"]},
            {"name":"🟤 Northern Leaf Blight",
             "symptoms":"Long gray-green cigar-shaped lesions running along the length of leaves",
             "treatment":["Spray Azoxystrobin + Propiconazole fungicide",
                          "Remove and destroy all crop debris after harvest"],
             "prevention":["Use blight-resistant hybrid varieties",
                           "Practice crop rotation and improve soil drainage"]},
        ],
        "Grapes": [
            {"name":"🍄 Downy Mildew",
             "symptoms":"Yellow patches on upper leaf surface; white powdery growth on the underside",
             "treatment":["Spray Metalaxyl + Mancozeb fungicide",
                          "Apply Fosetyl Aluminum for systemic protection",
                          "Remove and destroy all infected plant parts immediately"],
             "prevention":["Prune canopy regularly to improve air circulation",
                           "Use drip irrigation — keep the foliage dry",
                           "Follow a strict preventive spray schedule throughout the season"]},
            {"name":"⬜ Powdery Mildew",
             "symptoms":"White powdery coating on leaves, shoots, and developing berries",
             "treatment":["Spray Sulfur 80 WP at 2 g per liter of water",
                          "Apply Hexaconazole for severe or advanced infections"],
             "prevention":["Ensure adequate spacing between vines for air movement",
                           "Increase potassium application to strengthen plant tissues"]},
        ],
    }

    selected_crop = st.selectbox(
        "Select a crop to view its diseases",
        options=list(DISEASE_DB.keys()),
        format_func=lambda x: f"{CROP_EMOJIS.get(x.lower(), '🌿')}  {x}"
    )

    diseases = DISEASE_DB[selected_crop]
    st.markdown(
        f"### {CROP_EMOJIS.get(selected_crop.lower(), '🌿')} "
        f"{selected_crop} — {len(diseases)} Common Diseases"
    )

    for disease in diseases:
        with st.expander(f"**{disease['name']}** — click to expand"):
            d1, d2, d3 = st.columns(3)
            with d1:
                st.markdown("**🔍 Symptoms**")
                st.markdown(f'<div class="tip tip-amber">⚠️ {disease["symptoms"]}</div>',
                            unsafe_allow_html=True)
            with d2:
                st.markdown("**💊 Treatment**")
                for t in disease["treatment"]:
                    st.markdown(f'<div class="tip tip-red">✅ {t}</div>',
                                unsafe_allow_html=True)
            with d3:
                st.markdown("**🛡️ Prevention**")
                for p in disease["prevention"]:
                    st.markdown(f'<div class="tip">🔰 {p}</div>',
                                unsafe_allow_html=True)

    st.markdown("---")
    st.info(
        "💡 This guide provides general information. For accurate field diagnosis, "
        "consult your nearest Krishi Vigyan Kendra (KVK) or Agriculture Extension Officer."
    )


# ══════════════════════════════════════════════════════════════════════════════
# CROP INFORMATION
# ══════════════════════════════════════════════════════════════════════════════
elif "Information" in page:
    st.markdown("""
    <div class="hero">
        <h1>📊 Crop Information</h1>
        <p>Complete growing guide — season, water requirement, soil type, and expert tips</p>
    </div>
    """, unsafe_allow_html=True)

    search = st.text_input("🔍 Search a crop",
                           placeholder="e.g. rice, cotton, mango, banana...")
    filtered = {k: v for k, v in CROP_INFO.items()
                if search.lower() in k.lower()} if search else CROP_INFO

    if not filtered:
        st.warning("No crop found — try a different name")
    else:
        crops_items = list(filtered.items())
        for i in range(0, len(crops_items), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(crops_items):
                    name, info = crops_items[i + j]
                    with col:
                        with st.expander(
                            f"{info['emoji']}  **{name.title()}** — {info['desc']}"
                        ):
                            ia, ib, ic = st.columns(3)
                            ia.metric("📅 Season",     info.get("season","—"))
                            ib.metric("💧 Water Need", info.get("water","—"))
                            ic.metric("🪨 Soil Type",  info.get("soil","—"))
                            if info.get("tips"):
                                st.markdown("**🌱 Farming Tips:**")
                                for tip in info["tips"]:
                                    st.markdown(f'<div class="tip">💡 {tip}</div>',
                                                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ABOUT
# ══════════════════════════════════════════════════════════════════════════════
elif "About" in page:
    st.markdown("""
    <div class="hero">
        <h1>ℹ️ About This Project</h1>
        <p>Smart Crop Recommendation System</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class="card">
        <h3>🎯 Project Goal</h3>
        <p>Every Indian farmer deserves access to expert agricultural advice.
        This tool helps farmers choose the right crop, identify diseases early,
        and access complete growing information — all in one place, completely free.</p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="card">
        <h3>⚙️ Technology Used</h3>
        <ul>
        <li><b>ML Model:</b> Random Forest Classifier — 99.3% accuracy</li>
        <li><b>Dataset:</b> Crop Recommendation Dataset — 2,200 samples, 22 crops</li>
        <li><b>Weather:</b> OpenWeatherMap Live API</li>
        <li><b>UI Framework:</b> Streamlit + Custom CSS</li>
        <li><b>Language:</b> Python 3</li>
        </ul>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown("""<div class="card">
        <h3>📊 Dataset Details</h3>
        <ul>
        <li><b>File:</b> Crop_recommendation.csv</li>
        <li><b>Total Samples:</b> 2,200 rows</li>
        <li><b>Input Features:</b> N, P, K, Temperature, Humidity, pH, Rainfall</li>
        <li><b>Target:</b> 22 crop classes</li>
        <li><b>Split:</b> 80% training / 20% testing</li>
        </ul>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="card">
        <h3>🔧 How to Run This App</h3>
        <pre>
# Step 1 — Install libraries
pip install -r requirements.txt

# Step 2 — Run the app
streamlit run app.py

# Step 3 — Open your browser
http://localhost:8501
        </pre>
        </div>""", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import pickle
import requests

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Smart Farming",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;900&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', sans-serif; color: #1a1a1a; }
.stApp { background: #f4faf4; overflow-x: hidden; }
p, span, li, div, label { color: #1a1a1a; }
img { max-width: 100% !important; height: auto !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a3a1a 0%, #2e7d32 60%, #388e3c 100%);
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label { color: white !important; }
[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 10px 16px;
    margin: 4px 0;
    display: block;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    border: 1px solid rgba(255,255,255,0.2);
    color: white !important;
}
[data-testid="stSidebar"] .stRadio label:hover { background: rgba(255,255,255,0.25); }

.hero {
    background: linear-gradient(120deg, #1b5e20 0%, #2e7d32 55%, #558b2f 100%);
    border-radius: 24px;
    padding: 44px 36px;
    text-align: center;
    margin-bottom: 28px;
    box-shadow: 0 10px 40px rgba(27,94,32,0.35);
}
.hero h1 { color: #ffffff !important; font-size: 2.6rem; font-weight: 900; margin: 0 0 10px 0; }
.hero p  { color: #e8f5e9 !important; font-size: 1.1rem; margin: 4px 0; }

.card {
    background: #ffffff;
    border-radius: 18px;
    padding: 24px;
    margin: 10px 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border-top: 4px solid #43a047;
}
.card h3 { color: #1b5e20 !important; margin-top: 0; font-size: 1.1rem; }
.card p  { color: #333333 !important; font-size: 0.92rem; line-height: 1.6; }
.card ul { color: #333333 !important; }
.card li { color: #333333 !important; margin-bottom: 4px; }
.card pre { color: #222222 !important; }

.result-box {
    background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #388e3c 100%);
    border-radius: 22px;
    padding: 36px 30px;
    text-align: center;
    margin: 20px 0;
    box-shadow: 0 8px 32px rgba(27,94,32,0.4);
}
.result-box .crop-emoji { font-size: 4rem; margin-bottom: 8px; display: block; }
.result-box .crop-name  { color: #ffffff !important; font-size: 2.4rem; font-weight: 900; }
.result-box .crop-sub   { color: #e8f5e9 !important; font-size: 1rem; margin-top: 6px; }

.tip {
    background: #ffffff;
    border-left: 5px solid #43a047;
    border-radius: 10px;
    padding: 12px 18px;
    margin: 7px 0;
    font-size: 0.93rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    color: #1a1a1a !important;
    line-height: 1.5;
}
.tip-red   { border-left-color: #e53935; background: #fff8f8; }
.tip-amber { border-left-color: #fb8c00; background: #fffaf3; }

.sec-head {
    background: linear-gradient(90deg, #2e7d32, #66bb6a);
    color: #ffffff !important;
    padding: 11px 20px;
    border-radius: 12px;
    font-size: 1.05rem;
    font-weight: 700;
    margin: 22px 0 14px 0;
}

[data-testid="metric-container"] {
    background: #ffffff;
    border-radius: 14px;
    padding: 14px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.07);
    border-top: 4px solid #66bb6a;
}
[data-testid="metric-container"] label { color: #555555 !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #1b5e20 !important; font-weight: 800; }

.stButton > button {
    background: linear-gradient(135deg, #2e7d32 0%, #43a047 100%);
    color: #ffffff !important;
    border-radius: 50px;
    padding: 14px 48px;
    font-size: 1.1rem;
    font-weight: 700;
    border: none;
    box-shadow: 0 5px 18px rgba(46,125,50,0.4);
    width: 100%;
    transition: all 0.3s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 9px 24px rgba(46,125,50,0.5);
}

.crop-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 14px;
    text-align: center;
    box-shadow: 0 3px 14px rgba(0,0,0,0.08);
    margin: 6px 0;
    border-bottom: 3px solid #66bb6a;
}
.crop-card b { color: #1b5e20 !important; font-size: 1.0rem; display: block; margin: 4px 0; }
.crop-card p { color: #444444 !important; font-size: 0.8rem; margin: 2px 0 0 0; }

.weather-strip {
    background: #ffffff;
    border-radius: 14px;
    padding: 14px 20px;
    margin: 12px 0;
    border: 2px solid #a5d6a7;
}
.weather-strip b { color: #1b5e20 !important; }

.stSlider label, .stSelectbox label,
.stNumberInput label, .stTextInput label {
    font-weight: 700 !important;
    color: #1b5e20 !important;
    font-size: 0.95rem !important;
}

[data-testid="stDataFrame"] { color: #1a1a1a !important; }

/* ── Selectbox / Dropdown — full fix ── */
[data-baseweb="select"] { color: #1a1a1a !important; }
[data-baseweb="select"] * { color: #1a1a1a !important; }
[data-baseweb="select"] div { color: #1a1a1a !important; background: #ffffff !important; }
[data-baseweb="select"] span { color: #1a1a1a !important; }
[data-baseweb="popover"] { color: #1a1a1a !important; }
[data-baseweb="popover"] * { color: #1a1a1a !important; }
[data-baseweb="popover"] li { color: #1a1a1a !important; background: #ffffff !important; }
[data-baseweb="popover"] li:hover { background: #e8f5e9 !important; color: #1b5e20 !important; }
[data-baseweb="menu"] { background: #ffffff !important; }
[data-baseweb="menu"] * { color: #1a1a1a !important; }
[data-baseweb="option"] { color: #1a1a1a !important; background: #ffffff !important; }
[data-baseweb="option"]:hover { background: #e8f5e9 !important; }
div[role="listbox"] { background: #ffffff !important; }
div[role="listbox"] * { color: #1a1a1a !important; }
div[role="option"] { color: #1a1a1a !important; background: #ffffff !important; }
div[role="option"]:hover { background: #e8f5e9 !important; color: #1b5e20 !important; }

.stAlert p { color: #1a1a1a !important; }
hr { border-color: #c8e6c9; margin: 14px 0; }

/* ════════════════════════════════════════
   MOBILE RESPONSIVE — 768px and below
   ════════════════════════════════════════ */
@media (max-width: 768px) {

    /* Hero banner — smaller on mobile */
    .hero { padding: 22px 14px !important; border-radius: 14px !important; margin-bottom: 14px !important; }
    .hero h1 { font-size: 1.55rem !important; }
    .hero p  { font-size: 0.86rem !important; }

    /* Cards — less padding */
    .card { padding: 14px !important; border-radius: 12px !important; }
    .card h3 { font-size: 0.98rem !important; }
    .card p, .card li { font-size: 0.84rem !important; }
    .card pre { font-size: 0.76rem !important; overflow-x: auto; }

    /* Result box — readable on small screen */
    .result-box { padding: 18px 12px !important; border-radius: 14px !important; }
    .result-box .crop-emoji { font-size: 2.6rem !important; }
    .result-box .crop-name  { font-size: 1.45rem !important; word-break: break-word; }
    .result-box .crop-sub   { font-size: 0.82rem !important; }

    /* Tips */
    .tip { padding: 10px 12px !important; font-size: 0.84rem !important; }

    /* Section header */
    .sec-head { padding: 8px 14px !important; font-size: 0.9rem !important; margin: 14px 0 10px 0 !important; }

    /* Predict button — big thumb-friendly */
    .stButton > button {
        font-size: 1rem !important;
        padding: 15px 20px !important;
        min-height: 54px !important;
        border-radius: 14px !important;
    }

    /* Metric cards — compact */
    [data-testid="metric-container"] { padding: 10px 8px !important; }
    [data-testid="metric-container"] label { font-size: 0.75rem !important; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] { font-size: 1rem !important; }

    /* Crop gallery cards */
    .crop-card { padding: 8px 5px !important; border-radius: 10px !important; }
    .crop-card b { font-size: 0.76rem !important; }
    .crop-card p { font-size: 0.66rem !important; }

    /* Weather strip */
    .weather-strip { padding: 10px 12px !important; }

    /* Input labels */
    .stSlider label, .stSelectbox label,
    .stNumberInput label, .stTextInput label {
        font-size: 0.85rem !important;
    }

    /* Slider handle — bigger for thumbs */
    [data-testid="stSlider"] [role="slider"] {
        width: 24px !important;
        height: 24px !important;
    }

    /* Dropdown options — taller for thumbs */
    div[role="option"] { min-height: 46px !important; padding: 12px !important; }
}

/* ════════════════════════════════════════
   SMALL PHONES — 480px and below
   ════════════════════════════════════════ */
@media (max-width: 480px) {
    .hero h1 { font-size: 1.3rem !important; }
    .hero p  { font-size: 0.8rem !important; }
    .result-box .crop-name { font-size: 1.25rem !important; }
    .result-box .crop-emoji { font-size: 2.2rem !important; }
    .sec-head { font-size: 0.85rem !important; }
    .tip { font-size: 0.82rem !important; }
    .card h3 { font-size: 0.92rem !important; }
}

/* ── Slider touch targets ── */
[data-testid="stSlider"] [role="slider"] {
    width: 22px !important;
    height: 22px !important;
    touch-action: none;
}

/* ── Selectbox / Dropdown — full visibility fix ── */
[data-baseweb="select"]           { color: #1a1a1a !important; }
[data-baseweb="select"] *         { color: #1a1a1a !important; }
[data-baseweb="select"] div       { color: #1a1a1a !important; background: #ffffff !important; }
[data-baseweb="select"] span      { color: #1a1a1a !important; }
[data-baseweb="popover"]          { color: #1a1a1a !important; }
[data-baseweb="popover"] *        { color: #1a1a1a !important; }
[data-baseweb="popover"] li       { color: #1a1a1a !important; background: #ffffff !important; }
[data-baseweb="popover"] li:hover { background: #e8f5e9 !important; color: #1b5e20 !important; }
[data-baseweb="menu"]             { background: #ffffff !important; }
[data-baseweb="menu"] *           { color: #1a1a1a !important; }
[data-baseweb="option"]           { color: #1a1a1a !important; background: #ffffff !important; min-height: 44px; }
[data-baseweb="option"]:hover     { background: #e8f5e9 !important; }
div[role="listbox"]               { background: #ffffff !important; }
div[role="listbox"] *             { color: #1a1a1a !important; }
div[role="option"]                { color: #1a1a1a !important; background: #ffffff !important; min-height: 44px; }
div[role="option"]:hover          { background: #e8f5e9 !important; color: #1b5e20 !important; }
</style>
""", unsafe_allow_html=True)

# ── CROP DATABASE ──────────────────────────────────────────────────────────────
CROP_INFO = {
    "rice":        {"emoji":"🌾","season":"Kharif (Jun–Nov)","water":"High","soil":"Clay / Loamy",
                    "desc":"Staple grain — largest cultivated crop in India",
                    "tips":["Maintain 5 cm standing water during early growth",
                            "Allow 21 days submergence after transplanting",
                            "Apply Zinc Sulfate 25 kg/ha to prevent deficiency"]},
    "maize":       {"emoji":"🌽","season":"Kharif + Rabi","water":"Medium","soil":"Sandy Loam",
                    "desc":"Corn — used in food, livestock feed, and industry",
                    "tips":["Plant in 4–5 rows for proper bee pollination",
                            "Apply top-dress nitrogen at knee-high stage",
                            "Spray Chlorpyrifos to control stem borer"]},
    "chickpea":    {"emoji":"🫘","season":"Rabi (Oct–Mar)","water":"Low","soil":"Sandy Loam",
                    "desc":"High-protein pulse — major source of dietary protein",
                    "tips":["Use wilt-resistant certified varieties",
                            "Treat seeds with Rhizobium culture before sowing",
                            "Avoid waterlogging — chickpea is highly sensitive"]},
    "kidneybeans": {"emoji":"🫘","season":"Kharif","water":"Medium","soil":"Loamy",
                    "desc":"Rajma — popular legume in northern hill regions",
                    "tips":["Install trellis or support sticks for climbing growth",
                            "Spray neem-based insecticide to control pod borer",
                            "Harvest when pods are fully dry and firm"]},
    "pigeonpeas":  {"emoji":"🌿","season":"Kharif (Jun–Oct)","water":"Low","soil":"Sandy / Loam",
                    "desc":"Arhar / Toor Dal — drought-tolerant pulse crop",
                    "tips":["Excellent for intercropping with cereals",
                            "Use Fusarium wilt-resistant varieties",
                            "Matures in 100–120 days after sowing"]},
    "mothbeans":   {"emoji":"🫘","season":"Kharif","water":"Very Low","soil":"Sandy",
                    "desc":"Drought-hardy pulse — suited to arid and semi-arid regions",
                    "tips":["Can produce yield with very little rainfall",
                            "Best choice for dry, arid growing conditions",
                            "Fixes atmospheric nitrogen, improving soil fertility"]},
    "mungbean":    {"emoji":"🌱","season":"Kharif + Zaid","water":"Low","soil":"Sandy Loam",
                    "desc":"Green gram — fast-maturing, short-duration pulse",
                    "tips":["Ready for harvest in just 60–65 days",
                            "Can give 2–3 harvests in a single season",
                            "Spray fungicide early to prevent powdery mildew"]},
    "blackgram":   {"emoji":"🫘","season":"Kharif","water":"Low-Medium","soil":"Clay Loam",
                    "desc":"Urad Dal — essential pulse in South Indian cuisine",
                    "tips":["Monitor regularly for yellow mosaic virus",
                            "Control whitefly to prevent virus spread",
                            "Apply fungicide during high-humidity periods"]},
    "lentil":      {"emoji":"🫘","season":"Rabi (Oct–Mar)","water":"Low","soil":"Sandy Loam",
                    "desc":"Masoor Dal — cool-season pulse, rich in protein",
                    "tips":["Grows best in cool, dry weather",
                            "Weed control is critical in the first 40 days",
                            "Spray Mancozeb to manage rust disease"]},
    "pomegranate": {"emoji":"🍎","season":"Perennial","water":"Low","soil":"Sandy / Loam",
                    "desc":"High-value fruit — grown in Maharashtra and Karnataka",
                    "tips":["Drip irrigation is the most efficient method",
                            "Apply copper-based spray to prevent bacterial blight",
                            "Bahar treatment regulates and improves flowering"]},
    "banana":      {"emoji":"🍌","season":"Year Round","water":"High","soil":"Loamy",
                    "desc":"India's number one fruit crop by production volume",
                    "tips":["Choose Panama wilt-resistant varieties",
                            "Use pseudo stem for compost after harvest",
                            "Cover developing bunches to improve fruit quality"]},
    "mango":       {"emoji":"🥭","season":"Summer (Mar–Jun)","water":"Low-Medium","soil":"Alluvial",
                    "desc":"National fruit of India — king of tropical fruits",
                    "tips":["Use Paclobutrazol to regulate off-season flowering",
                            "Apply Imidacloprid to control mango hoppers",
                            "Regular pruning improves canopy and yield"]},
    "grapes":      {"emoji":"🍇","season":"Rabi (Oct–Feb)","water":"Medium","soil":"Sandy Loam",
                    "desc":"High-value fruit crop — major export from Maharashtra",
                    "tips":["Follow a strict fungicide schedule for mildew control",
                            "Pruning is essential for good bunch development",
                            "Bunch thinning improves fruit size and quality"]},
    "watermelon":  {"emoji":"🍉","season":"Summer / Zaid","water":"Medium","soil":"Sandy",
                    "desc":"Popular summer fruit — high water content, heat tolerant",
                    "tips":["Direct sow seeds — does not transplant well",
                            "Requires adequate pollinators for fruit set",
                            "Use protein bait traps to manage fruit fly"]},
    "muskmelon":   {"emoji":"🍈","season":"Summer / Zaid","water":"Medium","soil":"Sandy",
                    "desc":"Sweet melon — widely grown across North India",
                    "tips":["Drip irrigation improves sweetness and quality",
                            "Spray sulfur-based fungicide to control powdery mildew",
                            "Crop is ready for harvest in 75–80 days"]},
    "apple":       {"emoji":"🍎","season":"Summer (Jun–Sep)","water":"Medium","soil":"Loamy",
                    "desc":"Temperate fruit — grown in Himachal, J&K, Uttarakhand",
                    "tips":["Requires sufficient chilling hours for proper fruit set",
                            "Protect against apple scab and fire blight",
                            "Fruit thinning produces larger, better-quality apples"]},
    "orange":      {"emoji":"🍊","season":"Winter (Nov–Jan)","water":"Medium","soil":"Sandy Loam",
                    "desc":"Citrus fruit — Nagpur orange is world-famous",
                    "tips":["Apply copper spray to prevent citrus canker",
                            "Control psyllid insects to prevent greening disease",
                            "Ensure well-drained soil — citrus is waterlogging sensitive"]},
    "papaya":      {"emoji":"🍈","season":"Year Round","water":"Medium","soil":"Sandy Loam",
                    "desc":"Fast-growing fruit crop with high return on investment",
                    "tips":["Control whitefly to prevent papaya ring spot virus",
                            "Maintain a male to female ratio of 1:10",
                            "First harvest ready within 9–10 months of planting"]},
    "coconut":     {"emoji":"🥥","season":"Perennial","water":"High","soil":"Sandy / Loam",
                    "desc":"Tree of life — major crop along Kerala and Karnataka coasts",
                    "tips":["Protect palms from rhinoceros beetle damage",
                            "Apply ferrous sulfate to soil for micronutrient correction",
                            "Practice intercropping to maximize income per hectare"]},
    "cotton":      {"emoji":"🤍","season":"Kharif (May–Nov)","water":"Medium","soil":"Black Cotton",
                    "desc":"White gold — India is the world's largest cotton producer",
                    "tips":["Bt cotton varieties provide excellent bollworm protection",
                            "Apply Imidacloprid to manage sucking pests",
                            "Avoid excessive nitrogen — causes vegetative overgrowth"]},
    "jute":        {"emoji":"🌿","season":"Kharif (Mar–Jun)","water":"High","soil":"Alluvial",
                    "desc":"Golden fibre — mainly grown in West Bengal and Assam",
                    "tips":["Crop reaches harvest maturity in about 120 days",
                            "Apply Mancozeb to prevent stem rot disease",
                            "Follow proper water retting process for fibre quality"]},
    "coffee":      {"emoji":"☕","season":"Perennial","water":"High","soil":"Red Laterite",
                    "desc":"Plantation crop — grown in the hills of Karnataka and Kerala",
                    "tips":["Always grow under shade trees for best quality beans",
                            "Protect plants from white stem borer infestation",
                            "Wet processing method produces superior quality coffee"]},
}

CROP_EMOJIS = {k: v["emoji"] for k, v in CROP_INFO.items()}

# ── WEATHER API ────────────────────────────────────────────────────────────────
def get_weather(city):
    try:
        api_key = "9b8ac5eb7dc15a8c413ed690b9793507"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        data = requests.get(url, timeout=5).json()
        if data.get("cod") != 200:
            return None
        return {
            "temp":     round(data["main"]["temp"], 1),
            "humidity": data["main"]["humidity"],
            "rainfall": round(data.get("rain", {}).get("1h", 0), 1),
            "desc":     data["weather"][0]["description"].title(),
            "city":     data["name"]
        }
    except Exception:
        return None

# ── LOAD MODEL ─────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    return pickle.load(open("Model/crop_model.pkl", "rb"))
