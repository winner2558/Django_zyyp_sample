from datetime import datetime
import time
from django.http.response import FileResponse
from django.shortcuts import render, redirect
from zyms_app.models import *
import pandas as pd


# 首页
def index(request):
    return render(request, 'index.html', context={'flag': True})


# 登录
def login(request):
    # 用户登录信息判断
    if request.method == "POST":
        # 获取用户登录信息
        username = request.POST.get('username')
        userpass = request.POST.get('userpass')
        # 查询用户信息
        admin_user = Admin_users.objects.filter(au_account=username, au_pwd=userpass).first()
        if admin_user:
            rep = redirect('/adminpage')
            # 将cookie改为session
            # rep.set_cookie('adminuser', username)
            # rep.set_cookie('au_role', admin_user.au_role)
            request.session["adminuser"] = username
            request.session["au_role"] = admin_user.au_role
            return rep
    rep = render(request, 'index.html', context={'flag': False})
    # 将cookie改为session
    # request.delete_cookie("adminuser")
    request.session.flush()
    return rep


# 退出登录
def outlogin(request):
    rep = redirect('/')
    # 将cookie改为session
    # rep.delete_cookie("adminuser")
    request.session.flush()
    return rep


# 管理页面
def admin(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    if adminuser is not None:
        # 登录用户信息
        admin_user = Admin_users.objects.get(au_account=adminuser)
        admin_user_name = admin_user.au_name
        admin_user_role = admin_user.au_role
        if admin_user_role == 1:
            return render(request, 'admin_1.html', context={'admin_user_name': admin_user_name})
        if admin_user_role == 2:
            return render(request, 'admin_2.html', context={'admin_user_name': admin_user_name})
        if admin_user_role == 3:
            return render(request, 'admin_3.html', context={'admin_user_name': admin_user_name})
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 库存管理
def kcpg(request):
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 2):
        # 判断是否有查询信息
        if request.GET.get('s') is None or request.GET.get('s') == '':
            # 返回全部列表
            medicines_list = Medicines.objects.all().values()
            customers_suppliers = Customers_suppliers.objects.filter(cs_attitude='供应商').values()
            warehouse_record = Warehouse_record.objects.all()
            context = {'medicines': medicines_list, 'customers_suppliers': customers_suppliers,
                       'warehouse_record': warehouse_record}
            return render(request, 'funcpage/kcpg.html', context=context)
        # 返回符合查询内容的列表
        medicines_list = Medicines.objects.filter(medicine_name__contains=request.GET.get('s')).values()
        customers_suppliers = Customers_suppliers.objects.filter(cs_attitude='供应商').values()
        warehouse_record = Warehouse_record.objects.all().values()
        context = {'medicines': medicines_list, 'customers_suppliers': customers_suppliers,
                   'warehouse_record': warehouse_record}
        return render(request, 'funcpage/kcpg.html', context=context)
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 药品入库页面
def in_medicine(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 2):
        medicine_id = request.GET.get('id')
        medicine_data = list(Medicines.objects.filter(id=medicine_id).values())[0]
        customers_suppliers = Customers_suppliers.objects.filter(cs_attitude='供应商').values()
        return render(request, 'funcpage/in_medicine.html',
                      context={'medicine_data': medicine_data, 'customers_suppliers': customers_suppliers})
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 药品出库
def out_medicine(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 2):
        medicine_id = request.GET.get('id')
        medicine_data = list(Medicines.objects.filter(id=medicine_id).values())[0]
        customers_suppliers = Customers_suppliers.objects.filter(cs_attitude='客户').values()
        return render(request, 'funcpage/out_medicine.html',
                      context={'medicine_data': medicine_data, 'customers_suppliers': customers_suppliers})
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 药品入库保存
def in_medicine_save(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 2):
        medicine = Medicines.objects.filter(id=request.POST.get('id'))
        medicine.update(medicine_quantity=medicine[0].medicine_quantity + float(request.POST.get('medicine_quantity')))
        # 进货金额计算
        in_amount = float(request.POST.get('medicine_quantity')) * float(request.POST.get('medicine_purchase'))

        # 添加入库记录
        warehouse_record = Warehouse_record(wr_in_out='入库',
                                            wr_quantity=request.POST.get('medicine_quantity'),
                                            wr_cs_name=request.POST.get('medicine_suppliers'),
                                            # 将cookie改为session
                                            # wr_admin_name = request.COOKIES.get('adminuser'),
                                            wr_admin_name=request.session.get('adminuser'),
                                            wr_medicine_name=request.POST.get('medicine_name'),
                                            wr_in_out_time=time.strftime("%Y-%m-%d", time.localtime()),
                                            wr_amount=in_amount)
        warehouse_record.save()
        return redirect('/kcpg')
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 药品出库保存
def out_medicine_save(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 2):
        medicine = Medicines.objects.filter(id=request.POST.get('id'))
        if medicine[0].medicine_quantity >= float(request.POST.get('medicine_quantity')):
            medicine.update(
                medicine_quantity=medicine[0].medicine_quantity - float(request.POST.get('medicine_quantity')))
            # 出货金额计算
            out_amount = float(request.POST.get('medicine_quantity')) * float(request.POST.get('medicine_selling'))

            # 添加出库记录
            warehouse_record = Warehouse_record(wr_in_out='出库',
                                                wr_quantity=request.POST.get('medicine_quantity'),
                                                wr_cs_name=request.POST.get('medicine_suppliers'),
                                                # 将cookie改为session
                                                # wr_admin_name = request.COOKIES.get('adminuser'),
                                                wr_admin_name=request.session.get('adminuser'),
                                                wr_medicine_name=request.POST.get('medicine_name'),
                                                wr_in_out_time=time.strftime("%Y-%m-%d", time.localtime()),
                                                wr_amount=out_amount)
            warehouse_record.save()
            return redirect('/kcpg')
        else:
            return render(request, 'funcpage/error.html', context={'info': '库存数量已不够出库，请返回或重新填写出库数量', 'up': '/kcpg'},
                          status=403)
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 新增药品保存
def add_medicine(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 2):
        # 药品保存
        medicine = Medicines(medicine_name=request.POST.get('medicine_name'),
                             medicine_manufacturers=request.POST.get('medicine_manufacturers'),
                             medicine_trademark=request.POST.get('medicine_trademark'),
                             medicine_production_address=request.POST.get('medicine_production_address'),
                             medicine_code=request.POST.get('medicine_code'),
                             medicine_specification=request.POST.get('medicine_specification'),
                             medicine_purchase=request.POST.get('medicine_purchase'),
                             medicine_selling=request.POST.get('medicine_selling'))
        medicine.save()
        return redirect("/kcpg")
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 药品编辑页面
def edit_medicine_page(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 2):
        medicine_id = request.GET.get('id')
        medicine_data = list(Medicines.objects.filter(id=medicine_id).values())[0]
        return render(request, 'funcpage/edit_medicine.html', context={'medicine_data': medicine_data})
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 药品编辑保存
def edit_medicine_save(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 2):
        medicine = Medicines.objects.filter(id=request.POST.get('id'))
        medicine.update(medicine_name=request.POST.get('medicine_name'),
                        medicine_manufacturers=request.POST.get('medicine_manufacturers'),
                        medicine_trademark=request.POST.get('medicine_trademark'),
                        medicine_production_address=request.POST.get('medicine_production_address'),
                        medicine_code=request.POST.get('medicine_code'),
                        medicine_specification=request.POST.get('medicine_specification'),
                        medicine_purchase=request.POST.get('medicine_purchase'),
                        medicine_selling=request.POST.get('medicine_selling'))
        return redirect('/kcpg')
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 删除库存
def del_medicine(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 2):
        medicine = Medicines.objects.get(id=request.GET.get('id'))
        medicine.delete()
        return redirect("/kcpg")
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 客户管理
def khpg(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 3):
        # 判断是否有查询信息
        if request.GET.get('s') is None or request.GET.get('s') == '':
            customers_suppliers = Customers_suppliers.objects.filter(
                cs_attitude='客户').values()
            context = {'customers_suppliers': customers_suppliers}
            return render(request, 'funcpage/khpg.html', context=context)
        # 返回符合查询内容的列表
        customers_suppliers = Customers_suppliers.objects.filter(cs_unit__contains=request.GET.get('s')).values()
        context = {'customers_suppliers': customers_suppliers}
        return render(request, 'funcpage/khpg.html', context=context)
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 新增客户
def add_customers(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 3):
        customers = Customers_suppliers(cs_attitude=request.POST.get('cs_attitude'),
                                        cs_postCode=request.POST.get('cs_postCode'),
                                        cs_address=request.POST.get('cs_address'),
                                        cs_tel=request.POST.get('cs_tel'),
                                        cs_unit=request.POST.get('cs_unit'),
                                        cs_name=request.POST.get('cs_name'))
        customers.save()
        return redirect("/khpg")
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 客户编辑页面
def edit_customers_page(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 3):
        customers_id = request.GET.get('id')
        customers_data = list(Customers_suppliers.objects.filter(id=customers_id).values())[0]
        return render(request, 'funcpage/edit_customers.html', context=customers_data)
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 客户编辑保存
def edit_customers_save(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 3):
        medicine = Customers_suppliers.objects.filter(id=request.POST.get('id'))
        medicine.update(cs_postCode=request.POST.get('cs_postCode'),
                        cs_address=request.POST.get('cs_address'),
                        cs_tel=request.POST.get('cs_tel'),
                        cs_unit=request.POST.get('cs_unit'),
                        cs_name=request.POST.get('cs_name'))
        return redirect('/khpg')
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 删除客户
def del_customers(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 3):
        customers_suppliers = Customers_suppliers.objects.get(id=request.GET.get('id'))
        customers_suppliers.delete()
        return redirect("/khpg")
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 供应商管理
def gyspg(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 3):
        # 判断是否有查询信息
        if request.GET.get('s') is None or request.GET.get('s') == '':
            customers_suppliers = Customers_suppliers.objects.filter(
                cs_attitude='供应商').values()
            context = {'customers_suppliers': customers_suppliers}
            return render(request, 'funcpage/gyspg.html', context=context)
        # 返回符合查询内容的列表
        customers_suppliers = Customers_suppliers.objects.filter(cs_unit__contains=request.GET.get('s')).values()
        context = {'customers_suppliers': customers_suppliers}
        return render(request, 'funcpage/gyspg.html', context=context)
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 新增供应商
def add_suppliers(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 3):
        suppliers = Customers_suppliers(cs_attitude=request.POST.get('cs_attitude'),
                                        cs_postCode=request.POST.get('cs_postCode'),
                                        cs_address=request.POST.get('cs_address'),
                                        cs_tel=request.POST.get('cs_tel'),
                                        cs_unit=request.POST.get('cs_unit'),
                                        cs_name=request.POST.get('cs_name'))
        suppliers.save()
        return redirect("/gyspg")
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 供应商编辑页面
def edit_suppliers_page(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 3):
        suppliers_id = request.GET.get('id')
        suppliers_data = list(Customers_suppliers.objects.filter(id=suppliers_id).values())[0]
        return render(request, 'funcpage/edit_suppliers.html', context=suppliers_data)
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 供应商编辑保存
def edit_suppliers_save(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 3):
        suppliers = Customers_suppliers.objects.filter(id=request.POST.get('id'))
        suppliers.update(cs_postCode=request.POST.get('cs_postCode'),
                         cs_address=request.POST.get('cs_address'),
                         cs_tel=request.POST.get('cs_tel'),
                         cs_unit=request.POST.get('cs_unit'),
                         cs_name=request.POST.get('cs_name'))
        return redirect('/gyspg')
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 删除供应商
def del_suppliers(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1 or admin_user_role == 3):
        customers_suppliers = Customers_suppliers.objects.get(id=request.GET.get('id'))
        customers_suppliers.delete()
        return redirect("/gyspg")
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 统计分析
def tjpg(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1):
        try:
            # 年销售额/成本/占比
            # 年数据
            year_data = {}
            now_year = datetime.now().year
            year_in_warehouse_record = pd.DataFrame(
                Warehouse_record.objects.filter(wr_in_out='入库', wr_in_out_time__year=now_year).values())
            year_out_warehouse_record = pd.DataFrame(
                Warehouse_record.objects.filter(wr_in_out='出库', wr_in_out_time__year=now_year).values())
            # 年收入
            year_data['year_income'] = sum(year_out_warehouse_record['wr_amount'])
            # 年支出
            year_data['year_expenditure'] = sum(year_in_warehouse_record['wr_amount'])
            # 年利润
            year_data['year_profit'] = year_data['year_income'] - year_data['year_expenditure']
            # 年盈亏比
            year_data['year_ratio'] = round((year_data['year_profit'] / year_data['year_expenditure']) * 100, 3)

            # 月销售额/成本/占比
            # 月数据
            month_data = {}
            now_month = datetime.now().month
            month_in_warehouse_record = pd.DataFrame(
                Warehouse_record.objects.filter(wr_in_out='入库', wr_in_out_time__month=now_month).values())
            month_out_warehouse_record = pd.DataFrame(
                Warehouse_record.objects.filter(wr_in_out='出库', wr_in_out_time__month=now_month).values())
            # 月收入
            month_data['month_income'] = sum(month_out_warehouse_record['wr_amount'])
            # 月支出
            month_data['month_expenditure'] = sum(month_in_warehouse_record['wr_amount'])
            # 月利润
            month_data['month_profit'] = month_data['month_income'] - month_data['month_expenditure']
            # 月盈亏比
            month_data['month_ratio'] = round((month_data['month_profit'] / month_data['month_expenditure']) * 100, 3)

            # 药品排行
            medicine_ranking = {}
            # 年药品排行
            year_medicine = pd.DataFrame(
                Warehouse_record.objects.filter(wr_in_out='出库', wr_in_out_time__year=now_year).values())
            year_medicine = year_medicine.sort_values('wr_amount')
            year_medicine_ranking = year_medicine.groupby(['wr_medicine_name'])['wr_amount'].sum()[::-1]
            medicine_ranking['year_medicine_ranking'] = year_medicine_ranking.to_dict()

            # 月药品排行
            month_medicine = pd.DataFrame(
                Warehouse_record.objects.filter(wr_in_out='出库', wr_in_out_time__month=now_month).values())
            month_medicine = month_medicine.sort_values('wr_amount')
            month_medicine_ranking = month_medicine.groupby(['wr_medicine_name'])['wr_amount'].sum()[::-1]
            medicine_ranking['month_medicine_ranking'] = month_medicine_ranking.to_dict()
            # 盈利亏损情况
            pl = {}
            pl['year'] = True
            pl['month'] = True

            if year_data['year_profit'] < 0:
                pl['year'] = False

            if month_data['month_profit'] < 0:
                pl['month'] = False

            context = {'year_data': year_data, 'month_data': month_data, 'medicine_ranking': medicine_ranking, 'pl': pl}
            return render(request, 'funcpage/tjpg.html', context=context)
        except:
            return render(request, 'funcpage/error.html', context={'info': '现有出入库数据无法进行统计分析！', 'up': ''})

    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 库存数据下载
def down_kc(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1):
        # 生成数据文件
        data = pd.DataFrame(Medicines.objects.all().values())
        data.to_excel('hnyhms_app/data_file/kc_data.xls', index=False)
        # 返回文件
        file = open('hnyhms_app/data_file/kc_data.xls', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="kc_data_' + datetime.strftime(datetime.now(),
                                                                                              '%Y-%m-%d %H:%M:%S') + '.xls"'
        return response

    return render(request, 'funcpage/error.html', context={'info': '您没有权限下载文件！', 'up': '/'})


# 出入库记录下载
def down_io(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1):
        # 生成数据文件
        data = pd.DataFrame(Warehouse_record.objects.all().values())
        data.to_excel('hnyhms_app/data_file/io_data.xls', index=False)
        # 返回文件
        file = open('hnyhms_app/data_file/io_data.xls', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="io_data_' + datetime.strftime(datetime.now(),
                                                                                              '%Y-%m-%d %H:%M:%S') + '.xls"'
        return response

    return render(request, 'funcpage/error.html', context={'info': '您没有权限下载文件！', 'up': '/'})


# 客户数据下载
def down_kh(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1):
        # 生成数据文件
        data = pd.DataFrame(Customers_suppliers.objects.filter(cs_attitude='客户').values())
        data.to_excel('hnyhms_app/data_file/cs_data.xls', index=False)
        # 返回文件
        file = open('hnyhms_app/data_file/cs_data.xls', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="cs_data_' + datetime.strftime(datetime.now(),
                                                                                              '%Y-%m-%d %H:%M:%S') + '.xls"'
        return response

    return render(request, 'funcpage/error.html', context={'info': '您没有权限下载文件！', 'up': '/'})


# 供应商数据下载
def down_gys(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1):
        # 生成数据文件
        data = pd.DataFrame(Customers_suppliers.objects.filter(cs_attitude='供应商').values())
        data.to_excel('hnyhms_app/data_file/gys_data.xls', index=False)
        # 返回文件
        file = open('hnyhms_app/data_file/gys_data.xls', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="gys_data_' + datetime.strftime(datetime.now(),
                                                                                               '%Y-%m-%d %H:%M:%S') + '.xls"'
        return response

    return render(request, 'funcpage/error.html', context={'info': '您没有权限下载文件！', 'up': '/'})


# 系统管理
def xtpg(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1):
        admin_users = Admin_users.objects.all().values()
        context = {'admin_users': admin_users}
        return render(request, 'funcpage/xtpg.html', context=context)
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 新增管理员
def add_admin_users(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1):
        admin_users = Admin_users(au_name=request.POST.get('au_name'),
                                  au_account=request.POST.get('au_account'),
                                  au_pwd=request.POST.get('au_pwd'),
                                  au_role=request.POST.get('au_role'),
                                  au_tel=request.POST.get('au_tel'))
        admin_users.save()
        return redirect("/xtpg")
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 管理员编辑页面
def edit_admin_page(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1):
        admin_id = request.GET.get('id')
        admin_data = list(Admin_users.objects.filter(id=admin_id).values())[0]
        return render(request, 'funcpage/edit_admin.html', context=admin_data)
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 管理员编辑保存
def edit_admin_save(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1):
        admin = Admin_users.objects.filter(id=request.POST.get('id'))
        if request.POST.get('au_pwd') == '':
            admin.update(au_name=request.POST.get('au_name'),
                         au_account=request.POST.get('au_account'),
                         au_role=request.POST.get('au_role'),
                         au_tel=request.POST.get('au_tel'))
        else:
            admin.update(au_name=request.POST.get('au_name'),
                         au_account=request.POST.get('au_account'),
                         au_pwd=request.POST.get('au_pwd'),
                         au_role=request.POST.get('au_role'),
                         au_tel=request.POST.get('au_tel'))
        return redirect('/xtpg')
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)


# 删除管理员
def del_adminuser(request):
    # 收到浏览器的再次请求,判断浏览器携带的cookie是不是登录成功的时候响应的cookie
    # 将cookie改为session
    # adminuser = request.COOKIES.get('adminuser')
    adminuser = request.session.get('adminuser')
    # 权限判断
    admin_user_role = Admin_users.objects.get(au_account=adminuser).au_role
    if adminuser is not None and (admin_user_role == 1):
        admin_users = Admin_users.objects.get(id=request.GET.get('id'))
        admin_users.delete()
        return redirect("/xtpg")
    return render(request, 'funcpage/error.html', context={'info': '您没有权限访问该页面！', 'up': '/'}, status=403)
