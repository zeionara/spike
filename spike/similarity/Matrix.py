INSERTION_COST = 1
DELETION_COST = 1
REPLACEMENT_COST = 1
NO_OPERATION_COST = 0


class Matrix:
    def __init__(self, n_rows: int, n_cols: int):
        self.n_rows = n_rows
        self.n_cols = n_cols

        self.values = [
            [
                j if i == 0 else
                i if j == 0 else
                None
                for j in range(n_cols + 1)]
            for i in range(n_rows + 1)
        ]

    def set(self, i: int, j: int, equal: bool = False):
        self.values[i][j] = value = min(
            self.values[i][j - 1] + DELETION_COST,
            self.values[i - 1][j] + INSERTION_COST,
            self.values[i - 1][j - 1] + (
                NO_OPERATION_COST if equal else REPLACEMENT_COST
            )
        )

        return value

    def fit(self, lhs, rhs, compare: callable = lambda a, b: a == b):
        for i, x in enumerate(lhs):
            for j, y in enumerate(rhs):
                self.set(i + 1, j + 1, equal = compare(x, y))

        return self

    @property
    def distance(self):
        return self.values[self.n_rows][self.n_cols] / max(self.n_rows, self.n_cols)

    @property
    def similarity(self):
        return 1 - self.distance
