class Tweet:
    def __init__(self, contenu: str, auteur: str, date_creation: str, public_metrics: dict, *args,
                 **kwargs) -> None:
        self.public_metrics = public_metrics
        self.date_creation = date_creation
        self.auteur = auteur
        self.contenu = contenu
        self.other = kwargs
