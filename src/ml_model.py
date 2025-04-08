import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def create_features(df):
    """
    Generate basic features for ML model from stock DataFrame.
    :param df: DataFrame with stock price data
    :return: features X, labels y
    """
    df = df.copy()
    df['Return'] = df['Close'].pct_change()
    df['MA7'] = df['Close'].rolling(window=7).mean()
    df['MA30'] = df['Close'].rolling(window=30).mean()
    df['Volatility'] = df['Return'].rolling(window=5).std()
    df['Label'] = (df['Close'].shift(-1) > df['Close']).astype(int)

    df = df.dropna()
    X = df[['Return', 'MA7', 'MA30', 'Volatility']]
    y = df['Label']
    return X, y

def train_model(X, y):
    """
    Train an SVM model to predict stock movement.
    :return: trained model and scaler
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = SVC(kernel='linear')  # You can try 'rbf' later
    model.fit(X_train_scaled, y_train)
    accuracy = model.score(X_test_scaled, y_test)

    return model, scaler, accuracy

def make_prediction(model, scaler, X):
    """
    Predict future movement direction using the trained model.
    :return: prediction for each row in X
    """
    X_scaled = scaler.transform(X)
    predictions = model.predict(X_scaled)
    return predictions