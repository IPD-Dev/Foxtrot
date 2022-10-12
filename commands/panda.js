const https = require("https");
const { EmbedBuilder } = require("discord.js");

module.exports = {
    command: "panda",
    description: "gives you a big fluffy panda",
    category: "animals",
    admin: false,
    /**
     * @param {discord.Client} client 
     * @param {discord.Message} message 
     */
    execute: async function(client, message) {
        new https.request("https://some-random-api.ml/animal/panda", (res) => {
            var json = "";

            res.on("data", (chunk) => {
                json += chunk.toString();
            });

            res.on("end", () => {
                var object = JSON.parse(json);
                var fact = object.fact;
                var url = object.image;
                var embed = new EmbedBuilder()
                    .setTitle("panda!")
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