"""
NAAN MUDHALVAN - NM1130 AI AND DIGITAL SKILLS
EX.NO: 3  |  AI Applications
------------------------------------------------------------------
Department  : CSE (AI & ML)
College     : University College of Engineering (BIT Campus), Anna University, Tiruchirappalli

Aim
---
To demonstrate how AI is used in real-world fields. Every application follows
the same working mechanism given in the notes:

    Collect data -> Process data -> Learn patterns -> Generate output

Applications implemented
------------------------
1. Healthcare            - disease (tumour) prediction
2. Banking and Finance   - fraud detection
3. E-commerce / Media    - product recommendation
4. Agriculture           - crop yield prediction

Libraries : numpy, scikit-learn
Run       : python ai_applications.py
"""

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity

RANDOM_STATE = 7


def heading(title: str) -> None:
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# ---------------------------------------------------------------------------
# 1. HEALTHCARE - early detection of serious disease
# ---------------------------------------------------------------------------
def healthcare_demo() -> None:
    heading("1. HEALTHCARE - Disease prediction from medical measurements")
    data = load_breast_cancer()                                  # step 1: collect data
    X_train, X_test, y_train, y_test = train_test_split(         # step 2: process data
        data.data, data.target, test_size=0.25, random_state=RANDOM_STATE, stratify=data.target
    )
    model = RandomForestClassifier(n_estimators=150, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)                                  # step 3: learn patterns

    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"  Dataset  : {data.data.shape[0]} patients, {data.data.shape[1]} measurements each")
    print(f"  Accuracy : {accuracy:.2%} on unseen patients")

    patient = X_test[0].reshape(1, -1)                           # step 4: generate output
    probability = model.predict_proba(patient)[0]
    label = data.target_names[model.predict(patient)[0]]
    print(f"  Sample patient prediction: {label} (confidence {probability.max():.0%})")
    print("  Note: educational demo only - AI assists doctors, it does not replace them.")


# ---------------------------------------------------------------------------
# 2. BANKING - fraud detection
# ---------------------------------------------------------------------------
def banking_fraud_demo() -> None:
    heading("2. BANKING - Fraud detection (suspicious transaction finder)")
    rng = np.random.default_rng(RANDOM_STATE)

    # Normal behaviour: small daytime purchases. Columns = [amount in Rs., hour of day]
    normal = np.column_stack([rng.normal(1500, 500, 500).clip(100), rng.normal(14, 3, 500).clip(7, 22)])
    suspicious = np.array([[95000, 3], [120000, 2], [78000, 4]])  # big amounts at night
    transactions = np.vstack([normal, suspicious])

    detector = IsolationForest(contamination=0.01, random_state=RANDOM_STATE).fit(transactions)

    tests = [[1800, 13], [2200, 18], [99000, 3], [450, 10]]
    for amount, hour in tests:
        flag = detector.predict([[amount, hour]])[0]
        status = "SUSPICIOUS - block and verify" if flag == -1 else "normal"
        print(f"  Rs.{amount:>7,} at {hour:02d}:00  ->  {status}")


# ---------------------------------------------------------------------------
# 3. E-COMMERCE / ENTERTAINMENT - recommendation system
# ---------------------------------------------------------------------------
def recommendation_demo() -> None:
    heading("3. E-COMMERCE / ENTERTAINMENT - Recommendation engine")
    movies = ["Action Hero", "Space Quest", "Love in Paris", "Romantic Summer", "Robot Wars", "Funny Family"]
    # Ratings (0 = not watched) given by 5 users: rows = users, columns = movies
    ratings = np.array([
        [5, 4, 1, 0, 5, 2],
        [4, 5, 0, 1, 4, 1],
        [1, 0, 5, 5, 1, 3],
        [0, 1, 4, 5, 0, 4],
        [5, 5, 0, 0, 0, 0],   # new user who liked Action Hero and Space Quest
    ])
    similarity = cosine_similarity(ratings.T)  # how alike are the movies, based on user taste

    target_user = ratings[4]
    scores = similarity @ target_user          # score every movie using what the user already liked
    scores[target_user > 0] = -1               # do not recommend movies already watched
    top = np.argsort(scores)[::-1][:2]
    print("  User has watched: Action Hero (5 stars), Space Quest (5 stars)")
    print("  Recommended for you:", " and ".join(movies[i] for i in top))


# ---------------------------------------------------------------------------
# 4. AGRICULTURE - crop yield prediction
# ---------------------------------------------------------------------------
def agriculture_demo() -> None:
    heading("4. AGRICULTURE - Crop yield prediction")
    rng = np.random.default_rng(RANDOM_STATE)
    n = 200
    rainfall = rng.uniform(300, 1200, n)       # mm
    soil_ph = rng.uniform(5.5, 8.0, n)
    fertilizer = rng.uniform(20, 120, n)       # kg per acre
    # Hidden rule of nature (the model must discover it) + random noise
    yield_ton = 0.004 * rainfall + 0.015 * fertilizer - 0.3 * abs(soil_ph - 6.8) + rng.normal(0, 0.15, n)

    X = np.column_stack([rainfall, soil_ph, fertilizer])
    X_train, X_test, y_train, y_test = train_test_split(X, yield_ton, test_size=0.25, random_state=RANDOM_STATE)
    model = LinearRegression().fit(X_train, y_train)
    error = mean_absolute_error(y_test, model.predict(X_test))
    print(f"  Average prediction error : {error:.3f} tonnes per acre")

    field = [[850, 6.8, 80]]
    print(f"  Field with rainfall=850 mm, soil pH=6.8, fertilizer=80 kg -> predicted yield {model.predict(field)[0]:.2f} t/acre")


def main() -> None:
    print("NM1130 - EX.NO: 3 - AI APPLICATIONS")
    healthcare_demo()
    banking_fraud_demo()
    recommendation_demo()
    agriculture_demo()

    heading("ADVANTAGES vs CHALLENGES")
    print("  Advantages : efficiency, accuracy, fast results from large data, data-driven decisions")
    print("  Challenges : high cost, dependence on data quality, privacy/security, ethical issues")
    print("\nResult: AI applications demonstrated in healthcare, banking, e-commerce and agriculture.")


if __name__ == "__main__":
    main()
