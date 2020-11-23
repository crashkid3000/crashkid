from datetime import datetime, timezone
import json

import util
from fh4statspage.models import FHStatsPage, FHStats, CSGOStats, CSGOStatsPage
from django import template

register = template.Library()


@register.inclusion_tag('fh4statspage/api_fhstats.html', takes_context=True)
def render_forza_stats(context):
    retVal = {
        'request': context,
    }
    curr_page = FHStatsPage.objects.filter(id=context["curr_page_id"])
    curr_page = curr_page[0]
    if curr_page.apistats is None or (datetime.now(timezone.utc) - curr_page.apistats.object_last_updated).days >= 1:  # if at least 1 day passed since last update
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


@register.simple_tag(takes_context=True)
def refresh_csgo_stats(context):
    """Refreshes the CSGO stats after at least 24h have passed since the last update"""

    curr_page = CSGOStatsPage.objects.filter(id=context["curr_page_id"])[0]
    print(" -> curr_page wurde zugewiesen")
    if curr_page.stats is None or (datetime.now(timezone.utc) - curr_page.stats.object_last_updated).days >= 1:
        statsdict = util.retrieve_csgo_stats_crashkid()
        if "req_success" in statsdict.keys() and statsdict["req_success"] is True:
            statsdict = statsdict["playerstats"]["stats"]
            statsmodel = CSGOStats()
            updatectr = 0
            for stat in statsdict:
                if hasattr(statsmodel, stat["name"]):
                    setattr(statsmodel, stat["name"], stat["value"])
                    updatectr += 1
            print(str(updatectr) + " fields updated. :D")

            statsmodel.save()
            curr_page.stats = statsmodel
            curr_page.save()
        else:
            print("Could not update CSGOStats model!")
    # return context


@register.inclusion_tag('fh4statspage/csgo_weapons.html', takes_context=True)
def render_csgo_weapon_stats(context):
    curr_page = CSGOStatsPage.objects.filter(id=context["curr_page_id"])
    curr_page = curr_page[0]
    weapon_kills_ordered = curr_page.stats.sort_weapons_after_kills()
    context["weaponstats"] = weapon_kills_ordered
    return context


@register.simple_tag(takes_context=False)
def get_readable_weaponame(name=""):
    irregular_weapon_names = {  # ie those weapon names whose actual name is not just the capitalized weapon name
        "glock": "Glock-18",
        "p2k": "P2000/USP-S",
        "elite": "Dual Berettas",
        "fiveseven": "Five-seveN",
        "tec9": "Tec-9",
        "deagle": "Deagle/R8",
        "mag7": "MAG-7",
        "mac10": "MAC-10",
        "ump45": "UMP-45",
        "mp7": "MP7/MP5-SD",
        "bizon": "PP-Bizon",
        "galil": "Galil AR",
        "ak47": "AK-47",
        "m4a1": "M4A4/M4A1-S",
        "sg556": "SG553",
        "scar20": "SCAR-20",
    }
    if name in irregular_weapon_names:
        return irregular_weapon_names[name]
    else:
        return name.upper()


@register.inclusion_tag('fh4statspage/csgo_maps.html', takes_context=True)
def render_csgo_maps_stats(context):
    print(context["curr_page_id"])
    curr_page = CSGOStatsPage.objects.filter(id=context["curr_page_id"])
    curr_page = curr_page[0]
    map_wins_ordered = curr_page.stats.sort_maps_after_wins()
    context["mapwins"] = map_wins_ordered
    return context

