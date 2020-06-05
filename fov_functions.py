import tcod as libtcod

'''
Initialise le champ de vision sur une carte donnee
'''
def initialize_fov(game_map):
    """
    Initialise le champ de vision d'une carte donnée

    Parametres:
    ----------
    game_map : GameMap

    Renvoi:
    -------
    fov_map : tcod.map
        Champ de vision

    """
    fov_map = libtcod.map_new(game_map.width, game_map.height)
    for y in range(game_map.height):
        for x in range(game_map.width):
            libtcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight,
                                       not game_map.tiles[x][y].blocked)
    return fov_map


def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    """
    Recalcule le champ de vision à partir d'un FOV déjà existant

    Parametres:
    ----------
    fov_map : tcod.map

    x : int

    y : int

    radius : int

    light_walls : bool

    algorithm : int
        Intenditifiant de l'algorithme de calcul du FOV propre à libtcod

    Renvoi:
    -------
    Aucun

    """
    libtcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)
