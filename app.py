import numpy as np
import pickle
import streamlit as st
import lightgbm as lgb

# Load the trained LightGBM model
pickle_in = open("best_model_LightGBM.pkl", "rb")
best_model_LightGBM = pickle.load(pickle_in)

def predict_sewing_time(features, sub_garment, sewing_units):
    """Function to predict sewing time using the LightGBM model with additional time adjustments."""
    base_prediction = best_model_LightGBM.predict([features])[0]
    
    # Additional time adjustments based on Sub Garment Type
    additional_time = {
        'G String': 25,
        'Cami': 30,
        'Tank Top': 35,
        'Boy Short': 75,
        'Thong': 50,
        'Men Brief': 65,
        'Boxer': 105,
        'Hipster': 55,
        'Brief': 70,
        'Bralette': 95,
    }
    
    adjusted_time = base_prediction + additional_time.get(sub_garment, 0)
    final_time = adjusted_time * sewing_units + 10 # Multiply by the number of sewing units
    
    return final_time

def main():
    # HTML for styling
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">TARGET SEWING TIME PREDICTOR</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    # Create input fields for each feature
    SMO_Gender = st.selectbox("Sewing Machine Operator Gender", options=["Male", "Female"])
    SMO_Age = st.number_input("Sewing Machine Operator Age", min_value=0, step=1)
    SMO_KPI_Grade = st.selectbox("Sewing Machine Operator KPI Grade", options=["Supper", "A", "B", "C", "Not Graded"])

    Brand = st.selectbox("Department", options=['Victoria Secret', 'Calvin Klein', 'Tommy John', 'LIDL', 'Nike', 'Lacoste'])
    Sub_Garment_Type = st.selectbox("Sub Garment Type", options=['G String', 'Cami', 'Tank Top', 'Thong', 'Hipster', 'Men Brief', 'Brief', 'Boy Short', 'Bralette', 'Boxer'])
    Sample_Type = st.selectbox("Sample Type", options=[ 'Proto Sample', 'SMS Sample', 'Fit Sample', 'Photoshoot Sample', 'Size Set Sample', 'Pre Production Sample', 'Red Tag Sample'])
    Embellishment_Level = st.selectbox("Embellishment Level", options=['No Embellishment', 'Simple', 'Moderate', 'Difficult'])
    Fabric_Complexity = st.selectbox("Fabric Complexity", options=['Regular', 'Difficult'])
    Sewing_Units = st.number_input("Sewing Units", min_value=1, step=1)
    
    # Mapping dictionaries
    kpi_grade_map = {'Supper': 5, 'A': 4, 'B': 3, 'C': 2, 'Not Graded': 1}
    fabric_map = {'Regular': 1, 'Difficult': 2}
    embellishment_map = {'No Embellishment': 1, 'Simple': 2, 'Moderate': 3, 'Difficult': 4}
    sample_type_map = {'Proto Sample': 1, 'SMS Sample': 2, 'Fit Sample': 3, 'Photoshoot Sample': 4, 'Size Set Sample': 5, 'Pre Production Sample': 6, 'Red Tag Sample': 7}
    sub_garment_map = {'G String': 1, 'Cami': 2, 'Tank Top': 3, 'Thong': 4, 'Hipster': 5, 'Men Brief': 6, 'Brief': 7, 'Boy Short': 8, 'Bralette': 9, 'Boxer': 10}
    brand_map={'Victoria Secret':1, 'Calvin Klein':2, 'Tommy John':3, 'LIDL':4, 'Nike':5, 'Lacoste':6}
    smo_gender_map={'Female':1, 'Male':2}
    
    # Convert categorical inputs to numerical values
    features = [
        smo_gender_map[SMO_Gender], 
        SMO_Age, 
        kpi_grade_map[SMO_KPI_Grade], 
        brand_map[Brand], 
        sub_garment_map[Sub_Garment_Type],
        sample_type_map[Sample_Type], 
        embellishment_map[Embellishment_Level], 
        fabric_map[Fabric_Complexity],
        Sewing_Units,
    ]
    
    # Predict button
    if st.button("Predict"):
        result = predict_sewing_time(features, Sub_Garment_Type, Sewing_Units)
        st.success(f"The predicted Target Sewing Time For SMO: {result:.2f} minutes")

if __name__ == '__main__':
    main()
