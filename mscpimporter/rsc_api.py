from time import sleep

import requests
from molmass import Formula
from requests import Response

base_url = "https://api.rsc.org/compounds/v1"
RSC_API_KEY = "3tTT4BCtRVSAOZqkdWud5AGCW5agpnLN"
RSC_API_KEY = "3OQZOrXI0q00zVB4S7TheOnvV3vASoPi"


class RscApi:
    headers = {
        'apikey': RSC_API_KEY,
    }

    @staticmethod
    def formula_to_stoichiometric_formula(chemical_formula):
        return Formula(chemical_formula).formula

    def formula_to_best_hit_rsc_obj(self, chemical_formula):
        query_id = self.search_formula(chemical_formula)
        rsc_objs = self.get_results(query_id)
        if len(rsc_objs) == 0:
            # just return the formula, the only thing which is valid
            return {
                'formula': chemical_formula,
                'nominalMass': Formula(chemical_formula).isotope.massnumber,
                'monoisotopicMass': Formula(chemical_formula).isotope.mass,
                'commonName': '',
                'inchi': '',
                'inchiKey': ''}
        if len(rsc_objs) == 1:
            return rsc_objs[0]
        if len(rsc_objs) > 1:
            # return the element where most references are found. Likely the best one
            return sorted(rsc_objs, key=lambda k: k['referenceCount'], reverse=True)[0]

    def search_formula(self, chemical_formula):
        r = requests.post(
            url=base_url + "/filter/formula",
            headers=self.headers,
            json={
                "formula": chemical_formula,
                "orderBy": 'referenceCount',
                "orderDirection": "descending"
            })
        if r.status_code == 401:
            raise Exception(f'{r.reason}: Headers: {self.headers}')
        if r.status_code != 200:
            if "has invalid format" in r.reason:
                print(435)
                raise InvalidFormatException()
            raise Exception(f'Formula seems invalid: {r.reason}{r.status_code}')
        return r.json()["queryId"]

    def get_results(self, query_id):
        error_msg = ""
        for _ in range(20):
            sleep(0.2)
            r: Response = requests.get(
                url=base_url + f'/filter/{query_id}/results',
                headers=self.headers)
            if r.status_code == 200:
                return [self.get_rsc_obj(result) for result in r.json()['results'][:1]]
            error_msg = r.reason
            print("Error Message in get_results():", error_msg)
        raise Exception(f'Timeout or Bad Request: {error_msg}')

    def get_rsc_obj(self, record_id):
        fields = "inchi,inchiKey,formula,nominalMass,commonName,referenceCount"
        s = requests.get(
            url=base_url + f"/records/{record_id}/details?fields={fields}",
            headers=self.headers)
        return s.json()

    def convert(self, input_str, input_format, output_format):
        return requests.post(
            url='https://api.rsc.org/compounds/v1/tools/convert',
            headers=self.headers,
            json={
                "input": input_str,
                "inputFormat": input_format,
                "outputFormat": output_format
            })

    def inchi_to_inchikey(self, inchi):
        self.convert(input_str=inchi, input_format='inchi', output_format='inchikey')

    def inchikey_to_inchi(self, inchikey):
        self.convert(input_str=inchikey, input_format='inchikey', output_format='inchi')

    def inchikey_to_species_obj(self, inchikey):
        r = requests.post(
            url=base_url + '/filter/inchikey',
            headers=self.headers,
            json={
                "inchikey": inchikey
            })
        if r.status_code != 200:
            raise NameError(f'Seems invalid: {r.reason}')
        query_id = r.json()["queryId"]
        results = self.get_results(query_id)
        rsc_objs = []
        for record_id in results:
            rsc_objs.append(self.get_rsc_obj(record_id))
        return sorted(rsc_objs, key=lambda k: k['referenceCount'])

    def get_results_by_path(self, path, payload):
        r = requests.post(
            url=base_url + path,
            headers=self.headers,
            json=payload)
        if r.status_code != 200:
            raise NameError(f'Seems invalid: {r.reason}')
        query_id = r.json()["queryId"]
        return self.get_results(query_id)


class InvalidFormatException(Exception): pass
