"""
Runtime patches for genshin.py library gaps.
Apply at startup before any data fetching.
"""


def _extend_int_enum(enum_cls, known_range):
    """Add any missing integer values in `known_range` to an IntEnum class."""
    for value in known_range:
        if value not in enum_cls._value2member_map_:
            name = f"UNKNOWN_{value}"
            new_member = int.__new__(enum_cls, value)
            new_member._name_ = name
            new_member._value_ = value
            enum_cls._value2member_map_[value] = new_member
            enum_cls._member_map_[name] = new_member


def patch_zzz_enums() -> None:
    """Patch ZZZ enums to tolerate unknown values from new game content.

    genshin.py's enums only contain known values. When miHoYo adds a new
    element type or agent specialty, the API returns a value not yet in the
    enum, causing a pydantic validation error. We extend _value2member_map_
    with placeholders so ZZZElementType(unknown) and ZZZSpecialty(unknown)
    succeed instead of raising ValueError.
    """
    try:
        from genshin.models.zzz.character import ZZZElementType, ZZZSpecialty
        _extend_int_enum(ZZZElementType, list(range(200, 220)) + list(range(300, 320)))
        _extend_int_enum(ZZZSpecialty, range(1, 20))
    except Exception:
        pass


# Keep old name as alias so any lingering local imports still work
patch_zzz_element_type = patch_zzz_enums
