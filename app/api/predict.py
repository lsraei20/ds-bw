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
    blurb: str = Field(..., example='A bike that floats')
    goal: int = Field(..., example=5000)
    launch_date: str = Field(..., example='08/06/2020')
    deadline: str = Field(..., example='10/20/2020')
    category: str = Field(..., example='sports')

    def prep_data(self):
        """Prepare the data to be sent to the machine learning model"""
        df = pd.DataFrame([dict(self)])
        df['launch_date'] = pd.to_datetime(df['launch_date'], format='%m/%d/%Y')
        df['deadline'] = pd.to_datetime(df['deadline'], format='%m/%d/%Y')
        df['goal'] = pd.to_numeric(df['goal'])
        return df


@router.post('/predict')
async def predict(success: Success):
    """
    Make a prediction of kickstarter success or fail

    ### Request Body
     - 'title': 'string (title of campaign)',
     - 'blurb': 'string (Description of campaign)',
     - 'goal': 'int (monetary goal)',
     - 'launch_date': 'string (date in dd/mm/yyyy format)',
     - 'deadline': 'string (date in dd/mm/yyyy format)',
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
