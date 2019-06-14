import os
import re
from time import time

from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils import timezone

from pyMTRX import experiment
from background_task import background
from stm.models import Measurement, Image


class Log:
    def __init__(self, name):
        self.path = "{}/{}.log".format(settings.STM_STORAGE, name)

    def start(self):
        text = "Started import at {}\n".format(timezone.now().isoformat())
        with open(self.path, "a") as file:
            file.write(text)

    def write(self, message):
        with open(self.path, "a") as file:
            file.write("{}\n".format(message))


def read_images_async(measurement_id):
    start_time = time()
    # this function reads all images from a given folder

    m = Measurement.objects.get(id=measurement_id)

    path = os.path.join(settings.STM_STORAGE, m.name)
    logger = Log(m.name)
    logger.start()

    files = os.listdir(path)
    logger.write("found {} files in this path".format(len(files)))

    mainfile = None
    for file in files:
        if file.find('_0001.mtrx') != -1:
            # we found the main file
            mainfile = file
            break

    if mainfile is None:
        logger.write("didn't found the _0001.mtrx file!")

    ex = experiment.Experiment(os.path.join(path, mainfile))
    image_count = 0

    logger.write("start looping over all items")

    # read all images
    for scan, _ in ex._cmnt_lkup.items():
        read_images_task(scan, path, mainfile, measurement_id)
        image_count += 1

    logger.write("{} images added to django-background-tasks".format(image_count))

    return image_count, time() - start_time


@background(schedule=timezone.now())
def read_images_task(scan, path, mainfile, measurement_id):
    m = Measurement.objects.get(id=measurement_id)
    ex = experiment.Experiment(os.path.join(path, mainfile))
    logger = Log(m.name)
    logger.write("start scan import: {}".format(scan))

    # filename parsing
    filenumber_regex = '--([0-9]{1,2}_[0-9]{1,2})\.'
    regex = re.compile(filenumber_regex)

    # sub function to create data_field names from property names
    def convert_to_data_field(field_name):
        return field_name.lower()

    if 'I_mtrx' in scan or 'Z_mtrx' in scan:
        try:
            image = ex.import_scan(os.path.join(path, scan))

            try:
                image_obj = Image(measurement=m)
                logger.write("first created \"{}\"".format(scan))
                for prop, value in image[0][0].props.items():
                    try:
                        setattr(image_obj, convert_to_data_field(prop), value.value)
                    except:
                        logger.write("exception in: prop {} for scan {}".format(prop, scan))

                logger.write("added all props \"{}\"".format(scan))
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
                logger.write("saved image for scan {}".format(scan))
                # save png preview image
                fn = NamedTemporaryFile(delete=True)
                try:
                    image[0][0].save_png(fn.name)
                    image_obj.preview_image.save('{}.png'.format(image_obj.id), File(fn), save=True)
                    logger.write('Image {} written with success'.format(image_obj.id))
                except ValueError as e:
                    logger.write('Image {} could not be written: {}'.format(image_obj.id, e))
            except Exception as e:
                logger.write("exception inner for scan \"{}\":\n{}".format(scan, e))

        except Exception as e:
            logger.write("exception outer for scan \"{}\":\n{}".format(scan, e))
