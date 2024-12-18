from crewai.tools import BaseTool
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class CustomSerperDevTool(BaseTool):
    name: str = "Custom Serper Dev Tool"
    description: str = "Search the internet for Blockchain Related Data."

    def _run(self, query: str) -> str:
        """
        Search the internet for Blockchain Related Data.
        """

        url = "https://google.serper.dev/blockchain"

        payload = json.dumps({
            "q": query,
            "num": 2,
            "autocorrect": False,
            "tbs": "qdr: d"
        })

        headers = {
            'X-API-KEY': os.environ["SERPER_API_KEY"],
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        response_data = response.json()

        blockchain_data = response_data.get('news', [])

        return json.dumps(blockchain_data, indent=2)