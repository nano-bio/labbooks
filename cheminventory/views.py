from django.shortcuts import render
import cheminventory.models as models
import urllib.parse
import csv
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import datetime


# Prints door signs for a storage location
def print_doorsign(request, labid):
    lab = models.UsageLocation.objects.get(id=labid)
    chemsused = models.ChemicalInstance.objects.filter(usage_location=lab.id).values_list('chemical', flat=True)
    gascylindersused = models.GasCylinderUsageRecord.objects.filter(usage_location=lab.id).values_list('gas_cylinder',
                                                                                                       flat=True)
    gasesused = []
    for gascylinder in gascylindersused:
        m = models.GasCylinderUsageRecord.objects.filter(gas_cylinder=gascylinder).order_by('-date').all()[0:1].get()
        if m.usage_location.id == lab.id:
            gasesused.append(m.gas_cylinder.chemical.id)

    chems = models.Chemical.objects.filter(id__in=list(chemsused)).exclude(state_of_matter='GAS')
    gases = models.Chemical.objects.filter(id__in=list(gasesused))
    chemwarnings = []
    gaswarnings = []
    params2check = ['toxic', 'oxidizing', 'irritant', 'explosive', 'flammable', 'health_hazard', 'corrosive',
                    'environmentally_damaging']
    for param in params2check:
        for chem in chems:
            if chem.__dict__[param] is True:
                chemwarnings.append(param)
                break

    for param in params2check:
        for gas in gases:
            if gas.__dict__[param] is True:
                gaswarnings.append(param)
                break

    gaswarnings = set(gaswarnings)
    chemwarnings = set(chemwarnings)

    for chem in chems:
        hids = models.Chemical.objects.filter(id=chem.id).values_list('ghs_h', flat=True)
        pids = models.Chemical.objects.filter(id=chem.id).values_list('ghs_p', flat=True)
        chem.hs = models.GHS_H.objects.filter(id__in=hids)
        chem.ps = models.GHS_P.objects.filter(id__in=pids)

    for gas in gases:
        hids = models.Chemical.objects.filter(id=gas.id).values_list('ghs_h', flat=True)
        pids = models.Chemical.objects.filter(id=gas.id).values_list('ghs_p', flat=True)
        gas.hs = models.GHS_H.objects.filter(id__in=hids)
        gas.ps = models.GHS_P.objects.filter(id__in=pids)

    t = 'cheminventory/doorsign.html'
    datum = datetime.datetime.now()
    c = {'lab': lab, 'chems': chems, 'gases': gases, 'gaswarnings': gaswarnings, 'chemwarnings': chemwarnings,
         'datum': datum}

    return HttpResponse(render(request, t, c))


def print_chemwaste(request, locid):
    lab = models.StorageLocation.objects.get(id=locid)
    chemsstored = models.ChemicalInstance.objects.filter(storage_location=lab.id)

    t = 'cheminventory/chemwaste.html'
    c = {'lab': lab, 'chems': chemsstored}

    return HttpResponse(render(request, t, c))


def print_gas_cylinder_qr(request, gc_id):
    hostname = request.get_host()
    qr_url = reverse('admin:cheminventory_gascylinder_change', args=(gc_id,))
    http = u'http://'
    complete_link = http + hostname + qr_url

    url = conditional_escape("http://chart.apis.google.com/chart?%s" % \
                             urllib.parse.urlencode(
                                 {'chs': '300x300', 'cht': 'qr', 'chl': complete_link, 'choe': 'UTF-8'}))

    return HttpResponse(mark_safe(u"""<img class="qrcode" src="%s" width="300" height="300" alt="QR" />""" % (url)))


def csv_export(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="chemicals.csv"'

    qs = models.ChemicalInstance.objects.filter(group='SCHEIER').all()
    writer = csv.writer(response)

    writer.writerow(['Chemikalie', 'Menge', 'Hersteller', 'Aufbewahrungsort'])
    for chem in qs:
        writer.writerow([chem.chemical, chem.quantity, chem.company, chem.storage_location])

    return response
