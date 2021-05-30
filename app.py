from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

model_file = open('model.pkl', 'rb')
model = pickle.load(model_file, encoding='bytes')

@app.route('/')
def index():
    return render_template('index.html', insurance_cost=0)

@app.route('/predict', methods=['POST'])
def predict():
    '''
    Predict the insurance cost based on user inputs
    and render the result to the html page
    '''
    age, sex, smoker = [x for x in request.form.values()]

    data = []

    data.append(int(age))
    if sex == 'Laki-laki':
        data.extend([0, 1])
    else:
        data.extend([1, 0])

    if smoker == 'Ya':
        data.extend([0, 1])
    else:
        data.extend([1, 0])
    
    prediction = model.predict([data])

    output = round(prediction[0], 2)

    return render_template('index.html', insurance_cost=output, age=age, sex=sex, smoker=smoker)

@app.route('/predict_api', methods=['GET', 'POST'])
def predict_api():
    """
    Route for external API request with JSON data
    and returns all data + predicted insurance cost
    """
    item = request.json
    data = []

    data.append(int(item["Age"]))
    if item["Sex"] == 'Male':
        data.extend([0, 1])
    else:
        data.extend([1, 0])

    if item["Smoker"] == 'Yes':
        data.extend([0, 1])
    else:
        data.extend([1, 0])
    
    prediction = model.predict([data])

    output = round(prediction[0], 2)
    item["Insurance Cost"] = output

    res = jsonify(item)

    return res


if __name__ == '__main__':
    app.run(debug=True)