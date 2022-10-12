module.exports = {
    command: "pfp",
    description: "get a user's profile picture",
    category: "Utility",
    admin: false,
    /**
     * @param {discord.Client} client 
     * @param {discord.Message} message 
     */
    execute: async function(client, message) {
        var url = null;
        var tag = null;
        if(message.mentions.users.size > 0) {
            let user = message.mentions.users.first();
            url = user.avatarURL({format: "png", size: 4096});
            tag = user.tag;
        } else {
            url = message.author.avatarURL({format: "png", size: 4096});
            tag = message.author.tag;
        }
        message.reply(`**${tag}**'s profile pic: ${url}`);
    }
};