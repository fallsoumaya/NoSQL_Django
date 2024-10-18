import redis
from django.conf import settings

# Utiliser la configuration de Redis déjà définie dans settings.py
redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'], decode_responses=True)

def increment_book_score(book_id):
    redis_client.zincrby('book_scores', 1, book_id)

def get_top_books(limit=10):
    return redis_client.zrevrange('book_scores', 0, limit - 1, withscores=True)

def reset_book_scores():
    redis_client.delete('book_scores')
