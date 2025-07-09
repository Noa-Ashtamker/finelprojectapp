# app.py - Streamlit interface without second offense stage
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model
model = joblib.load('final_model.pkl')

st.set_page_config(page_title="סיווג עבירות בניה", layout="centered")
st.title("🏗️ סיווג עבירות בניה")
st.subheader("הזן מאפיינים לצורך חיזוי האם האיתור יהפוך למנהלי")

# 1. מחוז
district = st.selectbox("מחוז", ["בחר...", "Center", "Jerusalem", "North", "South"])

# 2. רבעון איתור ראשון
q1 = st.selectbox("רבעון איתור ראשון", ["בחר...", "Q1", "Q2", "Q3", "Q4"])

# 3. אופי איתור ראשון
types = [
    "Earthworks and clearance", "Site preparation", "Roads and approaches",
    "Drilling and foundations", "Base for columns", "Infrastructure",
    "Skeleton – beginning", "Skeleton – advanced", "Skeleton – general",
    "new floor", "concrete floor", "main structure", "light structures",
    "mobile structures", "add-ons and reinforcements", "termination/disposal"
]
type1 = st.selectbox("אופי איתור ראשון", ["בחר..."] + types)

# 4. ייעוד קרקע
land_use = st.selectbox("ייעוד קרקע", ["בחר...", 
    "Agricultural area", "Beach/ River", "Industrial & Employment", 
    "Nature & Conservation", "Tourism & Commerce", "Village", 
    "Urban & Residential", "Unknown & Other"
])

# 5. סוג מבנה ראשון
structure1 = st.radio("סוג מבנה איתור ראשון", ["קל", "קשיח"])

# 6-7. אזורים
city_area = st.radio("אזור עירוני", ["כן", "לא"])
jewish = st.radio("אזור יהודי", ["כן", "לא"])

# יצירת הפיצ'רים
features = {
    # מחוז
    'District_Center': int(district == 'Center'),
    'District_Jerusalem': int(district == 'Jerusalem'),
    'District_North': int(district == 'North'),
    'District_South': int(district == 'South'),

    # רבעון
    'Quarter_Update_1_Q1': int(q1 == 'Q1'),
    'Quarter_Update_1_Q2': int(q1 == 'Q2'),
    'Quarter_Update_1_Q3': int(q1 == 'Q3'),
    'Quarter_Update_1_Q4': int(q1 == 'Q4'),
}

# אופי העבירה הראשונה
for t in types:
    features[f"Potential_Type_1_Grouped_{t}"] = int(type1 == t)

# אופי העבירה השנייה – NAN
for t in types:
    features[f"Potential_Type_2_Grouped_{t}"] = np.nan

# ייעוד קרקע
land_options = ["Agricultural area", "Beach/ River", "Industrial & Employment",
                "Nature & Conservation", "Tourism & Commerce", "Village",
                "Urban & Residential", "Unknown & Other"]
for land in land_options:
    features[f"District_land_designation_{land}"] = int(land_use == land)

# מבנה ראשון
features['Kal_Kashiah_1'] = int(structure1 == "קשיח")
features['Kal_Kashiah_2'] = np.nan  # לא ידוע בשלב הניבוי

# אזורים
features['city_erea'] = int(city_area == "כן")
features['jewish_e'] = int(jewish == "כן")

# כפתור חיזוי
if st.button("חשב תוצאה"):
    input_df = pd.DataFrame([features])
    prediction = model.predict(input_df)[0]
    if prediction == 1:
        st.success("האיתור צפוי להפוך למנהלי")
    else:
        st.info("האיתור יישאר מודיעיני")

# כפתור איפוס (רק עיצובי – מרענן את הדף)
if st.button("🔄 איפוס הטופס"):
    st.experimental_rerun()
