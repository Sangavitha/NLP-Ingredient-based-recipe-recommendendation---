import streamlit as st
import pandas as pd
from recipe_matcher import load_data, get_recommendations

st.set_page_config(
    page_title="Indian Recipe Finder",
    page_icon="🍛",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400;500&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #FAFAF7; }

    .hero {
        background: linear-gradient(135deg, #C0392B, #E67E22);
        border-radius: 16px;
        padding: 28px 40px;
        color: white;
        margin-bottom: 20px;
        text-align: center;
    }
    .hero h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem;
        margin: 0;
    }
    .hero p { font-size: 1rem; opacity: 0.9; margin-top: 6px; }

    .stat-box {
        background: white;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        border: 1px solid #FAD7A0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .stat-number { font-size: 1.5rem; font-weight: 700; color: #C0392B; }
    .stat-label { font-size: 0.7rem; color: #666;
                  text-transform: uppercase; letter-spacing: 1px; }

    section[data-testid="stSidebar"] {
        background: #FEF9F0;
        border-right: 1px solid #FAD7A0;
    }

    .stButton > button {
        background: linear-gradient(135deg, #C0392B, #E67E22) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    .stButton > button:hover { opacity: 0.9 !important; }

    div[data-testid="stExpander"] {
        border: 1px solid #FAD7A0 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        margin-bottom: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ──────────────────────────────────────────────
@st.cache_data
def load():
    return load_data("data/IndianFoodDatasetCSV.csv")

with st.spinner("⏳ Loading..."):
    df = load()

# ══════════════════════════════════════════════════════════
# SIDEBAR — Compact Dropdowns
# ══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🎛️ Filters")
    st.markdown("---")

    cuisine = st.selectbox("🌍 Cuisine", [
        "All",
        "Indian",
        "North Indian Recipes",
        "South Indian Recipes",
        "Punjabi",
        "Bengali Recipes",
        "Gujarati Recipes",
        "Maharashtrian Recipes",
        "Kerala Recipes",
        "Tamil Nadu",
        "Andhra",
        "Chettinad",
        "Sindhi",
        "Mexican",
        "Chinese",
        "Thai",
        "Continental",
        "Fusion"
    ])

    course = st.selectbox("🍽️ Course", [
        "All",
        "Main Course",
        "Side Dish",
        "Lunch",
        "Dinner",
        "Appetizer",
        "Snack",
        "Dessert",
        "Indian Breakfast",
        "Brunch",
        "One Pot Dish"
    ])

    diet = st.selectbox("🥗 Diet", [
        "None",
        "Vegetarian",
        "Vegan",
        "Eggetarian",
        "Non Vegeterian",
        "High Protein Vegetarian",
        "High Protein Non Vegetarian",
        "Diabetic Friendly",
        "Gluten Free",
        "Sugar Free Diet",
        "No Onion No Garlic (Sattvic)"
    ])

    max_time = st.slider(
        "⏱️ Max Cook Time (mins)",
        min_value=5, max_value=180,
        value=60, step=5
    )

    st.markdown("---")

    # Active filters summary
    st.markdown("**Active Filters:**")
    if cuisine != "All":
        st.success(f"🌍 {cuisine}")
    if course != "All":
        st.success(f"🍽️ {course}")
    if diet != "None":
        st.success(f"🥗 {diet}")
    st.info(f"⏱️ Up to {max_time} mins")

# ══════════════════════════════════════════════════════════
# MAIN AREA
# ══════════════════════════════════════════════════════════

# Hero
st.markdown("""
<div class="hero">
    <h1>🍛 Indian Recipe Finder</h1>
    <p>Type your ingredients — we'll find the perfect Indian recipe!</p>
</div>
""", unsafe_allow_html=True)

# Stats
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="stat-box">
        <div class="stat-number">{len(df):,}</div>
        <div class="stat-label">Recipes</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="stat-box">
        <div class="stat-number">{df['cuisine'].nunique()}</div>
        <div class="stat-label">Cuisines</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="stat-box">
        <div class="stat-number">{df['diet'].nunique()}</div>
        <div class="stat-label">Diet Types</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="stat-box">
        <div class="stat-number">NLP</div>
        <div class="stat-label">Powered By</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Ingredient Input
user_input = st.text_area(
    "🥕 Enter your ingredients (separate with commas)",
    placeholder="e.g. paneer, onion, tomato, garlic, rice...",
    height=100
)
st.caption("💡 Tip: More ingredients = better matches!")

st.markdown("<br>", unsafe_allow_html=True)

# Search Button
if st.button("🔍 Find My Recipes", use_container_width=True):
    if not user_input.strip():
        st.warning("⚠️ Please enter at least one ingredient!")
    else:
        with st.spinner("🤖 Finding best matches..."):
            results = get_recommendations(
                user_input, df,
                cuisine_filter=cuisine,
                course_filter=course,
                diet_filter=diet if diet != "None" else None,
                max_time=max_time
            )

        if results.empty:
            st.error(
                "😕 No recipes found! "
                "Try 'All' for cuisine/course "
                "or increase cook time in sidebar."
            )
        else:
            st.success(
                f"✅ Found {len(results)} recipes "
                f"matching your ingredients!"
            )
            st.markdown("<br>", unsafe_allow_html=True)

            for _, row in results.iterrows():
                match = row['match_%']
                matched = int(row['matched_count'])
                total = int(row['total_user_ingredients'])

                with st.expander(
                    f"🍽️  {row['title']}  —  "
                    f"{row['match_label']}  ({match}%)"
                ):
                    # Tags row
                    tags = []
                    if pd.notna(row.get('cuisine')):
                        tags.append(f"🌍 {row['cuisine']}")
                    if pd.notna(row.get('diet')):
                        tags.append(f"🥗 {row['diet']}")
                    if pd.notna(row.get('course')):
                        tags.append(f"🍽️ {row['course']}")
                    if pd.notna(row.get('servings')):
                        tags.append(f"👥 Serves {row['servings']}")
                    st.markdown(
                        " &nbsp;|&nbsp; ".join(tags),
                        unsafe_allow_html=True
                    )
                    st.caption(
                        f"✅ {matched} out of {total} "
                        f"ingredients matched"
                    )
                    st.markdown("")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**📝 Ingredients Needed:**")
                        st.info(
                            str(row['ingredients'])[:500] + "..."
                            if len(str(row['ingredients'])) > 500
                            else str(row['ingredients'])
                        )
                    with col2:
                        st.markdown("**👨‍🍳 Instructions:**")
                        st.success(
                            str(row['instructions'])[:600] + "..."
                            if len(str(row['instructions'])) > 600
                            else str(row['instructions'])
                        )

                    if pd.notna(row.get('cook_time_mins')):
                        st.caption(
                            f"⏱️ Total time: "
                            f"{int(row['cook_time_mins'])} mins"
                        )

# Footer
st.markdown("---")
st.markdown(
    "<center><small>Built with Python • TF-IDF • Streamlit • "
    "Indian Food Dataset</small></center>",
    unsafe_allow_html=True
)