import aiohttp
from tests.test_endpoints.base_endpoint import BaseEndpoint


class CreateObject(BaseEndpoint):
    async def new_object(self, url, payload):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                self.response = response
                self.response_json = await self.response.json()
