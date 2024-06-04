from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from .models import save_data
import logging

from .chatting_model import chatting_model 
from .classification_model import Google_gemini as classificate_user_input 

logger = logging.getLogger(__name__)

@shared_task
def chatting_model_predict(user_input):
    try:
        # user_input을 사용하여 모델 예측
        result = chatting_model(user_input)
        return result
        
    except Exception as e:
        logger.error(f'tasks.py/chatting_model_predict -> Error: {e}')
        return ' '


@shared_task
def classification_model_predict(user_input, api_key):

    classification_output = classificate_user_input(
        user_input = user_input, 
        api_key = api_key
        )
    return classification_output