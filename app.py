import streamlit as st
import pandas as pd
import joblib

# ✅ טעינת המודל
model = joblib.load('final_model.pkl')

# ✅ הגדרת מצב איפוס
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False

# ✅ הגדרת כותרת
st.set_page_config(page_title="סיווג איתור מודיעיני", layout="centered")
st.title("🏗️ סיווג עבירות בניה")
st.subheader("הזן מאפיינים לצורך חיזוי האם האיתור יהפוך למנהלי")

# ✅ רשימות קבועות
districts = ["Center", "Jerusalem", "North", "South"]
quarters = ["Q1", "Q2", "Q3", "Q4"]
potential_types = [
    "Earthworks and clearance", "Site preparation", "Roads and approaches",
    "Drilling and foundations", "Base for columns", "Infrastructure",
    "Skeleton – beginning", "Skeleton – advanced", "Skeleton – general",
    "new floor", "concrete floor", "main structure", "light structures",
    "mobile structures", "add-ons and reinforcements", "termination/disposal"
]
land_options = ["Agricultural area", "Beach/ River", "Industrial & Employment",
                "Nature & Conservation", "Tourism & Commerce", "Village", "Urban & Residential", "Unknown & Other"]
structures = ["קל", "קשיח"]
binary_options = ["כן", "לא"]

# ✅ טופס
with st.form(key='classification_form'):

    # קלטים עם מפתחות ל-session_state
    district = st.selectbox("מחוז:", districts, index=None, placeholder="בחר מחוז", key="district")
    quarter_1 = st.selectbox("רבעון האיתור הראשון:", quarters, index=None, placeholder="בחר רבעון", key="quarter")
    potential_1 = st.selectbox("אופי האיתור הראשון:", potential_types, index=None, placeholder="בחר אופי איתור", key="potential")
    land_type = st.selectbox("ייעוד הקרקע במחוז:", land_options, index=None, placeholder="בחר ייעוד קרקע", key="land")
    structure_type = st.selectbox("סוג המבנה באיתור הראשון:", structures, index=None, placeholder="בחר סוג מבנה", key="structure")
    city_area = st.selectbox("האם מדובר באזור עירוני?", binary_options, index=None, placeholder="בחר כן / לא", key="city")
    jewish_area = st.selectbox("האם מדובר באזור יהודי?", binary_options, index=None, placeholder="בחר כן / לא", key="jewish")

    submitted = st.form_submit_button("חשב תחזית")
    reset = st.form_submit_button("אפס טופס")

# ✅ אפס לאחר ריצה
if st.session_state.reset_form:
    st.session_state.reset_form = False

# ✅ כפתור איפוס
if reset:
    for key in ["district", "quarter", "potential", "land", "structure", "city", "jewish"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.reset_form = True
    st.rerun()

# ✅ בדיקת תקינות קלט
valid_input = all([
    st.session_state.district is not None,
    st.session_state.quarter is not None,
    st.session_state.potential is not None,
    st.session_state.land is not None,
    st.session_state.structure is not None,
    st.session_state.city is not None,
    st.session_state.jewish is not None
])

# ✅ חישוב תחזית
if submitted:
    if not valid_input:
        st.error("אנא מלא את כל השדות לפני חישוב התחזית.")
    else:
        data = {}

        # מחוז
        for val in districts:
            data[f'District_{val}'] = int(st.session_state.district == val)

        # רבעון
        for q in quarters:
            data[f'Quarter_Update_1_{q}'] = int(st.session_state.quarter == q)
            data[f'Quarter_Update_2_{q}'] = int(st.session_state.quarter == q)

        # אופי עבירה
        for p in potential_types:
            key1 = f'Potential_Type_1_Grouped_{p}'
            key2 = f'Potential_Type_2_Grouped_{p}'
            data[key1] = int(st.session_state.potential == p)
            data[key2] = int(st.session_state.potential == p)

        # ייעוד קרקע
        for land in land_options:
            data[f'District_land_designation_{land}'] = int(st.session_state.land == land)

        # קשיחות
        data['Kal_Kashiah_1'] = int(st.session_state.structure == 'קשיח')
        data['Kal_Kashiah_2'] = int(st.session_state.structure == 'קשיח')

        # אזור עירוני ויהודי
        data['city_erea'] = int(st.session_state.city == 'כן')
        data['jewish_e'] = int(st.session_state.jewish == 'כן')

        # תחזית
        df = pd.DataFrame([data])
        prediction = model.predict(df)[0]
        result = "✔️ האיתור צפוי להפוך למנהלי" if prediction else "❌ האיתור לא צפוי להפוך למנהלי"
        st.success(result)
