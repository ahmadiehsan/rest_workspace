from django.conf import settings
from django.core.paginator import Paginator
from drf_haystack.serializers import FacetFieldSerializer
from rest_framework import serializers

from helpers.utils import clean_phone_number


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class PhoneNumberField(serializers.Field):
    def to_representation(self, value):
        return str(value).replace('+98', '0')

    def to_internal_value(self, data):
        return clean_phone_number(data)


class CustomFacetFieldSerializer(FacetFieldSerializer):
    """
    for fixing facet narrow_url problem

    remove `_exact` from narrow_url
    """

    def get_narrow_url(self, instance):
        """
        Return a link suitable for narrowing on the current item.
        """
        text = instance[0]
        request = self.context["request"]
        query_params = request.GET.copy()

        # Never keep the page query parameter in narrowing urls.
        # It will raise a NotFound exception when trying to paginate a narrowed queryset.
        page_query_param = self.get_paginate_by_param()
        if page_query_param and page_query_param in query_params:
            del query_params[page_query_param]

        selected_facets = set(query_params.pop(self.root.facet_query_params_text, []))
        selected_facets.add("%(field)s:%(text)s" % {"field": self.parent_field, "text": text})
        query_params.setlist(self.root.facet_query_params_text, sorted(selected_facets))

        path = "%(path)s?%(query)s" % {"path": request.path_info, "query": query_params.urlencode()}
        url = request.build_absolute_uri(path)
        return serializers.Hyperlink(url, "narrow-url")


def get_paginated_data(request, query_set, serializer):
    page_size = request.query_params.get('size') or settings.REST_FRAMEWORK.get('PAGE_SIZE') or 20
    paginator = Paginator(query_set.all(), page_size)

    page = request.query_params.get('page') or 1
    results = paginator.page(page)

    rtn = {
        'count': query_set.count(),
        'results': serializer(results, many=True).data
    }

    return rtn
