const https = require("https");
const { EmbedBuilder } = require("discord.js");

module.exports = {
    command: "fox",
    description: "gives flops",
    category: "animals",
    admin: false,
    /**
     * @param {discord.Client} client 
     * @param {discord.Message} message 
     */
    execute: async function(client, message) {
        new https.request("https://some-random-api.ml/animal/fox", (res) => {
            var json = "";

            res.on("data", (chunk) => {
                json += chunk.toString();
            });

            res.on("end", () => {
                var object = JSON.parse(json);
                var fact = object.fact;
                var url = object.image;
                var embed = new EmbedBuilder()
                    .setTitle("fluffy fox!")
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