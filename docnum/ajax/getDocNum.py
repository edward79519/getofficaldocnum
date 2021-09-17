import datetime

from django.http import JsonResponse
from docnum.models import Company, Department, OfficalDoc


def getdocnum(request):
    id_comp = request.GET.get('id_comp')
    id_dept = request.GET.get('id_dept')
    pubdate = request.GET.get('date')
    print(id_comp, id_dept, pubdate)
    pubyear = pubdate.split("-")[0]
    pubmon = pubdate.split("-")[1]
    pubday = pubdate.split("-")[2]
    comp_shtname = Company.objects.get(id=id_comp).shortname
    dept_shtname = Department.objects.get(id=id_dept).shortname
    doccnt = OfficalDoc.objects.filter(
        comp_id=id_comp,
        dept_id=id_dept,
        pubdate__year=int(pubyear)).count()
    if pubyear == "2021":
        doccnt += 100
    sn = "{}{}".format(str(int(pubyear)-1911), str(doccnt+1).zfill(7))
    full_sn = "{}{}字第 {} 號".format(comp_shtname, dept_shtname, sn)
    print(sn, full_sn)
    context = {
        'sn': sn,
        'full_sn': full_sn,
    }
    return JsonResponse(context)
