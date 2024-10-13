from django.contrib import admin
from zyms_app import models

# Register your models here.
class Admin_users_Admin(admin.ModelAdmin):
    list_display = ['id', 'au_name', 'au_account', 'au_pwd', 'au_role', 'au_tel']


class Customers_suppliers_Admin(admin.ModelAdmin):
    list_display = ['id', 'cs_attitude', 'cs_postCode', 'cs_address', 'cs_tel', 'cs_unit', 'cs_name']


class Medicines_Admin(admin.ModelAdmin):
    list_display = ['id', 'medicine_name', 'medicine_manufacturers', 'medicine_trademark', 'medicine_production_address', 'medicine_code', 'medicine_specification', 'medicine_purchase', 'medicine_selling']


class Warehouse_record_Admin(admin.ModelAdmin):
    list_display = ['id', 'wr_quantity', 'wr_cs_name', 'wr_admin_name', 'wr_medicine_name', 'wr_in_out_time', 'wr_in_out', 'wr_amount']


admin.site.register(models.Admin_users, Admin_users_Admin)
admin.site.register(models.Customers_suppliers, Customers_suppliers_Admin)
admin.site.register(models.Medicines, Medicines_Admin)
admin.site.register(models.Warehouse_record, Warehouse_record_Admin)
