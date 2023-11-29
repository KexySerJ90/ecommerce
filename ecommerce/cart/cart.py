from decimal import Decimal

from store.models import Product


class Cart:
    # Определение метода __init__
    def __init__(self, request):
        # Получение сессии из запроса
        self.session = request.session
        # Получение корзины по ключу сессии
        cart = self.session.get('session_key')
        # Если ключ "session_key" отсутствует в сессии, создаем пустую корзину
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        # Присваивание полученной корзины к переменной self.cart
        self.cart = cart

    # Определение метода add
    def add(self, product, product_qty):
        # Получение идентификатора продукта в виде строки
        product_id = str(product.id)
        # Если продукт уже присутствует в корзине, обновляем его количество
        if product_id in self.cart:
            self.cart[product_id]["qty"] = product_qty
        else:
            # Иначе добавляем продукт в корзину с указанием цены и количества
            self.cart[product_id] = {"price": str(product.price), "qty": product_qty}
        # Устанавливаем флаг модификации сессии в значение True
        self.session.modified = True


    def delete(self, product):
        product_id=str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True


    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())


    def __iter__(self):
        all_product_ids=self.cart.keys()
        products=Product.objects.filter(id__in=all_product_ids)
        cart=self.cart.copy()
        for product in products:
            cart[str(product.id)]['product']=product

        for item in cart.values():
            item['price']=Decimal(item['price'])

            item['total']=item['price']*item['qty']
            yield item


    def get_total(self):
        return sum(Decimal(item['price'])*item['qty'] for item in self.cart.values())