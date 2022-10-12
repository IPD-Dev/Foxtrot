const https = require("https");
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const { discord, EmbedBuilder } = require("discord.js");

module.exports = {
    command: "comrade",
    description: "something something Vladimir Putin",
    category: "Filters",
    admin: false,
    /**
     * @param {discord.Client} client 
     * @param {discord.Message} message 
     */
    execute: async function(client, message) {
        var url = message.content.split(" ")[2];
        if(!message.content.split(" ")[2] || message.mentions.users.size > 0) {
            if(message.mentions.users.size > 0) {
                url = message.mentions.users.first().avatarURL({format: "png", size: 4096});
            } else {
                url = message.author.avatarURL({format: "png", size: 4096});
            }    
        }

        new https.request(`https://some-random-api.ml/canvas/comrade?avatar=${url}`, (res) => {
            var comradeDir = path.join(__dirname, "..", "imgs", "comrade");
            const id = crypto.randomUUID();
            var filename = path.join(comradeDir, `${id}.png`);
            if(!fs.existsSync(comradeDir)) {
                fs.mkdirSync(comradeDir, {recursive: true});
            }

            var writeStream = new fs.createWriteStream(filename);
            res.pipe(writeStream);

            res.on("end", async () => {
                var attachment = new discord.MessageAttachment(filename);
                var embed = new EmbedBuilder()
                    .setTitle("Comrade")
                    .setColor(0xf1f1f1)
                    .setFooter({iconURL: message.author.avatarURL(), text: `Command executed by ${message.author.tag}`})
                    .setTimestamp()
                    .setImage(`attachment://${id}.png`);
                await message.channel.send({embeds: [embed], files: [attachment]});
                fs.unlinkSync(filename);
            });

            res.on("error", async (err) => {
                await message.channel.send({content: `An unexpected error happened, Steve.. I told you this already! ${err}`});
                fs.unlinkSync(filename);
            });
        }).end();
    }
};