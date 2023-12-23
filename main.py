import streamlit as st

st.title("Gupta Postoperative Respiratory Failure Risk Calculator")
st.write("This app is a simple calculator to predict the risk of postoperative respiratory failure, \
         i.e., requiring mechanical ventilation for over 48 hours post-surgery or unplanned \
         intubation within 30 days of surgery. This calculator is based on the paper \
         [Development and Validation of a Risk Calculator Predicting Postoperative Respiratory Failure](https://pubmed.ncbi.nlm.nih.gov/21757571/).")
st.write("Answer the questions below to calculate the estimated risk. ")

functional_status_pts = {
    "Independent": 0,
    "Partially dependent": 0.7678,
    "Totally dependent": 1.4046,

}
ASA_class_points = {
    "1 - A normal healthy patient": -3.5265,
    "2 - A patient with mild systemic disease": -2.0028,
    "3 - A patient with severe systemic disease": -0.6201,
    "4 - A patient with severe systemic disease that is a constant threat to life": 0.2441,
    "5 - A moribound patient who is not expected to survive without the operation": 0,
}
preoperative_sepsis_points = {
    "None": -0.7840,
    "Systemic inflammatory response syndrome": 0,
    "Sepsis": 0.2752,
    "Septic shock": 0.9035
}
emergency_case_points = {
    "Yes": 0,
    "No": -0.5739
}
surgery_points = {
    "Hernia surgery": 0,
    "Anorectal": -1.3530,
    "Aortic": 1.0781,
    "Bariatric": -1.0112,
    "Brain": 0.7336,
    "Breast": -2.6462,
    "Cardiac": 0.2744,
    "ENT": 0.1060,
    "Foregut/hepatopancreatobiliary": 0.9694,
    "GBAAS": -0.5668,
    "Intestinal": 0.5737,
    "Neck": -0.5271,
    "OB/GYN": 1.2431,
    "Orthopedic": -0.8577,
    "Other abdomen": 0.2416,
    "Peripheral vascular": -0.2389,
    "Skin": -0.3206,
    "Spine": -0.5220,
    "Thoracic": 0.6715,
    "Vein": -2.0080,
    "Urology": 0.3093
}

def calculate_natural_log_odds(functional_status, ASA_class, preoperative_sepsis, emergency_case, surgery):
    natural_log_odds = -1.7397 + functional_status_pts[functional_status] + ASA_class_points[ASA_class] + \
                       preoperative_sepsis_points[preoperative_sepsis] + emergency_case_points[emergency_case] + \
                       surgery_points[surgery]
    return natural_log_odds
def estimate_risk_probability(natural_log_odds):
    e = 2.718281828459045
    risk_probability = e**natural_log_odds / (1 + e**natural_log_odds)
    return risk_probability
st.subheader("Questions")
functional_status = st.radio("What is the patient's functional status?", ("Independent", "Partially dependent", "Totally dependent"), horizontal=True)
asa_class = st.selectbox("What is the patient's ASA class?", ("1 - A normal healthy patient", 
                                                          "2 - A patient with mild systemic disease", 
                                                          "3 - A patient with severe systemic disease", 
                                                          "4 - A patient with severe systemic disease that is a constant threat to life", 
                                                          "5 - A moribound patient who is not expected to survive without the operation", 
                                                          "6 - A declared brain-dead patient whose organs are being removed for donor purposes"),  
                                                          help = "See [Statement on ASA Physical Status Classification System](https://www.asahq.org/standards-and-practice-parameters/statement-on-asa-physical-status-classification-system) for more details and examples of each ASA class.")
preoperative_sepsis = st.radio("What is the patient's preoperative sepsis status?", ("None", "Systemic inflammatory response syndrome", "Sepsis", "Septic shock"), horizontal=True)
emergency_case = st.radio("Is this an emergency case?", ("No", "Yes"), horizontal=True)
surgery_type = st.selectbox("What type of surgery is this?", ("Hernia surgery", "Anorectal", "Aortic", "Bariatric", "Brain", "Breast", "Cardiac", "ENT", "Foregut/hepatopancreatobiliary", "GBAAS", "Intestinal", "Neck", "OB/GYN", "Orthopedic", "Other abdomen", "Peripheral vascular", "Skin", "Spine", "Thoracic", "Vein", "Urology"))
st.subheader("Risk Probability")
if asa_class.startswith("6"):
    st.write("The Gupta calculator is not applicable to patients who are declared brain-dead.")
    st.stop()
risk_points = calculate_natural_log_odds(functional_status, asa_class, preoperative_sepsis, emergency_case, surgery_type)
risk_probability = round(estimate_risk_probability(risk_points) * 1000)/10

st.write("The patient's estimated risk of postoperative respiratory failure is **" + str(risk_probability) + "%**.")