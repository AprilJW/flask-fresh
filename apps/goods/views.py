from flask.views import MethodView
from utils.auth import login_required, request
from flask import render_template, redirect, url_for
from utils.extentions import db
from utils.tools import get_redis_connection
from .models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner, GoodsSKU


class IndexView(MethodView):
    decorators = [login_required]

    def get(self):
        # 获取商品种类
        # types = GoodsType.objects.all()
        types = db.session.query(GoodsType).all()
        # 获取首页轮播商品信息
        # GoodsBanner = IndexGoodsBanner.objects.all().order_by('index')
        GoodsBanner = db.session.query(IndexGoodsBanner).order_by('index').all()
        # 获取首页活动信息
        # PromotionBanner = IndexPromotionBanner.objects.all().order_by('index')
        PromotionBanner = db.session.query(IndexPromotionBanner).order_by('index').all()
        # 获取首页分类商品展示信息
        for type in types:
            # print(type)
            # type.img_banner = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
            type.img_banner = db.session.query(IndexTypeGoodsBanner).filter(IndexTypeGoodsBanner._type == type,
                                                                            IndexTypeGoodsBanner.display_type == 1).order_by(
                'index').all()

            # type.tltle_banner = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')
            type.tltle_banner = db.session.query(IndexTypeGoodsBanner).filter(IndexTypeGoodsBanner._type == type,
                                                                              IndexTypeGoodsBanner.display_type == 0).order_by(
                'index').all()

        # 获取购物车商品数量
        cart_count = 0
        if request.user.is_authenticated:
            coon = get_redis_connection()
            cart_key = 'cart_%d' % request.user.id
            cart_count = coon.hlen(cart_key)
        # 模板上下文
        context = {
            'types': types,
            'GoodsBanner': GoodsBanner,
            'PromotionBanner': PromotionBanner,
            'cart_count': cart_count,
            'user': request.user
        }

        return render_template('index.html', **context)


class DetailView(MethodView):
    def get(self, pk):
        # 查询商品id是否存在
        # try:
        #     sku = GoodsSKU.objects.get(pk=pk)
        # except GoodsSKU.DoesNotExist:
        #     return redirect(reverse('goods:index'))
        sku = db.session.query(GoodsSKU).filter(GoodsSKU.id == pk).first()
        if not sku:
            return redirect(url_for('goods.index'))

        # # 获取商品的分类信息
        # types = GoodsType.objects.all()
        types = db.session.query(GoodsType).all()
        # # 获取商品的评论
        # sku_orders = OrderGoods.objects.filter(sku=sku).exclude(comment='')
        # sku_orders = OrderGoods.objects.filter(sku=sku).exclude(comment='')
        # # 获取新品信息
        # new_skus = GoodsSKU.objects.filter(
        #     type=sku.type).order_by('-create_time')[0:2]
        #
        # # 获取同一商品spu的其他规格商品
        # same_spu_skus = GoodsSKU.objects.filter(goods=sku.goods).exclude(pk=pk)
        #
        # # 获取购物车商品数量
        # cart_count = 0
        # if request.user.is_authenticated:
        #     coon = get_redis_connection('default')
        #     cart_key = 'cart_%d' % request.user.id
        #     cart_count = coon.hlen(cart_key)
        #
        #     # 添加用户的历史浏览记录
        #     coon = get_redis_connection('default')
        #     history_key = 'history_%d' % request.user.id
        #     # 移除之前的该商品id
        #     coon.lrem(history_key, 0, pk)
        #     # 把goods_id左侧插入redis列表
        #     coon.lpush(history_key, pk)
        #     # 取用户保存的最新5条信息
        #     coon.ltrim(history_key, 0, 4)
        #
        # context = {
        #     'sku': sku,
        #     'types': types,
        #     'sku_order': sku_orders,
        #     'new_skus': new_skus,
        #     'cart_count': cart_count,
        #     'same_spu_skus': same_spu_skus
        # }

        return render_template('detail.html', )
