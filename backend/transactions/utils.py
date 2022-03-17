from dateutil.parser import parse


def get_transaction_qs(model, type_enum, params):
    print(params)
    start_date = None
    end_date = None

    if params.get('start_date'):
        try:
            start_date = parse(params.get('start_date'))
            print(start_date)
        except (TypeError, ValueError):
            pass

    if params.get('end_date'):
        try:
            end_date = parse(params.get('end_date'))
            print(end_date)
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

    order = params.get('order')
    if order:
        qs = qs.order_by(params.get('order'), '-pk' if order.startswith('-') else 'pk')
    else:
        qs.order_by('-created_at', '-pk')

    try:
        _type = int(params.get('type'))
        if _type == 0:
            pass
        elif _type in type_enum.values():
            qs = qs.filter(type=_type)
    except (ValueError, TypeError):
        pass

    return qs
