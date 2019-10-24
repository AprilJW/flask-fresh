from datetime import datetime

from flask import redirect, url_for, render_template, jsonify
from flask.views import MethodView

from apps.goods.models import GoodsSKU
from apps.order.models import OrderInfo, OrderGoods
from apps.user.models import Address
from utils.auth import login_required, request
from utils.extentions import db
from alipay import AliPay
from utils.tools import get_redis_connection
import config
from time import sleep


class OrderPlaceView(MethodView):
    decorators = [login_required]

    def post(self):

        user = request.user

        sku_ids = request.form.getlist('sku_ids')

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


# 悲观锁
class OrderCommitView(MethodView):
    decorators = [login_required]

    # @transaction.atomic
    def post(self):
        user = request.user

        if not user.is_authenticated:
            return jsonify({'res': 0, 'errmsg': '用户未登录!'})

        addr_id = request.form.get('addr_id')
        pay_method = request.form.get('pay_method')
        sku_ids = request.form.get('sku_ids')

        if not all([addr_id, pay_method, sku_ids]):
            return jsonify({'res': 1, 'errmsg': '参数不完整!'})

        # todo 校验支付方式
        if pay_method not in OrderInfo.PAY_METHODS.keys():
            return jsonify({'res': 2, 'errmsg': '非法的支付方式!'})

        # try:
        #     addr = Address.objects.get(pk=addr_id)
        # except Address.DoesNotExist:
        #     return jsonify({'res': 3, 'errmsg': '地址非法'})
        addr = Address.query.filter(Address.id == addr_id).first()
        if not addr:
            return jsonify({'res': 3, 'errmsg': '地址非法'})

        # TODO: 创建订单
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        # 运费
        transit_price = 10  # 假数据， 写死
        total_count = 0
        total_price = 0
        coon = get_redis_connection()
        cart_key = 'cart_%d' % user.id
        # 设置保存点
        save_id = db.session.begin_nested()

        # TODO  想订单信息表中添加一条记录
        order = OrderInfo(
            id=order_id,
            _user=user,
            _addr=addr,
            pay_method=pay_method,
            total_count=total_count,
            total_price=total_price,
            transit_price=transit_price
        )
        db.session.add(order)
        db.session.commit()
        # todo 用户的订单中有几个商品就要添加几条记录
        sku_ids = sku_ids.split(',')
        for sku_id in sku_ids:
            sku = db.session.query(GoodsSKU).filter(GoodsSKU.id == sku_id).with_for_update(read=True).first()
            if not sku:
                db.session.rollback()
                return jsonify({'res': 4, 'errmsg': '商品不存在!'})

            # 获取商品的数目
            count = coon.hget(cart_key, sku_id)

            # todo 判断商品的库存
            if int(count) > sku.stock:
                db.session.rollback()
                return jsonify({'res': 6, 'errmsg': '商品库存不足'})

            # todo to订单信息表中添加一条记录
            order = OrderGoods(
                _order=order,
                _sku=sku,
                count=int(count),
                price=sku.price,
            )
            db.session.add(order)
            db.session.commit()
            # todo 更新商品的库存销量和库存
            sku.stock -= int(count)
            sku.sales += int(count)
            db.session.add(sku)
            db.session.commit()

            # todo 累加计算商品的订单的总数量和总价格
            amount = sku.price * int(count)
            total_count += int(count)
            total_price += amount

        # todo 更新订单信息表中的商品的总数量和价格
        order.total_count = total_count
        order.total_price = total_price
        db.session.add(order)
        db.session.commit()
        # except Exception:
        #     db.session.rollback()
        #     return jsonify({'res': 7, 'errmsg': '下单失败!'})
        # 提交
        db.session.commit()
        # todo 清楚用户的购物车记录
        coon.hdel(cart_key, *sku_ids)

        return jsonify({'res': 5, 'message': '创建成功!'})


class OrderPayView(MethodView):
    # decorators = [login_required]

    def post(self):
        user = request.user
        if not user.is_authenticated:
            return jsonify({'res': 0, 'errmsg': '请先登录!'})

        order_id = request.form.get('order_id')

        if not order_id:
            return jsonify({'res': 1, 'errmsg': '无效的订单id'})

        # try:
        #     order = OrderInfo.objects.get(
        #         order_id=order_id, user=user, pay_method=3, order_status=1)
        # except OrderInfo.DoesNotExist:
        #     return JsonResponse({'res': 2, 'errmsg': '订单错误！'})
        order = OrderInfo.query.filter(
            OrderInfo.id == order_id,
            OrderInfo._user == user,
            OrderInfo.pay_method == 3,
            OrderInfo.order_status == 1,
        ).first()

        if not order:
            return jsonify({'res': 2, 'errmsg': '订单错误！'})

        alipay = AliPay(
            appid=config.ALIPAY_APP_ID,
            app_notify_url=None,  # 默认回调url
            app_private_key_path=config.APP_PRIVATE_KEY_PATH,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=config.ALIPAY_PUBLIC_KEY_PATH,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )
        total_pay = order.total_price + order.transit_price
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(total_pay),
            subject='天天生鲜%s' % order_id,
            return_url=None,
            notify_url=None  # 可选, 不填则使用默认notify url
        )

        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string

        return jsonify({'res': 3, 'pay_url': pay_url})


class OrderCheckView(MethodView):
    def post(self):
        user = request.user
        if not user.is_authenticated:
            return jsonify({'res': 0, 'errmsg': '请先登录!'})

        order_id = request.form.get('order_id')

        if not order_id:
            return jsonify({'res': 1, 'errmsg': '无效的订单id'})

        # try:
        #     order = OrderInfo.objects.get(
        #         order_id=order_id, user=user, pay_method=3, order_status=1)
        # except OrderInfo.DoesNotExist:
        #     return JsonResponse({'res': 2, 'errmsg': '订单错误！'})
        order = OrderInfo.query.filter(
            OrderInfo.id == order_id,
            OrderInfo._user == user,
            OrderInfo.pay_method == 3,
            OrderInfo.order_status == 1,
        )
        if not order:
            return jsonify({'res': 2, 'errmsg': '订单错误！'})

        alipay = AliPay(
            appid=config.ALIPAY_APP_ID,
            app_notify_url=None,  # 默认回调url
            app_private_key_path=config.APP_PRIVATE_KEY_PATH,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=config.ALIPAY_PUBLIC_KEY_PATH,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )

        # 调用支付宝的交易查询接口
        while True:
            response = alipay.api_alipay_trade_query(order_id)

            code = response.get('code')
            if code == '10000' and response.get(
                    'trade_status') == 'TRADE_SUCCESS':
                # 支付成功
                # 更新订单的状态
                train_no = response.get('trade_no')
                order.trade_no = train_no
                # 将支付状态改为待评价
                order.order_status = 4
                db.session.add(order)
                db.session.commit()
                # order.save()
                return jsonify({'res': 3, 'message': '支付成功!'})
            elif (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY') or code == '40004':
                # 等待支付
                sleep(5)
                continue
            else:
                # 支付失败
                return jsonify({'res': 4, 'errmsg': '支付失败!'})
