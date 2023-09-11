def put_prefix(uri: str, prefix: str):
    parts = uri.split('#')

    if len(parts) < 2:
        return uri

    return f'{prefix}:{parts[1]}'


def cut_prefix(uri: str, prefixes: dict[str, str], sep: str = '#'):
    reversed_parts = uri[::-1].split(sep, maxsplit = 1)
    parts = [part[::-1] for part in reversed_parts[::-1]]

    if len(parts) < 2:
        if sep == '#':
            return cut_prefix(uri, prefixes, sep = '/')
        return uri

    if prefix := prefixes.get(parts[0]):
        return f'{prefix}:{parts[1]}'

    raise ValueError(f'Cannot find prefix shortcut for uri {parts[0]}')
