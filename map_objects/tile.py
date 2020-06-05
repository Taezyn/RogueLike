class Tile:
    def __init__(self, blocked, block_sight=None):
        """
        Crée une case

        Parametres:
        ----------
        blocked : bool

        block_sight : bool


        Renvoi:
        -------
        Aucun.

        """
        self.blocked = blocked
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight
        self.explored = False
