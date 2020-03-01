from django import template
from overview.models import (FH4Track, FH4Championship, FH4Tune)
import util

register = template.Library()


@register.inclusion_tag('overview/overview_track.html', takes_context=True)
def fh4_all_tracks(context, url=""):
    """ Will display all FH4 Tracks (or one if 'id' is in querystring of URL. """
    get_options = util.get_GET_options(url)
    retVal = {
        'request': context['request'],
    }
    if "id" in get_options:
        try:
            GET_id = int(get_options['id']) - 1
        except ValueError:
            GET_id = -1
    else:
        GET_id = -1

    if GET_id is not -1 and FH4Track.objects.all().count() > GET_id:
        retVal['events'] = [FH4Track.objects.all()[GET_id], ]
    else:
        retVal['events'] = context["events"]

    return retVal


@register.inclusion_tag('overview/overview_champ.html', takes_context=True)
def fh4_all_champs(context, url=''):
    """ Will display all FH4 championships (or one if 'id' is in querystring of URL). """
    get_options = util.get_GET_options(url)
    retVal = {
        'request': context['request'],
    }
    if "id" in get_options:
        try:
            GET_id = int(get_options['id']) - 1
        except ValueError:
            GET_id = -1
    else:
        GET_id = -1

    if GET_id is not -1 and FH4Championship.objects.all().count() > GET_id:
        retVal['champs'] = [FH4Championship.objects.all()[GET_id], ]
    else:
        retVal['champs'] = context["champs"]

    return retVal


@register.inclusion_tag('overview/overview_tune.html', takes_context=True)
def fh4_all_tunes(context, url=''):
    """ Will display all FH4 setups (or one if 'id' is in querystring of URL). """
    get_options = util.get_GET_options(url)
    retVal = {
        'request': context['request'],
    }
    if "id" in get_options:
        try:
            GET_id = int(get_options['id']) - 1
        except ValueError:
            GET_id = -1
    else:
        GET_id = -1

    if GET_id is not -1 and FH4Tune.objects.all().count() > GET_id:
        retVal['tunes'] = [FH4Tune.objects.all()[GET_id], ]
    else:
        retVal['tunes'] = context["tunes"]

    return retVal


@register.simple_tag(takes_context=True)
def subtract(context, int1=0, int2=0):
    return int1 - int2
