
var guildIndex = {}
window.onload = function() {
    request("/api/guilds")
        .then(guilds => {
            const guildParent = dquery(".guild-container")
            guildIndex = guilds
            for (guild in guilds) {
                guildParent.append(renderGuild(guilds[guild]))
            }
        })

        
    // const rem = parseFloat(getComputedStyle(document.documentElement).fontSize)
    const grid = GridStack.init()
    /*const globalWindow = dcreate("div", "window", `
        <div class="subtitle">Global Stream</div>
        <div class="messages-container" id="globalMessagesContainer"></div>
    `)
    globalWindow["gs-w='3'"]
    grid.makeWidget(globalWindow, { x: 0, y: 0, width: 3, height: 1 })
    */

    // render global
    setTimeout(() => {
        const globalMessageParent = document.querySelector("#globalMessagesContainer");
        socket.on("MESSAGE_CREATE", (data) => {
            globalMessageParent.append(renderMessage(data, ("guild_id" in data) ? guildIndex[data.guild_id] : null));
            globalMessageParent.scrollTop = globalMessageParent.scrollHeight;
        });
    }, 0);
}