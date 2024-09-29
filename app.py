from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
import csv

app = Flask(__name__)

# Load data from CSV file
data = pd.read_csv('disease.csv')
data['Symptoms'] = data['Symptoms'].apply(lambda x: x.split(';'))

descriptions = {}
with open('disease_descriptions.csv', mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        descriptions[row['Disease']] = row['Description']

doctors = {}
with open('doctors.csv', mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        disease = row['Disease']
        doctor_info = f"{row['Doctor_Type']} - {row['Doctor_Name']}"
        if disease in doctors:
            doctors[disease].append(doctor_info)
        else:
            doctors[disease] = [doctor_info]

# Prepare symptom and disease lists
symptoms = list(set([symptom for sublist in data['Symptoms'] for symptom in sublist]))
diseases = data['Disease'].unique()

# Create input features (X) and target output (y)
X = np.array([[1 if symptom in symptoms_list else 0 for symptom in symptoms] for symptoms_list in data['Symptoms']])
y = np.array([[1 if d == disease else 0 for d in diseases] for disease in data['Disease']])

class SimpleNN:
    def __init__(self, input_size, hidden_size, output_size):
        self.W1 = np.random.rand(input_size, hidden_size)
        self.W2 = np.random.rand(hidden_size, output_size)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def feedforward(self, X):
        self.hidden = self.sigmoid(np.dot(X, self.W1))
        self.output = self.sigmoid(np.dot(self.hidden, self.W2))
        return self.output

    def backpropagation(self, X, y, learning_rate):
        output_error = y - self.output
        output_delta = output_error * self.sigmoid_derivative(self.output)

        hidden_error = output_delta.dot(self.W2.T)
        hidden_delta = hidden_error * self.sigmoid_derivative(self.hidden)

        self.W2 += self.hidden.T.dot(output_delta) * learning_rate
        self.W1 += X.T.dot(hidden_delta) * learning_rate

    def train(self, X, y, epochs, learning_rate):
        for _ in range(epochs):
            self.feedforward(X)
            self.backpropagation(X, y, learning_rate)

# Train the neural network
nn = SimpleNN(len(symptoms), 5, len(diseases))
nn.train(X, y, epochs=10000, learning_rate=0.1)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    symptoms_input = data['symptoms']

    # Create input array for the model
    sample_input = np.array([[1 if symptom in symptoms_input else 0 for symptom in symptoms]])
    output = nn.feedforward(sample_input)

    # Get predictions
    predictions = {disease: output[0][i] for i, disease in enumerate(diseases)}
    sorted_predictions = sorted(predictions.items(), key=lambda item: item[1], reverse=True)

    # Prepare top 5 predictions
    top_predictions = [
        {
            'disease': sorted_predictions[i][0],
            'probability': sorted_predictions[i][1],
            'description': descriptions.get(sorted_predictions[i][0], ''),
            'doctors': doctors.get(sorted_predictions[i][0], [])
        } 
        for i in range(min(5, len(sorted_predictions)))
    ]

    return jsonify(top_predictions=top_predictions)

@app.route('/submit', methods=['POST'])
def submit():
    disease = request.form['disease']
    symptoms = request.form.getlist('symptoms')
    symptoms_str = ';'.join(symptoms)

    with open('disease.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([disease, symptoms_str])

    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True)
