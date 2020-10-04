const Discord = require('discord.js')
const bot =  new Discord.Client()
const DiscordKey = process.env.DISCORD_KEY;
//-//
const fs = require("fs");


// mycommands :
const Help = require('./commands/Help')
const Google = require('./commands/Google')
const Bank = require('./commands/Bank')
const Coin = require('./commands/Coin')
const Play = require('./commands/Play')
const Trans = require('./commands/Trans')
const Work = require('./commands/Work')
const Joke = require('./commands/Joke')
const Say = require('./commands/Say')

////
var srvDmz
var srvTamco
var srvPdPortal
var srvPdFr
var srvOr
var srvBeCode

var tamikara
var prefix = "$"

bot.login(DiscordKey)

bot.on('ready', () => { //WHEN THE BOT IS READY.....

    /// définitions des différents serveurs + info bot \\\
    
    srvTamco = bot.guilds.get("183999429504794625")
    srvDmz = bot.guilds.get("430139146028187658")
    srvPdPortal = bot.guilds.get("463756861649453056")
    srvPdFr = bot.guilds.get("282981239969808385")
    srvBeCode = bot.guilds.get("674600177402642465")
    
    botId = 469072242865602561

    // console.log(bot.guilds)
    // console.log(srvDmz.name)    

    //-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-\\
    
    var server_list = bot.guilds.array().sort();

    console.log("Number of Available Servers: " + bot.guilds.size)
    console.log("Available Servers name: " + server_list)
    console.log("Number of Available Channels: " + bot.channels.size)
    console.log("Number of Online users: " + bot.users.size)
    
    bot.user.setActivity("$help").catch(console.error)

    //-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-\\

})


bot.on('guildMemberAdd', (member) => { // QUAND QUELQUN REJOIN LE SERVEUR...
    if (member.guild.id === srvDmz.id){ //Si le mec est sur le serveur DMZ
        member.setRoles(['430142179890167818']).catch(console.error)
        bot.channels.get("430139980598214656").send('hummm welcome ? '+member).catch(console.error)
    }
})


bot.on('message', async message => { //QUAND UN MESSAGE EST ENVOYE....
    
    if (message.author.id == "183999045168005120"){ // It's me !
        tamikara = message.author
    }

    //ATTENTION CECI EST UN TEST DANGEREUX A DESTINATION D'ODILE
    // if (message.author.id == "712279385926795275"){
    //     message.reply("Et si on se parlait... forever ?")
    // }

    /////////////////////FIN DU TEST/////////////////////////////

    let regex_lea = /é|è/gi //variable contenant les charactères a remplacer ainsi que les paramètres (pour le replace())
    let leamessage = message.toString().replace(regex_lea, "e").toLowerCase() //restructuration du message pour pouvoir le travailler

    
    if (message.guild){ //Si le message est bien envoyé sur un serveur ( et pas en DM par exemple )
        console.log("Message du serveur "+message.guild.name+" - "+message.author.username+" sur le chan "+message.channel.name+" : " +message)

        //############################# DMZ SERVER ##############################################//
        if (message.guild.id === srvDmz.id){ // si le message est envoyé sur le dmz server...
            if (leamessage.search('lea') != -1 ){
                message.reply('azy tg la')
            }
            //quand X emoji est ajouté à un message du serveur .... ( oui pas très utile je sais )
            bot.on('messageReactionAdd', (reaction, user) => {
                if (reaction.emoji.name == '💻') {
                    console.log("adding role")
                    const guildMember = reaction.message.guild.members.get(user.id);
                    const role = reaction.message.guild.roles.get('430179395530129430');
                    guildMember.addRole(role);
                } 
                if (reaction.emoji.name == '🎮') {
                    console.log("adding role")
                    const guildMember = reaction.message.guild.members.get(user.id);
                    const role = reaction.message.guild.roles.get('430179395530129430');
                    guildMember.addRole(role);
                } 
                if (reaction.emoji.name == '😂') {
                    return message.channel.send("haha")
                } 
            });
            bot.on('messageReactionRemove', (reaction, user) => {
                if (reaction.emoji.name == '💻') {
                    console.log("remove role")
                    const guildMember = reaction.message.guild.members.get(user.id);
                    const role = reaction.message.guild.roles.get('430179395530129430');
                    guildMember.removeRole(role);
                } 
                if (reaction.emoji.name == '🎮') {
                    console.log("remove role")
                    const guildMember = reaction.message.guild.members.get(user.id);
                    const role = reaction.message.guild.roles.get('430179395530129430');
                    guildMember.removeRole(role);
                } 
            });
        }
    //si le message n'est PAS envoyé sur un serveur ...
    } else if ( message.author.id != botId && message.author.id != tamikara.id ) { // si le message N'EST PAS envoyé sur un serveur ( genre en DM ) et que ce n'est pas un message du bot ...
        console.log("Message en DM au bot de "+message.author.username+" : " +message)
        message.reply('tu fais quoi là ?')
        
        if (message.content == "loopme" || message.content =="don't try me dude!"){ //petite boucle pour le troll si on envoie "loopme" en privé au bot
            message.reply("don't try me dude!")
        } 
    
    } else {
        console.log("Message en DM au bot de "+message.author.username+" : " +message)
    }

    
    
    
    //////////////////// COMMANDE GENERALE (tout serveur)

    if(message.content == prefix+"ping"){ // Check if message is "!ping"
        const m = await message.channel.send("Pinging...");
        m.edit(`Pong! en ${m.createdTimestamp - message.createdTimestamp}ms. Latence API : ${Math.round(bot.ping)}ms`);
    }

    if (message.content === prefix+"pingme"){
        message.reply('I ping you')
    }

    ////////// TROLL
    if (message.content === prefix+"rayane" || message.content === prefix+"rayane_san" || message.content === prefix+"Rayane_San" ){
        message.channel.send("https://www.youtube.com/watch?v=na2XWHa_g6k")
    }

    // if (message.content === "!presence"){
    //    console.log(message.author.presence.game.name) 
    // }


    ///////////////// EPIC COMMANDS ///////////////////

    //commands/Google.js
    if (Help.match(message, prefix)){
        return Help.action(message, prefix)
    }
    if (Google.match(message, prefix)){
        return Google.action(message)
    }
    if (Bank.match(message, prefix)){
        let bdd = JSON.parse(fs.readFileSync("monnaie.json", "utf8"));
        return Bank.action(message, bdd)
    }
    if (Coin.match(message, prefix)){
        let bdd = JSON.parse(fs.readFileSync("monnaie.json", "utf8"));
        return Coin.action(message, bdd, fs, tamikara) // FS c'est pour pouvoir ecrire
    }
    if (Work.match(message, prefix)){
        let bdd = JSON.parse(fs.readFileSync("monnaie.json", "utf8"));
        return Work.action(message, bdd, fs)
    }
    if (Joke.match(message, prefix)){
        let bdd = JSON.parse(fs.readFileSync("joke.json", "utf8"));
        return Joke.action(message, bdd, fs)
    }
    if (Play.match(message, prefix)){
        return Play.action(message)
    }
    if (Trans.match(message, prefix)){
        return Trans.action(message)
    }
    if (Say.match(message, prefix)){
        return Say.action(message, bot, tamikara)
    }
})