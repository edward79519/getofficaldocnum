import datetime

from django.http import JsonResponse
from docnum.models import Company, Department, OfficalDoc


def getdocnum(request):
    id_comp = request.GET.get('id_comp')
    id_dept = request.GET.get('id_dept')
    pubdate = request.GET.get('date')
    pubyear = pubdate.split("-")[0]
    pubmon = pubdate.split("-")[1]
    pubday = pubdate.split("-")[2]
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
    sn = "{}{}{}".format(str(int(pubyear)-1911), sn_paper, str(doccnt+1).zfill(6))
    full_sn = "{}{}字第 {} 號".format(comp_shtname, dept_shtname, sn)
    context = {
        'sn': sn,
        'full_sn': full_sn,
    }
    return JsonResponse(context)
