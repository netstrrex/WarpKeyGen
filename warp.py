import random
from aiohttp import ClientSession

class WarpKeyGenerator:

    _headers: dict = {
        "CF-Client-Version": "a-6.11-2223",
        "Host": "api.cloudflareclient.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.1",
    }

    _available_keys_url: str = "https://keysesforwarp.serdarad.repl.co/"
    _cloudflare_endpoint: str = "https://api.cloudflareclient.com/v0a2223"

    def __init__(self, session: ClientSession) -> None:
        self.session: ClientSession = session


    async def _get_available_keys(self) -> list:

        async with self.session.post(self._available_keys_url) as response:
            raw_keys: str = await response.text()
            
        return raw_keys.split(',')


    async def generate_key(self) -> str:
        ids: list = []
        tokens: list = []
        licenses: list = []

        for _ in range(2):

            async with self.session.post(self._cloudflare_endpoint + "/reg", headers = self._headers) as response:
                data: dict = await response.json()

            ids.append(data["id"])
            tokens.append(data["token"])
            licenses.append(data["account"]["license"])

        headers_post = {
                "Content-Type": "application/json; charset=UTF-8",
                "Authorization": f"Bearer {tokens[0]}",
            }

        await self.session.patch(self._cloudflare_endpoint + f"/reg{ids[0]}", headers = headers_post, json = {"referrer": f"{ids[1]}"})
        await self.session.delete(self._cloudflare_endpoint + f"/reg{ids[1]}", headers = {"Authorization": f"Bearer {tokens[1]}"})
        key = random.choice(await self._get_available_keys())
        await self.session.put(self._cloudflare_endpoint + f"/reg/{ids[0]}/account", headers = headers_post, json = {"license": f"{key}"})
        await self.session.put(self._cloudflare_endpoint + f"/reg/{ids[0]}/account", headers = headers_post, json = {"license": f"{licenses[0]}"})

        async with self.session.get(self._cloudflare_endpoint + f"/reg/{ids[0]}/account", headers = {"Authorization": f"Bearer {tokens[0]}"}) as response:
            data: dict = await response.json()

        await self.session.delete(self._cloudflare_endpoint + f"/reg/{ids[0]}", headers = {"Authorization": f"Bearer {tokens[0]}"})

        return data["license"]