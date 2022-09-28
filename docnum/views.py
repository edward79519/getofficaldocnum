import csv
import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import OfficalDoc, Company, Department, ReceiveDoc
from .forms import AddDocForm, AddReceiveDocForm
from django.db import transaction, DatabaseError
from django.contrib import messages
from django.shortcuts import redirect

# Global Variable
MNGR_GROUP = "OffDoc Manager"  # 管理單位名稱


# Create your views here.


def index(request):
    template = loader.get_template('docnum/index.html')
    context = {}

    return HttpResponse(template.render(context, request))


@login_required
def doc_list(request):
    mngr_group = Group.objects.get(name=MNGR_GROUP)
    if mngr_group in request.user.groups.all():
        doc_list = OfficalDoc.objects.all().order_by("-addtime")
    else:
        doc_list = OfficalDoc.objects.filter(author_id=request.user.id).order_by("-addtime")
    templates = loader.get_template('docnum/officaldoc/send_list.html')
    context = {
        'doc_list': doc_list,
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
    comps = Company.objects.all()
    template = loader.get_template("docnum/company/list.html")
    context = {
        'comp_list': comps,
    }
    return HttpResponse(template.render(context, request))


@login_required
def comp_detail(request, comp_id):
    mngr_group = Group.objects.get(name=MNGR_GROUP)
    comp = Company.objects.get(id=comp_id)
    if mngr_group in request.user.groups.all():
        doc_list = OfficalDoc.objects.filter(comp_id=comp_id).order_by("-addtime")
        rcv_list = ReceiveDoc.objects.filter(rcvcomp_id=comp_id).order_by("-addtime")
    else:
        doc_list = OfficalDoc.objects.filter(comp_id=comp_id, author_id=request.user.id).order_by("-addtime")
        rcv_list = ReceiveDoc.objects.filter(rcvcomp=comp_id, author_id=request.user.id).order_by("-addtime")
    template = loader.get_template("docnum/company/detail.html")
    context = {
        'comp': comp,
        'doc_list': doc_list,
        'rcv_list': rcv_list,
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
        doc_list = ReceiveDoc.objects.all().order_by("-addtime")
    else:
        doc_list = ReceiveDoc.objects.filter(author_id=request.user.id).order_by("-addtime")
    templates = loader.get_template('docnum/officaldoc/receive_list.html')
    context = {
        'doc_list': doc_list,
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
        if form.is_valid():
            rcvdoc = form.save()
            messages.add_message(request, messages.SUCCESS, "新增成功！")
            return redirect('Receive_result', id_rcvdoc=rcvdoc.id)
    else:
        form = AddReceiveDocForm()
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
