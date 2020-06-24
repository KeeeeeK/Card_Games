class CG_Card:
    __slots__ = ('name', 'description')

    def __init__(self, name: str, description: str):
        self.name: str = name
        self.description: str = description

    def __str__(self):
        return self.name
