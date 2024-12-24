const socket = io()

function formatGuildName(name) {
    return name.split(" ").slice(0, 2).map(i => i[0].toUpperCase()).join("")
}

function formatDateSimplified(iso) {
    const date = new Date(iso)
    const options = { hour: '2-digit', minute: '2-digit', hour12: true }
    return date.toLocaleString('en-US', options)
}

function renderGuild(guild) {
    const e = dcreate("a", "guild centered-children", `
        <img src=${(guild.icon) ? `https://cdn.discordapp.com/icons/${guild.id}/${guild.icon}.png?size=${SETTINGS.image_resolution}` : "/static/assets/placeholder_256.png"}>
        ${(!guild.icon) ? `<div class="guild-name">${formatGuildName(guild.name)}</div>` : ""}
    `)
    e.title = guild.name
    e.href = `/guilds/${guild.id}`
    return e
}

function renderMessage(message, guild) {
    return dcreate("div", "message", `
    <div class="message-header horizontal-container">
        <img src="https://cdn.discordapp.com/avatars/${message.author.id}/${message.author.avatar}.png?size=${SETTINGS.image_resolution}">
        <b>${message.author.username}</b>
        ${formatDateSimplified(message.timestamp)}
        ${(guild) ? `
        <div class="server-tag centered-children">
            ${guild.name}
            <img src=${(guild.icon) ? `https://cdn.discordapp.com/icons/${guild.id}/${guild.icon}.png?size=${SETTINGS.image_resolution}` : "/static/assets/placeholder_256.png"}>
        </div>` : ""}
    </div>
    <div class="message-content">${(message.content.length > 0) ? message.content : "<i style='color: red;'>Unsupported message type!</i>"}</div>
    `)
}