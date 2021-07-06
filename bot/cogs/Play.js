const YoutubeStream = require('youtube-audio-stream')
var videoState = 0 // 1 == lecture en cour


module.exports = class Play {

    static match(message, prefix) {
        if (message.content.startsWith(prefix+'song')){
            return message.content
        }
    }

    static action(message) {
        console.log("channel vocal : " + message.member.voiceChannel.name)
        if (message.member.voiceChannel != undefined) { //Si le message est envoyé par un membre connecté a un voice channel ...
            var voiceChannel = message.member.voiceChannel
        } else {

            //Si pas, on se récupère le premier channel de type voice
            // var voiceChannel = message.guild.channels
            //     .filter(function (channel) {
            //         return channel.type === 'voice'
            //     })
            //     .first() 

            message.reply("Tu n'es connecté à aucun channel vocal")
            return false;
            
        }

        if (videoState != 1) {//Si aucune vidéo en cour de lecture....
            
            // On récupère les arguments de la commande 
            let args = message.content.split(' ')
            console.log(args)
            let url = args[1] 
            let regex_ytb = /^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$/ // expression régulière pour valider le lien youtube
            
            if (url.match(regex_ytb)){
                console.log("continue")
                // On rejoint le channel audio
                voiceChannel.join().then(function (connection) {
                    console.log("connection")
                    // On démarre un stream à partir de la vidéo youtube
                    let stream = YoutubeStream(args[1])
                    connection.playStream(stream).on('error', function () {
                        message.reply("Je n'ai pas réussi à lire cette vidéo :(")
                        connection.disconnect()
                        return false;
                    })
                    videoState = 1
                    // On envoie le stream au channel audio
                    // Il faudrait ici éviter les superpositions (envoie de plusieurs vidéo en même temps)
                    connection.playStream(stream).on('end', function () {
                        videoState = 0
                        console.log("Video End")
                        connection.disconnect()
                    })
                })
            }else {
                console.log("stop")
                message.reply("Bad URL !")
            }
        }else {
            message.reply("Je diffuse déjà du contenu, veuillez patentier")
        }
    }
}