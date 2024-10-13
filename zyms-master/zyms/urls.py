from django.contrib import admin
from django.urls import path
from zyms_app import views

urlpatterns = [
    # Django管理页面
    path('admin/', admin.site.urls),
    # 首页
    path("", views.index),

    # 登录
    path('login', views.login),
    # 退出登录
    path('outlogin', views.outlogin),
    # 管理员页面
    path("adminpage", views.admin),

    # 库存管理页面
    path("kcpg", views.kcpg),
    # 添加药品
    path('add_medicine', views.add_medicine),
    # 药品编辑页面
    path('edit_medicine_page', views.edit_medicine_page),
    # 药品编辑保存
    path('edit_medicine_save', views.edit_medicine_save),
    # 删除库存
    path('del_medicine', views.del_medicine),
    # 药品入库
    path('in_medicine', views.in_medicine),
    # 药品入库保存
    path('in_medicine_save', views.in_medicine_save),
    # 药品出库
    path('out_medicine', views.out_medicine),
    # 药品出库保存
    path('out_medicine_save', views.out_medicine_save),

    # 客户管理页面
    path("khpg", views.khpg),
    # 新增客户
    path('add_customers', views.add_customers),
    # 客户编辑页面
    path('edit_customers_page', views.edit_customers_page),
    # 客户编辑保存
    path('edit_customers_save', views.edit_customers_save),
    # 删除客户
    path('del_customers', views.del_customers),

    # 供应商管理页面
    path("gyspg", views.gyspg),
    # 新增供应商
    path('add_suppliers', views.add_suppliers),
    # 客户编辑页面
    path('edit_suppliers_page', views.edit_suppliers_page),
    # 客户编辑保存
    path('edit_suppliers_save', views.edit_suppliers_save),
    # 删除供应商
    path('del_suppliers', views.del_suppliers),

    # 统计页面
    path("tjpg", views.tjpg),
    # 库存下载
    path('down_kc', views.down_kc),
    # 出入库记录下载
    path('down_io', views.down_io),
    # 客户数据下载
    path('down_kh', views.down_kh),
    # 供应商数据下载
    path('down_gys', views.down_gys),

    # 系统管理
    path("xtpg", views.xtpg),
    # 新增管理员
    path('add_admin_users', views.add_admin_users),
    # 管理员编辑页面
    path('edit_admin_page', views.edit_admin_page),
    # 管理员编辑保存
    path('edit_admin_save', views.edit_admin_save),
    # 删除管理员
    path('del_adminuser', views.del_adminuser)
]
