import streamlit as st

def compute_cvh_score(diet, pa_minutes, nicotine_status, sleep_hours, bmi, non_hdl_cholesterol, 
                      blood_glucose, systolic_bp, diastolic_bp, is_treated_bp=False, is_indoor_smoker=False):
    
    try:
        # Diet score (assuming diet is given as percentile for populations or MEPA score for individuals)
        if diet >= 95:
            diet_score = 100
        elif diet >= 75:
            diet_score = 80
        elif diet >= 50:
            diet_score = 50
        elif diet >= 25:
            diet_score = 25
        else:
            diet_score = 0

        # PA score
        if pa_minutes >= 150:
            pa_score = 100
        elif pa_minutes >= 120:
            pa_score = 90
        elif pa_minutes >= 90:
            pa_score = 80
        elif pa_minutes >= 60:
            pa_score = 60
        elif pa_minutes >= 30:
            pa_score = 40
        elif pa_minutes >= 1:
            pa_score = 20
        else:
            pa_score = 0

        # Nicotine score
        nicotine_scores = {
            "never": 100,
            "quit_5y": 75,
            "quit_1-5y": 50,
            "quit_<1y_or_nds": 25,
            "current": 0
        }
        nicotine_score = nicotine_scores.get(nicotine_status, 0)
        if is_indoor_smoker and nicotine_score > 0:
            nicotine_score -= 20

        # Sleep score
        if 7 <= sleep_hours < 9:
            sleep_score = 100
        elif 9 <= sleep_hours < 10:
            sleep_score = 90
        elif 6 <= sleep_hours < 7:
            sleep_score = 70
        elif 5 <= sleep_hours < 6 or sleep_hours >= 10:
            sleep_score = 40
        elif 4 <= sleep_hours < 5:
            sleep_score = 20
        else:
            sleep_score = 0

        # BMI score
        if bmi < 25:
            bmi_score = 100
        elif 25 <= bmi < 30:
            bmi_score = 70
        elif 30 <= bmi < 35:
            bmi_score = 30
        elif 35 <= bmi < 40:
            bmi_score = 15
        else:
            bmi_score = 0

        # Non-HDL cholesterol score
        if non_hdl_cholesterol < 130:
            cholesterol_score = 100
        elif 130 <= non_hdl_cholesterol < 160:
            cholesterol_score = 60
        elif 160 <= non_hdl_cholesterol < 190:
            cholesterol_score = 40
        elif 190 <= non_hdl_cholesterol < 220:
            cholesterol_score = 20
        else:
            cholesterol_score = 0
        if is_treated_bp:
            cholesterol_score -= 20

        # Blood glucose score (assuming given as FBG, adjust accordingly for HbA1c)
        if blood_glucose < 100:  # Or check HbA1c
            glucose_score = 100
        elif 100 <= blood_glucose < 126:  # Or check HbA1c
            glucose_score = 60
        # Add other ranges based on HbA1c if needed

        # BP score
        if systolic_bp < 120 and diastolic_bp < 80:
            bp_score = 100
        elif 120 <= systolic_bp < 130 and diastolic_bp < 80:
            bp_score = 75
        elif 130 <= systolic_bp < 140 or 80 <= diastolic_bp < 90:
            bp_score = 50
        elif 140 <= systolic_bp < 160 or 90 <= diastolic_bp < 100:
            bp_score = 25
        else:
            bp_score = 0
        if is_treated_bp:
            bp_score -= 20

        # Averaging the scores
        total_score = (diet_score + pa_score + nicotine_score + sleep_score + bmi_score + cholesterol_score + glucose_score + bp_score)/8
        return total_score
    
    except Exception as ex:
        return "Cannot compute"


def initialize_health_params():

#Set defaults
    st.set_page_config(page_title="Set User Profile", page_icon="📈")

    st.markdown("Set User Profile")

    st.title("User Profile")
    user_input = st.text_area("Add additional text about yourself")


    bmi=st.slider("BMI", 20,35,st.session_state.bmi)
    age=st.slider("Age", 20,90,st.session_state.age)
    gender=st.radio("Sex", ['male','female'],st.session_state.gender)
    nicotine=st.radio("Nicotine", ['current','former','never'],st.session_state.nicotine)
    mepa=st.slider("MEPA Percentile", 0,100,st.session_state.mepa)
    sleep=st.slider("Sleep", 3,10, st.session_state.sleep)
    lipids=st.slider("Lipids (non-HDL)", 50,500, st.session_state.lipids)
    pa=st.slider("Physical Activity mins/week", 0,300,st.session_state.pa)

    glucose=st.slider("Glucose mg/dL", 50,500, st.session_state.glucose)
    sbp=st.slider("Systolic BP", 50,250, st.session_state.sbp)
    dbp=st.slider("Diastolic BP", 40,200, st.session_state.dbp)
    is_treated_bp=True
    is_indoor_smoker=False
    
        #Compute Score
    # score = compute_cvh_score(mepa, pa, nicotine, sleep, bmi, lipids, glucose=0, sbp=0, dbp=0, is_treated_bp=False, is_indoor_smoker=False)
    st.sidebar.header(
        f"""
            Profile Score: {compute_cvh_score(mepa, pa, nicotine, sleep, bmi, lipids, glucose, sbp, dbp, is_treated_bp=False, is_indoor_smoker=False)}
            Is a {gender}\n
            Age {age}\n
            \n
            BMI {bmi}\n
            Smoking {nicotine}\n
            Sleeps avg ~{sleep} hours/day \n
            Works out ~{pa} mins/day
            \n
            has non-HLD ~{lipids}\n
            eats MEPA Percentile {mepa}
    """
    )  


    st.session_state.bmi=bmi
    st.session_state.age=age
    st.session_state.gender=[idx for idx,val in enumerate(['male','female']) if val == gender][0]
    st.session_state.nicotine=[idx for idx,val in enumerate(['current','former','never']) if val == nicotine][0]
    st.session_state.mepa=mepa
    st.session_state.sleep=sleep
    st.session_state.lipids=lipids
    st.session_state.pa=pa
    st.session_state.glucose=glucose
    st.session_state.sbp=sbp  

def main():
    initialize_health_params()

if __name__ == '__main__':
    main()
