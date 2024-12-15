import aiohttp
from tests.test_endpoints.base_endpoint import BaseEndpoint


class GetObjectByID(BaseEndpoint):

    async def get_object_by_id(self, url, object_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}{object_id}") as response:
                self.response = response
                self.response_json = await self.response.json()
