labbooks
========

The repo holds our labbook software (currently used by VG).
Requires django >= 1.4

Changelog
=========

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
