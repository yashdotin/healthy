from django.shortcuts import render

from .utils import (
    build_heart_input,
    build_diabetes_input,
    build_stress_input,
    get_advice,
    heart_features,
    heart_model,
    diabetes_features,
    diabetes_model,
    stress_features,
    stress_model,
    predict_percentage,
    safe_float,
)


def home(request):
    return render(request, "index.html")


def heart(request):
    result = None
    risk_percent = None
    advice = None
    main_value = None

    if request.method == "POST":
        main_value = safe_float(request.POST.get("age", 0), 40)
        row = build_heart_input(main_value)
        risk_percent = predict_percentage(heart_model, heart_features, row)
        result = "High Risk ❤️" if risk_percent >= 60 else "Low Risk 💚"
        advice = get_advice("heart", risk_percent, main_value)

    return render(
        request,
        "heart.html",
        {
            "result": result,
            "risk_percent": risk_percent,
            "advice": advice,
            "main_value": main_value,
        },
    )


def diabetes(request):
    result = None
    risk_percent = None
    advice = None
    main_value = None

    if request.method == "POST":
        main_value = safe_float(request.POST.get("glucose", 0), 110)
        row = build_diabetes_input(main_value)
        risk_percent = predict_percentage(diabetes_model, diabetes_features, row)
        result = "Positive 🧪" if risk_percent >= 60 else "Negative ✅"
        advice = get_advice("diabetes", risk_percent, main_value)

    return render(
        request,
        "diabetes.html",
        {
            "result": result,
            "risk_percent": risk_percent,
            "advice": advice,
            "main_value": main_value,
        },
    )


def stress(request):
    result = None
    risk_percent = None
    advice = None
    main_value = None

    if request.method == "POST":
        main_value = safe_float(request.POST.get("age", 0), 21)
        row = build_stress_input(main_value)
        risk_percent = predict_percentage(stress_model, stress_features, row)
        result = "High Stress 😰" if risk_percent >= 60 else "Low Stress 😊"
        advice = get_advice("stress", risk_percent, main_value)

    return render(
        request,
        "stress.html",
        {
            "result": result,
            "risk_percent": risk_percent,
            "advice": advice,
            "main_value": main_value,
        },
    )