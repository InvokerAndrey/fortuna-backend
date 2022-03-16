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
    PLAYER_TO_ADMIN_PROFIT = 2
    ADMIN_TO_PLAYER_SALARY = 3


class RoomTransactionTypeEnum(BaseEnum):
    DEPOSIT = 1
    WITHDRAWAL = 2


class RoomTransactionSortEnum(BaseEnum):
    CREATED_AT = {
        'field': 'created_at',
        'sort_param': '-created_at'
    }

    @classmethod
    def get_sort_by_field(cls, field_name):
        for field in cls:
            if field.value['field'] == field_name:
                return field.value['sort_param']
