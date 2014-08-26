from django.contrib import admin, messages
from cheminventory.models import StorageLocation, Chemical, ChemicalInstance, StorageLocation, GHS_H, GHS_P, UsageLocation, Person
from django.http import HttpResponseRedirect

# Register your models here.

class ChemicalInstanceAdmin(admin.ModelAdmin):
    search_fields = ('chemical__name', 'chemical__chemical_formula', 'chemical__cas', 'chemical__inchi')
    list_display = ('__unicode__', 'cas', 'state_of_matter', 'irritant', 'toxic', 'explosive', 'oxidizing', 'flammable', 'health_hazard', 'corrosive', 'environmentally_damaging')
    list_filter = ('storage_location', 'chemical__state_of_matter', 'chemical__irritant', 'chemical__toxic', 'chemical__explosive', 'chemical__oxidizing', 'chemical__flammable', 'chemical__health_hazard', 'chemical__corrosive', 'chemical__environmentally_damaging', 'group')
    save_on_top = True
    raw_id_fields = ('chemical', )
    ordering = ['chemical__name']

class ChemicalAdmin(admin.ModelAdmin):
    search_fields = ('cas', 'name', 'chemical_formula', 'inchi', 'csid', 'inchikey')
    list_display = ('name', 'chemical_formula', 'cas', 'csid', 'state_of_matter', 'irritant', 'toxic', 'explosive', 'oxidizing', 'flammable', 'health_hazard', 'corrosive', 'environmentally_damaging')
    list_filter = ('state_of_matter', 'irritant', 'toxic', 'explosive', 'oxidizing', 'flammable', 'health_hazard', 'corrosive', 'environmentally_damaging')
    save_on_top = True
    filter_horizontal = ('ghs_p', 'ghs_h')

    actions = ['new_instance']

    def new_instance(self, request, queryset):
        if len(queryset) == 1:
            s = queryset.get()
        else:
            return messages.error(request, 'Select only one chemical!')
        return HttpResponseRedirect('/admin/cheminventory/chemicalinstance/add/?chemical=%s' % (str(s.id)))

class ChemicalInstanceInline(admin.TabularInline):
    model = ChemicalInstance

class UsageLocationAdmin(admin.ModelAdmin):
    actions = ['print_doorsign']

    inlines = [ChemicalInstanceInline]

    def print_doorsign(self, request, queryset):
        if len(queryset) == 1:
            s = queryset.get()
        else:
            return messages.error(request, 'Select only one location!')
        return HttpResponseRedirect('/cheminventory/doorsign/%s' % (str(s.id)))

class GHS_H_Admin(admin.ModelAdmin):
    save_on_top = True

class GHS_P_Admin(admin.ModelAdmin):
    save_on_top = True

admin.site.register(Chemical, ChemicalAdmin)
admin.site.register(ChemicalInstance, ChemicalInstanceAdmin)
admin.site.register(StorageLocation)
admin.site.register(GHS_H, GHS_H_Admin)
admin.site.register(GHS_P, GHS_P_Admin)
admin.site.register(UsageLocation, UsageLocationAdmin)
admin.site.register(Person)
