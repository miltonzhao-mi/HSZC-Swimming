"""分页器"""
from rest_framework.pagination import PageNumberPagination as DRFPageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class MyPageNumberPagination(DRFPageNumberPagination):
    """自定义分页器"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('code', 200),
            ('message', 'success'),
            ('data', OrderedDict([
                 ('items', data),
                 ('total', self.page.paginator.count),
                 ('page', self.page.number),
                 ('page_size', self.get_page_size(self.request)),
                 ('total_pages', self.page.paginator.num_pages),
            ]))
        ]))

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'code': {'type': 'integer', 'example': 200},
                'message': {'type': 'string', 'example': 'success'},
                'data': {
                    'type': 'object',
                    'properties': {
                        'items': {'type': 'array'},
                        'total': {'type': 'integer'},
                        'page': {'type': 'integer'},
                        'page_size': {'type': 'integer'},
                        'total_pages': {'type': 'integer'},
                    },
                },
            },
        }
