import tcod as libtcod


# Initialise le champ de vision sur une carte donnee
def initialize_fov(game_map):
    fov_map = libtcod.map_new(game_map.width, game_map.height)
    for y in range(game_map.height):
        for x in range(game_map.width):
            libtcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight,
                                       not game_map.tiles[x][y].blocked)
    return fov_map


# Recalcule le champ de vision a partir d'une carte de vision deja existante
def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    libtcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)
