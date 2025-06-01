from celery import Celery
from dash import Dash, CeleryManager
import redis
import orjson

from .page_content import register_page_content_callbacks
from .navbar import register_nav_callbacks
from settings import settings


redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

redis_url = (
    f"{settings.REDIS_URL}?ssl_cert_reqs=CERT_NONE"
    if "rediss" in settings.REDIS_URL
    else settings.REDIS_URL
)
celery_app = Celery(__name__, broker=redis_url, backend=redis_url)
background_callback_manager = CeleryManager(celery_app, expire=30)


def store_data(data_key, data, expire=60 * 60 * 24 * 7):
    return redis_client.set(data_key, data, ex=expire)


def retrieve_data(key, jsonize=True):
    try:
        data = redis_client.get(key)
        if jsonize:
            data = orjson.loads(data) if data else None
        return data
    except redis.exceptions.ConnectionError as e:
        print(e)
        return None


def register_callbacks(app: Dash):
    app._background_manager = background_callback_manager
    register_nav_callbacks(app)
    register_page_content_callbacks(app, store_data, retrieve_data)
