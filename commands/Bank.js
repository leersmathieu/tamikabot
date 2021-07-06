//COMMANDE POUR VOIR SON SOLDE (coins)

module.exports = class Bank {

    static match (message, prefix) {
        return message.content.startsWith(prefix+'bank')
    }

    static action (message, bdd) {
        let mentionned = message.mentions.users.first();
        let user;
        if(mentionned) { //Si mention, alors on affiche le compte de la personne mentionnée
            user = mentionned;
            if (bdd[user.id]){
                let coin = bdd[user.id].coin; 
                if(coin === 1){
                    message.channel.send(`${user} dispose de ${coin} coin `);
                }else {
                    message.channel.send(`${user} dispose de ${coin} coins `);
                }
            }else {
                message.channel.send(`${user} n'a pas encore de coins `);
            }
        }
        else { // Sinon, on affiche le compte de la personne qui a tapé la commande
            user = message.author;
            if (bdd[user.id]){
                let coin = bdd[user.id].coin; 
                if(coin === 1){
                    message.channel.send(`Tu disposes de ${coin} coin `);
                }else {
                    message.channel.send(`Tu disposes de ${coin} coins `);
                }
            }else {
                message.channel.send(`Tu n'as pas encore de coins `);
            }
        } 
    }


}