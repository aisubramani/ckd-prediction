from django.shortcuts import render
from django.conf import settings
import os
import pickle
import sklearn

# Load the model
model_path = os.path.join(settings.BASE_DIR, 'predictor', 'final_RF_Model.sav')
load_model = pickle.load(open(model_path, 'rb'))

def home(request):
    result = None
    form_data = {
        "albumin_level": "",
        "blood_glucose_random": "",
        "blood_urea": "",
        "serum_creatinine": "",
        "packed_cell_volume": "",
        "White_blood_cell_count": ""
    }

    if request.method == "POST":
        if "clear" in request.POST:
            # Clear button pressed, return empty form
            return render(request, "predictor/home.html", {"result": None, "form_data": form_data})

        # Otherwise, process prediction
        form_data["albumin_level"] = request.POST.get("albumin_level", "")
        form_data["blood_glucose_random"] = request.POST.get("blood_glucose_random", "")
        form_data["blood_urea"] = request.POST.get("blood_urea", "")
        form_data["serum_creatinine"] = request.POST.get("serum_creatinine", "")
        form_data["packed_cell_volume"] = request.POST.get("packed_cell_volume", "")
        form_data["White_blood_cell_count"] = request.POST.get("White_blood_cell_count", "")

        try:
            prediction_input = [
                float(form_data["albumin_level"]),
                float(form_data["blood_glucose_random"]),
                float(form_data["blood_urea"]),
                float(form_data["serum_creatinine"]),
                float(form_data["packed_cell_volume"]),
                float(form_data["White_blood_cell_count"])
            ]

            prediction = load_model.predict([prediction_input])

            if prediction[0] == 1:
                 result = '<span style="color:red;">🩺 Positive , The patient is likely to have Chronic Kidney Disease (CKD).</span>'
            else:
                result = '<span style="color:green;">✅ Negative , The patient is likely NOT to have Chronic Kidney Disease (CKD).</span>'
            
        except ValueError:
            result = "⚠️ Invalid input. Please enter valid numeric values."

    return render(request, "predictor/home.html", {"result": result, "form_data": form_data})