import aiohttp
from tests.test_endpoints.base_endpoint import BaseEndpoint


class GetAllObject(BaseEndpoint):

    async def get_all_objects(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                self.response = response
