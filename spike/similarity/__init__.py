from .Matrix import Matrix


def compare(lhs: str, rhs: str):
    return Matrix(len(lhs), len(rhs)).fit(lhs, rhs).similarity

    # dst = (matrix := Matrix(len(lhs), len(rhs)).fit(lhs, rhs)).distance

    # print(matrix.values)

    # print(dst)


def rank(lhs: str, rhs: [str], top_n: int = None, get_utterance: callable = lambda x: x, threshold: float = 0.5):
    unsorted_entries = []

    for item in rhs:
        if (score := compare(lhs, get_utterance(item))) >= threshold:
            unsorted_entries.append((score, item))

    entries = sorted(
        unsorted_entries,
        key = lambda a: a[0],
        reverse = True
    )

    if top_n is None:
        return [item[1] for item in entries]
    else:
        print([item[0] for item in entries[:top_n]])
        return [item[1] for item in entries[:top_n]]
