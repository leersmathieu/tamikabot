const translate = require('translate-google')
const { ar } = require('translate-google/languages')

  module.exports = class Trans {

    static match (message, prefix) {
        return message.content.startsWith(prefix+'to')
    }

    static action (message) {
        let args = message.content.split(" ")
        args.shift()
        if (args == ""){
            message.channel.send('Insert <lang> and <message>')
        }else {
            let tolang = args[0].toLowerCase()
            args.shift()
            let final_args = args.join(" ")
            translate(final_args, {to: tolang}).then(res => {
                console.log(res)
                message.reply("Traduction : "+res)
            }).catch(err => {
                console.error(err)
            })
        }
    }
}
