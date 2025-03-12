from datetime import datetime, timedelta

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Q, Count
from django_filters import rest_framework as filters

from apps.models import Stadium


class StadiumListFilter(filters.FilterSet):
    ORDER_BY_CHOICES = (
        ('location_asc', 'Location Asc'),
        ('location_desc', 'Location Desc'),
    )

    location = filters.CharFilter(method='filter_location')
    order_by = filters.ChoiceFilter(method='order_by_location', choices=ORDER_BY_CHOICES)
    start_date = filters.DateFilter(method='return_queryset1')
    end_date = filters.DateFilter(method='return_queryset')

    class Meta:
        model = Stadium
        fields = ['location', 'order_by', 'start_date', 'end_date']

    def return_queryset1(self, queryset, *args, **kwargs):
        return queryset

    def return_queryset(self, queryset, name, end_date):
        if self.data.get('start_date') and end_date:
            start_date = datetime.strptime(self.data.get('start_date'), "%m/%d/%Y").date()
            filter_order_count = Q(order__date__gte=start_date) & Q(order__date__lt=end_date)
        elif end_date:
            start_date = datetime.today().date()
            filter_order_count = Q(order__date__gte=start_date) & Q(order__date__lt=end_date)
        else:
            return queryset

        calculate_counts = (end_date - start_date).days
        queryset = queryset.annotate(count_orders=Count('order', filter=filter_order_count)).filter(
            count_orders__lt=calculate_counts * 24
        )
        return queryset

    def filter_location(self, queryset, name, value):
        return queryset

    def order_by_location(self, queryset, name, value):
        current_location = self.data.get('location')
        if current_location:
            point = GEOSGeometry(current_location)
            order_by = ('' if value == 'location_asc' else '-') + 'distance'
            return queryset.annotate(distance=Distance('address', point)).order_by(order_by)
        else:
            if value == 'location_asc':
                return queryset.order_by('address')
            else:
                return queryset.order_by('-address')
