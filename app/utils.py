from pathlib import Path
import os
import random

import joblib
import pandas as pd
from django.conf import settings

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


BASE_DIR = Path(__file__).resolve().parent.parent

heart_model = joblib.load(BASE_DIR / "models" / "heart_model.pkl")
heart_features = joblib.load(BASE_DIR / "models" / "heart_features.pkl")

diabetes_model = joblib.load(BASE_DIR / "models" / "diabetes_model.pkl")
diabetes_features = joblib.load(BASE_DIR / "models" / "diabetes_features.pkl")

stress_model = joblib.load(BASE_DIR / "models" / "stress_model.pkl")
stress_features = joblib.load(BASE_DIR / "models" / "stress_features.pkl")


def safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def _rng(seed_value, salt=0):
    try:
        seed = int(abs(float(seed_value)) * 1000)
    except Exception:
        seed = sum(ord(c) for c in str(seed_value))
    return random.Random(seed + salt)


def _pick_one_hot(row, columns, rng, allow_none=True):
    for c in columns:
        row[c] = 0

    if not columns:
        return

    pool = columns[:] + ([None] if allow_none else [])
    chosen = rng.choice(pool)
    if chosen is not None:
        row[chosen] = 1


def build_heart_input(age):
    rng = _rng(age, 11)
    row = {f: 0 for f in heart_features}

    row["age"] = max(18, min(90, int(safe_float(age, 40))))
    row["sex"] = rng.randint(0, 1)
    row["trestbps"] = rng.randint(100, 160)
    row["chol"] = rng.randint(140, 320)
    row["fbs"] = rng.randint(0, 1)
    row["thalach"] = rng.randint(110, 190)
    row["exang"] = rng.randint(0, 1)
    row["oldpeak"] = round(rng.uniform(0.0, 4.5), 1)
    row["slope"] = rng.choice([0, 1, 2])
    row["ca"] = rng.randint(0, 3)

    _pick_one_hot(row, ["cp_1", "cp_2", "cp_3"], rng)
    _pick_one_hot(row, ["restecg_1", "restecg_2"], rng)
    _pick_one_hot(row, ["thal_1", "thal_2", "thal_3"], rng)

    return row


def build_diabetes_input(glucose):
    rng = _rng(glucose, 23)
    row = {f: 0 for f in diabetes_features}

    row["Pregnancies"] = rng.randint(0, 5)
    row["Glucose"] = max(60, min(260, safe_float(glucose, 110)))
    row["BloodPressure"] = rng.randint(70, 130)
    row["SkinThickness"] = rng.randint(10, 45)
    row["Insulin"] = rng.randint(15, 250)
    row["BMI"] = round(rng.uniform(18.0, 39.0), 1)
    row["DiabetesPedigreeFunction"] = round(rng.uniform(0.1, 1.6), 2)
    row["Age"] = rng.randint(18, 70)

    return row


STRESS_BASES = [
    "Choose your gender",
    "What is your course?",
    "Your current year of Study",
    "What is your CGPA?",
    "Marital status",
    "Do you have Depression?",
    "Do you have Anxiety?",
    "Do you have Panic attack?",
    "Did you seek any specialist for a treatment?",
]


def build_stress_input(age):
    rng = _rng(age, 37)
    row = {f: 0 for f in stress_features}

    if "Age" in row:
        row["Age"] = max(15, min(40, int(safe_float(age, 21))))

    for base in STRESS_BASES:
        cols = [c for c in stress_features if c.startswith(base + "_")]
        if cols:
            for c in cols:
                row[c] = 0
            chosen = rng.choice(cols + [None])
            if chosen is not None:
                row[chosen] = 1

    return row


def predict_percentage(model, features, row):
    df = pd.DataFrame([row], columns=features)

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(df)
        if probs.ndim == 2 and probs.shape[1] > 1:
            return round(float(probs[0][1]) * 100, 2)
        return round(float(probs[0][0]) * 100, 2)

    pred = model.predict(df)[0]
    return 100.0 if int(pred) == 1 else 0.0


def local_advice(condition, risk_percent, main_value):
    if condition == "heart":
        if risk_percent >= 70:
            return (
                f"High heart risk detected for age {main_value}.\n"
                "Do 30–40 minutes of brisk walking or cycling 5 days a week.\n"
                "Reduce fried food, salt, smoking, and late-night heavy meals.\n"
                "Track BP and cholesterol regularly and book a doctor check-up."
            )
        if risk_percent >= 40:
            return (
                "Moderate heart risk.\n"
                "Add daily walking, light cardio, and more vegetables and fiber.\n"
                "Keep blood pressure, sleep, and stress consistent.\n"
                "Try 10 minutes of deep breathing twice a day."
            )
        return (
            "Low heart risk.\n"
            "Keep 7–8 hours sleep, daily walking, stretching, and balanced meals.\n"
            "Continue regular activity and avoid long sitting hours."
        )

    if condition == "diabetes":
        if risk_percent >= 70:
            return (
                f"High diabetes risk detected with glucose value {main_value}.\n"
                "Use a low-sugar, high-fiber diet.\n"
                "Walk for 15–20 minutes after meals.\n"
                "Limit sweets, soft drinks, and refined carbs.\n"
                "Check sugar regularly and consult a clinician."
            )
        if risk_percent >= 40:
            return (
                "Moderate diabetes risk.\n"
                "Use balanced portions, protein + fiber meals, and regular walking.\n"
                "Reduce sugary snacks and stay hydrated.\n"
                "Add light home exercise 5 days a week."
            )
        return (
            "Low diabetes risk.\n"
            "Keep a stable meal routine, daily movement, and consistent sleep.\n"
            "Continue healthy carbs, protein, and fiber balance."
        )

    if condition == "stress":
        if risk_percent >= 70:
            return (
                "High stress signal.\n"
                "Do 4-7-8 breathing for 5 rounds, stretch shoulders, and take screen breaks.\n"
                "Walk for 15 minutes, reduce caffeine, and sleep on time.\n"
                "Talk to someone you trust if pressure feels heavy."
            )
        if risk_percent >= 40:
            return (
                "Moderate stress signal.\n"
                "Try deep breathing, short walks, and a fixed sleep schedule.\n"
                "Study in 25-minute blocks with 5-minute breaks.\n"
                "Reduce multitasking and keep one task at a time."
            )
        return (
            "Low stress signal.\n"
            "Maintain your current routine, stretch daily, and stay active.\n"
            "Keep hydration, sleep, and short mindful breaks in place."
        )

    return "Keep a balanced routine and monitor your health regularly."


def get_advice(condition, risk_percent, main_value):
    fallback = local_advice(condition, risk_percent, main_value)

    api_key = getattr(settings, "NVIDIA_API_KEY", None)
    if not api_key or OpenAI is None:
        return fallback

    try:
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key,
        )

        prompt = (
            f"You are a concise health assistant.\n"
            f"Condition: {condition}\n"
            f"Risk percentage: {risk_percent}%\n"
            f"Main user value: {main_value}\n\n"
            "Give 4 short points only:\n"
            "1) what this means\n"
            "2) one exercise\n"
            "3) one diet/lifestyle recommendation\n"
            "4) one next step\n"
            "Keep it simple, supportive, and not alarming."
        )

        completion = client.chat.completions.create(
            model="meta/llama3-70b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            top_p=1,
            max_tokens=250,
        )

        text = completion.choices[0].message.content.strip()
        return text or fallback
    except Exception:
        return fallback