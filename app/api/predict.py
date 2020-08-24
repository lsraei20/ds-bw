import logging
import random

from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator

log = logging.getLogger(__name__)
router = APIRouter()


class Success(BaseModel):
    """Use this data model to parse the request body JSON."""
    title: str = Field(..., example='banjo')
    blurb: str = Field(..., example='banjo')
    goal: int = Field(..., example=-42)
    launch_date: str = Field(..., example='banjo')
    deadline: str = Field(..., example='banjo')
    category: str = Field(..., example='banjo')

    def to_df(self):
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])


@router.post('/predict')
async def predict(success: Success):
    """
    Make random baseline predictions for classification problem 🔮

    ### Request Body
    - `x1`: positive float
    - `x2`: integer
    - `x3`: string

    ### Response
    - `prediction`: boolean, at random
    - `predict_proba`: float between 0.5 and 1.0, 
    representing the predicted class's probability

    Replace the placeholder docstring and fake predictions with your own model.
    """

    campaign_id = 23548
    result = 'pass'
    return {
        'campaign id': campaign_id,
        'prediction': result
    }

