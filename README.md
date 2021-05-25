# Covid Vaccine Tracker

A tool to poll Cowin website and notify when slots are open for vaccination in chosen centres

## Tech Stack

* Python
* Asyncio
* Aiohttp
* Scheduler
* Json

## References

* https://docs.aiohttp.org/en/stable/client_quickstart.html
* https://stackoverflow.com/questions/46991562/how-to-reuse-aiohttp-clientsession-pool
## Notes
* Cowin URL to poll 
```
https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=294&date=18-05-2021
```