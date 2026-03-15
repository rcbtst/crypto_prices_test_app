from src.config import settings

task_acks_late = True
task_acks_on_failure_or_timeout = True
task_reject_on_worker_lost = False
task_time_limit = 60
worker_max_tasks_per_child = 60
worker_prefetch_multiplier = 1
worker_hijack_root_logger = False
worker_proc_alive_timeout = 120
result_backend = settings.CELERY_RESULT_BACKEND
result_expires = 60 * 60 * 24
broker_url = settings.CELERY_BROKER_URL
task_serializer = "json"
accept_content = ["json"]
