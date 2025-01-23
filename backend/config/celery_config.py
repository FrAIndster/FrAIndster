from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'generate-ai-interactions': {
        'task': 'tasks.ai_interactions.generate_autonomous_interactions',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
}

CELERY_TIMEZONE = 'UTC' 