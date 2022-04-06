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


class PlayerTransactionTypeEnum(BaseEnum):
    ADMIN_TO_PLAYER_GAME = 1
    PLAYER_TO_ADMIN_DUTY = 2
    PLAYER_TO_ADMIN_PROFIT = 3


class RoomTransactionTypeEnum(BaseEnum):
    DEPOSIT = 1
    WITHDRAWAL = 2


class FundTransactionTypeEnum(BaseEnum):
    DEPOSIT = 1
    WITHDRAWAL = 2
