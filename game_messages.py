import tcod as libtcod
import textwrap


# Ce module gere la boite dans laquelle les messages defilent.


class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    # Ajoute un message a la boite des messages, coupe un message trop long pour l'afficher
    # sur plusieurs lignes si besoin
    def add_message(self, message):
        new_msg_lines = textwrap.wrap(message.text, self.width)
        for line in new_msg_lines:
            if len(self.messages) == self.height:
                del self.messages[0]
            self.messages.append(Message(line, message.color))
