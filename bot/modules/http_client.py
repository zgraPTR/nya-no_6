""" httpクライアント"""

import aiohttp


class HttpClient:
    """HttpClient"""

    def __init__(self):
        """"""
        self.session = aiohttp.ClientSession()

    async def get_data(self, url: str) -> dict:
        async with self.session.get(url) as response:
            json_data = await response.json()
        return json_data

    async def get_status(self, url: str) -> int:
        async with self.session.get(url) as response:
            return response.status

    async def post_json(self, url: str, data: dict, headers: dict = None) -> dict:
        """JSONデータをPOSTするメソッド
        Args:
            url (str): JSONデータをPOSTするURL
            json_data (dict): POSTするJSONデータ
            headers (dict, optional): POSTする際のヘッダー. Defaults to None.
        Returns:
            dict: POSTしたJSONデータのレスポンス
        """
        async with self.session.post(url=url, data=data, headers=headers) as response:
            return await response.json()
