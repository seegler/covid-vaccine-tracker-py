import aiohttp
import asyncio
import sys

class VaccineSearch:

    def __init__(self):
        # self.url = 'http://www.google.com'
        self.url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
        # https://cdn-api.co-vin.in/api/v2/admin/location/states
        self.params = {'district_id': 294, 'date': '18-05-2021'}
        self.headers = {'Accept': 'application/json, text/plain, */*',
                        'Accept - Encoding': 'gzip, deflate, br',
                        'Origin' : 'https://www.cowin.gov.in',
                        'Referer' : 'https://www.cowin.gov.in/',
                        'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'
                        }
        self.http_session = None
        self.is_started = False
        self.writer = None

    async def start(self):
        loop = asyncio.get_event_loop()
        w_transport, w_protocol = await loop.connect_write_pipe(asyncio.streams.FlowControlMixin, sys.stdout)
        self.writer = asyncio.StreamWriter(w_transport, w_protocol, None, loop)
        self.http_session = aiohttp.ClientSession()
        self.is_started = True

    async def stop(self):
        await self.http_session.close()
        self.is_started = False

    async def do_scheduled_job(self): # called from scheduler
        if self.is_started:
            print(self.url)
            async with self.http_session.get(self.url, params=self.params, headers= self.headers) as resp:
                print(resp.status, resp.url)
                if resp.status == 200:
                    if self.writer:
                        self.writer.write(await resp.read())
                else:
                    pass
        else:
            print("Tracker not started")
