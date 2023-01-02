from django.db import models

LABBOOK_EXPERIMENTS = [
    ['clustof', 'ClustTof'],
    ['toffy', 'Toffy'],
    ['toffy2', 'Toffy2'],
    ['surftof', 'SurfTof']
]


class MscpToken(models.Model):
    token = models.CharField(max_length=50)


class Experiment(models.Model):
    labbook_experiment = models.CharField(
        max_length=10,
        choices=LABBOOK_EXPERIMENTS,
        unique=True)
    experiment_id_mscp = models.IntegerField(
        help_text="Go to https://ideadb.uibk.ac.at/mscp/admin/node/experiment/ and use that ID here.")

    def __str__(self):
        return self.get_labbook_experiment_display()
