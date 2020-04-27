import tcod as libtcod
from death_functions import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location, all_dead
from fov_functions import initialize_fov, recompute_fov
from game_messages import Message
from game_states import GameStates
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from render_functions import clear_all, render_all
from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box, command_menu
import pygame
import sound_manager.sound_manager as sm


#############################################################################################################
# Petit - Pedreno, groupe TD5, projet Roguelike
#############################################################################################################
# Pour le bon fonctionnement du jeu, il faut prendre soin d'installer ces modules
# pyagme : pip install pygame
# libtcod : pip install tcod
# shelve : pip install shelve
# Il est egalement necessaire de telecharger le package sound_manager a placer
# a la racine du dossier : https://drive.google.com/file/d/1QoRqnRn0m8dKuj2Xk8YpXeL8tOeouQtu/view?usp=sharing
#############################################################################################################
# Ce module gere l'execution du jeu dans son ensemble.
# Les explications seront donnees au sein meme des fonction afin
# de conserver une vision globale des choses.
#############################################################################################################


def main():
    # Initialise le jeu en commencant par afficher le menu principal
    constants = get_constants()

    libtcod.console_set_custom_font('arial10x10 - Copie.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], "Rogue doesn't like", False)

    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
    panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False
    show_command_menu = False

    main_menu_background_image = libtcod.image_load('menu_background.png')

    bg_music = sm.Son(constants.get('sound').get('background_music')[0])

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        # Si le menu principal est affiche :
        if show_main_menu:
            main_menu(con, main_menu_background_image, constants['screen_width'], constants['screen_height'])
            if show_load_error_message:
                message_box(con, 'Rien a charger', 70, constants['screen_width'], constants['screen_height'])

            libtcod.console_flush()

            action = handle_main_menu(key)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')
            sound = action.get('sound')
            command = action.get('command')
            back_to_game = action.get('back_to_game')

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            # Cree une nouvelle partie
            elif new_game:
                player, entities, game_map, message_log, game_state = get_game_variables(constants)
                game_state = GameStates.PLAYERS_TURN
                show_main_menu = False
            # Charge une partie existante, si possible
            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                save_game(player, entities, game_map, message_log, game_state)
                sm.close_sound()
                break
            # Lit ou arrete la musique de fond
            elif sound:
                bg_music.playpause()
            elif command:
                show_command_menu = True
                show_main_menu = False
            elif back_to_game and show_main_menu:
                show_main_menu = False

        elif show_command_menu:
            action = handle_main_menu(key)
            command_menu(con, main_menu_background_image, constants['screen_width'], constants['screen_height'])
            libtcod.console_flush()
            back_to_game = action.get('back_to_game')
            if back_to_game:
                show_main_menu = False
                show_command_menu = False
                libtcod.console_clear(con)

        # Lance une partie
        else:
            libtcod.console_clear(con)
            player, entities, game_map, message_log, game_state = play_game(player, entities, game_map, message_log, game_state, con, panel, constants)
            show_main_menu = True


def play_game(player, entities, game_map, message_log, game_state, con, panel, constants):
    sword_sounds = constants.get('sound').get('sword')
    hurt_sound = sm.Son(constants.get('sound').get('hurt')[0])
    clean_stage_sound = sm.Son(constants.get('sound').get('clean_stage')[0])

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    targeting_item = None

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'],
                          constants['fov_algorithm'])
        # Affiche la carte generee
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log,
                   constants['screen_width'], constants['screen_height'], constants['bar_width'],
                   constants['panel_height'], constants['panel_y'], mouse, constants['colors'], game_state)

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        # Lit les touches pressees pour en deduire quoi faire
        # Depend du gamestate
        move = action.get('move')
        wait = action.get('wait')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        take_stairs = action.get('take_stairs')
        level_up = action.get('level_up')
        show_character_screen = action.get('show_character_screen')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        player_turn_results = []

        hp80 = 0.80*player.fighter.max_hp
        hp60 = 0.60*player.fighter.max_hp
        hp40 = 0.40*player.fighter.max_hp
        hp20 = 0.20*player.fighter.max_hp

        # Si c'est au joueur et qu'il presse une touche de deplacement
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)
                if target:
                    attack_results = player.fighter.attack(target)
                    sword = sm.choose_sound(sword_sounds)
                    sword.playpause()
                    player_turn_results.extend(attack_results)
                    if all_dead(entities):
                        player.level.add_xp(0.1 * player.level.level_up_base)
                        clean_stage_sound.playpause()
                        message_log.add_message(Message('Plus de monstres, bonus 10% XP', libtcod.yellow))
                        for entity in entities:
                            if entity.stairs:
                                entity.visible = True

                else:
                    player.move(dx, dy)
                    fov_recompute = True
                game_state = GameStates.ENEMY_TURN

        # Si le joueur passe son tour
        elif wait:
            game_state = GameStates.ENEMY_TURN

        # Si le joueur ramasse un objet
        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)
                    break
            else:
                message_log.add_message(Message('Rien a ramasser', libtcod.yellow))

        # Si le joueur consulte son inventaire
        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        # Si le joueur souhaite jeter un item
        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        # Si le joueur est dans son inventaire : que faire pour utiliser ou jetter un item
        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD \
                and inventory_index < len(player.inventory.items):
            item = player.inventory.items[inventory_index]
            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        # Passage au niveau suivant
        if take_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    entities = game_map.next_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)
                    break
            else:
                message_log.add_message(Message("Il n'y a pas d'escaliers ici.", libtcod.yellow))

        if level_up:
            if level_up == 'hp':
                player.fighter.max_hp += 20
                player.fighter.hp += 20
            elif level_up == 'str':
                player.fighter.power += 1
            elif level_up == 'def':
                player.fighter.defense += 1
            game_state = previous_game_state

        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN

        # Si le joueur est en train de cibler avec un parchemin
        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click
                item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                        target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN, GameStates.MENU_SCREEN):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                return player, entities, game_map, message_log, game_state

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # Execute tous les resultats precedent
        # Qui ne sont pas None
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            xp = player_turn_result.get('xp')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)
                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)
                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING
                targeting_item = targeting
                message_log.add_message(targeting_item.item.targeting_message)

            if targeting_cancelled:
                game_state = previous_game_state
                message_log.add_message(Message('Targeting cancelled'))

            if xp:
                leveled_up = player.level.add_xp(xp)
                message_log.add_message(Message('+{0} XP'.format(xp)))
                if leveled_up:
                    message_log.add_message(Message('Level UP : niveau {0} atteint !'.format(
                        player.level.current_level), libtcod.yellow))
                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP

        # Gere le tour des enemis : parcours toutes les entites et fait jouer les fighter ai
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    hp_before_attack = player.fighter.hp
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)
                    if (player.fighter.hp <= hp80 < hp_before_attack) \
                            or (player.fighter.hp <= hp60 < hp_before_attack) \
                            or (player.fighter.hp <= hp40 < hp_before_attack) \
                            or (player.fighter.hp <= hp20 < hp_before_attack):
                        hurt_sound.playpause()
                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')
                        if message:
                            message_log.add_message(message)
                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)
                            message_log.add_message(message)
                            if game_state == GameStates.PLAYER_DEAD:
                                break
                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN

    #return player, entities, game_map, message_log, game_state


if __name__ == '__main__':
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
    main()
