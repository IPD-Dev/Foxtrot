/* eslint-disable no-undef */
/* eslint-disable no-unreachable */
const { Client, GatewayIntentBits } = require("discord.js");
const config = require("./config.json");
const path = require("path");
const fs = require("fs");
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildMembers,
    ],
});
var logschannel = client.channels.cache.get(config.logsChannel);
var commandCache = null;
client.categories = null;
var commandsFolder = path.join(__dirname, "commands");
function requireUncached(module) {
    delete require.cache[require.resolve(module)];
    return require(module);
}

function calculateCommandsAndCategories() {
    commandCache = new Map();
    client.categories = new Map();
    fs.readdirSync(commandsFolder, {encoding: "utf-8"}).forEach((file) => {
        var module = requireUncached(path.join(commandsFolder, file));

        if(client.categories.has(module.category)) {
            var cats = client.categories.get(module.category);
            cats.push(module);
            client.categories.get(module.category, cats);
        }else{
            client.categories.set(module.category, [module]);
        }
        commandCache.set(module.command, module);
    });
}
calculateCommandsAndCategories();

fs.watch(commandsFolder, (type) => {
    calculateCommandsAndCategories();
});

/**
 * Execute command for message
 * @param {discord.Message} message 
 * @returns Promise
 */
function executeCommandFor(message) {
    return new Promise((resolve, reject) => {
        var command = message.content.split(config.prefix)[1].split(" ")[0];
        if (commandCache.has(command)) {
            var cmd = commandCache.get(command);
            if(cmd.admin){
                if (config.developers .includes(message.author.id)) {
                    commandCache.get(command).execute(client, message);
                }else{
                    reject();
                    if(logschannel){
                        logschannel.send(`${client.msg.author}(${client.msg.author.id} has tried to execute an admin only command.)`);
                    }// made configurable in-case of abuse.
                }
            }else{
                commandCache.get(command).execute(client, message);
            }
            resolve();
        }else{ reject(); }
    });
}

client.on("messageCreate", async (message) => {
    if(message.content.startsWith(config.prefix)){
        message.channel.sendTyping();
        executeCommandFor(message).catch(() => {
            message.reply("Command not found");
        });
    }
});

function updatePresence() {
    client.user.setPresence({status: "online", activities: [{name: `the superbowl with ${client.guilds.cache.size} guilds.`, type: "WATCHING"}]});
}

setInterval(() => {
    updatePresence();
}, 30000);

client.once("ready", () => {
    console.log(`Logged in as ${client.user.tag}`);
    updatePresence();
});

client.on("guildCreate", updatePresence);
process.on("uncaughtException", (exception) => {
    console.warn(exception);
    return;
    console.error(exception);
    var last = "dnd";
    for (i = 0; i < 10; i++) {
        setTimeout(() => {
            last = (last == "dnd") ? "idle": "dnd";
            client.user.setPresence({status: last, activities: [{name: "Error, check console."}]});
        }, 1000 * i);
    }
    setTimeout(() => {
        client.user.setPresence({status: "invisible"});
        client.destroy();
        setTimeout(() => {
            process.exit(-1);
        }, 1000);
    }, 11000);
});

client.login(config.token);