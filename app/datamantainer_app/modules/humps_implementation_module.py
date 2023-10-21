from humps import camelize, kebabize


def to_camel(string: str) -> str:
    return camelize(string)


def to_kebab(string: str) -> str:
    return kebabize(string)
