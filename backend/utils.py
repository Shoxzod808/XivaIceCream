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

from .models import Product, InventoryProduct, OrderProduct, Payment, Refund
def intcomma(number):
    """
    Функция для форматирования целых чисел с добавлением запятых как разделителя разрядов.
    
    Args:
        number (int): Целое число для форматирования.
    
    Returns:
        str: Отформатированная строка с добавлением запятых как разделителя разрядов.
    """
    parts = []
    for i, digit in enumerate(reversed(str(number))):
        if i > 0 and i % 3 == 0:
            parts.append(' ')
        parts.append(digit)
    return ''.join(reversed(parts))


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


def calculate_order_cash(order, payed):
    if payed:
        cash = 0
        for payment in Payment.objects.filter(order=order):
            cash += payment.cash
    else:
        cash = order.cash
        for payment in Payment.objects.filter(order=order):
            cash -= payment.cash
        for refund in Refund.objects.filter(order=order):
            cash -= refund.cash
    return intcomma(cash)