from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import OfficalDoc, Company
from .forms import AddDocForm


# Create your views here.


def index(request):
    template = loader.get_template('docnum/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


@login_required
def doc_list(request):
    mngr_group = Group.objects.get(name="manager")
    if mngr_group in request.user.groups.all():
        doc_list = OfficalDoc.objects.all().order_by("-addtime")
    else:
        doc_list = OfficalDoc.objects.filter(author_id=request.user.id).order_by("-addtime")
    templates = loader.get_template('docnum/officaldoc/list.html')
    context = {
        'doc_list': doc_list,
    }
    return HttpResponse(templates.render(context, request))


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
    mngr_group = Group.objects.get(name="manager")
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
