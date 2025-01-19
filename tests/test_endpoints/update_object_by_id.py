import aiohttp
from tests.test_endpoints.base_endpoint import BaseEndpoint


class UpdateObjectByID(BaseEndpoint):

    async def update_object_by_id(self, url, payload, token, method="PUT"):
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers={"Cookie": f"users_access_token={token}"}, json=payload) as response:
                self.response = response
                self.response_json = await self.response.json()
