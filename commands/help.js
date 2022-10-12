const config = require("../config.json");

module.exports = {
    command: "help",
    description: "gives you the helps",
    category: "Utility",
    admin: false,
    /**
     * Execute the command
     * @param {discord.Client} client 
     * @param {discord.Message} message 
     */
    execute: async function(client, message) {
        var msg = "```Foxtrot Help:";
        
        for(var category of client.categories.keys()) {
            msg += `\n\n\t${category} Category:`;
            var commands = client.categories.get(category);
            commands.forEach((command) => {
                if(command.admin) {
                    if(config.developers.includes(message.author.id)) {
                        msg += `\n\t\t${command.command} (admin) - ${command.description}`;
                    }
                } else {
                    msg += `\n\t\t${command.command} - ${command.description}`;
                }
            });
        }
        msg += "```";
        message.reply({content: msg});
    }
};