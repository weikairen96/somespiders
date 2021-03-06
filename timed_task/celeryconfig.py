# -*- coding:UTF-8 -*-
from datetime import timedelta
BROKER_URL = 'redis://localhost:6379/0' # 使用RabbitMQ作为消息代理

CELERY_RESULT_BACKEND = 'redis://localhost:6379/1' # 把任务结果存在了Redis

CELERY_TASK_SERIALIZER = 'json' # 任务序列化和反序列化使用msgpack方案

CELERY_RESULT_SERIALIZER = 'json' # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON

CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显

CELERY_ACCEPT_CONTENT = ['json'] # 指定接受的内容类型

CELERYBEAT_SCHEDULE = {

    'store_sse_news': {

        'task': 'timed_task.tasks.store_sse_news',

       'schedule': timedelta(seconds=600),



    }
}