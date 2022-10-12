const crypto = require("crypto");

module.exports = {
    command: "meme",
    description: "random meme",
    category: "Utility",
    admin: false,
    /**
     * @param {discord.Client} client 
     * @param {discord.Message} message 
     */
    execute: async function (client, message) {
        
        var id = crypto.randomUUID();
        var urls = [`https://timeout.zone/api/random?redirect=1&id=${id}`, `https://p90.zone/?${id}`];
        message.channel.send(urls[Math.floor(Math.random() * urls.length)]);
    }
}