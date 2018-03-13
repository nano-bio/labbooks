import sys

sys.path.append('/var/opt')

from django.db import models
from django.core.exceptions import ValidationError
import re
import fitlib.chemlib
import validations
from inchivalidation import inchi2chemicalformula


SOM = (
    ('FLUID', 'Fluid'),
    ('GAS', 'Gas Phase'),
    ('SOLID', 'Solid'),
)

GROUPS = (
    ('DENIFL', 'Denifl'),
    ('SCHEIER', 'Scheier'),
)

class StorageLocation(models.Model):
    name = models.CharField(max_length = 200)

    suitable_for = models.CharField(max_length = 5, choices = SOM)

    toxic_or_health_hazard_necessary = models.BooleanField(default = False)
    explosive_necessary = models.BooleanField(default = False)
    oxidizing_necessary = models.BooleanField(default = False)
    flammable_necessary = models.BooleanField(default = False)
    irritant_necessary = models.BooleanField(default = False)
    corrosive_necessary = models.BooleanField(default = False)
    environmentally_damaging_necessary = models.BooleanField(default = False)
    h2o_reactivity_necessary = models.BooleanField(default = False)

    toxic_allowed = models.BooleanField(default = False)
    explosive_allowed = models.BooleanField(default = False)
    oxidizing_allowed = models.BooleanField(default = False)
    flammable_allowed = models.BooleanField(default = False)
    irritant_allowed = models.BooleanField(default = False)
    corrosive_allowed = models.BooleanField(default = False)
    health_hazard_allowed = models.BooleanField(default = False)
    environmentally_damaging_allowed = models.BooleanField(default = False)
    h2o_reactivity_allowed = models.BooleanField(default = False)

    def __unicode__(self):
        return u'%s' % (self.name)

    def clean(self):
        params2check = ['oxidizing', 'irritant', 'explosive', 'flammable', 'corrosive', 'environmentally_damaging']
        for parameter in params2check:
            if self.__dict__[parameter + '_necessary'] is True and self.__dict__[parameter + '_allowed'] is False:
                raise ValidationError('If a hazard is necessary, it must also be allowed!')

        if self.toxic_or_health_hazard_necessary is True and (self.toxic_allowed is False or self.health_hazard_allowed is False):
                raise ValidationError('If a hazard is necessary, it must also be allowed!')

class Person(models.Model):
    name = models.CharField(max_length = 200)
    office_phone = models.IntegerField()
    mobile = models.CharField(max_length = 15)

    def __unicode__(self):
        return u'%s' % (self.name)

class UsageLocation(models.Model):
    name = models.CharField(max_length = 200)
    room_number = models.CharField(max_length = 6)
    responsible_persons = models.ManyToManyField(Person)
    experiment = models.TextField(max_length = 1000, blank = True)

    def __unicode__(self):
        return u'%s' % (self.name)

class GHS_H(models.Model):
    number = models.CharField(max_length = 12)
    text = models.CharField(max_length = 400)

    def __unicode__(self):
        return u'%s' % (self.number)

    class Meta:
        verbose_name_plural = 'GHS H'
        verbose_name = 'GHS H'
        ordering = ['number']


class GHS_P(models.Model):
    number = models.CharField(max_length = 12)
    text = models.CharField(max_length = 400)

    def __unicode__(self):
        return u'%s' % (self.number)

    class Meta:
        verbose_name_plural = 'GHS P'
        verbose_name = 'GHS P'
        ordering = ['number']

class Chemical(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Common Name', validators=[validations.validate_name])
    chemical_formula = models.CharField(max_length=40, db_index=True, verbose_name='Chemical Formula', default = '', blank = True, validators=[validations.validate_chemical_formula])
    inchi = models.CharField(max_length=700,db_index=True,verbose_name='InChI', blank = True)
    inchikey = models.CharField(max_length=27, db_index=True, verbose_name='InChI-Key', blank = True)
    cas = models.CharField(max_length=12,verbose_name='CAS-Number', blank = True, validators = [validations.validate_CAS])
    csid = models.IntegerField(blank = True, null = True, verbose_name = 'CSID')
    no_chemspider_sync = models.BooleanField(default = False, verbose_name = 'Do not sync with chemspider service')
    state_of_matter = models.CharField(max_length = 5, choices = SOM, default = 'FLUID')

    irritant = models.BooleanField()
    toxic = models.BooleanField()
    explosive = models.BooleanField()
    oxidizing = models.BooleanField()
    flammable = models.BooleanField()
    health_hazard = models.BooleanField()
    corrosive = models.BooleanField()
    environmentally_damaging = models.BooleanField(verbose_name = 'Environ. dam.')
    h2o_reactivity = models.BooleanField()

    ghs_h = models.ManyToManyField(GHS_H, blank = True)
    ghs_p = models.ManyToManyField(GHS_P, blank = True)

    class Meta:
        # in case we have chemicals in solution there should only be one with the same state of matter, CAS and dangers to it
        unique_together = (('cas','state_of_matter','irritant','toxic','explosive','oxidizing','flammable','health_hazard','corrosive','environmentally_damaging','h2o_reactivity'),
                           ('inchikey','state_of_matter','irritant','toxic','explosive','oxidizing','flammable','health_hazard','corrosive','environmentally_damaging','h2o_reactivity'),
                           ('csid','state_of_matter','irritant','toxic','explosive','oxidizing','flammable','health_hazard','corrosive','environmentally_damaging','h2o_reactivity'))
        ordering = ['name']

    def __unicode__(self):
        if self.chemical_formula is not u'':
            return u'%s (%s)'%(self.name, self.chemical_formula)
        else:
            return u'%s'%(self.name)

    def clean(self):
        if self.cas != u'':
            validations.validate_CAS(self.cas)

        if self.no_chemspider_sync is False:
            if self.csid is not None:
                chemobj = fitlib.chemlib.ChemicalObject(csid = self.csid)
            else:
                chemobj = fitlib.chemlib.ChemicalObject(name = self.name, inchi = self.inchi, inchikey = self.inchikey, cas = self.cas)

            chemobj.complete()

            if (self.inchi != '') and (self.inchi != chemobj.inchi):
                raise ValidationError('The given InChI and the one retrieved from Chemspider do not match. %s %s' % (self.inchi, chemobj.inchi))

            if (self.inchikey != '') and (self.inchikey != chemobj.inchikey):
                raise ValidationError('The given InChI-Key and the one retrieved from Chemspider do not match. %s %s' % (self.inchikey, chemobj.inchikey))

            if (self.csid is not None) and (self.csid != chemobj.csid):
                raise ValidationError('The given CSID and the one retrieved from Chemspider do not match. %s %s' % (str(self.csid), chemobj.csid))

            self.inchi = chemobj.inchi
            self.inchikey = chemobj.inchikey
            self.csid = chemobj.csid

        if self.inchi != '' and self.chemical_formula != '':
            if self.chemical_formula != inchi2chemicalformula(self.inchi):
                raise ValidationError('Chemical Formula does not match InChI')
        elif self.chemical_formula == '' and self.inchi != '':
            self.chemical_formula = inchi2chemicalformula(self.inchi)

class ChemicalInstance(models.Model):
    chemical = models.ForeignKey(Chemical, related_name = 'chemical_instance')
    company = models.CharField(max_length = 100, blank = True)
    item_number = models.CharField(max_length = 100, blank = True)
    quantity = models.CharField(max_length = 100, blank = True)
    delivery_date = models.DateField(blank = True, null = True)
    group = models.CharField(max_length = 7, null = True, choices = GROUPS, default = 'DENIFL')
    last_used = models.DateField(blank = True, null = True)
    last_user = models.CharField(max_length = 100, blank = True, null = True)
    storage_location = models.ForeignKey(StorageLocation)
    usage_location = models.ForeignKey(UsageLocation, blank = True, null = True)

    cylinder_number = models.IntegerField(blank = True, null = True, unique = True, verbose_name = 'Number of gas cylinder in wiki')

    comments = models.TextField(max_length = 1000, blank = True)

    class Meta:
        order_with_respect_to = 'chemical'

    def __unicode__(self):
        if self.chemical.state_of_matter == 'GAS':
            return u'%s Gas (Cylinder No. %s)' % (self.chemical.name, self.cylinder_number)
        if self.chemical.chemical_formula is not u'':
            return u'%s (%s) at %s'%(self.chemical.name, self.chemical.chemical_formula, self.storage_location.name)
        else:
            return u'%s at %s'%(self.chemical.name, self.storage_location)

    def state_of_matter(self):
        return self.chemical.state_of_matter
    state_of_matter.admin_order_field = 'chemical__state_of_matter'
    state_of_matter.short_description = 'State'

    def cas(self):
        return self.chemical.cas
    cas.admin_order_field = 'chemical__cas'
    cas.short_description = 'CAS'

    def irritant(self):
        return self.chemical.irritant
    irritant.admin_order_field = 'chemical__irritant'
    irritant.boolean = True

    def toxic(self):
        return self.chemical.toxic
    toxic.admin_order_field = 'chemical__toxic'
    toxic.boolean = True

    def explosive(self):
        return self.chemical.explosive
    explosive.admin_order_field = 'chemical__explosive'
    explosive.boolean = True

    def oxidizing(self):
        return self.chemical.oxidizing
    oxidizing.admin_order_field = 'chemical__oxidizing'
    oxidizing.boolean = True

    def flammable(self):
        return self.chemical.flammable
    flammable.admin_order_field = 'chemical__flammable'
    flammable.boolean = True

    def health_hazard(self):
        return self.chemical.health_hazard
    health_hazard.admin_order_field = 'chemical__health_hazard'
    health_hazard.boolean = True

    def corrosive(self):
        return self.chemical.corrosive
    corrosive.admin_order_field = 'chemical__corrosive'
    corrosive.boolean = True

    def environmentally_damaging(self):
        return self.chemical.environmentally_damaging
    environmentally_damaging.admin_order_field = 'chemical__environmentally_damaging'
    environmentally_damaging.boolean = True

    def clean(self):
        # chemical allowed?
        params2check = ['toxic', 'oxidizing', 'irritant', 'explosive', 'flammable', 'health_hazard', 'corrosive', 'environmentally_damaging']
        for parameter in params2check:
            if self.chemical.__dict__[parameter] is True and self.storage_location.__dict__[parameter + '_allowed'] is False:
                raise ValidationError('This sample is not stored in a place where %s materials are allowed' % (parameter))

        # does the chemical fulfill the requirements?
        params2check = ['oxidizing', 'irritant', 'explosive', 'flammable', 'corrosive', 'environmentally_damaging']
        for parameter in params2check:
            if self.chemical.__dict__[parameter] is False and self.storage_location.__dict__[parameter + '_necessary'] is True:
                raise ValidationError('This sample must be stored in a place where materials must be %s' % (parameter))

        # is it either toxic or a health hazard?
        if self.storage_location.toxic_or_health_hazard_necessary is True:
            if self.chemical.toxic is False and self.chemical.health_hazard is False:
                raise ValidationError('This sample is stored in a place where materials must be toxic or a health hazard and it is neither')

        # we also have to check whether the state of matter is correct
        if self.chemical.state_of_matter != self.storage_location.suitable_for:
            raise ValidationError('The state of matter of this sample is not allowed in this storage location')

class GasCylinder(models.Model):
    cylinder_number = models.IntegerField(unique = True, verbose_name = 'Number of gas cylinder')
    chemical = models.ForeignKey(Chemical, related_name = 'gas_cylinder')
    pressure = models.FloatField(default = 200)
    quality = models.FloatField(default = 5.0)
    company = models.CharField(max_length = 100, blank = True)
    quantity = models.CharField(max_length = 100, blank = True)
    delivery_date = models.DateField(blank = True, null = True)
    group = models.CharField(max_length = 7, null = True, choices = GROUPS, default = 'SCHEIER')
    storage_location = models.ForeignKey(StorageLocation)
    comments = models.TextField(max_length = 1000, blank = True)

    def current_usage_location(self):
        name = GasCylinderUsageRecord.objects.filter(gas_cylinder = self.id).order_by('-date')[0:1].get().usage_location.name
        return name

    current_usage_location.admin_order_field = 'UsageRecord__usage_location'

    def __unicode__(self):
        return u'%s Gas (Cylinder No. %s, %s bar)' % (self.chemical.name, self.cylinder_number, self.pressure)

    def cas(self):
        return self.chemical.cas
    cas.admin_order_field = 'chemical__cas'
    cas.short_description = 'CAS'

    # this gets the lowest free gas cylinder number. this seems kind of ugly, but I cannot think
    # of a better solution right now.
    @staticmethod
    def get_lowest_free_number():
        for i in range(0,1000):
            amount_with_this_id = GasCylinder.objects.filter(cylinder_number = i).count()
            if amount_with_this_id == 0:
                return i

    def chemical__name(self):
        return self.chemical.name
    chemical__name.admin_order_field = 'chemical__name'
    chemical__name.short_descriptioN = 'Gas'

class GasCylinderUsageRecord(models.Model):
    gas_cylinder = models.ForeignKey(GasCylinder)
    date = models.DateField()
    user = models.ForeignKey(Person)
    usage_location = models.ForeignKey(UsageLocation)
    comment = models.CharField(max_length = 100, blank = True)

    def __unicode__(self):
        return u'Cylinder %s (%s) used at %s on %s' % (self.gas_cylinder.id, self.gas_cylinder.chemical.name, self.usage_location, self.date) 
