from urllib.parse import quote

from django.contrib import messages
from django.http import HttpResponseRedirect


def create_new_entry_based_on_existing_one_url(s, forbidden_items):
    # this variable will hold all the values and is the address to the new setting form
    redirect_address = u'add/?'

    # walk through all fields of the model
    for item in s.__dict__:
        if item not in forbidden_items:  # we don't want these to be adopted
            if s.__dict__[item] is not None:
                # ForeignKey fields have to be named without "_id", so the last 3 chars are truncated
                if "id" in quote(item) and len(quote(item)) > 2:
                    redirect_address += quote(item)[:-3] + '=' + quote(str(s.__dict__[item])) + '&'
                else:
                    redirect_address += quote(item) + '=' + quote(str(s.__dict__[item])) + '&'
    return redirect_address


def create_new_entry_based_on_existing_one(request, queryset, forbidden_items):
    # we can only base it on one measurement
    if len(queryset) == 1:
        s = queryset.get()
        # redirect to newly created address
        return HttpResponseRedirect(create_new_entry_based_on_existing_one_url(s, forbidden_items))
    else:
        messages.error(request, 'You can only base a new entry on ONE existing setting, stupid.')
