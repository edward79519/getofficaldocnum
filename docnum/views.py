import csv
import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import OfficalDoc, Company, Department, ReceiveDoc, Contract, ContractStatus
from .forms import AddDocForm, AddReceiveDocForm, AddCompanyForm, AddDepartmentForm, AddContractForm, UpdateContractForm
from django.db import transaction, DatabaseError
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from simple_history.utils import update_change_reason

# Global Variable
MNGR_GROUP = "OffDoc Manager"  # 管理單位名稱


# Create your views here.


@login_required
def doc_list(request):
    mngr_group = Group.objects.get(name=MNGR_GROUP)
    if mngr_group in request.user.groups.all():
        docs = OfficalDoc.objects.all().order_by("-addtime")
    else:
        docs = OfficalDoc.objects.filter(author_id=request.user.id).order_by("-addtime")
    templates = loader.get_template('docnum/officaldoc/send_list.html')
    context = {
        'doc_list': docs,
    }
    return HttpResponse(templates.render(context, request))


# 舊版新增文件
@login_required
def doc_add(request):
    template = loader.get_template('docnum/officaldoc/add.html')
    print(request.user.id, User.objects.get(id=request.user.id))
    if request.method == "POST":
        form = AddDocForm(request.POST)
        form.fields["author"].queryset = User.objects.filter(id=request.user.id)
        form.fields["author"].initial = User.objects.get(id=request.user.id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../')
    else:
        form = AddDocForm()
        form.fields["author"].queryset = User.objects.filter(id=request.user.id)
        form.fields["author"].initial = User.objects.get(id=request.user.id)
        if request.GET.get("comp_id"):
            form.fields["comp"].initial = Company.objects.get(id=request.GET.get("comp_id"))
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))


def comp_list(request):
    mngr_group = Group.objects.get(name=MNGR_GROUP)
    comps = Company.objects.all()
    template = loader.get_template("docnum/company/list.html")
    form = AddCompanyForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            if mngr_group in request.user.groups.all():
                form.save()
                messages.add_message(request, messages.SUCCESS, "新增成功！")
            else:
                messages.add_message(request, messages.ERROR, "你無此權限操作！")
            return redirect('Comp_index')
    context = {
        'comp_list': comps,
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def comp_del(request, comp_id):
    comp = Company.objects.get(id=comp_id)
    mngr_group = Group.objects.get(name=MNGR_GROUP)
    if mngr_group in request.user.groups.all():
        if comp.officaldocs.count() == 0 and comp.receivedocs.count() == 0:
            comp.delete()
            messages.add_message(request, messages.SUCCESS, "刪除成功！")
            return redirect('Comp_index')
        else:
            messages.add_message(request, messages.ERROR, "有關聯的檔案不能刪除！")
            return redirect('Comp_index')
    else:
        messages.add_message(request, messages.ERROR, "你無此操作權限！")
        return redirect('Comp_index')


@login_required
def comp_detail(request, comp_id):
    mngr_group = Group.objects.get(name=MNGR_GROUP)
    comp = Company.objects.get(id=comp_id)
    if mngr_group in request.user.groups.all():
        docs = OfficalDoc.objects.filter(comp_id=comp_id).order_by("-addtime")
        rcvs = ReceiveDoc.objects.filter(rcvcomp_id=comp_id).order_by("-addtime")
    else:
        docs = OfficalDoc.objects.filter(comp_id=comp_id, author_id=request.user.id).order_by("-addtime")
        rcvs = ReceiveDoc.objects.filter(rcvcomp=comp_id, author_id=request.user.id).order_by("-addtime")
    template = loader.get_template("docnum/company/detail.html")
    context = {
        'comp': comp,
        'doc_list': docs,
        'rcv_list': rcvs,
    }
    return HttpResponse(template.render(context, request))


def get_docnum(id_comp, id_dept, pubdate):
    pubyear = pubdate.split("-")[0]
    comp_shtname = Company.objects.get(id=id_comp).shortname
    dept_shtname = Department.objects.get(id=id_dept).shortname

    # 計算目前有多少份公文
    doccnt = OfficalDoc.objects.filter(
        comp_id=id_comp,
        dept_id=id_dept,
        pubdate__year=int(pubyear)).count()

    # 2021 從 100 起跳
    if pubyear == "2021":
        doccnt += 100

    # 有電子公文的公司從 XXX1XXXXXX 開始編
    had_paper = ['寶晶', '城電']
    if comp_shtname in had_paper:
        sn_paper = 1
    else:
        sn_paper = 0
    sn = "{}{}{}".format(str(int(pubyear) - 1911), sn_paper, str(doccnt + 1).zfill(6))
    full_sn = "{}{}字第 {} 號".format(comp_shtname, dept_shtname, sn)
    context = {
        'sn': sn,
        'full_sn': full_sn,
    }
    return context


# 第二版新增，送出後才給號寫進資料庫，給號期間使用 transaction 確保不會重複要到號
@login_required
def doc_add_v2(request):
    template = loader.get_template('docnum/officaldoc/add_send.html')
    if request.method == "POST":
        id_comp = request.POST['comp']
        id_dept = request.POST['dept']
        pubdate = request.POST['pubdate']
        try:
            with transaction.atomic():
                sn = get_docnum(id_comp, id_dept, pubdate)
                post_copy = request.POST.copy()
                post_copy['sn'] = sn['sn']
                post_copy['fullsn'] = sn['full_sn']
                post_copy['author'] = request.user.id
                form = AddDocForm(post_copy)
                if form.is_valid():
                    doc = form.save()
                    messages.add_message(request, messages.SUCCESS, "新增成功！")
                    return redirect('Doc_add_result', id_docnum=doc.id)
        except DatabaseError as e:
            print(e)
    else:
        form = AddDocForm()
        form.fields["comp"].queryset = Company.objects.filter(valid=True)
        form.fields["dept"].queryset = Department.objects.filter(valid=True)
        # 從公司頁面點選進入時，自動帶入公司名稱。
        if request.GET.get("comp_id"):
            form.fields["comp"].initial = Company.objects.get(id=request.GET.get("comp_id"))
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def doc_result(request, id_docnum):
    doc = OfficalDoc.objects.get(id=id_docnum)
    template = loader.get_template("docnum/officaldoc/send_result.html")
    context = {
        'doc': doc,
    }
    return HttpResponse(template.render(context, request))


@login_required
def send_export(request):
    alldata = OfficalDoc.objects.all().values_list('pubdate', 'comp__fullname', 'dept__fullname', 'fullsn',
                                                   'author__last_name', 'author__first_name', 'title', 'addtime')
    data_list = []
    for data in alldata:
        data_row = []
        for field in data:
            if type(field) is not str:
                data_row.append(field.strftime('%Y-%m-%d'))
            else:
                data_row.append(field)
        data_list.append(data_row)
    column_name = ['發文日期', '公司名稱', '發文部門', '發文字號', '發文人_姓', '發文人_名', '發文主旨', '新增日期']

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="OfficialSendDocList_{}.csv"'.format(
        datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))

    writer = csv.writer(response)
    writer.writerow(column_name)
    writer.writerows(data_list)

    return response


def get_rcvdocnum(id_comp, pubdate):
    pubyear = pubdate.split("-")[0]
    pubmon = pubdate.split("-")[1]
    comp_shrtname = Company.objects.get(id=id_comp).shortname

    # 計算目前有多少份公文
    doccnt = ReceiveDoc.objects.filter(
        rcvcomp_id=id_comp,
        senddate__year=int(pubyear),
        senddate__month=int(pubmon),
    ).count()

    sn = "{}{}{}".format(str(int(pubyear) - 1911), pubmon, str(doccnt + 1).zfill(4))
    full_sn = "{}收字第 {} 號".format(comp_shrtname, sn)
    data = {
        'sn': sn,
        'full_sn': full_sn,
    }
    return data


@login_required
def receivedoc_list(request):
    mngr_group = Group.objects.get(name=MNGR_GROUP)
    if mngr_group in request.user.groups.all():
        docs = ReceiveDoc.objects.all().order_by("-addtime")
    else:
        docs = ReceiveDoc.objects.filter(author_id=request.user.id).order_by("-addtime")
    templates = loader.get_template('docnum/officaldoc/receive_list.html')
    context = {
        'doc_list': docs,
    }
    return HttpResponse(templates.render(context, request))


@login_required
def receivedoc_add(request):
    template = loader.get_template("docnum/officaldoc/add_receive.html")
    if request.method == "POST":
        id_cmp = request.POST['rcvcomp']
        senddate = request.POST['senddate']
        post_copy = request.POST.copy()
        sn_data = get_rcvdocnum(id_cmp, senddate)
        post_copy['sn'] = sn_data['sn']
        post_copy['fullsn'] = sn_data['full_sn']
        post_copy['author'] = request.user.id
        form = AddReceiveDocForm(post_copy)
        form.fields["rcvcomp"].queryset = Company.objects.filter(valid=True)
        if form.is_valid():
            rcvdoc = form.save()
            messages.add_message(request, messages.SUCCESS, "新增成功！")
            return redirect('Receive_result', id_rcvdoc=rcvdoc.id)
    else:
        form = AddReceiveDocForm()
        form.fields["rcvcomp"].queryset = Company.objects.filter(valid=True)
        if request.GET.get('comp_id'):
            form.fields['rcvcomp'].initial = request.GET.get('comp_id')
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required()
def receivedoc_result(request, id_rcvdoc):
    rcvdoc = ReceiveDoc.objects.get(id=id_rcvdoc)
    template = loader.get_template('docnum/officaldoc/receive_result.html')
    context = {
        'rcvdoc': rcvdoc,
    }
    return HttpResponse(template.render(context, request))


@login_required
def receive_export(request):
    alldata = ReceiveDoc.objects.all().values_list('senddate', 'rcvcomp__fullname', 'fullsn', 'senddept', 'sendsn',
                                                   'abstract', 'author__last_name', 'author__first_name', 'addtime')
    data_list = []
    for data in alldata:
        data_row = []
        for field in data:
            if type(field) is not str:
                data_row.append(field.strftime('%Y-%m-%d'))
            else:
                data_row.append(field)
        data_list.append(data_row)

    column_name = ['來函日期', '收文機關', '收文字號', '來函機關', '來函字號', '主旨', '收文人_姓', '收文人_名', '新增日期']

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="OfficialReceiveDocList_{}.csv"'.format(
        datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))

    writer = csv.writer(response)
    writer.writerow(column_name)
    writer.writerows(data_list)

    return response


@login_required
def switch_comp(request, comp_id):
    mngr_group = Group.objects.get(name=MNGR_GROUP)
    if mngr_group in request.user.groups.all():
        comp = Company.objects.get(id=comp_id)
        comp.valid = not comp.valid
        comp.save()
        return redirect('Comp_index')
    else:
        return HttpResponse("你無操作此權限，請返回上一頁")


@login_required
def dept_list(request):
    mngr_group = Group.objects.get(name=MNGR_GROUP)
    depts = Department.objects.all()
    template = loader.get_template('docnum/company/dept_list.html')
    form = AddDepartmentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            if mngr_group in request.user.groups.all():
                form.save()
                messages.add_message(request, messages.SUCCESS, "新增成功！")
            else:
                messages.add_message(request, messages.ERROR, "你無此權限操作！")
            return redirect('Dept_list')
    context = {
        'dept_list': depts,
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def dept_del(request, dept_id):
    dept = Department.objects.get(id=dept_id)
    mngr_group = Group.objects.get(name=MNGR_GROUP)
    if mngr_group in request.user.groups.all():
        if dept.officaldocs.count() == 0:
            dept.delete()
            messages.add_message(request, messages.SUCCESS, "刪除成功！")
            return redirect('Dept_list')
        else:
            messages.add_message(request, messages.ERROR, "有關聯的檔案不能刪除！")
            return redirect('Dept_list')
    else:
        messages.add_message(request, messages.ERROR, "你無此操作權限！")
        return redirect('Dept_list')


@login_required
def switch_dept(request, dept_id):
    mngr_group = Group.objects.get(name=MNGR_GROUP)
    if mngr_group in request.user.groups.all():
        dept = Department.objects.get(id=dept_id)
        dept.valid = not dept.valid
        dept.save()
        return redirect('Dept_list')
    else:
        return HttpResponse("你無操作此權限，請返回上一頁")


def get_contractsn(comp_id, cate_id, date):
    contract_count = Contract.objects.filter(
        comp_id=comp_id,
        category_id=cate_id,
        add_time__year=date.year,
        add_time__month=date.month,
    ).count()

    contract_sn = 'C{}{}{}{}{}'.format(
        str(comp_id).zfill(2),
        str(cate_id).zfill(2),
        str(date.year)[-2:],
        str(date.month).zfill(2),
        str(contract_count + 1).zfill(3)
    )
    return contract_sn


@login_required
def contract_add(request):
    template = loader.get_template('docnum/contract/add.html')
    if request.method == "POST":
        # get form data for getting sn
        post_copy = request.POST.copy()
        today = timezone.localtime(timezone.now()).date()
        comp_id = post_copy['comp']
        cate_id = post_copy['category']
        # fill field not in template -- changed_by, created_by, status, sn
        post_copy['changed_by'] = request.user.id
        post_copy['created_by'] = request.user.id
        post_copy['status'] = 1
        post_copy['sn'] = get_contractsn(comp_id=comp_id, cate_id=cate_id, date=today)
        form = AddContractForm(post_copy)
        if form.is_valid():
            new_contra = form.save()
            messages.add_message(request, messages.SUCCESS, "新增合約: {} 成功！".format(new_contra.sn))
            return redirect('Contract_detail', contra_id=new_contra.id)
    else:
        form = AddContractForm()
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def contract_list(request):
    template = loader.get_template('docnum/contract/list.html')
    contracts = Contract.objects.filter(is_valid=True)
    context = {
        'contracts': contracts,
    }
    return HttpResponse(template.render(context, request))


@login_required
def contract_detail(request, contra_id):
    template = loader.get_template('docnum/contract/detail.html')
    contract = Contract.objects.get(id=contra_id)
    context = {
        'contract': contract,
    }
    return HttpResponse(template.render(context, request))


@login_required
def contract_update(request, contra_id):
    template = loader.get_template('docnum/contract/update.html')
    contract = Contract.objects.get(id=contra_id)
    if request.method == "POST":
        post_copy = request.POST.copy()
        post_copy['changed_by'] = request.user.id
        form = UpdateContractForm(post_copy, instance=contract)
        if form.is_valid():
            new_contract = form.save()
            update_change_reason(new_contract, post_copy['change_reason'])
            messages.add_message(request, messages.SUCCESS, "修改合約: {} 成功！".format(new_contract.sn))
            return redirect('Contract_detail', contra_id=new_contract.id)
    else:
        form = UpdateContractForm(instance=contract)
    context = {
        'contract': contract,
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def contract_disable(request, contra_id):
    contract = Contract.objects.get(id=contra_id)
    mngr_group = Group.objects.get(name=MNGR_GROUP)
    disable_reason = request.POST['change_reason']

    # 判斷是否為管理員/作者
    is_mngr = mngr_group in request.user.groups.all()
    is_author = request.user.id is contract.created_by.id
    if is_author or is_mngr:
        contract.is_valid = False
        contract.changed_by = request.user
        contract.save()
        update_change_reason(contract, disable_reason)
        messages.add_message(request, messages.SUCCESS, "作廢合約: {}-{}-{} 成功！ 原因：{}".format(
            contract.sn, contract.comp.shortname, contract.category.name, disable_reason
        ))
    else:
        return redirect('Non_auth_error')

    return redirect('Contract_list')


def non_auth_page(request):
    err_tmp = loader.get_template('frame/error_page.html')
    context = {
        'error_message': '您無權限操作，請返回上一頁。'
    }
    return HttpResponse(err_tmp.render(context, request))


@login_required
def contract_confirm(request, contra_id):
    contract = Contract.objects.get(id=contra_id)
    mngr_group = Group.objects.get(name=MNGR_GROUP)
    is_mngr = mngr_group in request.user.groups.all()
    is_author = request.user.id == contract.created_by.id
    if is_author:
        if contract.status.name == "已取號":
            contract.status = ContractStatus.objects.get(name="已確認")
            contract.changed_by = request.user
            contract.save()
            update_change_reason(contract, "確認表單")
            messages.add_message(request, messages.SUCCESS, "合約: {}-{}-{} 已確認。".format(
                contract.sn, contract.comp.shortname, contract.category.name
            ))
            return redirect('Contract_detail', contra_id=contra_id)
        elif contract.status.name == "已確認":
            contract.status = ContractStatus.objects.get(name="已取號")
            contract.changed_by = request.user
            contract.save()
            update_change_reason(contract, "取消確認")
            messages.add_message(request, messages.WARNING, "合約: {}-{}-{} 已取消確認。".format(
                contract.sn, contract.comp.shortname, contract.category.name
            ))
            return redirect('Contract_detail', contra_id=contra_id)
        else:
            messages.add_message(request, messages.ERROR, "操作失敗，請聯絡管理員。")
            return redirect('Contract_detail', contra_id=contra_id)
    elif is_mngr:
        if contract.status.name == "已確認":
            contract.status = ContractStatus.objects.get(name="已取號")
            contract.changed_by = request.user
            contract.save()
            update_change_reason(contract, "管理者取消確認")
            messages.add_message(request, messages.WARNING, "合約: {}-{}-{} 已取消確認。".format(
                contract.sn, contract.comp.shortname, contract.category.name
            ))
            return redirect('Contract_detail', contra_id=contra_id)
        else:
            return redirect('Non_auth_error')
    else:
        return redirect('Non_auth_error')


@login_required
def contract_archive(request, contra_id):
    contract = Contract.objects.get(id=contra_id)
    mngr_group = Group.objects.get(name=MNGR_GROUP)
    is_mngr = mngr_group in request.user.groups.all()
    if is_mngr:
        if contract.status.name == "已確認":
            contract.status = ContractStatus.objects.get(name="已歸檔")
            contract.changed_by = request.user
            contract.save()
            update_change_reason(contract, "管理者歸檔")
            messages.add_message(request, messages.SUCCESS, "合約: {}-{}-{} 已歸檔。".format(
                contract.sn, contract.comp.shortname, contract.category.name
            ))
            return redirect('Contract_detail', contra_id=contra_id)
        else:
            return redirect('Non_auth_error')
    else:
        return redirect('Non_auth_error')
