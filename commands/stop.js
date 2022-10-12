module.exports = {
    command: "stop",
    description: "stops the bot",
    category: "Action",
    admin: true,
    /**
     * @param {discord.Client} client 
     * @param {discord.Message} message 
     */
    execute: async function (client, message) {
        await message.delete();
        console.log(`Bot stopped by ${message.author.tag}!`);
        client.destroy();
        setTimeout(() => {
            process.exit(0);
        }, 1000);
    }
};