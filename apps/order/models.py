from sqlalchemy.orm import relationship

from utils.extentions import db


class OrderInfo(db.Model):
    """订单模型类"""
    PAY_METHODS = {
        '1': "货到付款",
        '2': "微信支付",
        '3': "支付宝",
        '4': '银联支付'
    }

    PAY_METHODS_ENUM = {
        "CASH": 1,
        "ALIPAY": 2
    }

    ORDER_STATUS = {
        1: '待支付',
        2: '待发货',
        3: '待收货',
        4: '待评价',
        5: '已完成'
    }

    PAY_METHOD_CHOICES = (
        (1, '货到付款'),
        (2, '微信支付'),
        (3, '支付宝'),
        (4, '银联支付')
    )

    ORDER_STATUS_CHOICES = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成')
    )
    __tablename__ = 'df_order_info'
    # order_id = models.CharField(max_length=128, primary_key=True,verbose_name='订单id')
    id = db.Column(db.String(125), primary_key=True)
    # user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='用户')
    user = db.Column(db.ForeignKey('user.id', ondelete='CASCADE'))
    # addr = models.ForeignKey('user.Address', on_delete=models.CASCADE, verbose_name='地址')
    addr = db.Column(db.ForeignKey('df_address.id', ondelete='CASCADE'))
    # pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=3, verbose_name='支付方式')
    pay_method = db.Column(db.SmallInteger, default=3)
    # total_count = models.IntegerField(default=1, verbose_name='商品数量')
    total_count = db.Column(db.Integer, default=1)
    # total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    total_price = db.Column(db.DECIMAL)
    # transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='运费')
    transit_price = db.Column(db.DECIMAL)
    # order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='订单状态')
    order_status = db.Column(db.SmallInteger, default=1)
    # trade_no = models.CharField(max_length=128, default='', verbose_name='支付编号')
    trade_no = db.Column(db.String(125))

    _user = relationship('User', backref='order_info')
    _addr = relationship('Address', backref='order_info')
    # class Meta:
    #     db_table = 'df_order_info'
    #     verbose_name = '订单'
    #     verbose_name_plural = verbose_name


class OrderGoods(db.Model):
    """订单商品模型类"""
    __tablename__ = 'df_order_goods'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    # order = models.ForeignKey('OrderInfo', on_delete=models.CASCADE, verbose_name='订单')
    order = db.Column(db.ForeignKey('df_order_info.id', ondelete='CASCADE'))
    # sku = models.ForeignKey('goods.GoodsSKU', on_delete=models.CASCADE, verbose_name='商品SKU')
    sku = db.Column(db.ForeignKey('df_goods_sku.id', ondelete='CASCADE'))
    # count = models.IntegerField(default=1, verbose_name='商品数目')
    count = db.Column(db.Integer, default=1)
    # price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')  # 总价格
    price = db.Column(db.DECIMAL)
    # comment = models.CharField(max_length=256, default='', verbose_name='评论')
    comment = db.Column(db.String(256), default='')

    _order = relationship('OrderInfo', backref='order_goods')
    _sku = relationship('GoodsSKU', backref='order_goods')
    # class Meta:
    #     db_table = 'df_order_goods'
    #     verbose_name = '订单商品'
    #     verbose_name_plural = verbose_name