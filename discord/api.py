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
        raw_data = self.session.get('https://discord.com/api/v9/users/@me/guilds').json()
        parsed_data = {}
        for item in raw_data:
            parsed_data[item['id']] = item
        return parsed_data

    def get_guild_channels(self, guild_id):
        return self.session.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels').json()