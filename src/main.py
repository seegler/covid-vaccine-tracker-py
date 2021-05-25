import signal
import time
import asyncio
import sys
import aioconsole
from scheduler import VaccineScheduler
from vaccinesearch import VaccineSearch
from aio_keypress import AIOKeyPress

tracker_loop = None
vaccine_tracker = None
aio_keypress = None
tracker = None


class VaccineTracker:

    def __init__(self, scheduler: VaccineScheduler = None):
        self.scheduler = scheduler
        signal.signal(signal.SIGINT, lambda signal, frame: self._signal_handler())

    def _signal_handler(self):
        self.close()
        sys.exit(1)

    def close(self):
        print(f'self.scheduler:{self.scheduler}')
        if self.scheduler:
            print('Stopping scheduler')
            self.scheduler.stop()
        # pending = asyncio.Task.all_tasks()
        # Run loop until tasks done:
        # loop.run_until_complete(asyncio.gather(*pending))
        # tracker_loop.stop()

    async def launch_and_wait(self):
        if self.scheduler:
            await self.scheduler.start()
            print('scheduler exit')
        else:
            print('Scheduler not set')
            await time.sleep(0)


# async iostreams to capture ctrl-D
async def echo():
    stdin, stdout = await aioconsole.get_standard_streams()
    async for line in stdin:
        # while True:
        #line = await aioconsole.ainput()
        stdout.write(f'len: {len(line)}, line: {line}')


# Close async tasks on CTRL-D
def keypress(ch):
    if ch == 4: # CTRL-D
        print("CTRL-D detcted, Graceful exit...")
        print('Please wait!. This may take some time')
        print(f'{keyboard_task}, {vaccine_tracker}')
        vaccine_tracker.close()
        aio_keypress.close()
        # pending = asyncio.Task..all_tasks()
        # Run loop until tasks done:
        # tracker_loop.run_until_complete(asyncio.gather(*pending))
        # tracker_loop.stop()


if __name__ == '__main__':
    print('Starting .... Press-CTRL-C to exit')

    tracker_loop = asyncio.get_event_loop()

    vaccine_search = VaccineSearch()
    print("Starting vaccine search client")
    tracker_loop.run_until_complete(vaccine_search.start())

    scheduler = VaccineScheduler(job=vaccine_search, interval=10)

    vaccine_tracker = VaccineTracker(scheduler=scheduler)

    aio_keypress = AIOKeyPress(keypress)

    tracker_task = tracker_loop.create_task(vaccine_tracker.launch_and_wait(), name='vaccine_tracker_task')
    keyboard_task = tracker_loop.create_task(aio_keypress.listen(), name='keyboard_task')

    pending = {tracker_task, keyboard_task}
    print(f'pending tasks: {pending}')
    tracker_loop.run_until_complete(asyncio.gather(*pending))

    print("Closing vaccine search client")
    tracker_loop.run_until_complete(vaccine_search.stop())

    #tracker_loop.run_forever()
    print("Close tracker loop")
    tracker_loop.stop()
    tracker_loop.close()