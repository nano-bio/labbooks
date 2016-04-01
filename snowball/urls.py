from django.conf.urls import patterns, url, include
from models import Measuremente, JournalEntry, Turpopump
from django.views.generic import ListView
from django.contrib.flatpages import views as flatpagesvies
from django.http import HttpResponseRedirect

import snowball.views
