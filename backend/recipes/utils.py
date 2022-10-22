import io
import os

from django.conf import settings
from django.http import FileResponse, HttpResponse
from reportlab.lib import pagesizes
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.rl_config import defaultPageSize


def get_shopping(request):       
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
    p  = canvas.Canvas (buffer, pagesize=A4, bottomup=0)
    textob  = p.beginText()
    textob.setTextOrigin(cm, cm)
    textob.setFont('Verdana', 14)
    for line in content:
        textob.textLine(line)
    p.drawText(textob)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='shopping_list.pdf')
