from .Matrix import Matrix


def compare(lhs: str, rhs: str):
    return Matrix(len(lhs), len(rhs)).fit(lhs, rhs).similarity

    # dst = (matrix := Matrix(len(lhs), len(rhs)).fit(lhs, rhs)).distance

    # print(matrix.values)

    # print(dst)
