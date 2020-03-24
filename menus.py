import tcod as libtcod


# Cree les differents menus affiches au cours d'une partie

# Permet l'affichage d'un menu generique dont les lignes
# sont ecrites dans la variable 'options'
def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Plus de 26 items.')
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


# Cree un menu de l'inventaire avec pour chaque item une option
def inventory_menu(con, header, inventory, inventory_width, screen_width, screen_height):
    if len(inventory.items) == 0:
        options = ['Inventaire vide.']
    else:
        options = [item.name for item in inventory.items]
    menu(con, header, options, inventory_width, screen_width, screen_height)


# Cree le menu principal du jeu
def main_menu(con, background_image, screen_width, screen_height):
    libtcod.image_blit_2x(background_image, 0, 0, 0)
    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width/2), 2, libtcod.BKGND_NONE,
                             libtcod.CENTER, "Rogue doesn't like")
    menu(con, '', ['Nouvelle partie', 'Continuer la partie precedente', '(Rage)quit', '', 'Son on/off', 'Commandes'], 24, screen_width, screen_height)


# Cree le menu de level-up
def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ['Sante (+20 PV, actuellement {0})'.format(player.fighter.max_hp),
               'Force (+1 attaque, actuellement {0})'.format(player.fighter.power),
               'Defense (+1 defense, actuellement {0})'.format(player.fighter.defense)]
    menu(con, header, options, menu_width, screen_width, screen_height)


# Cree le menu d'info personnage
def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = libtcod.console_new(character_screen_width, character_screen_height)
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, "--- Informations d'@ ---")
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


# Cree la boite de messages defilants
def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)


# Cree le menu avec les commandes disponibles
def command_menu(con, background_image, screen_width, screen_height):
    libtcod.image_blit_2x(background_image, 0, 0, 0)
    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), 2, libtcod.BKGND_NONE,
                             libtcod.CENTER, "Rogue doesn't like")
    libtcod.console_print_ex(0, int(screen_width / 2), 10, libtcod.BKGND_NONE,
                             libtcod.CENTER, 'Comment jouer ?')
    menu(con, '', ['Deplacement : Fleches et Z,Q,S,D', 'Diagonale : A,E,W,C',
                   'Passer un tour : X', 'Attraper un item : G', 'Lacher un item : L',
                   'Prendre les escaliers > : Entree', '', 'Retour au jeu : Echap'],
         40, screen_width, screen_height)
