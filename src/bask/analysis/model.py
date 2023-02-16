"""Functions for fitting the regression model."""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from bask.data_management.clean_data import clean_split_data

df_past = clean_split_data()[0]


def split_data(df):
    X_train, X_test, y_train, y_test = train_test_split(
        df,
        iris.target,
        test_size=0.2,
        random_state=42,
    )


# Create a logistic regression classifier
lr = LogisticRegression()

# Train the classifier on the training set
lr.fit(X_train, y_train)


# Predict the classes of the test set
y_pred = lr.predict(X_test)

# Evaluate the accuracy of the classifier
accuracy = accuracy_score(y_test, y_pred)

# see example of other branch
