from django.contrib import admin
from wagtail.contrib.modeladmin.options import (ModelAdmin, modeladmin_register)

from .models import (FH4Track, FH4Route, FH4Championship, FH4Tune)

# Register your models here.


class Fh4TrackAdmin(ModelAdmin):
    model = FH4Track
    menu_label = "FH4 Event"
    menu_icon = "placeholder"
    menu_order = 102
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "sharecode", "car_power", "description", "laps", "season", "car_class", "time_of_day", "weather", "track", "event_image",)
    search_fields = ("name", "track", "sharecode",)


class Fh4RouteAdmin(ModelAdmin):
    model = FH4Route
    menu_label = "FH4 Route"
    menu_icon = "placeholder"
    menu_order = 101
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "type", "length_per_round", "track_image",)
    search_fields = ("name", "type", "length_per_round",)


class Fh4ChampionshipAdmin(ModelAdmin):
    model = FH4Championship
    menu_label = "FH4 Championship"
    menu_icon = "placeholder"
    menu_order = 103
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "description", "prize_money", "further_prize",)
    search_fields = ("name",)


class Fh4TuneAdmin(ModelAdmin):
    model = FH4Tune
    menu_label = "FH4 Tune"
    menu_icon = "placeholder"
    menu_order = 104
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "car", "pi", "tune_type")
    search_fields = ("name", "car", "tune_type")


modeladmin_register(Fh4TrackAdmin)
modeladmin_register(Fh4RouteAdmin)
modeladmin_register(Fh4ChampionshipAdmin)
modeladmin_register(Fh4TuneAdmin)
