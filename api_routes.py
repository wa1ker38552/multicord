from __main__ import client
from __main__ import app
from __main__ import db
import urllib3
import time

@app.route('/api/settings')
def api_settings():
    return db.get('settings')

@app.route('/api/guilds')
def api_guilds():
    db.create_session()
    if time.time()-db.session['guilds']['last_refresh'] > db.session['settings']['refresh_cooldown']:
        try:
            guild_data = client.api.get_guilds()
            db.set(['guilds'], {
                'last_refresh': time.time(),
                'data': guild_data
            })
        except urllib3.exceptions.ProtocolError:
            guild_data = db.get(['guilds', 'data']) # it updates? not exactly sure what causes this
    else:
        guild_data = db.session['guilds']['data']
    return guild_data

@app.route('/api/guilds/<guild_id>/channels')
def api_guild_channels(guild_id):
    db.create_session()
    if 'channels' in db.session['guilds']['data'][guild_id]:
        if time.time()-db.session['guilds']['data'][guild_id]['last_refresh'] > db.session['settings']['refresh_cooldown']:
            channel_data = client.api.get_guild_channels(guild_id)
            db.set(['guilds', 'data', guild_id, 'channels'], channel_data)
            db.set(['guilds', 'data', guild_id, 'last_refresh'], time.time())
        else:
            channel_data = db.session['guilds']['data'][guild_id]['channels']
    else:
        channel_data = client.api.get_guild_channels(guild_id)
        db.set(['guilds', 'data', guild_id, 'channels'], channel_data)
        db.set(['guilds', 'data', guild_id, 'last_refresh'], time.time())
    return channel_data