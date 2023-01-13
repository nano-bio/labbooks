#!/usr/bin/python

import re
import requests
import json

url = 'https://api.rsc.org/compounds/v1/tools/convert'
headers = {'apikey': '3OQZOrXI0q00zVB4S7TheOnvV3vASoPi'}


def inchi2inchikey(inchi):
    """Convert InChI to InChI-Key"""
    request_body = {
        'input': inchi,
        'inputFormat': 'InChI',
        'outputFormat': 'InChIKey'
    }
    try:
        result = json.loads(requests.post(url, json=request_body, headers=headers).text).get('output')
    except (requests.exceptions.RequestException, ValueError):
        result = ''
    return result


def inchikey2inchi(inchikey):
    """Convert InChI-Key to InChI"""
    request_body = {
        'input': inchikey,
        'inputFormat': 'InChIKey',
        'outputFormat': 'InChI'
    }
    try:
        result = json.loads(requests.post(url, json=request_body, headers=headers).text).get('output')
    except (requests.exceptions.RequestException, ValueError):
        result = ''
    return result


def inchi2chemicalformula(inchi):
    """Extract chemical formula from InChI"""
    match = re.match('^InChI=1S/(([A-Z]{1}[a-z]{0,2}[0-9]{0,3})+)+(/)?.*$', str(inchi))
    if match is not None:
        return match.group(1)
    else:
        splitup = str(inchi).split('/')
        if len(splitup) > 1:
            return splitup[1]
        else:
            return ''


def inchikey2chemicalformula(inchikey):
    """Convert InChi to InChI-Key and extract chemical formula from InChI"""
    inchi = inchikey2inchi(inchikey)
    return inchi2chemicalformula(inchi)
