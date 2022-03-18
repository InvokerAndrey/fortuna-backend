from dateutil.parser import parse


def get_qs_by_dates_from_params(model, params):
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
        qs = model.objects.filter(created_at__range=[start_date, end_date])
    elif start_date:
        qs = model.objects.filter(created_at__gte=start_date)
    elif end_date:
        qs = model.objects.filter(created_at__lte=end_date)
    else:
        qs = model.objects.all()
    return qs


def order_qs_from_params(qs, params):
    order = params.get('order')
    if order:
        return qs.order_by(params.get('order'), '-pk' if order.startswith('-') else 'pk')
    return qs.order_by('-created_at', '-pk')
