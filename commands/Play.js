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
        if (videoState != 1) {
            
            // On récupère les arguments de la commande 
            // il faudrait utiliser une expression régulière pour valider le lien youtube
            let args = message.content.split(' ')
            // On rejoint le channel audio
            voiceChannel.join().then(function (connection) {
                // On démarre un stream à partir de la vidéo youtube
                let stream = YoutubeStream(args[1])
                stream.on('error', function () {
                    message.reply("Je n'ai pas réussi à lire cette vidéo :(")
                    connection.disconnect()
                })
                videoState = 1
                // On envoie le stream au channel audio
                // Il faudrait ici éviter les superpositions (envoie de plusieurs vidéo en même temps)
                connection.playStream(stream).on('end', function () {
                    videoState = 0
                    connection.disconnect()
                })
            })
        }else {
            message.reply("Je diffuse déjà du contenu, veuillez patentier")
        }
    }
}