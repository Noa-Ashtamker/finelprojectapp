import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load('final_model.pkl')

st.set_page_config(page_title="סיווג עבירות בניה", layout="centered")
st.title("🏗️ סיווג עבירות בניה")
st.subheader("הזן מאפיינים לצורך חיזוי האם האיתור יהפוך למנהלי")

# 1. מחוז
district = st.selectbox("מחוז", ["בחר מחוז", "Center", "Jerusalem", "North", "South"])

# 2. רבעון איתור ראשון
q1 = st.selectbox("רבעון איתור ראשון", ["בחר רבעון", "Q1", "Q2", "Q3", "Q4"])

# 3. רבעון איתור שני
q2 = st.selectbox("רבעון איתור שני", ["בחר רבעון", "Q1", "Q2", "Q3", "Q4"])

# 4-5. אופי איתור ראשון ושני
types = [
    "Earthworks and clearance", "Site preparation", "Roads and approaches",
    "Drilling and foundations", "Base for columns", "Infrastructure",
    "Skeleton – beginning", "Skeleton – advanced", "Skeleton – general",
    "new floor", "concrete floor", "main structure", "light structures",
    "mobile structures", "add-ons and reinforcements", "termination/disposal"
]
type1 = st.selectbox("אופי איתור ראשון", ["בחר אופי"] + types)
type2 = st.selectbox("אופי איתור שני", ["בחר אופי"] + types)

# 6. ייעוד קרקע
land_options = [
    "Agricultural area", "Beach/ River", "Industrial & Employment", 
    "Nature & Conservation", "Tourism & Commerce", "Village", 
    "Urban & Residential", "Unknown & Other"
]
land_use = st.selectbox("ייעוד קרקע", ["בחר ייעוד"] + land_options)

# 7-8. סוג מבנה ראשון ושני
structure1 = st.radio("סוג מבנה איתור ראשון", ["בחר", "קל", "קשיח"])
structure2 = st.radio("סוג מבנה איתור שני", ["בחר", "קל", "קשיח"])

# 9. אזור עירוני
city_area = st.radio("אזור עירוני", ["בחר", "כן", "לא"])

# 10. אזור יהודי
jewish = st.radio("אזור יהודי", ["בחר", "כן", "לא"])

# חיזוי רק אם נבחרו ערכים תקינים
if st.button("חשב תוצאה"):
    if "בחר" in [district, q1, q2, type1, type2, land_use, structure1, structure2, city_area, jewish]:
        st.warning("אנא מלא את כל השדות לפני ביצוע חיזוי.")
    else:
        features = {
            'District_Center': int(district == 'Center'),
            'District_Jerusalem': int(district == 'Jerusalem'),
            'District_North': int(district == 'North'),
            'District_South': int(district == 'South'),

            'Quarter_Update_1_Q1': int(q1 == 'Q1'),
            'Quarter_Update_1_Q2': int(q1 == 'Q2'),
            'Quarter_Update_1_Q3': int(q1 == 'Q3'),
            'Quarter_Update_1_Q4': int(q1 == 'Q4'),

            'Quarter_Update_2_Q1': int(q2 == 'Q1'),
            'Quarter_Update_2_Q2': int(q2 == 'Q2'),
            'Quarter_Update_2_Q3': int(q2 == 'Q3'),
            'Quarter_Update_2_Q4': int(q2 == 'Q4'),
        }

        for t in types:
            col1 = f"Potential_Type_1_Grouped_{t}"
            col2 = f"Potential_Type_2_Grouped_{t}"
            features[col1] = int(type1 == t)
            features[col2] = int(type2 == t)

        for land in land_options:
            features[f"District_land_designation_{land}"] = int(land_use == land)

        features['Kal_Kashiah_1'] = int(structure1 == "קשיח")
        features['Kal_Kashiah_2'] = int(structure2 == "קשיח")

        features['city_erea'] = int(city_area == "כן")
        features['jewish_e'] = int(jewish == "כן")

        input_df = pd.DataFrame([features])
        prediction = model.predict(input_df)[0]
        if prediction == 1:
            st.success("האיתור צפוי להפוך למנהלי")
        else:
            st.info("האיתור יישאר מודיעיני")
