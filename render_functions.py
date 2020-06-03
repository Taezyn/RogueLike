import tcod as libtcod
from enum import Enum, auto
from game_states import GameStates
from menus import inventory_menu, level_up_menu, character_screen

'''
Ce module gere le rendu visuel des differentes entites
'''

'''
Permet de gerer la priorite des affichages
comme un systeme de calques
'''
class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    STAIRS = auto()
    ACTOR = auto()
    SHOW_INVENTORY = auto()
    DROP_INVENTORY = auto()


'''
Affiche le nom de l'entite sous le pointeur de la souris
'''
def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)
    entities_under_mouse = [entity for entity in entities
             if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    for i in range(len(entities_under_mouse)):
        if entities_under_mouse[i].fighter:
            entities_under_mouse[i] = entities_under_mouse[i].name + ' ' + str(entities_under_mouse[i].fighter.hp) + \
                                      '/' + str(entities_under_mouse[i].fighter.max_hp)
        else:
            entities_under_mouse[i] = entities_under_mouse[i].name
    names = ', '.join(entities_under_mouse)
    return names.capitalize()


'''
Cree une barre de progression, utilisee pour l'XP ou les HP
'''
def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)
    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))


def load_customfont():
    # The index of the first custom tile in the file
    a = 256
    # The "y" is the row index, here we load the sixth row in the font file. Increase the "6" to load any new rows from the file
    for y in range(5, 6):
        libtcod.console_map_ascii_codes_to_font(a, 32, 0, y)
        a += 32


'''
Affiche les pieces, les entites, les menus et tous les elements du jeu
'''
def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width,
               screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state, graphics):
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight
                if visible:
                    if wall:
                        libtcod.console_put_char_ex(con, x, y, graphics.get('wall'), libtcod.white, libtcod.black)
                    else:
                        libtcod.console_put_char_ex(con, x, y, graphics.get('floor'), libtcod.white, libtcod.black)
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_put_char_ex(con, x, y, graphics.get('wall'), libtcod.light_grey, libtcod.black)
                    else:
                        libtcod.console_put_char_ex(con, x, y, graphics.get('floor'), libtcod.light_grey, libtcod.black)
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)
        if entity.ai:
            if entity.ai.ai_name == 'Boss':
                if entity.ai.aoeing:
                    if entity.ai.turn % 10 == 0:
                        color = libtcod.lightest_red
                    elif entity.ai.turn % 10 == 1:
                        color = libtcod.lighter_red
                    elif entity.ai.turn % 10 == 2:
                        color = libtcod.light_red
                    elif entity.ai.turn % 10 == 3:
                        color = libtcod.red
                    radius = entity.ai.radius
                    for x in range(entity.x - radius, entity.x + radius + 1):
                        for y in range(entity.y - radius, entity.y + radius + 1):
                            if ((x - entity.x)**2 + (y - entity.y)**2)**0.5 <= radius:
                                    libtcod.console_set_char_foreground(con, x, y, color)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)
    libtcod.console_print_ex(panel, 1, 2, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Salle : {0} - LVL : {1}'.format(game_map.dungeon_level, player.level.current_level))
    boss_bar = False
    for entity in entities:
        if entity.name == 'Boss':
            boss_bar = True
            boss = entity.fighter
    if boss_bar:
        render_bar(panel, 1, 3, bar_width, 'Boss HP', boss.hp, boss.max_hp,
                   libtcod.orange, libtcod.darker_orange)
    else:
        render_bar(panel, 1, 3, bar_width, 'XP', player.level.current_xp, player.level.experience_to_next_level,
                   libtcod.light_purple, libtcod.darker_purple)
    libtcod.console_print_ex(panel, 1, 4, libtcod.BKGND_NONE, libtcod.LEFT,
                             'ATQ : {0} - DEF : {1}'.format(player.fighter.power, player.fighter.defense))

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             get_names_under_mouse(mouse, entities, fov_map))
    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)
    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Echap pour quitter, A/B/C... pour utiliser.\n'
        else:
            inventory_title = 'Echap pour quitter, A/B/C... pour lacher\n'
        inventory_menu(con, inventory_title, player, 50, screen_width, screen_height)
    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, 'Level up, choisis une amelioration :', player, 40, screen_width, screen_height)
    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)


'''
Affiche une entite visible
'''
def draw_entity(con, entity, fov_map, game_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        if entity.visible:
            libtcod.console_set_default_foreground(con, entity.color)
            libtcod.console_put_char_ex(con, entity.x, entity.y, entity.char, libtcod.white, libtcod.black)
    elif game_map.tiles[entity.x][entity.y].explored:
        libtcod.console_put_char_ex(con, entity.x, entity.y, 257, libtcod.light_grey, libtcod.black)

'''
Permet au changement d'etage d'effacer l'affichage des items, monstres et cadavres
'''
def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)


'''
Efface toutes les entites de l'ecran
'''
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)
