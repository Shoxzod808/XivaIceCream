# myapp/utils.py
""" from .models import Template, Template2Button, FileForDocuments


def get_text(title, lang, button=False):
    try:
        if button:
            text = Template2Button.objects.get(title=title)
        else:
            text = Template.objects.get(title=title)
        if lang == 'ru':
            text = text.body_ru
        elif lang == 'en':
            text = text.body_en
        else:
            text = text.body_uz
    except Exception:
        text = f'Шаблон: {title} не найден!!! '
    return text


def get_document(id):
    result = FileForDocuments.objects.filter(document=id)
    return result """

from .models import Product, InventoryProduct, OrderProduct

def refresh_count_for_products():
    products  =Product.objects.all()
    for product in products:
        product.count = 0
        inventory_products = InventoryProduct.objects.filter(product=product)
        order_products = OrderProduct.objects.filter(product=product)
        for p in inventory_products:
            product.count += p.count
        for p in order_products:
            product.count -= p.count
        product.save()


def calculate_order_cash(cash, payed):
    return 120