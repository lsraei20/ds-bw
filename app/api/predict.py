# import string
#
# import nltk
# import pandas as pd
# # from wordcloud import WordCloud
# import spacy
# from sklearn.base import TransformerMixin
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.model_selection import train_test_split
# from sklearn.pipeline import Pipeline
# from spacy.lang.en import English
# from spacy.lang.en.stop_words import STOP_WORDS
# from xgboost import XGBClassifier
#
# nltk.download('stopwords')
#
# from pathlib import Path
#
# # --------------Cleaning begins -------------------#
# BASE_DIR = Path(__file__).resolve(strict=True).parent
#
# # training data
#
# df = pd.read_csv('/Users/israel/PycharmProjects/ds-bw/app/api/data/kickstarter_data_with_features.csv', index_col=0)
# df = df[['name', 'goal', 'blurb', 'launched_at', 'deadline', 'category', 'state', 'country']]
# english_countries = ['US', 'IE', 'GB', 'AU', 'CA', 'NZ', ]
# df = df[df['country'].isin(english_countries)]
# suc_filt = ['failed', 'successful']
# df = df[df['state'].isin(suc_filt)]
# df['state'] = df['state'].replace({'failed': 0, 'successful': 1})
#
# columns = ['name', 'blurb', 'state']
# to_df = df.copy()
# to_df = to_df[columns]
# to_df.fillna(' ', inplace=True)
# to_df['text'] = to_df['name'] + ' ' + to_df['blurb']
#
# punctuations = string.punctuation
# stop_words = spacy.lang.en.stop_words.STOP_WORDS
# parser = English()
#
#
# def spacy_tokenizer(sentence):
#     mytokens = parser(sentence)
#     mytokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens]
#     mytokens = [word for word in mytokens if word not in stop_words and word not in punctuations]
#     return mytokens
#
#     # Custom transformer using spaCy
#     class predictors(TransformerMixin):
#         def transform(self, X, **transform_params):
#             return [clean_text(text) for text in X]
#
#     def fit(self, X, y=None, **fit_params):
#         return self
#
#     def get_params(self, deep=True):
#         return {}
#
#     def clean_text(text):
#         # Removing spaces and converting text into lowercase
#         return text.strip().lower()
#
#     bow_vector = CountVectorizer(tokenizer=spacy_tokenizer, ngram_range=(1, 3))
#
#     train, test = train_test_split(to_df, train_size=0.80, test_size=0.20,
#                                    stratify=to_df['state'], random_state=3)
#
#     train, val = train_test_split(train, train_size=0.80, test_size=0.20,
#                                   stratify=train['state'], random_state=3)
#     features = 'text'
#     target = 'state'
#     X_train = train[features]
#     X_val = val[features]
#     X_test = test[features]
#     y_train = train[target]
#     y_val = val[target]
#     y_test = test[target]
#     xgm = XGBClassifier(n_jobs=-1, max_depth=200, learning_rate=0.2, min_child_weight=5)
#
#     # Create pipeline using Bag of Words
#     pipe = Pipeline([("cleaner", predictors()),
#                      ('vectorizer', bow_vector),
#                      ('classifier', xgm)])
#
#     # fitting our model.
#     pipe.fit(X_train, y_train)
#     joblib.dump(pipe, "model_mk1_v2.joblib")
#     # pickle.dump(pipe, open('pickle_model', 'wb'))
#     print("hello!")
#

import logging
import joblib

from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)
router = APIRouter()


class Success(BaseModel):
    """Use this data model to parse the request body JSON."""
    title: str = Field(..., example='Water bike')
    description: str = Field(..., example='A bike that floats')
    monetary_goal: int = Field(..., example=5000)
    launch_date: str = Field(..., example='2020/08/06')
    finish_date: str = Field(..., example='2020/10/20')
    category: str = Field(..., example='sports')

    def prep_data(self):
        """Prepare the data to be sent to the machine learning model"""
        df = pd.DataFrame([dict(self)])
        df['title_desc'] = df['title'] + " " + df['description']
        df2 = df['title_desc']
        print(df2)
        df['launch_date'] = pd.to_datetime(df['launch_date'], format='%Y/%m/%d')
        df['finish_date'] = pd.to_datetime(df['finish_date'], format='%Y/%m/%d')
        df['monetary_goal'] = pd.to_numeric(df['monetary_goal'])
        return df2


@router.post('/predict')
async def predict(success: Success):
    """
    Make a prediction of kickstarter success or fail

    ### Request Body
     - 'title': 'string (title of campaign)',
     - 'description': 'string (Description of campaign)',
     - 'monetary_goal': 'int (monetary goal)',
     - 'launch_date': 'string (date in yyyy/mm/dd format)',
     - 'finish_date': 'string (date in yyyy/mm/dd format)',
     - 'category': 'string (category of campaign)'

    ### Response
    - `campaign_id`: unique campaign identifier
    - `prediction`: boolean, pass or fail,
    representing the predicted class's probability

    """

    campaign_id = 23548
    result = 'Success'
    return {
        'campaign_id': campaign_id,
        'prediction': result
    }
