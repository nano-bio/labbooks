import os
import re

from pyMTRX import experiment

from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from background_task import background
from stm.models import Measurement, Image
from django.utils import timezone


class Log():
    def __init__(self):
        self.text = ''

    def write(self, message):
        self.text = self.text + '\n' + message

@background(schedule=timezone.now())
def read_images_async(id):
    # this function reads all images from a given folder

    # sub function to create data_field names from property names
    def convert_to_data_field(field_name):
        return field_name.lower()

    m = Measurement.objects.get(id=id)

    path = os.path.join(settings.STM_STORAGE, m.name)
    logger = Log()

    files = os.listdir(path)
    mainfile = None
    for file in files:
        if file.find('_0001.mtrx') != -1:
            # we found the main file
            mainfile = file
            break

    if mainfile is None:
        pass # TODO: warning

    ex = experiment.Experiment(os.path.join(path, mainfile))
    image_count = 0

    # filename parsing
    filenumber_regex = '--([0-9]{1,2}_[0-9]{1,2})\.'
    regex = re.compile(filenumber_regex)

    # read all images
    for scan, _ in ex._cmnt_lkup.items():
        if 'I_mtrx' in scan or 'Z_mtrx' in scan:
            try:
                image = ex.import_scan(os.path.join(path, scan))
                success = True
            except:
                success = False

            if success:
                image_count = image_count + 1
                image_obj = Image(measurement=m)
                for prop, value in image[0][0].props.items():
                    try:
                        setattr(image_obj, convert_to_data_field(prop), value.value)
                    except:
                        pass # todo maybe log that

                if 'I_mtrx' in scan:
                    image_obj.type = Image.I
                else:
                    image_obj.type = Image.V

                # note name
                matches = regex.search(scan)
                if matches is not None:
                    groups = matches.groups()
                    image_obj.name = groups[0]

                image_obj.save()

                # save png preview image
                fn = NamedTemporaryFile(delete=True)
                try:
                    image[0][0].save_png(fn.name)
                    image_obj.preview_image.save('{}.png'.format(image_obj.id), File(fn), save=True)
                except ValueError:
                    logger.write('Image {} could not be written'.format(image_obj.id))
    return image_count


