class Random:
    def __init__(self, name: str, id: int, birthadate: str):
        self.name = name
        self.id = id
        self.birthadate = birthadate

    def __repr__(self):
        return f"Random(name={self.name!r}, id={self.id!r}, birthadate={self.birthadate!r})"
