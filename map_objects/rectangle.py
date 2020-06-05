class Rect:
    """
    Gère la création d'une pièce et permet de tester son
    intersection avec une autre pièce déjà existante.
    """
    def __init__(self, x, y, w, h):
        """
        Crée un objet Rect.

        Parametres:
        ----------
        x : int
            Abscisse de l'angle supérieur gauche
        y : int
            Ordonnée de l'angle supérieur gauche
        w : int
            Largeur
        h : int
            Hauteur

        Renvoi:
        -------
        Aucun
        """
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        """
        Détermine le centre d'une pièce

        Parametres:
        ----------
        Aucun

        Renvoi:
        -------
        center_x : int

        center_y : int

        """
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    def intersect(self, other):
        """
        Teste l'intersection d'une pièce avec une autre

        Parametres:
        ----------
        other : Rect

        Renvoi:
        -------
        bool

        """
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
