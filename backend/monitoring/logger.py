import logging
import json
from datetime import datetime
from elasticsearch import Elasticsearch
from django.conf import settings

class CustomLogger:
    def __init__(self):
        self.es = Elasticsearch(settings.ELASTICSEARCH_HOST)
        self.logger = logging.getLogger(__name__)

    def log_interaction(self, interaction_type: str, data: dict):
        """Log AI interactions to Elasticsearch"""
        log_entry = {
            'timestamp': datetime.utcnow(),
            'type': interaction_type,
            'data': data
        }
        
        try:
            self.es.index(
                index=f'ai-interactions-{datetime.utcnow().strftime("%Y-%m")}',
                document=log_entry
            )
        except Exception as e:
            self.logger.error(f"Failed to log to Elasticsearch: {str(e)}")

    def log_api_request(self, request, response, execution_time):
        """Log API requests"""
        log_entry = {
            'timestamp': datetime.utcnow(),
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'execution_time': execution_time,
            'user_id': str(request.user.id) if request.user.is_authenticated else None
        }
        
        try:
            self.es.index(
                index=f'api-logs-{datetime.utcnow().strftime("%Y-%m")}',
                document=log_entry
            )
        except Exception as e:
            self.logger.error(f"Failed to log API request: {str(e)}") 