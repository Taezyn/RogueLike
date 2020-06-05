from equipment_slots import EquipmentSlots


class Equipment:
    """
    Classe gérant les objets de type équipable.
    """

    def __init__(self, main_hand=None, off_hand=None):
        """
        Initialise un objet equipable

        Parametres:
        ----------
        main_hand : Entity ou None
            Objet équipé en main droite
        off_hand : Entity ou None
            Objet équipé en main gauche

        Renvoi:
        -------
        Aucun

        """
        self.main_hand = main_hand
        self.off_hand = off_hand

    @property
    def max_hp_bonus(self):
        """
        Permet l'ajout d'HP au joueur si un objet possède cette caractéristique

        Parametres:
        ----------
        Aucun

        Renvoi:
        -------
        Aucun

        """
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus

        return bonus

    @property
    def power_bonus(self):
        """
        Permet l'ajout d'attaque au joueur si un objet possède cette caractéristique

        Parametres:
        ----------
        Aucun

        Renvoi:
        -------
        Aucun

        """
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.power_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.power_bonus

        return bonus

    @property
    def defense_bonus(self):
        """
        Permet l'ajout de défense au joueur si un objet possède cette caractéristique

        Parametres:
        ----------
        Aucun

        Renvoi:
        -------
        Aucun

        """
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defense_bonus

        return bonus

    def toggle_equip(self, equippable_entity):
        """
        Equipe ou déséquipe un objet équipable

        Parametres:
        ----------
        equippable_entity : Entity
            L'objet à équiper ou déséquiper

        Renvoi:
        -------
        results : list
            Liste des résultats. Utilisée dans engine.

        """
        results = []
        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand:
                    results.append({'dequipped': self.main_hand})
                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})
                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        return results
