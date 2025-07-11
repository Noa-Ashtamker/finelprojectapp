import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load('final_model.pkl')

st.set_page_config(page_title="סיווג עבירות בניה", layout="centered")
st.title("🏗️ סיווג עבירות בניה")
st.subheader("הזן מאפיינים לצורך חיזוי האם האיתור יהפוך למנהלי")

# פונקציה לאיפוס הטופס
def reset_form():
    st.session_state.clear()

# שדות חובה
def required_select(label, options):
    selected = st.selectbox(label, ["בחר"] + options, key=label)
    if selected == "בחר":
        st.warning(f"אנא בחר ערך עבור {label}")
        st.stop()
    return selected

def required_radio(label, options):
    selected = st.radio(label, options, key=label)
    if selected is None:
        st.warning(f"אנא בחר ערך עבור {label}")
        st.stop()
    return selected

# 1. מחוז
district = required_select("מחוז", ["Center", "Jerusalem", "North", "South"])

# 2. רבעון איתור ראשון
q1 = required_select("רבעון איתור ראשון", ["Q1", "Q2", "Q3", "Q4"])

# 3. אופי איתור ראשון
types = [
    "Earthworks and clearance", "Site preparation", "Roads and approaches",
    "Drilling and foundations", "Base for columns", "Infrastructure",
    "Skeleton – beginning", "Skeleton – advanced", "Skeleton – general",
    "new floor", "concrete floor", "main structure", "light structures",
    "mobile structures", "add-ons and reinforcements", "termination/disposal"
]
type1 = required_select("אופי איתור ראשון", types)

# 4. ייעוד קרקע
land_use = required_select("ייעוד קרקע", [
    "Agricultural area", "Beach/ River", "Industrial & Employment", 
    "Nature & Conservation", "Tourism & Commerce", "Village", 
    "Urban & Residential", "Unknown & Other"
])

# 5. סוג מבנה ראשון
structure1 = required_radio("סוג מבנה איתור ראשון", ["קל", "קשיח"])

# 6. אזור עירוני
city_area = required_radio("אזור עירוני", ["כן", "לא"])

# 7. אזור יהודי
jewish = required_radio("אזור יהודי", ["כן", "לא"])

# יצירת הקלט למודל
features = {
    'District_Center': int(district == 'Center'),
    'District_Jerusalem': int(district == 'Jerusalem'),
    'District_North': int(district == 'North'),
    'District_South': int(district == 'South'),
    'Quarter_Update_1_Q1': int(q1 == 'Q1'),
    'Quarter_Update_1_Q2': int(q1 == 'Q2'),
    'Quarter_Update_1_Q3': int(q1 == 'Q3'),
    'Quarter_Update_1_Q4': int(q1 == 'Q4'),
    'Kal_Kashiah_1': int(structure1 == "קשיח"),
    'city_erea': int(city_area == "כן"),
    'jewish_e': int(jewish == "כן"),
}

# פיצ'רים של אופי עבירה ראשון
for t in types:
    features[f"Potential_Type_1_Grouped_{t}"] = int(type1 == t)

# ייעוד קרקע
lands = [
    "Agricultural area", "Beach/ River", "Industrial & Employment",
    "Nature & Conservation", "Tourism & Commerce", "Village",
    "Urban & Residential", "Unknown & Other"
]
for land in lands:
    features[f"District_land_designation_{land}"] = int(land_use == land)

# לחיזוי
if st.button("חשב תוצאה"):
    input_df = pd.DataFrame([features])
    prediction = model.predict(input_df)[0]
    if prediction == 1:
        st.success("✔️ האיתור צפוי להפוך למנהלי")
    else:
        st.info("ℹ️ האיתור יישאר מודיעיני")

# כפתור לאיפוס הטופס
if st.button("איפוס הטופס"):
    reset_form()
