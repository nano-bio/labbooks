from django.apps import AppConfig


class StmConfig(AppConfig):
    name = 'stm'
    verbose_name = 'Awesome STM'

    def ready(self):
        import stm.signals
