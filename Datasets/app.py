from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

# Set the path to the templates directory
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Patient Page', 'templates'))

app = Flask(__name__, template_folder=template_dir)

# Load your datasets
symptoms_df = pd.read_csv('Datasets/Symptoms.csv')
diseases_df = pd.read_csv('Datasets/Diseases.csv')
diseases_symptoms_df = pd.read_csv('Datasets/Training.csv', encoding='latin1')

symptoms = symptoms_df['Symptoms'].tolist()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_diseases', methods=['POST'])
def get_diseases():
    user_symptoms = request.form['symptoms'].split(',')
    user_symptoms = [symptom.strip().capitalize() for symptom in user_symptoms]

    valid_symptoms = [symptom for symptom in user_symptoms if symptom in symptoms]

    if not valid_symptoms:
        return "No valid symptoms were found."

    mask = [symptoms.index(symptom) for symptom in valid_symptoms]
    matching_scores = diseases_symptoms_df.iloc[:, 1:].iloc[:, mask].sum(axis=1)
    matching_diseases = diseases_symptoms_df[matching_scores == len(valid_symptoms)]['Disease'].tolist()

    if matching_diseases:
        return "Matching Diseases: " + ", ".join(matching_diseases)
    else:
        return "No diseases found."

@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    return jsonify(symptoms)

if __name__ == '__main__':
    app.run(debug=True)
