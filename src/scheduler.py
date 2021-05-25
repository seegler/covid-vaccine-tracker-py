import asyncio
from contextlib import suppress



class VaccineScheduler:

    def __init__(self, job=None, interval=5):
        print(f'Initialize scheduler. interval={interval} sec.')
        self.job = job
        self.interval = interval
        self._task = None
        self.is_started = False

    async def _run(self):
        while True:
            if self.job is not None:
                print('execute task')
                await self.job.do_scheduled_job()
            else:
                print('execute task not found. Exit!')
                break
            await asyncio.sleep(self.interval)

    def stop(self):
        if self.is_started:
            print("Cancel scheduler...")
            # Stop task and await it stopped:
            self._task.cancel()
            # with suppress(asyncio.CancelledError):
            #    await self._task
            self.is_started = False

        else:
            print("Scheduler not started")

    async def start(self):
        if not self.is_started:
            self.is_started = True
            # Start task to call func periodically:
            self._task = asyncio.ensure_future(self._run())
            with suppress(asyncio.CancelledError):
                await self._task
        else:
            print("scheduler task already started")





