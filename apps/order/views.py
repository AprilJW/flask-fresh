from flask import redirect, url_for, render_template
from flask.views import MethodView

from apps.goods.models import GoodsSKU
from apps.user.models import Address
from utils.auth import login_required, request
from utils.tools import get_redis_connection


class OrderPlaceView(MethodView):
    decorators = [login_required]

    def post(self):

        user = request.user

        sku_ids = request.form.getlist('sku_ids')
        print(sku_ids)
        print(dir(request.form))

        if not sku_ids:
            return redirect(url_for('cart.show'))

        coon = get_redis_connection()

        cart_key = 'cart_%d' % user.id

        skus = []
        total_count = 0
        total_price = 0

        for sku_id in sku_ids:
            sku = GoodsSKU.query.filter(GoodsSKU.id == sku_id).first()
            # 获取商品的数量
            conut = coon.hget(cart_key, sku_id)
            amount = sku.price * int(conut)
            sku.count = int(conut.decode())
            sku.amount = amount
            skus.append(sku)
            total_count += int(conut)
            total_price += amount

        # 运费
        transit_price = 10  # 假数据， 写死
        # 实付费
        total_pay = total_price + transit_price

        # addrs = Address.objects.filter(user=user)
        addrs = Address.query.filter(Address._user == user)

        sku_ids = ",".join(sku_ids)

        # 组织上下文
        context = {
            'skus': skus,
            'total_count': total_count,
            'total_price': transit_price,
            'transit_price': transit_price,
            'total_pay': total_pay,
            'addrs': addrs,
            'sku_ids': sku_ids,
            'user': request.user
        }

        return render_template('place_order.html', **context)
