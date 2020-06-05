import tcod as libtcod
from read_scores import read_scores

"""
Cree les differents menus affiches au cours d'une partie
"""


def menu(con, header, options, width, screen_width, screen_height):
    """
    Permet l'affichage d'un menu générique dont les lignes sont écrites dans la variable options

    Parametres:
    ----------
    con : tcod.console
        Console
    header : str
        Titre du menu
    options : list
        Liste des options du menu
    width : int
        Largeur du menu
    screen_width : int
        Largeur de l'écran
    screen_height : int
        Hauteur de l'écran

    Renvoi:
    -------
    Aucun

    """
    if len(options) > 26:
        raise ValueError('Plus de 26 items.')
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height
    window = libtcod.console_new(width, height)
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        if option_text != '':
            text = '(' + chr(letter_index) + ') ' + option_text
            libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
            y += 1
            letter_index += 1
        else:
            text = ''
            libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
            y += 1
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
    """
    Permet l'affichage de l'inventaire

    Parametres:
    ----------
    con : tcod.console
        Console
    header : str
        Titre du menu
    player : Entity
        Joueur
    inventory_width : int
        Largeur du menu
    screen_width : int
        Largeur de l'écran
    screen_height : int
        Hauteur de l'écran

    Renvoi:
    -------
    Aucun

    """
    if len(player.inventory.items) == 0:
        options = ['Inventaire vide.']
    else:
        options = []
        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append('{0} main droite'.format(item.name))
            elif player.equipment.off_hand == item:
                options.append('{0} main gauche'.format(item.name))
            else:
                options.append(item.name)
    libtcod.console_print_ex(0, int(screen_width / 2), 10, libtcod.BKGND_NONE, libtcod.CENTER, "Inventaire : " +
                             str(len(player.inventory.items)) + '/' + str(player.inventory.capacity))
    menu(con, header, options, inventory_width, screen_width, screen_height)


def main_menu(con, background_image, screen_width, screen_height):
    """
    Permet l'affichage du menu principal

    Parametres:
    ----------
    con : tcod.console
        Console
    background_image : fichier .png
        Image de fond du menu
    screen_width : int
        Largeur de l'écran
    screen_height : int
        Hauteur de l'écran

    Renvoi:
    -------
    Aucun

    """
    black_screen(con, screen_width, screen_height)
    libtcod.image_blit_2x(background_image, 0, 0, 0)
    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width/2), 2, libtcod.BKGND_NONE,
                             libtcod.CENTER, "Rogue dislike")
    menu(con, '', ['Nouvelle partie', 'Reprendre partie sauvegardee', '(Rage)quit', '', 'Son on/off', 'Commandes', 'Scores'], 32, screen_width, screen_height)


def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    """
    Permet l'affichage d'un menu lors d'un level-up

    Parametres:
    ----------
    con : tcod.console
        Console
    header : str
        Titre du menu
    player : Entity
        Joueur
    menu_width : int
        Largeur du menu
    screen_width : int
        Largeur de l'écran
    screen_height : int
        Hauteur de l'écran

    Renvoi:
    -------
    Aucun

    """
    options = ['Sante (+20 PV, actuellement {0})'.format(player.fighter.max_hp),
               'Force (+1 attaque, actuellement {0})'.format(player.fighter.power),
               'Defense (+1 defense, actuellement {0})'.format(player.fighter.defense)]
    if len(player.inventory.items) <= 24:
        options = options + ['', '            Bonus :', "Taille de l'inventaire : +2"]
    elif len(player.inventory.items) == 25:
        options = options + ['', '            Bonus :', "Taille de l'inventaire : +1"]
    menu(con, header, options, menu_width, screen_width, screen_height)


def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    """
    Permet l'affichage d'un menu d'infos personnage

    Parametres:
    ----------
    player : Entity
        Joueur
    character_screen_width : int
        largeur du menu
    character_screen_height : int
        Hauteur du menu
    screen_width : int
        Largeur de l'écran
    screen_height : int
        Hauteur de l'écran

    Renvoi:
    -------
    Aucun

    """
    window = libtcod.console_new(character_screen_width, character_screen_height)
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, "---- Informations ----")
    libtcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Niveau : {0}'.format(player.level.current_level))
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'XP : {0}'.format(player.level.current_xp))
    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Prochain niveau : {0}'.format(player.level.experience_to_next_level - player.level.current_xp))
    libtcod.console_print_rect_ex(window, 0, 5, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'PV max : {0}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Attaque: {0}'.format(player.fighter.power))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Defense: {0}'.format(player.fighter.defense))
    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)


def message_box(con, header, width, screen_width, screen_height):
    """
    Permet l'affichage d'une boite de dialogue si le joueur veut charger une sauvegarde alors qu'il n'en a pas

    Parametres:
    ----------
    con : tcod.console
        Console
    header : str
        Message d'erreur
    width : int
        Largeur du menu
    screen_width : int
        Largeur de l'écran
    screen_height : int
        Hauteur de l'écran

    Renvoi:
    -------
    Aucun

    """
    menu(con, header, [], width, screen_width, screen_height)


def command_menu(con, background_image, screen_width, screen_height):
    """
    Permet l'affichage d'un menu avec les commandes de jeu

    Parametres:
    ----------
    con : tcod.console
        Console
    background_image : fichier .png
        Image de fond
    screen_width : int
        Largeur de l'écran
    screen_height : int
        Hauteur de l'écran

    Renvoi:
    -------
    Aucun

    """
    libtcod.image_blit_2x(background_image, 0, 0, 0)
    black_screen(con, screen_width, screen_height)
    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), 2, libtcod.BKGND_NONE,
                             libtcod.CENTER, "Rogue dislike")
    libtcod.console_print_ex(0, int(screen_width / 2), 10, libtcod.BKGND_NONE,
                             libtcod.CENTER, 'Comment jouer ?')
    menu(con, '', ['Deplacement : Fleches et Z,Q,S,D', 'Diagonale : A,E,W,C',
                   'Passer un tour : X', 'Attraper un item : G', 'Lacher un item : L',
                   'Prendre les escaliers > : Entree', '', 'Retour au jeu : Echap'],
         40, screen_width, screen_height)


def scores_menu(con, background_image, screen_width, screen_height):
    """
    Permet l'affichage d'un tableau des scores

    Parametres:
    ----------
    con : tcod.console
        Console
    background_image : fichier .png
        Image de fond
    screen_width : int
        Largeur de l'écran
    screen_height : int
        Hauteur de l'écran

    Renvoi:
    -------
    Aucun

    """
    libtcod.image_blit_2x(background_image, 0, 0, 0)
    black_screen(con, screen_width, screen_height)
    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), 2, libtcod.BKGND_NONE,
                             libtcod.CENTER, "Rogue dislike")
    libtcod.console_print_ex(0, int(screen_width / 2), 10, libtcod.BKGND_NONE,
                             libtcod.CENTER, '*** Hall of Fame ***')
    menu(con, '', read_scores(), 30, screen_width, screen_height)


def black_screen(con, screen_width, screen_height):
    """
    Permet l'affichage d'un écran noir, servant à cacher le menu précédant pour en afficher un nouveau
    en évitant toute superposition

    Parametres:
    ----------
    con : tcod.console
        Console
    screen_width : int
        Largeur de l'écran
    screen_height : int
        Hauteur de l'écran

    Renvoi:
    -------
    Aucun

    """
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
    libtcod.console_set_default_background(con, libtcod.black)
    libtcod.console_clear(con)
