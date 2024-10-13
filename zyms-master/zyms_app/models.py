from django.db import models


# Create your models here.
# 管理员
class Admin_users(models.Model):
    au_name = models.CharField('姓名', max_length=30)
    au_account = models.CharField('账号', max_length=30)
    au_pwd = models.CharField('密码', max_length=30)
    au_role = models.IntegerField('角色', default=2)
    au_tel = models.CharField('电话', max_length=30)

    def __str__(self):
        return self.au_name

    class Meta:
        verbose_name = '管理员'
        verbose_name_plural = '管理员'


# 供应商和客户
class Customers_suppliers(models.Model):
    cs_attitude = models.CharField('供应商/客户', max_length=20)
    cs_postCode = models.IntegerField('邮编', default=0)
    cs_address = models.CharField('地址', max_length=50)
    cs_tel = models.CharField('电话', max_length=20)
    cs_unit = models.CharField('单位', max_length=30)  # 单位
    cs_name = models.CharField('联系人', max_length=30)  # 联系人

    def __str__(self):
        return self.cs_unit

    class Meta:
        verbose_name = '供应商和客户'
        verbose_name_plural = '供应商和客户'


# 药品
class Medicines(models.Model):
    medicine_name = models.CharField('药品名', max_length=30)
    medicine_manufacturers = models.CharField('生产商', max_length=30)  # 生产商
    medicine_trademark = models.CharField('品牌', max_length=30)  # 品牌
    medicine_production_address = models.CharField('生产地址', max_length=50)  # 生产地址
    medicine_code = models.CharField('条码号', max_length=30)
    medicine_specification = models.CharField('规格', max_length=20)  # 规格
    medicine_purchase = models.FloatField('进货价', default=0)  # 进货价
    medicine_selling = models.FloatField('出售价', default=0)  # 出售价
    medicine_quantity = models.IntegerField('数量', default=0)  # 出售价

    def __str__(self):
        return self.medicine_name

    class Meta:
        verbose_name = '药品'
        verbose_name_plural = '药品'


# 出入库
class Warehouse_record(models.Model):
    wr_in_out = models.CharField('入库/出库', max_length=20)
    wr_quantity = models.IntegerField('数量', default=0)  # 出入库量
    wr_cs_name = models.CharField('供应商/客户', max_length=20)
    wr_admin_name = models.CharField('记录管理员', max_length=20)
    wr_medicine_name = models.CharField('药品名', max_length=20)
    wr_in_out_time = models.DateField('时间', auto_now=True)
    wr_amount = models.FloatField('金额', default=0)

    class Meta:
        verbose_name = '出入库记录'
        verbose_name_plural = '出入库记录'

