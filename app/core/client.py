import requests


class HDIClient:

    @staticmethod
    def post(url, headers=None, data=None, json=None):
        return requests.post(
            url=url,
            headers=headers,
            data=data,
            json=json
        )

    @staticmethod
    def get(url, headers=None):
        return requests.get(
            url=url,
            headers=headers
        )
