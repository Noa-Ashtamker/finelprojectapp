
# 🖼️ ממשק משתמש עם Streamlit – סיווג איתור מודיעיני
import streamlit as st
import pandas as pd
import joblib

# טעינת המודל
model = joblib.load('model.pkl')

st.set_page_config(page_title="סיווג איתור מודיעיני", layout="centered")
st.title("🏗️ סיווג עבירות בניה")
st.subheader("הזן מאפיינים לצורך חיזוי האם האיתור יהפוך למנהלי")

# טופס קלט
with st.form(key='classification_form'):

    # 🟦 מאפיין 1 – מחוז
    district = st.selectbox("מחוז: *", ['בחר...', 'Center', 'Jerusalem', 'North', 'South'])

    # 🟨 מאפיין 2 – רבעון איתור ראשון (רבעון שני נקבע לפי זה)
    quarter_1 = st.selectbox("רבעון האיתור הראשון: *", ['בחר...', 'Q1', 'Q2', 'Q3', 'Q4'])

    # 🟩 מאפיין 4 – אופי איתור ראשון (רבעון שני יקבל אותו אוטומטית)
    potential_types = [
        "Earthworks and clearance", "Site preparation", "Roads and approaches",
        "Drilling and foundations", "Base for columns", "Infrastructure",
        "Skeleton – beginning", "Skeleton – advanced", "Skeleton – general",
        "new floor", "concrete floor", "main structure", "light structures",
        "mobile structures", "add-ons and reinforcements", "termination/disposal"
    ]
    potential_1 = st.selectbox("אופי האיתור הראשון: *", ['בחר...'] + potential_types)

    # 🟫 מאפיין 6 – ייעוד קרקע
    land_options = [
        "Agricultural area", "Beach/ River", "Industrial & Employment", "Nature & Conservation",
        "Tourism & Commerce", "Village", "Urban & Residential", "Unknown & Other"
    ]
    land_type = st.selectbox("ייעוד הקרקע במחוז: *", ['בחר...'] + land_options)

    # 🟥 מאפיין 7 – סוג מבנה איתור ראשון (ושני)
    structure_type = st.selectbox("סוג המבנה באיתור הראשון: *", ['בחר...', 'קל', 'קשיח'])

    # 🟪 מאפיין 9 – אזור עירוני
    city_area = st.selectbox("האם מדובר באזור עירוני? *", ['בחר...', 'כן', 'לא'])

    # 🟦 מאפיין 10 – אזור יהודי
    jewish_area = st.selectbox("האם מדובר באזור יהודי? *", ['בחר...', 'כן', 'לא'])

    # ⬜ כפתורים
    submitted = st.form_submit_button("חשב תחזית")
    reset = st.form_submit_button("אפס טופס")

# ✅ תנאי לווידוא שכל השדות נבחרו
valid_input = all([
    district != 'בחר...',
    quarter_1 != 'בחר...',
    potential_1 != 'בחר...',
    land_type != 'בחר...',
    structure_type != 'בחר...',
    city_area != 'בחר...',
    jewish_area != 'בחר...'
])

if submitted:
    if not valid_input:
        st.error("אנא מלא את כל השדות לפני חישוב התחזית.")
    else:
        # 🧠 יצירת רשומת קלט לפיצ'רים הבינאריים
        data = {}

        # מחוז
        for val in ['Center', 'Jerusalem', 'North', 'South']:
            data[f'District_{val}'] = int(district == val)

        # רבעון
        for q in ['Q1', 'Q2', 'Q3', 'Q4']:
            data[f'Quarter_Update_1_{q}'] = int(quarter_1 == q)
            data[f'Quarter_Update_2_{q}'] = int(quarter_1 == q)  # זהה

        # אופי עבירה
        for p in potential_types:
            key1 = f'Potential_Type_1_Grouped_{p}'
            key2 = f'Potential_Type_2_Grouped_{p}'
            data[key1] = int(potential_1 == p)
            data[key2] = int(potential_1 == p)

        # ייעוד קרקע
        for land in land_options:
            data[f'District_land_designation_{land}'] = int(land_type == land)

        # קשיחות
        data['Kal_Kashiah_1'] = int(structure_type == 'קשיח')
        data['Kal_Kashiah_2'] = int(structure_type == 'קשיח')

        # אזור עירוני
        data['city_erea'] = int(city_area == 'כן')

        # אזור יהודי
        data['jewish_e'] = int(jewish_area == 'כן')

        # 🧮 הפעלת המודל
        input_df = pd.DataFrame([data])
        prediction = model.predict(input_df)[0]
        result_text = "✔️ האיתור צפוי להפוך למנהלי" if prediction else "❌ האיתור לא צפוי להפוך למנהלי"
        st.success(result_text)

elif reset:
    st.experimental_rerun()
