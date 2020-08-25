import logging
import random

from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator

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
    result = 'pass'
    return {
        'campaign_id': campaign_id,
        'prediction': result
    }
