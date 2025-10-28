from django.shortcuts import render
import pickle
import numpy as np

# Load model
model_path = 'insurance/model/insurance_rf_model.sav'
loaded_model = pickle.load(open(model_path, 'rb'))

def home(request):
    result = None
    values = {'age': '', 'sex': '', 'bmi': '', 'children': '', 'smoker': ''}

    if request.method == 'POST':
        if 'clear' in request.POST:
            # Clear button pressed – reset all
            result = None
            values = {'age': '', 'sex': '', 'bmi': '', 'children': '', 'smoker': ''}
        else:
            # Predict button pressed
            values = {
                'age': request.POST.get('age', ''),
                'sex': request.POST.get('sex', ''),
                'bmi': request.POST.get('bmi', ''),
                'children': request.POST.get('children', ''),
                'smoker': request.POST.get('smoker', ''),
            }

            try:
                features = np.array([[float(values['age']), int(values['sex']),
                                      float(values['bmi']), int(values['children']),
                                      int(values['smoker'])]])
                prediction = loaded_model.predict(features)
                result = round(prediction[0], 2)
            except Exception:
                result = "Invalid Input"

    return render(request, 'insurance/insurance_home.html', {'result': result, 'values': values})
