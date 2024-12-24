client = Client(open('token.txt', 'r').read())

@client.event
async def on_ready():
    print('ready!')

@client.event
async def on_message(message):
    # print(message)
    print(message['author']['username'], message['content'])

client.run()