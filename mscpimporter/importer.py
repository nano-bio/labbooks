import json
import tempfile
from glob import glob

import h5py
import molmass
import numpy
import requests
from dateutil.parser import parse
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from numpy import array
from scipy.optimize import curve_fit

from clustof.models import Measurement as MeasurementClustof
from clustof.views import get_mass_spectrum as clustof_get_mass_spectrum
from massspectra.views import get_mass_spectrum_from_csv
from toffy.models import Measurement as MeasurementToffy
from toffy2.models import Measurement as MeasurementToffy2
from .models import Experiment
from .rsc_api import RscApi

LOCAL = False
if LOCAL:
    ROOT_URL = "http://127.0.0.1:8000/mscp/"
else:
    ROOT_URL = "https://ideadb.uibk.ac.at/mscp/"

API_URL = f"{ROOT_URL}api/"
SPECIES_ELECTRON_ID = 6
SPECIES_HND_ID = 7


def request(path, method, data, token):
    if path[-1] != "/":
        path += "/"
    try:
        return requests.request(
            method=method,
            url=API_URL + path,
            headers={"Authorization": "Token " + token},
            json=data)
    except Exception as e:
        print(data)
        raise


def post(path, data, token):
    return request(path, 'post', data, token)


def patch(path, data, token):
    return request(path, 'patch', data, token)


def create_data_set(data, token):
    r = post('dataSet', data, token)
    if r.status_code != 201:
        raise Exception(f'No Data Set created. Status: {r.status_code}, Message: {r.text}')
    return r.json()['id']


def remove_empty_values_from_dict(d):
    return {k: v for k, v in d.items() if v is not None and v != ""}


class LabbookImporter:
    mass_spectrum = None
    measurement_data_for_comment = None
    date_iso_format = None

    def __init__(self, measurement_id, token, experiment):
        self.measurement_id = measurement_id
        self.experiment = experiment
        self.token = token
        if experiment == 'clustof':
            self.get_clustof_data()
        elif 'toffy' in experiment:
            self.get_toffy_like_data()
        elif experiment == 'surftof':
            self.get_surftof_data()
        else:
            raise Exception("Wrong experiment name!")

    def get_clustof_data(self):
        self.mass_spectrum = clustof_get_mass_spectrum(self.measurement_id)
        measurement_obj = get_object_or_404(MeasurementClustof, pk=self.measurement_id)
        self.measurement_data_for_comment = serialize(
            "json", [measurement_obj])
        self.date_iso_format = measurement_obj.time.date().isoformat()

    def get_toffy_like_data(self):
        if self.experiment == 'toffy':
            measurement_obj = get_object_or_404(MeasurementToffy, pk=self.measurement_id)
        else:
            measurement_obj = get_object_or_404(MeasurementToffy2, pk=self.measurement_id)

        self.measurement_data_for_comment = serialize("json", [measurement_obj])
        self.date_iso_format = measurement_obj.time.date().isoformat()
        self.mass_spectrum = get_mass_spectrum_from_csv(
            measurement_obj.data_file.path)

    def create_data_set(self):
        return create_data_set(data={
            'experiment': get_object_or_404(Experiment, labbook_experiment=self.experiment).experiment_id_mscp,
            'experiment_internal_id': str(self.measurement_id),
            'date_measurement': self.date_iso_format,
            'mass_spectrum_data': {
                'x': list(self.mass_spectrum[0]),
                'y': list(self.mass_spectrum[1])},
            'comment': str(remove_empty_values_from_dict(
                json.loads(self.measurement_data_for_comment)[0]['fields']))
        }, token=self.token)


def create_source():
    r = post('source', {
        'year': '2022',
        'source_type': "database",
        'authors': ";".join(["Scheier, P.", "Duensing, F."])
    })
    if r.status_code != 201:
        raise Exception(f'No source created. Status: {r.status_code}, Message: {r.text}')
    return r.json()['id']


def create_experiment(data=None):
    if data is None:
        data = {
            'name': 'ClusTOF',
            'doi': "10.1002/mas.21699",
            'comments': "A large descriptive comment."
        }
    r = post('experiment', data)
    if r.status_code != 201:
        raise Exception(f'No Experiment created. Status: {r.status_code}, Message: {r.text}')
    return r.json()['id']


def create_species(species):
    r = post('species', species)
    if r.status_code != 201:
        raise Exception(f'No species created. Status: {r.status_code}, Message: {r.text}')
    return r.json()['id']


def write_error_to_html(r):
    with open('a.html', 'wb') as f:
        f.write(r.content)


def create_specieses():
    specieses = []
    while True:
        atom_molecule_solid_or_nothing = input(
            "\nAdd (a)tom, (m)olecule, (s)olid or cluster? Leave blank and enter if not.\n")
        if atom_molecule_solid_or_nothing == "":
            break
        elif atom_molecule_solid_or_nothing == 'a':
            input_string = input('Name of atom, element symbol, charge, mass number (optional) separated by ";"\n')
            if len(input_string.split(';')) == 4:
                mass_number = input_string.split(';')[3]
            else:
                mass_number = None
            specieses.append(
                get_or_create_atom(name=input_string.split(';')[0],
                                   element_symbol=input_string.split(';')[1],
                                   charge=input_string.split(';')[2],
                                   mass_number=mass_number))
        elif atom_molecule_solid_or_nothing == 'm':
            input_string = input('Name of molecule, chemical formula, charge, separated by ";"\n')
            specieses.append(
                get_or_create_molecule(name=input_string.split(';')[0],
                                       chemical_formula=input_string.split(';')[1],
                                       charge=input_string.split(';')[2]))
        elif atom_molecule_solid_or_nothing == 's':
            species_name = input(
                'Name of solid/cluster. Example: Helium Nano Droplet or Beryllium Surface\n')
            layers = []
            while True:
                layer_name = input("Define at least 1 layer with a name. Example: Helium. Leave blank if done.\n")
                if layer_name == "":
                    break
                layer_components = []
                while True:
                    layer_components_string = input(
                        "Define at least 1 layer component with an element symbol and a stoichiometric value. "
                        "Example: He;1. Leave blank if done.\n")
                    if layer_components_string == "":
                        break
                    layer_components.append({
                        'element_symbol': layer_components_string.split(';')[0],
                        'stoichiometric_value': layer_components_string.split(';')[1]})
                layers.append({'name': layer_name, 'components': layer_components})
            layer_ids = []
            for layer in layers:
                layer_ids.append(
                    create_solid_layer(
                        name=layer['name'],
                        solid_layer_components=layer['components']))
            specieses.append(
                create_species({
                    'name': species_name,
                    'Layers': layer_ids,
                    'species_type': 'solid'}))
        else:
            specieses.append(int(atom_molecule_solid_or_nothing))
    print(specieses)
    return specieses


def get_or_create_atom(name, element_symbol, charge,
                       inchi=None, inchi_key=None, mass_number=None):
    if not mass_number:
        mass_number = molmass.Formula(element_symbol).isotope.massnumber
    if not inchi:
        inchi, inchi_key = get_inchi(element_symbol)

    species_id = filter_species(inchi_key, charge)
    if species_id:
        return species_id
    else:
        return create_species({
            'name': name,
            'inchi': inchi,
            'inchi_key': inchi_key,
            'charge': charge,
            'element_symbol': element_symbol,
            'mass_number': mass_number,
            'species_type': 'atom'
        })


def get_or_create_molecule(name, chemical_formula, charge,
                           inchi=None, inchi_key=None, mass_number=None):
    if not mass_number:
        mass_number = molmass.Formula(chemical_formula).isotope.massnumber
    if not inchi:
        inchi, inchi_key = get_inchi(chemical_formula)

    species_id = filter_species(inchi_key, charge, mass_number)
    if species_id:
        return species_id
    else:
        return create_species({
            'name': name,
            'inchi': inchi,
            'inchi_key': inchi_key,
            'charge': charge,
            'chemical_formula': chemical_formula,
            'mass_number': mass_number,
            'species_type': 'molecule'
        })


def create_solid_layer(name, solid_layer_components):
    r = post('solidLayer', {'name': name})
    if r.status_code != 201:
        raise Exception(f'No source created. Status: {r.status_code}, Message: {r.text}')
    solid_layer_id = r.json()['id']
    for solid_layer_component in solid_layer_components:
        r = post('solidLayerComponent', {
            'element_symbol': solid_layer_component['element_symbol'],
            'stoichiometric_value': solid_layer_component['stoichiometric_value'],
            'solid_layer': solid_layer_id
        })
        if r.status_code != 201:
            raise Exception(f'No source created. Status: {r.status_code}, Message: {r.text}')
    return solid_layer_id


def get_inchi(search_string):
    rsc_api = RscApi()
    rsc_obj = rsc_api.formula_to_best_hit_rsc_obj(f"{search_string}")
    return rsc_obj['inchi'], rsc_obj['inchiKey']


def filter_species(inchi_key, charge, mass_number=None):
    filtered_all_species = False
    while not filtered_all_species:
        response = requests.get('https://ideadb.uibk.ac.at/mscp/api/species').json()
        for result in response['results']:
            if (
                    inchi_key == result['inchi_key'] and
                    str(charge) == str(result['charge']) and
                    (
                            mass_number is None or
                            str(mass_number) == str(result['mass_number'])
                    )
            ):
                return int(result['id'])
        if not response['next']:
            filtered_all_species = True
    return False


def slice_data(x_data, y_data, x_min, x_max):
    # returns part of the x and y includes as a function of
    # x min and x max
    def find_index_of_nearest(array, value):
        array = numpy.asarray(array)
        return (numpy.abs(array - value)).argmin()

    x_min_index = find_index_of_nearest(x_data, x_min)
    x_max_index = find_index_of_nearest(x_data, x_max)

    x_data = x_data[x_min_index:x_max_index]
    y_data = y_data[x_min_index:x_max_index]

    return x_data, y_data


def get_mass_spectrum(file_name_full, mass_max=100):
    with h5py.File(file_name_full, 'r') as f:
        y_data = array(f['FullSpectra']['SumSpectrum'])
        x_data = array(f['FullSpectra']['MassAxis'])

    if mass_max is None:
        return x_data, y_data
    return slice_data(x_data, y_data, 0, mass_max)


# found = 0
# root = "/var/storage/clustof/"
# clustof_data = requests.get('http://138.232.74.41/clustof/json/60/').json()
# exp = []
# for i, m in enumerate(clustof_data):
#     try:
#         f_size = getsize(root + m['fields']['data_filename'][8:])
#         if 10_000_000 > f_size > 1000:
#             found += 1
#             print(m['pk'], f_size, m['fields']['data_filename'])
#             xs, ys = get_mass_spectrum(root + m['fields']['data_filename'][8:])
#             clustof_data[i]['xs'] = [float(x) for x in xs]
#             clustof_data[i]['ys'] = [int(y) for y in ys]
#             exp.append(clustof_data[i])
#             if found > 50:
#                 print(50)
#                 break
#     except FileNotFoundError:
#         pass
# with open("export.json", "w") as f:
#     json.dump(exp, f)


class TooLargeMassSpecException(Exception):
    pass


def save_clustof_meta_data():
    all_labbooks_data = requests.get("http://138.232.74.41/clustof/json/10000000000/").json()
    with open('clustof-meta-data.json', 'w') as f:
        json.dump(all_labbooks_data, f)


def get_clustof_meta_data(pk):
    with open('clustof-meta-data.json', 'r') as f:
        data = json.load(f)
        for measurement in data:
            if str(measurement['pk']) == str(pk):
                return measurement
    raise FileNotFoundError()


def create_data_set_clustof(pk):
    data = get_clustof_meta_data(pk)
    print(f"- - - - - - - - - - - - -\nLabbooks Clustof Measurement ID {data['pk']}\n"
          f"Comment:\n{data['fields']['substance']}")

    specieses = create_specieses()

    date_time = parse(data['fields']['time'])
    mass_spec = import_mass_spectrum(pk)
    create_data_set(data={
        'experiment': 1,
        'experiment_internal_id': str(pk),
        'date_measurement': date_time.date().isoformat(),
        # 'source': source,
        'mass_spectrum_data': mass_spec,
        'comment': str(remove_empty_values_from_dict(data['fields'])),
        "specieses": [*specieses, SPECIES_ELECTRON_ID, SPECIES_HND_ID],
    })


def create_experiment_clustof():
    clustof_description = {
        "name": "ClusTOF",
        "doi": "10.1002/mas.21699",
        "comments": "Helium droplets represent a cold inert matrix, "
                    "free of walls with outstanding properties to grow "
                    "complexes and clusters at conditions that are "
                    "perfect to simulate cold and dense regions of the "
                    "interstellar medium. At sub‐Kelvin temperatures, "
                    "barrierless reactions triggered by radicals or ions "
                    "have been observed and studied by optical spectroscopy "
                    "and mass spectrometry. The present review summarizes "
                    "developments of experimental techniques and methods "
                    "and recent results they enabled."}
    print(865, create_experiment(clustof_description))


def import_mass_spectrum_clustof(pk):
    if requests.get(f"http://138.232.74.41/clustof/export-file-size/{pk}/").json()['size'] > 500_000_000:
        raise TooLargeMassSpecException('File larger than 500MB')
    u = requests.get(f"http://138.232.74.41/clustof/export/{pk}/")
    f = tempfile.TemporaryFile()
    f.write(u.content)

    try:
        with h5py.File(f) as f_h5:
            y_data = array(f_h5['FullSpectra']['SumSpectrum'])
            x_data = array(f_h5['FullSpectra']['MassAxis'])
    except Exception as e:
        print('f', f, f.name, pk)
        print('e', e)
        raise e

    return {
        'x': list(map(float, x_data)),
        'y': list(map(float, y_data)),
    }


def TOFFY_TOFFY_TOFFY_TOFFY_TOFFY_TOFFY_TOFFY_TOFFY_TOFFY_TOFFY():
    pass


EXPERIMENT_ID_TOFFY = 3


def create_experiment_toffy():
    toffy_description = {
        "name": "Toffy",
        "doi": "10.1063/1.5133112",
        "comments": "The demand for nanoscale materials of ultra-high purity and narrow size "
                    "distribution is addressed. Clusters of Au, C60, H2O, and serine are produced "
                    "inside helium nanodroplets using a combination of ionization, mass filtering, "
                    "collisions with atomic or molecular vapor, and electrostatic extraction, "
                    "in a specific and novel sequence. The helium droplets are produced in an expansion "
                    "of cold helium gas through a nozzle into vacuum. The droplets are ionized "
                    "by electron bombardment and subjected to a mass filter. The ionic and mass-selected "
                    "helium droplets are then guided through a vacuum chamber filled with atomic "
                    "or molecular vapor where they collide and “pick up” the vapor. The dopants then "
                    "agglomerate inside the helium droplets around charge centers to singly charged "
                    "clusters. Evaporation of the helium droplets is induced by collisions in a "
                    "helium-filled radio frequency (RF)-hexapole, which liberates the cluster ions "
                    "from the host droplets. The clusters are analyzed with a time-of-flight mass "
                    "spectrometer. It is demonstrated that using this sequence, the size distribution "
                    "of the dopant cluster ions is distinctly narrower compared to ionization after "
                    "pickup. Likewise, the ion cluster beam is more intense. The mass spectra show, as "
                    "well, that ion clusters of the dopants can be produced with only few helium atoms "
                    "attached, which will be important for messenger spectroscopy. All these findings "
                    "are important for the scientific research of clusters and nanoscale materials in "
                    "general."}
    print(create_experiment(toffy_description))


def get_meta_data_toffy(pk):
    return requests.get(f"http://138.232.74.41/toffy/measurement/{pk}.json").json()[0]


def import_mass_spectrum(file_path):
    u = requests.get(f"http://138.232.74.41/files/{file_path}")
    f = tempfile.TemporaryFile()
    f.write(u.content)
    f.seek(0)
    data = numpy.genfromtxt(f, delimiter='\t')
    return {
        'x': list(map(float, data[:, 0])),
        'y': list(map(float, data[:, 1])),
    }


def create_data_set_toffy(pk):
    meta_data = get_meta_data_toffy(pk)
    print(f"- - - - - - - - - - - - -\nLabbooks Toffy Measurement ID {meta_data['pk']}\n"
          f"\nShort Description:\n{meta_data['fields']['short_description']}")

    specieses = create_specieses()

    date_time = parse(meta_data['fields']['time'])
    mass_spec = import_mass_spectrum(meta_data['fields']['data_file'])
    create_data_set(data={
        'experiment': EXPERIMENT_ID_TOFFY,
        'experiment_internal_id': str(pk),
        'date_measurement': date_time.date().isoformat(),
        # 'source': source,
        'mass_spectrum_data': mass_spec,
        'comment': str(remove_empty_values_from_dict(meta_data['fields'])),
        "specieses": [*specieses, SPECIES_ELECTRON_ID, SPECIES_HND_ID],
    })


EXPERIMENT_ID_SURFTOF = 2


def surftof_import_mass_spectrum(pk):
    def quadratic_fit_function(x, a, t0):
        return a * (x + t0) ** 2

    with h5py.File(glob(f"Z:/Experiments/SurfTOF/Measurements/rawDATA/{pk}/*.h5")[0], 'r') as f:
        y_data = numpy.array(f['SPECdata']['AverageSpec'])
        x_data = numpy.array(f['CALdata']['Mapping'])
        masses = []
        times = []
        for row in x_data:
            if row[0] != 0 and row[1] != 0:
                masses.append(row[0])
                times.append(row[1])
        popt, pcov = curve_fit(quadratic_fit_function, times, masses, p0=(1e-8, 10000))
        x_data = quadratic_fit_function(numpy.array(numpy.arange(len(y_data))), *popt)

    return {
        'x': list(map(float, x_data)),
        'y': list(map(float, y_data)),
    }


def create_experiment_surftof():
    surftof_description = {
        "name": "SurfTOF",
        "doi": "10.1063/1.5145170",
        "comments": "The device described is the combination of two mass spectrometers, with a surface sample "
                    "placed between them. Its aim is to allow for detailed research on low-energy ion-surface "
                    "interactions, involving and triggering surface chemistry. This task is fulfilled by a "
                    "carefully chosen geometry: Projectile ions from an electron impact source are "
                    "mass-per-charge selected using a quadrupole. Such continuous bombardment allows for good "
                    "control of the surface condition. Species emerging from the collisions are focused onto a "
                    "beam and analyzed using a purpose-built orthogonal pulsing time-of-flight mass "
                    "spectrometer. Neutral species can be post-ionized using a second electron impact source. "
                    "Neutral gases can be adsorbed to the surface from the gas phase in a controlled manner, "
                    "using a feedback-controlled pressure regulator. In order to minimize the discrimination "
                    "of secondary ions, the distance from the surface to the analyzing mass spectrometer "
                    "system was kept as short as possible and the acceptance angle of the lens system as large "
                    "as possible. This increased the sensitivity five orders of magnitude compared to its "
                    "predecessor. The rigorous use of computer aided design software is responsible for the "
                    "successful commissioning of the new device. This article describes first which parameters "
                    "can be measured or controlled. Then, these are linked to the physical processes that "
                    "occur in reactive ion-surface interactions. Next, the design goal and the design "
                    "implementation are presented. In the end, a performance comparison, measurements of "
                    "hydrogen surface chemistry with extensive use of isotope labeling, and measurements of "
                    "post-ionized beryllium are presented."}
    print(create_experiment(surftof_description))


def get_meta_data_surftof(pk):
    return requests.get(f"http://138.232.74.41/surftof/measurement/{pk}.json").json()[0]


def create_data_set_surftof(pk, specieses=None):
    meta_data = get_meta_data_surftof(pk)

    print(f"- - - - - - - - - - - - -\nLabbooks Surftof Measurement ID {meta_data['pk']}\n"
          f"\nShort Description:\n{meta_data['fields']['short_description']}"
          f"\nProjectile:\n{meta_data['fields']['projectile']}"
          f"\nSurface:\n{meta_data['fields']['surface_material']}")
    if not specieses:
        specieses = create_specieses()

    date_time = parse(meta_data['fields']['time'])
    mass_spec = import_mass_spectrum(pk)
    create_data_set(data={
        'experiment': EXPERIMENT_ID_SURFTOF,
        'experiment_internal_id': str(pk),
        'date_measurement': date_time.date().isoformat(),
        # 'source': source,
        'mass_spectrum_data': mass_spec,
        'comment': str(remove_empty_values_from_dict(meta_data['fields'])),
        "specieses": [*specieses],
    })
