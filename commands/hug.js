module.exports = {
    command: "hug",
    description: "give someone a cuddle",
    category: "Action",
    admin: false,
    /**
     * @param {discord.Client} client 
     * @param {discord.Message} message 
     */
    execute: async function(client, message) {
        if(message.mentions.users.size > 0) {
            message.reply(`${message.author.username} hugs ${message.mentions.users.first().username}! :3`);
        } else {
            message.reply(`Foxtrot hugs ${message.author.username}! :3`);
        }
    }
};