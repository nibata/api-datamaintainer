from humps import camelize, kebabize


def to_camel(string: str) -> str:  # pragma: no cover
    return camelize(string)


def to_kebab(string: str) -> str:
    return kebabize(string)
