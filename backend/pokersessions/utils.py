from core.utils import get_qs_by_dates_from_params, order_qs_from_params


def get_session_qs(model, player, params):
    qs = get_qs_by_dates_from_params(model, player, params)
    qs = order_qs_from_params(qs, params)

    try:
        result = int(params.get('result'))
        if result == 0:
            pass
        elif result == 1:
            qs = qs.filter(result__gte=0)
        elif result == 2:
            qs = qs.filter(result__lt=0)
    except (ValueError, TypeError):
        pass

    return qs
