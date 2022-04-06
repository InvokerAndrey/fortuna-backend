from core.utils import get_qs_by_dates_from_params, order_qs_from_params
from dateutil.parser import parse


def get_transaction_qs(model, type_enum, player, params):
    qs = get_qs_by_dates_from_params(model, player, params)
    qs = order_qs_from_params(qs, params)
    qs = filter_by_type(qs, params, type_enum)
    return qs


def get_fund_transactions_qs(model, type_enum, fund, params):
    start_date = None
    end_date = None

    if params.get('start_date'):
        try:
            start_date = parse(params.get('start_date'))
        except (TypeError, ValueError):
            pass

    if params.get('end_date'):
        try:
            end_date = parse(params.get('end_date'))
        except (TypeError, ValueError):
            pass

    if all([start_date, end_date]):
        qs = model.objects.filter(created_at__range=[start_date, end_date], fund=fund)
    elif start_date:
        qs = model.objects.filter(created_at__gte=start_date, fund=fund)
    elif end_date:
        qs = model.objects.filter(created_at__lte=end_date, fund=fund)
    else:
        qs = model.objects.filter(fund=fund)

    order = params.get('order')
    if order:
        qs = qs.order_by(params.get('order'), '-pk' if order.startswith('-') else 'pk')
    else:
        qs = qs.order_by('-created_at', '-pk')
    qs = filter_by_type(qs, params, type_enum)
    return qs


def filter_by_type(qs, params, type_enum):
    try:
        type_ = int(params.get('type'))
        if type_ in type_enum.values():
            return qs.filter(type=type_)
        return qs
    except (ValueError, TypeError):
        return qs
