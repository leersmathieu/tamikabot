module.exports = class Joke {

    static match (message, prefix) {
        if (message.content.startsWith(prefix+'joke') || message.content.startsWith(prefix+'jk')){
            return message.content
        }
    }

    static action (message, bdd, fs) {
        console.log("bdd length : "+bdd.length)
        let rnumber = Math.floor(Math.random() * Math.floor(bdd.length))
        console.log(bdd[rnumber])
        message.channel.send(bdd[rnumber]['joke'])
          
    }
}

