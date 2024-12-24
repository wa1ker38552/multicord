
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

    // render global
    const globalMessageParent = dquery("#globalMessagesContainer")
    socket.on("MESSAGE_CREATE", (data) => {
        globalMessageParent.append(renderMessage(data, ("guild_id" in data) ? guildIndex[data.guild_id] : null))
        globalMessageParent.scrollTop = globalMessageParent.scrollHeight
    })
}