"""
NAAN MUDHALVAN - NM1130 AI AND DIGITAL SKILLS
EX.NO: 1  |  AI Fluency
------------------------------------------------------------------
Department  : CSE (AI & ML)
College     : University College of Engineering (BIT Campus), Anna University, Tiruchirappalli

Aim
---
To understand the core ideas of Artificial Intelligence - machine learning,
deep learning, NLP and the four basic AI algorithm types (classification,
regression, clustering and optimization) - by running small working examples.

Libraries : numpy, scikit-learn
Run       : python ai_fluency.py
"""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris, make_blobs
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, r2_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42


def heading(title: str) -> None:
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# ---------------------------------------------------------------------------
# 1. AI history timeline (from the experiment notes)
# ---------------------------------------------------------------------------
def show_ai_timeline() -> None:
    heading("1. AI HISTORY TIMELINE")
    timeline = [
        (1966, "ELIZA - first chatbot, created by Joseph Weizenbaum"),
        (1968, "Group Method of Data Handling - precursor of deep learning"),
        (1997, "Deep Blue defeats world chess champion Garry Kasparov"),
        (2011, "IBM Watson wins the Jeopardy! quiz show"),
        (2010, "Deep learning breakthroughs in image and speech recognition"),
        (2023, "Generative AI and Large Language Models (LLMs) go mainstream"),
    ]
    for year, event in sorted(timeline):
        print(f"  {year}  ->  {event}")


# ---------------------------------------------------------------------------
# 2. Machine learning - classification (supervised learning)
# ---------------------------------------------------------------------------
def classification_demo() -> None:
    heading("2. MACHINE LEARNING - CLASSIFICATION (Supervised Learning)")
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.3, random_state=RANDOM_STATE, stratify=iris.target
    )

    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train, y_train)  # TRAINING: learn patterns from known data

    train_acc = accuracy_score(y_train, model.predict(X_train))
    test_acc = accuracy_score(y_test, model.predict(X_test))  # VALIDATION on unseen data
    print(f"  Training accuracy   : {train_acc:.2%}")
    print(f"  Validation accuracy : {test_acc:.2%}")

    sample = [[5.1, 3.5, 1.4, 0.2]]
    predicted = iris.target_names[model.predict(sample)[0]]
    print(f"  New flower {sample[0]} is predicted as: {predicted}")


# ---------------------------------------------------------------------------
# 3. Regression - predicting a number
# ---------------------------------------------------------------------------
def regression_demo() -> None:
    heading("3. REGRESSION - Predicting marks from study hours")
    rng = np.random.default_rng(RANDOM_STATE)
    hours = rng.uniform(1, 10, size=60).reshape(-1, 1)
    marks = 30 + 6 * hours.ravel() + rng.normal(0, 4, size=60)  # pattern + noise

    X_train, X_test, y_train, y_test = train_test_split(
        hours, marks, test_size=0.25, random_state=RANDOM_STATE
    )
    model = LinearRegression().fit(X_train, y_train)
    print(f"  Learned equation : marks = {model.intercept_:.1f} + {model.coef_[0]:.1f} x hours")
    print(f"  R^2 on test data : {r2_score(y_test, model.predict(X_test)):.3f}")
    print(f"  Predicted marks for 8 study hours: {model.predict([[8]])[0]:.1f}")


# ---------------------------------------------------------------------------
# 4. Clustering (unsupervised learning)
# ---------------------------------------------------------------------------
def clustering_demo() -> None:
    heading("4. CLUSTERING (Unsupervised Learning) - grouping without labels")
    X, _ = make_blobs(n_samples=300, centers=3, cluster_std=1.0, random_state=RANDOM_STATE)
    kmeans = KMeans(n_clusters=3, n_init=10, random_state=RANDOM_STATE).fit(X)
    sizes = np.bincount(kmeans.labels_)
    for i, (centre, size) in enumerate(zip(kmeans.cluster_centers_, sizes)):
        print(f"  Cluster {i}: {size:3d} points, centre = ({centre[0]:.2f}, {centre[1]:.2f})")


# ---------------------------------------------------------------------------
# 5. Optimization - gradient descent
# ---------------------------------------------------------------------------
def optimization_demo() -> None:
    heading("5. OPTIMIZATION - Gradient Descent")
    # Minimise f(x) = (x - 3)^2 + 2  ->  the best value is x = 3
    f = lambda x: (x - 3) ** 2 + 2
    gradient = lambda x: 2 * (x - 3)

    x, learning_rate = 10.0, 0.2
    for step in range(1, 26):
        x -= learning_rate * gradient(x)
        if step in (1, 5, 10, 25):
            print(f"  Step {step:2d}: x = {x:.4f}, f(x) = {f(x):.4f}")
    print("  The algorithm moved towards the minimum at x = 3.")


# ---------------------------------------------------------------------------
# 6. Deep learning - a small neural network
# ---------------------------------------------------------------------------
def deep_learning_demo() -> None:
    heading("6. DEEP LEARNING - Artificial Neural Network")
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.3, random_state=RANDOM_STATE, stratify=iris.target
    )
    scaler = StandardScaler().fit(X_train)

    net = MLPClassifier(hidden_layer_sizes=(16, 8), max_iter=1000, random_state=RANDOM_STATE)
    net.fit(scaler.transform(X_train), y_train)
    acc = accuracy_score(y_test, net.predict(scaler.transform(X_test)))
    print("  Network layers  : 4 inputs -> 16 neurons -> 8 neurons -> 3 outputs")
    print(f"  Test accuracy   : {acc:.2%}")


# ---------------------------------------------------------------------------
# 7. Natural Language Processing - sentiment analysis
# ---------------------------------------------------------------------------
def nlp_demo() -> None:
    heading("7. NATURAL LANGUAGE PROCESSING - Sentiment Analysis")
    sentences = [
        "I love this phone, the camera is excellent",
        "Great service and very friendly staff",
        "The course was wonderful and easy to follow",
        "Amazing quality, I am very happy with it",
        "Terrible experience, the product broke in a day",
        "Very poor support and slow delivery",
        "I hate this app, it keeps crashing",
        "Worst purchase ever, totally disappointed",
    ]
    labels = ["positive"] * 4 + ["negative"] * 4

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(sentences)  # text -> numbers (bag of words)
    classifier = MultinomialNB().fit(X, labels)

    tests = [
        "The staff was friendly and the service was excellent",
        "Poor quality and the app keeps crashing",
    ]
    for text in tests:
        print(f"  '{text}' -> {classifier.predict(vectorizer.transform([text]))[0]}")


def main() -> None:
    print("NM1130 - EX.NO: 1 - AI FLUENCY")
    show_ai_timeline()
    classification_demo()
    regression_demo()
    clustering_demo()
    optimization_demo()
    deep_learning_demo()
    nlp_demo()
    print("\nResult: AI concepts demonstrated successfully.")


if __name__ == "__main__":
    main()
