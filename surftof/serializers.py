from surftof.models import CountsPerMass
from rest_framework import serializers
from surftof.helper import *


class CountsPerMassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountsPerMass
        exclude = [
            'surface_temperature',
            'surface_impact_energy',
            'pressure_is',
            'pressure_tof',
            'pressure_surf',
            'surface_current']

    def create(self, validated_data):
        measurement = validated_data['measurement']
        # calculate pressures
        pressures = import_pressure(measurement.id)
        pressure_is = pressures['is']
        pressure_surf = pressures['surf']
        pressure_tof = pressures['tof']

        # calculate temperature
        temperature = float(get_temp_from_file(measurement.id).split(' ')[0])

        if 'comment' in validated_data:
            comment = validated_data['comment']
        else:
            comment = ''
        if 'molecule' in validated_data:
            molecule = validated_data['molecule']
        else:
            molecule = ''

        # calculate surface current
        surface_current = import_pico_log_and_median(measurement.id)

        # get surface impact energy
        if measurement.potential_settings and \
                measurement.potential_settings.source_ion_spacer is not None and \
                measurement.potential_settings.surface is not None:
            impact_energy = measurement.potential_settings.source_ion_spacer - measurement.potential_settings.surface
        else:
            impact_energy = None

        defaults = {
            'counts': validated_data['counts'],
            'counts_err': validated_data['counts_err'],
            'surface_temperature': temperature,
            'pressure_is': pressure_is,
            'pressure_surf': pressure_surf,
            'pressure_tof': pressure_tof,
            'surface_impact_energy': impact_energy,
            'surface_current': surface_current,
            'molecule': molecule,
            'comment': comment
        }

        cpm, created = CountsPerMass.objects.update_or_create(
            mass=validated_data['mass'],
            measurement=measurement,
            defaults=defaults)

        return cpm
