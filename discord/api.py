import requests

class APIManager:
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.headers = {
            'Authorization': self.token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

    def get_guilds(self):
        return self.session.get('https://discord.com/api/v9/users/@me/guilds').json()