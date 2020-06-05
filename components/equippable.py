class Equippable:
    """
    Permet l'ajout d'un composant "equipable" à une entité.
    """
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
        """
        Initialise un composant "équipable" à une entité.

        Parametres:
        ----------
        slot : int
            1 ou 2 pour la main droite ou gauche
        power_bonus : int
            Bonus d'attaque
        defense_bonus : int
            Bonus de défense
        max_hp_bonus : int
            Bonus d'HP

        Renvoi:
        -------
        Aucun

        """
        self.slot = slot
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
