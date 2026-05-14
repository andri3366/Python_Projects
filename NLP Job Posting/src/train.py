import pandas as pd
import joblib

from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler

from src.preprocess import clean_text

df = pd.read_csv('../data/fake_job_postings_cleaned.csv')

'''
    Selected columns for training
    [Text features]
    - title
    - company_profile
    - description
    - requirements
    - benefits
    [Binary features]
    - telecommuting
    - has_company_logo
    - has_questions
    [Categorical features]
    - enrollment_type
    - required_experience
    - required_education
    - country
    [Target variable]
    - fraudulent 
'''

# Combine the text
df['combined_text'] = (
    df['title'] + ' ' +
    df['company_profile'] + ' ' +
    df['description'] + ' ' +
    df['requirements'] + ' ' +
    df['benefits']
)

df['combined_text'] = df['combined_text'].apply(clean_text)

# Apply TF-IDF
vectorizer = TfidfVectorizer(max_features=1000)
text_features = vectorizer.fit_transform(df['combined_text'])

# Handle binary features
binary_features = df[['telecommuting', 'has_company_logo', 'has_questions']]

# Handle categorical features
cat_columns = ['employment_type', 'required_experience', 'required_education', 'country']
cat_features = pd.get_dummies(df[cat_columns], drop_first=True)


# Combine all features
X = hstack([text_features, binary_features, cat_features])
y = df['fraudulent']

# Modeling
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(class_weight='balanced', max_iter=1000).fit(X_train, y_train)

pred = model.predict(X_test)
    
joblib.dump(model, '../model/lr_model.pkl')
joblib.dump(vectorizer, '../model/lr_vectorizer.pkl')
joblib.dump(cat_features.columns, '../model/lr_cat_features.pkl')