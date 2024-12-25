
var guildIndex = {}
window.onload = function() {
    request("/api/guilds")
        .then(guilds => {
            const guildParent = dquery(".guild-container")
            guilds.forEach(function(guild) {
                guildIndex[guild.id] = guild
                guildParent.append(renderGuild(guild))
            })
        })

        
    // const rem = parseFloat(getComputedStyle(document.documentElement).fontSize)
    const grid = GridStack.init()
    const globalWindow = dcreate("div", "window", `
        <div class="subtitle">Global Stream</div>
        <div class="messages-container" id="globalMessagesContainer"></div>
    `)
    grid.addWidget(globalWindow, { x: 0, y: 0, width: 3, height: 1 })

    // render global
    setTimeout(() => {
        const globalMessageParent = document.querySelector("#globalMessagesContainer");
        socket.on("MESSAGE_CREATE", (data) => {
            globalMessageParent.append(renderMessage(data, ("guild_id" in data) ? guildIndex[data.guild_id] : null));
            globalMessageParent.scrollTop = globalMessageParent.scrollHeight;
        });
    }, 0);
}