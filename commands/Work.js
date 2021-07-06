module.exports = class Work {

    static match (message, prefix) {
        if (message.content.startsWith(prefix+'work') || message.content.startsWith(prefix+'w')){
            return message.content
        }
    }

    static action (message, bdd, fs) {
        // let args = message.content.split (' ')
        // args.shift()

        // TODO
        // Creer un timer pour le "travail"
        // TODO
        // Ecrire le code pour ajouter les coins du au "travail"
        // Randomisation ?
    }
}