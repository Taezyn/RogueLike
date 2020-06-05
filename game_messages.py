import tcod as libtcod
import textwrap

"""
Ce module gere la boite dans laquelle les messages defilent.
"""


class Message:
    """
    Gère l'objet Message
    """
    def __init__(self, text, color=libtcod.white):
        """
        Crée un message

        Parametres:
        ----------
        text : str
            Le message en lui même
        color : tcod.color
            Sa couleur

        Renvoi:
        -------
        Aucun

        """
        self.text = text
        self.color = color


class MessageLog:
    """
    Gère la boîte de dialogue dans laquelle s'affichent les message
    """
    def __init__(self, x, width, height):
        """
        Crée un boîte de dialogue

        Parametres:
        ----------
        x : int
            Ancrage de la boîte de dialogue
        width : int
            Largeur
        height : int
            Hauteur

        Renvoi:
        -------
        Aucun

        """
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        """
        Ajoute un message à la boîte de dialogue, le coupe en plusieurs ligne si besoin

        Parametres:
        ----------
        message : Message

        Renvoi:
        -------
        Aucun

        """
        new_msg_lines = textwrap.wrap(message.text, self.width)
        for line in new_msg_lines:
            if len(self.messages) == self.height:
                del self.messages[0]
            self.messages.append(Message(line, message.color))
