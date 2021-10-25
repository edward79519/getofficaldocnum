from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import OfficalDoc, Company, Department
from .forms import AddDocForm
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
    templates = loader.get_template('docnum/officaldoc/list.html')
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
    else:
        doc_list = OfficalDoc.objects.filter(comp_id=comp_id, author_id=request.user.id).order_by("-addtime")
    template = loader.get_template("docnum/company/detail.html")
    context = {
        'comp': comp,
        'doc_list': doc_list,
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
    template = loader.get_template('docnum/officaldoc/add_v2.html')
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
    template = loader.get_template("docnum/result.html")
    context = {
        'doc': doc,
    }
    return HttpResponse(template.render(context, request))