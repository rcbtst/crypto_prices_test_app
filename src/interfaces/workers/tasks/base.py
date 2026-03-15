import asyncio

from celery import Task


class AsyncTask(Task):
    def __init__(self):
        self.loop = asyncio.new_event_loop()

    def __call__(self, *args, **kwargs):
        return self.loop.run_until_complete(self.run(*args, **kwargs))
