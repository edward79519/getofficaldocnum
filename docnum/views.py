from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import OfficalDoc
from .forms import AddDocForm


# Create your views here.


def index(request):
    template = loader.get_template('docnum/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def doc_list(request):
    doc_list = OfficalDoc.objects.all().order_by("-addtime")
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
        print(form.fields["author"])
        form.fields["author"].queryset = User.objects.filter(id=request.user.id)
        print(form.fields["author"])
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../')
    else:
        form = AddDocForm()
        print(form.fields["author"])
        form.fields["author"].queryset = User.objects.filter(id=request.user.id)
        print(form.fields["author"])
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))
