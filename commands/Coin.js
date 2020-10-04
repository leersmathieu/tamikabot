//COMMANDE POUR GERE LES COINS

const { convertStringToNumber } = require('convert-string-to-number') // named export
// const converter = require('convert-string-to-number'); // default export

module.exports = class Coin {

    static match (message, prefix) {
        return message.content.startsWith(prefix+'coin')
    }

    static action (message, bdd, fs, tamikara, prefix) {

        if ( message.author.id == botId || message.author.id == tamikara.id) { // si le message est bien envoyé par moi ou par le bot...

            let messageSplit = message.content.trim().split(' ')
            let subCommand 

            if (messageSplit[1] == "give" || messageSplit[1] == "remove"){

                subCommand = messageSplit[1]

                if (subCommand == "give"){

                    let mentionned = message.mentions.users.first(); //personne mentionnée
                    let nombreDeCoins
                    let user
    
                    if (mentionned) {
                        user = mentionned
                    } else {
                        console.log(messageSplit)
                        return message.channel.send("Syntax Error 2 : mention manquante")
                    }
        
                    if (messageSplit[3]){
                        nombreDeCoins = convertStringToNumber(messageSplit[3]) //nombre de coins a ajouter
                    }else {
                        console.log(messageSplit)
                        return message.channel.send("Syntax Error 3 : Wrong number")
                    }
            
                    console.log(messageSplit)
                    console.log(nombreDeCoins)
                    
            
                    if (!bdd[user.id]){ //Si l'utilisateur n'est pas en bdd on crée un nouvelle utilisateur sur cette ID
                        bdd[user.id] = {
                            "coin": 0,
                            "username" : "undefined"
                        }
                    }
            
                    if (nombreDeCoins) {
                        bdd[user.id].coin = bdd[user.id].coin + nombreDeCoins //Ajoute X coin à la personne mentionnée
                        bdd[user.id].username = user.username
                
                        fs.writeFile("./monnaie.json", JSON.stringify(bdd), (err) => {
                            if(err) message.channel.send("Une erreur est survenue");
                        }); //Permet de sauvegarder dans la bdd
                        message.channel.send(`Vous avez donné ${nombreDeCoins} coins à ${user.username}`)
                    } 
                }
                if (subCommand == "remove"){

                    let mentionned = message.mentions.users.first(); //personne mentionnée
                    let nombreDeCoins
                    let user
    
                    if (mentionned) {
                        user = mentionned
                    } else {
                        console.log(messageSplit)
                        return message.channel.send("Syntax Error 2 : mention manquante")
                    }
        
                    if (messageSplit[3]){
                        nombreDeCoins = convertStringToNumber(messageSplit[3]) //nombre de coins a ajouter
                    }else {
                        console.log(messageSplit)
                        return message.channel.send("Syntax Error 3 : Wrong number")
                    }
            
                    console.log(messageSplit)
                    console.log(nombreDeCoins)
                    
            
                    if (!bdd[user.id]){ //Si l'utilisateur n'est pas en bdd on crée un nouvelle utilisateur sur cette ID
                        bdd[user.id] = {
                            "coin": "0",
                            "username" : "undefined"
                        }
                    }
            
                    if (nombreDeCoins) {
                        bdd[user.id].coin = bdd[user.id].coin - nombreDeCoins //Ajoute X coin à la personne mentionnée
                        bdd[user.id].username = user.username
                
                        fs.writeFile("./monnaie.json", JSON.stringify(bdd), (err) => {
                            if(err) message.channel.send("Une erreur est survenue");
                        }); //Permet de sauvegarder dans la bdd
                        message.channel.send(`Vous avez retiré ${nombreDeCoins} coins à ${user.username}`)
                    } 
                }

            }else {
                console.log(messageSplit)
                return message.channel.send("Syntax Error 1 : insert arguments (give, remove...)")
            }
         
        } else {
            return message.channel.send("Vous n'avez pas le droit !")
        }
    }
}