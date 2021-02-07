class CountFromBy:
    def __init__(self, v: int = 0, i: int = 1) -> None:
        self.val = v
        self.increment = i

    def increase(self) -> None:
        self.val += self.increment

    ''' add a dunder to print object's representation '''
    def __repr__(self) -> str:
        return str(self.val)


if __name__ == '__main__':
    g = CountFromBy(100, 10)
    g.increase()

    print("object.increment = ", g.increment)
    print("object.val =", g.val)

    print("Object value = ", g)
