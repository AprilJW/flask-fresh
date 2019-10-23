from flask.views import MethodView
from flask import jsonify, render_template
from utils.auth import request

from apps.goods.models import GoodsSKU
from utils.auth import login_required
from utils.tools import get_redis_connection


class CartAddView(MethodView):
    decorators = [login_required]

    def post(self):

        user = request.user

        sku_id = request.form.get('sku_id')
        count = request.form.get('count')

        if not all([sku_id, count]):
            return jsonify({'res': 1, 'errmsg': '数据不完整!'})

        try:
            count = int(count)
        except Exception:
            return jsonify({'res': 2, 'errmsg': '商品数目错误'})

        sku = GoodsSKU.query.filter(GoodsSKU.id == sku_id).first()
        if not sku:
            return jsonify({'res': 3, 'errmsg': '商品不存在'})

        coon = get_redis_connection()

        cart_key = 'cart_%d' % user.id

        cart_count = coon.hget(cart_key, sku_id)

        if count > sku.stock:
            return jsonify({'res': 4, 'errmsg': '存库不足!'})

        if cart_count:
            count += int(cart_count)

        # 设置hash中sku对应得值
        coon.hset(cart_key, sku_id, count)

        total_count = coon.hlen(cart_key)
        coon.close()

        return jsonify({'res': 5, 'message': '添加成功!', 'total_count': total_count})


class CartInfoView(MethodView):
    decorators = [login_required]

    def get(self, ):
        user = request.user
        # 获取购物车商品信息
        coon = get_redis_connection()
        cart_key = 'cart_%d' % user.id

        cart_dict = coon.hgetall(cart_key)

        skus = []
        total_count = 0
        total_price = 0
        for sku_id, count in cart_dict.items():
            sku = GoodsSKU.query.filter(GoodsSKU.id == sku_id).first()
            print(sku)
            print(dir(sku))
            amount = sku.price * int(count)
            sku.amount = amount
            sku.count = int(count)
            skus.append(sku)
            total_count += int(count)
            total_price += amount

        context = {
            'total_count': total_count,
            'total_price': total_price,
            'skus': skus,
            'user': user
        }
        coon.close()
        return render_template('cart.html', **context)


# 购物车记录更新
class CartUpdateView(MethodView):
    def post(self):
        user = request.user
        if not user.is_authenticated:
            return jsonify({'res': 0, 'errmsg': '请先登录'})

        sku_id = request.form.get('sku_id')
        count = request.form.get('count')

        if not all([sku_id, count]):
            return jsonify({'res': 1, 'errmsg': '数据不完整!'})

        try:
            count = int(count)
        except Exception:
            return jsonify({'res': 2, 'errmsg': '商品数目错误'})

        # try:
        #     sku = GoodsSKU.objects.get(pk=sku_id)
        # except GoodsSKU.DoesNotExist:
        #     return JsonResponse({'res': 3, 'errmsg': '商品不存在'})
        sku = GoodsSKU.query.filter(GoodsSKU.id == sku_id).first()
        if not sku:
            return jsonify({'res': 3, 'errmsg': '商品不存在'})

        coon = get_redis_connection()

        cart_key = 'cart_%d' % user.id

        if count > sku.stock:
            return jsonify({'res': 4, 'errmsg': '存库不足!'})

        # 设置hash中sku对应得值
        coon.hset(cart_key, sku_id, count)

        values = coon.hvals(cart_key)

        total_count = sum(values)

        return jsonify({'res': 5, 'message': '更新成功!',
                        'total_count': total_count})


class CartDeleteView(MethodView):
    def post(self):
        user = request.user
        if not user.is_authenticated:
            return jsonify({'res': 0, 'errmsg': '请先登录'})

        sku_id = request.form.get('sku_id')

        if not sku_id:
            return jsonify({'res': 1, 'errmsg': '无效的商品id'})

        # try:
        #     GoodsSKU.objects.get(pk=sku_id)
        # except GoodsSKU.DoesNotExist:
        #     return jsonify({'res': 2, 'errmsg': '商品不存在!'})
        sku = GoodsSKU.query.filter(GoodsSKU.id == sku_id).first()
        if not sku:
            return jsonify({'res': 3, 'errmsg': '商品不存在'})

        coon = get_redis_connection()

        cart_key = 'cart_%d' % user.id

        coon.hdel(cart_key, sku_id)

        values = coon.hvals(cart_key)

        values = [int(value.decode()) for value in values]

        total_count = sum(values)

        return jsonify({'res': 3, 'message': '删除成功!',
                             'total_count': total_count})