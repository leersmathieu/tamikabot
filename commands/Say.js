module.exports = class Say {

    static match (message, prefix) {
        if (message.content.startsWith(prefix+'say')){
            return message.content
        }
    }

    static action (message, bot, tamikara) {
        if ( message.author.id == botId || message.author.id == tamikara.id) {
            let args = message.content.split (' ')
            args.shift()
            let chanId = args[0]
            args.shift()
            args = args.join(' ')
            // console.log(args)
            bot.channels.get(chanId).send(args);
        } else {
            message.reply("Vous ne pouvez pas parler à ma place !")
        }
    }
}