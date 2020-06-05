class Item:
    """
    Définit le composant Item
    """

    def __init__(self, use_function=None, targeting=False, targeting_message=None, **kwargs):
        """
        Crée un item.

        Parametres:
        ----------
        use_function : function
            Eventuelle fonction de l'item à utiliser lors de l'activation
        targeting : bool
            Le joueur doit-il cibler un monstre ?
        targeting_message : Message
            Le cas échant : le message à afficher lors du ciblage
        **kwargs : dict
            Arguments de use_function

        Renvoi:
        -------
        Aucun

        """
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs
