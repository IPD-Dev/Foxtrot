const https = require("https");
const { EmbedBuilder } = require("discord.js");

module.exports = {
    command: "koala",
    description: "is this an onlykoalalive reference?",
    category: "animals",
    admin: false,
    /**
     * @param {discord.Client} client 
     * @param {discord.Message} message 
     */
    execute: async function(client, message) {
        new https.request("https://some-random-api.ml/animal/koala", (res) => {
            var json = "";

            res.on("data", (chunk) => {
                json += chunk.toString();
            });

            res.on("end", () => {
                var object = JSON.parse(json);
                var fact = object.fact;
                var url = object.image;
                var embed = new EmbedBuilder()
                    .setTitle("onlykoalalive likes this.")
                    .setDescription(fact)
                    .setImage(url)
                    .setColor(0xce7125)
                    .setFooter({iconURL: message.author.avatarURL(), text: `Command executed by ${message.author.tag}`})
                    .setTimestamp();
                message.channel.send({embeds: [embed]});
            });

            res.on("error", (error) => {
                message.channel.send(`Received unexpected error ${error}`);
            });
        }).end();
    }
};