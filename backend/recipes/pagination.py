from rest_framework.pagination import PageNumberPagination


class RecipePaginator(PageNumberPagination):
    page_size = 6
