from rest_framework.pagination import PageNumberPagination


class RecipePaginations(PageNumberPagination):
    page_size = 6
