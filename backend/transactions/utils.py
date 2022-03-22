from core.utils import get_qs_by_dates_from_params, order_qs_from_params


def get_transaction_qs(model, type_enum, player, params):
    qs = get_qs_by_dates_from_params(model, player, params)
    qs = order_qs_from_params(qs, params)

    try:
        _type = int(params.get('type'))
        if _type == 0:
            pass
        elif _type in type_enum.values():
            qs = qs.filter(type=_type)
    except (ValueError, TypeError):
        pass

    return qs
