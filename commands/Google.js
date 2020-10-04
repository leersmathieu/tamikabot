module.exports = class Google {

    static match (message, prefix) {
        if (message.content.startsWith(prefix+'google') || message.content.startsWith(prefix+'goo')){
            return message.content
        }
    }

    static action (message) {
        let args = message.content.split (' ')
        args.shift()
        if (args[0]){
            message.reply('https://www.google.com/search?q='+args.join('%20'))
        }else{
            message.reply("Insert Argument")
        }
    }
}