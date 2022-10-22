import io
import os

from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib import pagesizes
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.rl_config import defaultPageSize
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from users.permissions import IsAuthorOrReadOnly
from users.serializers import RecipeSubscriptionSerializer

from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from recipes.serializers import (FavoriteSerializer, IngredientSerializer,
                                 RecipeReadSerializer, RecipeWriteSerializer,
                                 TagSerializer)

from .filters import IngredientFilter, RecipeFilter
from .pagination import RecipePaginator


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = ('get',)


class IngredientViewset(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = RecipePaginator
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action in ('list', 'retreieve'):
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticatedOrReadOnly]
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            favorite_recipe, created = Favorite.objects.get_or_create(
                user=user, recipe=recipe
            )
            if created is True:
                serializer = FavoriteSerializer()
                return Response(
                    serializer.to_representation(instance=favorite_recipe),
                    status=status.HTTP_201_CREATED
                )
        if request.method == 'DELETE':
            Favorite.objects.filter(
                user=user, recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticatedOrReadOnly]
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            ShoppingCart.objects.get_or_create(user=user, recipe=recipe)
            serializer = RecipeSubscriptionSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            ShoppingCart.objects.filter(
                user=user, recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(
    #     detail=False,
    #     methods=['GET'],
    #     permission_classes=[IsAuthenticated]
    # )
    # def download_shopping_cart(self, request):
    #     shopping_cart = ShoppingCart.objects.filter(user=request.user).all()
    #     shopping_list = {}
    #     for item in shopping_cart:
    #         for ingredient_amount in item.recipe.ingredient_amount.all():
    #             name = ingredient_amount.ingredient.name
    #             unit = ingredient_amount.ingredient.measurement_unit
    #             amount = ingredient_amount.amount
    #             if name not in shopping_list:
    #                 shopping_list[name] = {
    #                     'name': name,
    #                     'measurement_unit': unit,
    #                     'amount': amount
    #                 }
    #             else:
    #                 shopping_list[name]['amount'] += amount
    #     content = (
    #         [f'{item["name"]} ({item["measurement_unit"]}) '
    #          f' - {item["amount"]}\n'
    #          for item in shopping_list.values()]
    #     )      
    #     buffer = io.BytesIO()
    #     p  = canvas.Canvas (buffer, pagesize=A4, bottomup=0)
    #     textob  = p.beginText()
    #     textob.setTextOrigin(cm, cm)
    #     textob.setFont("Helvetica", 14)
    #     for line in content:
    #         textob.textLine(line)
    #     p.drawText(textob)
    #     p.showPage()
    #     p.save()
    #     buffer.seek(0)
    #     return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
        )
    def download_shopping_cart(self, request):
        def firstPageContent(page_canvas, document):
            header_content = 'Список покупок'
            headerHeight = defaultPageSize[1] - 50
            headerWidth = defaultPageSize[0]/2.0

            page_canvas.saveState()
            page_canvas.setFont('Verdana', 18)
            page_canvas.drawCentredString(
                headerWidth,
                headerHeight,
                header_content
            )
            page_canvas.restoreState()
        
        pdfmetrics.registerFont(
            TTFont('Verdana', os.path.join(settings.FONTS_ROOT, 'Verdana.ttf'))
        )

        shopping_cart = ShoppingCart.objects.filter(user=request.user).all()
        shopping_list = {}
        for item in shopping_cart:
            for ingredient_amount in item.recipe.ingredient_amount.all():
                name = ingredient_amount.ingredient.name
                unit = ingredient_amount.ingredient.measurement_unit
                amount = ingredient_amount.amount
                if name not in shopping_list:
                    shopping_list[name] = {
                        'name': name,
                        'measurement_unit': unit,
                        'amount': amount
                    }
                else:
                    shopping_list[name]['amount'] += amount
        content = (
            [f'{item["name"]} ({item["measurement_unit"]}) '
             f' - {item["amount"]}\n'
             for item in shopping_list.values()]
        )

        buffer = io.BytesIO()
        document = SimpleDocTemplate(
            buffer,
            pagesize=pagesizes.portrait(pagesizes.A4),
        )

        #columns_width = [6*inch, 1*inch, 1*inch]
        table = Table(
            content,
            rowHeights=20,
            repeatRows=1,
            #colWidths=columns_width,
            hAlign='CENTER'
        )

        table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 18),
            ('FONTNAME', (0, 0), (-1, -1), "Verdana"),
        ]))

        document.build([table], onFirstPage=firstPageContent)

        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True, filename='shopping_cart.pdf',
        )
        
        
