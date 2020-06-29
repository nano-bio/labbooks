from django.urls import path

import cheminventory.views

urlpatterns = [
    path('doorsign/<int:labid>/',
         cheminventory.views.print_doorsign,
         name="cheminventory-print-doorsign"),
    path('chemwaste/<int:locid>/',
         cheminventory.views.print_chemwaste,
         name="cheminventory-print-chemwaste"),
    path('qrcode/<int:gc_id>/',
         cheminventory.views.print_gas_cylinder_qr,
         name="cheminventory-print-gas-cylinder-qr"),
    path('csv',
         cheminventory.views.csv_export,
         name="cheminventory-csv-export"),
]
