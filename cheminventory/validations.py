#!/usr/bin/python
""" provides some basic chemical functions """
from django.core.exceptions import ValidationError
import re

# list of nominal mass of most abundant isotopes
# taken from http://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl
atommasses = {
    'H': 1,
    'D': 2,
    'He': 4,
    'Li': 7,
    'Be': 9,
    'B': 11,
    'C': 12,
    'N': 14,
    'O': 16,
    'F': 19,
    'Ne': 20,
    'Na': 23,
    'Mg': 24,
    'Al': 27,
    'Si': 28,
    'P': 31,
    'S': 32,
    'Cl': 35,
    'Ar': 40,
    'K': 39,
    'Ca': 40,
    'Sc': 45,
    'Ti': 48,
    'V': 51,
    'Cr': 52,
    'Mn': 55,
    'Fe': 56,
    'Co': 59,
    'Ni': 58,
    'Cu': 63,
    'Zn': 64,
    'Ga': 69,
    'Ge': 74,
    'As': 75,
    'Se': 80,
    'Br': 79,
    'Kr': 84,
    'Rb': 85,
    'Sr': 88,
    'Y': 89,
    'Zr': 90,
    'Nb': 93,
    'Mo': 98,
    'Tc': 98,
    'Ru': 102,
    'Rh': 103,
    'Pd': 106,
    'Ag': 107,
    'Cd': 114,
    'In': 115,
    'Sn': 120,
    'Sb': 121,
    'Te': 130,
    'I': 127,
    'Xe': 132,
    'Cs': 133,
    'Ba': 138,
    'La': 139,
    'Ce': 140,
    'Pr': 141,
    'Nd': 142,
    'Pm': 145,
    'Sm': 152,
    'Eu': 153,
    'Gd': 158,
    'Tb': 159,
    'Dy': 162,
    'Ho': 165,
    'Er': 166,
    'Tm': 169,
    'Yb': 174,
    'Lu': 175,
    'Hf': 180,
    'Ta': 181,
    'W': 184,
    'Re': 187,
    'Os': 192,
    'Ir': 193,
    'Pt': 195,
    'Au': 197,
    'Hg': 202,
    'Tl': 205,
    'Pb': 208,
    'Bi': 209,
    'Po': 209,
    'At': 210,
    'Rn': 211,
    'Fr': 223,
    'Ra': 223,
    'Ac': 227,
    'Th': 232,
    'Pa': 231,
    'U': 238,
}

# we define the regex object for chemical formulas
rechem = re.compile('^([A-Z]{1}[a-z]{0,2}[0-9]{0,3})+$')


def checkatoms(chemical_formula):
    """ Checks each atom in a chemical formula for validity (e.g. listing in atommasses) """
    result = 0
    match = re.findall('([A-Z]{1}[a-z]{0,2})', str(chemical_formula))
    for atom in match:
        try:
            mass = atommasses[atom]
        except KeyError:
            result = atom

    return result


# define validations for CAS and chemical formulas

def validate_CAS(cas):
    sum = 0
    cas_arr = cas.split('-')
    if len(cas_arr) < 3:
        raise ValidationError(u'%s is not a valid CAS-number!' % cas)
    length = len(cas_arr[0]) + 2
    for x in cas_arr[0]:
        sum = sum + length * int(x)
        length = length - 1
    sum = sum + 2 * int(cas_arr[1][0]) + int(cas_arr[1][1])
    if sum % 10 != int(cas_arr[2]):
        raise ValidationError(u'%s is not a valid CAS-number!' % cas)


def validate_chemical_formula(chemical_formula):
    """ checks chemical formulae for plausibility """

    # first we check if the formula seems like a chemical formula
    m = rechem.match(chemical_formula)
    if m is None:
        # it could be one of those cases, where it starts with a number and everything up to
        # the dot must be multiplied
        dotsplit = chemical_formula.split('.')
        if len(dotsplit) > 1:
            if dotsplit[0][0].isdigit():
                # tbm = to be multiplied
                tbm = dotsplit[0].lstrip('0123456789')
                new = []
                factor = int(dotsplit[0][0])
                for char in tbm:
                    if char.isdigit():
                        new.append(str(int(char) * factor))
                    else:
                        new.append(char)
                newsumformula = ''.join(new)
                dotsplit[0] = newsumformula
                corr_formula = ''.join(dotsplit)
                if rechem.match(corr_formula) is None:
                    raise ValidationError(u'%s does not seem to be a chemical formula' % chemical_formula)
            else:
                raise ValidationError(u'%s does not seem to be a chemical formula' % chemical_formula)
        else:
            raise ValidationError(u'%s does not seem to be a chemical formula' % chemical_formula)

    # we outsource the checking of individual atoms to the chemlib
    result = checkatoms(chemical_formula)
    if result != 0:
        raise ValidationError(u'%s is not an atom' % result)


def validate_name(name):
    m = rechem.match(name)
    if m is not None:
        raise ValidationError(u'%s seems to be a chemical formula. Please use a normal name or leave it blank.' % name)
