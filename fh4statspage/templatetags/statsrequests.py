from datetime import datetime, timezone

import util
from fh4statspage.models import FHStatsPage, FHStats
from django import template

register = template.Library()


@register.inclusion_tag('fh4statspage/api_fhstats.html', takes_context=True)
def render_forza_stats(context):
    retVal = {
        'request': context,
    }
    print("    >>> id: " + context["curr_page_id"])
    curr_page = FHStatsPage.objects.filter(id=context["curr_page_id"])
    curr_page = curr_page[0]
    if (datetime.now(timezone.utc) - curr_page.apistats.object_last_updated).days >= 1:  # if at least 1 day passed since last update
        if curr_page.game == "FH4":
            stats = util.retrieve_xboxlive_stats_crashkid(1985701699)  # 1985701699: gameid of Forza Horizon 4
            stats = util.improve_dict_access_for_fh_stats(stats)
            for i in range(len(stats)):
                if stats[i]['name'] == 'TotalCarsOwnedUpdated':
                    cars = stats[i]['value']
                elif stats[i]['name'] == 'InfluenceUpdated':
                    influence = stats[i]['value']
                elif stats[i]['name'] == 'MinutesPlayed':
                    playtime = stats[i]['value']
            last_update = datetime.now()
        elif curr_page.game == "FH3":
            stats = util.retrieve_xboxlive_stats_crashkid(1289871275)  # 1289871275: gameid of Forza Horizon 3
            stats = util.improve_dict_access_for_fh_stats(stats)
            for i in range(len(stats)):
                if stats[i]['name'] == 'CarsInGarage':
                    cars = stats[i]['value']
                elif stats[i]['name'] == 'XPGained':
                    influence = stats[i]['value']
                elif stats[i]['name'] == 'MinutesPlayed':
                    playtime = stats[i]['value']
            last_update = datetime.now()
        else:
            stats = {0: {}}
            stats[0]['name'] = ''
            stats[0]['value'] = -1
            stats[0]['display'] = 'Error: Game type not supported'
            playtime = -1
            cars = -1
            influence = -1

        if stats[0]['value'] != -1:  # if we could fetch the data
            curr_page.apistats = FHStats(playtime=playtime, cars_owned=cars, influence=influence, object_last_updated=datetime.now(timezone.utc))
    retVal["apistats"] = curr_page.apistats
    return retVal