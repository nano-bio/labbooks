labbooks
========

The repo holds our labbook software (currently used by VG, CLUSTOF, WIPPI, SURFTOF).
Requires django >= 1.8 (tested until 1.9.4)

Changelog
=========

06.09.2106

* WIPPI/NEW/Josi: Changed textfield substance in WIPPI to a ForeignKey of cheminventory.chemical. Nice migrations saved the da[ta|y]!

18.07.2016

* CHEMICALINVENTORY/FIX/Josi: Properly search for gas cylinder usage records in admin interface
* CLUSTOF/NEW/Josi: New fields for gas inlets / pickup oven chemicals. Optional and is also used by search.
* CLUSTOF/FIX/Josi: Default nozzle size now 5 mum
* CLUSTOF/NEW/Josi: Two more operators

13.06.2016

* CHEMINVENTORY/NEW/Josi: Print date on doorsigns

25.04.2016

* SNOWBALL/NEW/Loernz: The Snowball side is added to the labbook (ALPHA)

19.04.2016

* CHEMINVENTORY/FIX: Do not allow gas-phase chemical instances (should be gas bottles)

18.04.2016

* CLUSTOF/NEW/Josi: Include temperature for vacuum status in CLUSTOF
* CLUSTOF/FIX/Josi: Fix new IPs for Snowball

05.04.2016

* WIPPI/VG/NEW/Josi: Field "fragment" for measured fragment in energy scan
* VG/NEW/Josi: added new functions to export F2, SF5 and SF6/SF6 energy scans

01.04.2016
* WIPPI/NEW/Lorenz: some new Lenses and fixes 

31.03.2016
* SURFTOF/FIX/Lorenz: corrected some content errors in Surftof

23.03.2016
* SURFTOF/NEW/Loernz: some more new Ionsource stuff

22.03.2016:

* ALL/FIX/Josi: change urls.py to be compatible with future releases >= 1.10
* SURFTOF/NEW/Lorenz: New lenses

21.03.2016:

* CLUSTOF/NEW: Also search for measurement ID in admin

29.02.2016:

* VG/WIPPI/FIX: Shorten link to measurement file download in admin

11.01.2016:

* SURFTOF/FIX: Add machine IP for SURFTOF

21.12.2015:

* SURFTOF/NEW: SurfTOF is completely new
* ALL/FIX: add template jscss.html which includes all basic jQuery and CSS inclusions (and update to jQ 1.11.3 min version)

15.12.2015:

* CLUSTOF/NEW: Implement reading, writing and saving pressures via JSON
* CLUSTOF/FIX: Don't save empty images in technical journal of clustof

09.11.2015:

* CHEMINVENTORY/NEW: Option to show all chemicals affected by certain GHS statements
* CHEMINVENTORY/NEW: Implement gas cylinder handling

07.07.2015:

* CLUSTOF/NEW: Allow for hand drawings in journal entries -> aimed at tablets
* CLUSTOF/FIX: Better search functions for journal entries
* CLUSTOF/FIX: proper handling for copying actions 

03.05.2015:

* CLUSTOF/FIX: Check for path in model.clean method

25.03.2015:

* ALL/FIX: Final changes for Django 1.7.7
* VG/NEW: Add Turbopump current tracking
* ALL/FIX: Prepare for Django 1.7

05.02.2015:

* CLUSTOF/NEW: Measurement properties can now be exported
* CLUSTOF/FIX: Upload limit for evaluation files now 500mb

02.02.2015:

* CLUSTOF/NEW: check sign of ion block voltage if measurement is negative

29.01.2015:

* CLUSTOF/NEW: Add Turbopump current tracking

14.01.2015:

* CLUSTOF/FIX: Properly label deflector lenses (oben/unten/links/rechts)

09.12.2014:

* CLUSTOF/NEW: Autocorrect filename if filename looks like TOF file, but doesn't have an extension

21.11.2014:

* VG/WIPPI/NEW: Direct link to viewing page in admin measurement list

03.10.2014:

* CLUSTOF/FIX: Enable admin to show measurements within +/- one week

01.10.2014:

* CLUSTOF/FIX: no more warning if EE cannot be calculated (mostly due to ES)
* CHEMINVENTORY/NEW: possibility to print automatic chem disposal sheets

22.08.2014:

* CLUSTOF/FIX: electron_energy wasn't renamed in the CurrentSettings model -> send2labbook 
               didn't work

21.08.2014:

* CLUSTOF/FIX: gunicorn 0.19 needs a different HTTP Request parameter to retrieve the
               client IP. Also: use settings.CLUSTOFIP to check IP for readsettings.

14.08.2014:

* VG/NEW: Allow for CID Scans

13.08.2014:

* CHEMINVENTORY/NEW: New action to add new instance from chemical list

25.07.2014:

* CHEMINVENTORY/NEW: Well, the entire thing is new. 

21.07.2014:

* WIPPI/FIX: Enable editing of Journal Entry dates in WIPPI

30.06.2014:

* WIPPI/VG/FIX: Increased maximum filename length for data files in WIPPI and VG

18.06.2014:

* CLUSTOF/NEW: Enable download of data file from admin measurement overview
* CLUSTOF/FIX: Minor cosmetic enhancements to admin measurement overview

17.06.2014:

* CLUSTOF/NEW: Enable download of evaluation file from admin measurement overview

13.06.2014:

* WIPPI/NEW: Calibrations with CCl4 now work
* WIPPI/FIX: Energyscan plots now also plot negative values
* VG/FIX: correctly determine whether a calibration is quadratic

12.06.2014:

* CLUSTOF/FIX: Add nozzle temp in admin interface

26.05.2014:

* CLUSTOF/FIX: Update labbook for new clustof computer (direct file export)
* CLUSTOF/FIX: Other minor CLUSTOF fixes

01.04.2014:

* ALL/FIX: Set max upload size to 200M for CLUSTOF evaluations

17.02.2014:

* CLUSTOF/NEW: new feature to export filename of measurement (for IsotopeFit)

11.02.2014:

* CLUSTOF/FIX: Add "evaluated by" field to admin

30.01.2014:

* CLUSTOF/FIX: Minor changes to measurement list template

27.01.2014:

* CLUSTOF/NEW: Export to tab-separated and JSON for Eval Software
* CLUSTOF/NEW: New fields evaluated_by and evaluation_file to quickly find unevaluated measurements

17.01.2014:

* VG/CLUSTOF/FIX: Minor fixes for compatibility with Django 1.6.1
* WIPPI/NEW: New WIPPI labbook. Currently testing.

16.01.2014:

* CLUSTOF/NEW: Show filename in CLUSTOF measurement list

09.11.2013:

* VG/NEW: vg/export_all_f_urls gives a list of URLs to all F-/SF6 scans used in calibrations
* VG/NEW: in a measurement view, one can now fit up to 5 Gaussians and retrieve the positions

04.11.2013:

* VG/FIX: Plural name of Journal Entries now correct
* VG/NEW: New column in measurement admin page: polarity
* VG/NEW: New filter option in measurement admin page: polarity
* VG/FIX: When adding a new journal entry, one can now manually set the date
* VG/NEW: Zoom feature in measurement view
* VG/NEW: New field gatetime
* VG/FIX: Avoid duplicate code by moving plotting code to a .js-file
