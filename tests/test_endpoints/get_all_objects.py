import aiohttp
from tests.test_endpoints.base_endpoint import BaseEndpoint


class GetAllObject(BaseEndpoint):

    async def get_all_objects(self, url, token):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"Cookie": f"users_access_token={token}"}) as response:
                self.response = response
                self.response_json = await response.json()