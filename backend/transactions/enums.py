import enum


class BaseEnum(enum.Enum):
    @classmethod
    def choices(cls):
        return tuple((field.value, field.name) for field in cls)

    @classmethod
    def values(cls):
        return [field.value for field in cls]

    @classmethod
    def get_name_by_value(cls, value):
        for field in cls:
            if field.value == value:
                return field.name
        return None


class PlayerTransactionEnum(BaseEnum):
    ADMIN_TO_PLAYER_GAME = 1
    PLAYER_TO_ADMIN_PROFIT = 2
    ADMIN_TO_PLAYER_SALARY = 3


class RoomTransactionEnum(BaseEnum):
    PLAYER_TO_ROOM = 1
    ROOM_TO_PLAYER = 2
