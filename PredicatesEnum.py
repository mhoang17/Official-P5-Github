import enum


class PredicatesEnum(enum.Enum):
    STARRED_IN = 'starred_in'
    HAS_ACTOR = 'has_actor'
    DIRECTED = 'directed'
    HAS_DIRECTOR = 'has_director'
    WROTE = 'wrote'
    HAS_WRITER = 'has_writer'
