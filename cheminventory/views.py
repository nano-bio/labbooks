from django.shortcuts import render
import models
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

# Prints door signs for a storage location
def print_doorsign(request, labid):
    lab = models.UsageLocation.objects.get(id = labid)
    chemsused  = models.ChemicalInstance.objects.filter(usage_location = lab.id).values_list('chemical', flat = True)
    chems = models.Chemical.objects.filter(id__in = list(chemsused)).exclude(state_of_matter = 'GAS')
    gases = models.Chemical.objects.filter(id__in = list(chemsused)).filter(state_of_matter = 'GAS')
    chemwarnings = []
    gaswarnings = []
    params2check = ['toxic', 'oxidizing', 'irritant', 'explosive', 'flammable', 'health_hazard', 'corrosive', 'environmentally_damaging']
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
        hids = models.Chemical.objects.filter(id = chem.id).values_list('ghs_h', flat = True)
        pids = models.Chemical.objects.filter(id = chem.id).values_list('ghs_p', flat = True)
        chem.hs = models.GHS_H.objects.filter(id__in = hids)
        chem.ps = models.GHS_P.objects.filter(id__in = pids)

    for gas in gases:
        hids = models.Chemical.objects.filter(id = gas.id).values_list('ghs_h', flat = True)
        pids = models.Chemical.objects.filter(id = gas.id).values_list('ghs_p', flat = True)
        gas.hs = models.GHS_H.objects.filter(id__in = hids)
        gas.ps = models.GHS_P.objects.filter(id__in = pids)

    t = get_template('cheminventory/doorsign.html')
    c = Context({'lab': lab, 'chems': chems, 'gases': gases, 'gaswarnings': gaswarnings, 'chemwarnings': chemwarnings})

    html = t.render(c)
    return HttpResponse(html)

def print_chemwaste(request, locid):
    lab = models.StorageLocation.objects.get(id = locid)
    #chemsstored  = models.ChemicalInstance.objects.filter(storage_location = lab.id).values_list('chemical', flat = True)
    chemsstored  = models.ChemicalInstance.objects.filter(storage_location = lab.id)

    t = get_template('cheminventory/chemwaste.html')
    c = Context({'lab': lab, 'chems': chemsstored})

    html = t.render(c)
    return HttpResponse(html)

