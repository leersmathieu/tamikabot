module.exports = class Help {

    static match (message, prefix) {
        if (message.content.startsWith(prefix+'help') || message.content.startsWith(prefix+'com')){
            return message.content
        }
    }

    static action (message, prefix) {
        message.channel.send(prefix + " commande")
        message.channel.send("help, ping, bank, coin[give/remove], google <search>, song <ytb link>, to <lang>, pingme")
    }
}