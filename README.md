labbooks
========

The repo holds our labbook software (currently used by VG).
Requires django >= 1.4 (tested until 1.6.2)

Changelog
=========

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
