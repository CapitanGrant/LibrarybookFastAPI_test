import aiohttp
from tests.test_endpoints.base_endpoint import BaseEndpoint


class DeleteObject(BaseEndpoint):
    async def delete_object(self, url, payload):
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, json=payload) as response:
                self.response = response
                self.response_json = await self.response.json()
