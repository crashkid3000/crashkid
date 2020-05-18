from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel
from wagtail.core.fields import RichTextField
import re

# Create your models here.


class FHStats(models.Model):
    """This model saves data from Forza Horizon games that can be retrieved from the API"""
    # data available from the API
    playtime = models.IntegerField(blank=False, null=False, default=-1, verbose_name="Playtime", help_text="Time spent playing the game in minutes.")  # in minutes
    cars_owned = models.IntegerField(blank=False, null=False, default=-1, verbose_name="Cars Owned", help_text="Number of cars in the garage.")
    influence = models.IntegerField(blank=False, null=False, default=-1, verbose_name="Influence", help_text="How much influence was earned.")
    object_last_updated = models.DateTimeField(auto_now_add=True, blank=False, null=False,
                                               verbose_name="last update of object",
                                               help_text="When this object was last updated")


class FHStatsPage(Page):

    GAMES = [('FH3', 'Forza Horizon 3'),
             ('FH4', 'Forza Horizon 4')]

    template = "fh4statspage/fhstats.html"

    game = models.CharField(max_length=3, blank=False, null=True, choices=GAMES, verbose_name="Game", help_text="The game this page is for")

    # data that needs to be updated manually
    tunings_released = models.IntegerField(blank=True, null=False, verbose_name="Tunings released", help_text="How many tunings were released.")
    designs_released = models.IntegerField(blank=True, null=False, verbose_name="Designs released", help_text="How many designs were released.")
    events_released = models.IntegerField(blank=True, null=False, verbose_name="Events released", help_text="How many events were published.")

    tunings_downloaded = models.IntegerField(blank=True, null=False, verbose_name="Tunings downloaded",
                                           help_text="How many tunings were downloaded by others.")
    designs_downloaded = models.IntegerField(blank=True, null=False, verbose_name="Designs downloaded",
                                           help_text="How many designs were downloaded by others.")
    events_played = models.IntegerField(blank=True, null=False, verbose_name="Events driven by others",
                                          help_text="How many events were played by others.")

    tunings_favd = models.IntegerField(blank=True, null=False, verbose_name="Tunings favoured",
                                           help_text="How many tunings were favored by others.")
    designs_favd = models.IntegerField(blank=True, null=False, verbose_name="Designs favoured",
                                           help_text="How many designs were favored by others.")
    events_favd = models.IntegerField(blank=True, null=False, verbose_name="Events favoured",
                                          help_text="How many events were favored by others.")

    cash = models.IntegerField(blank=True, null=False, verbose_name="Cash", help_text="How much cash is on the bank.")
    total_income = models.IntegerField(blank=True, null=False, verbose_name="Total income", help_text="How much money was earned.")
    garage_value = models.IntegerField(blank=True, null=False, verbose_name="Garage value", help_text="The combined cash value of all cars,")

    total_skillpoints = models.IntegerField(blank=True, null=False, verbose_name="Total skillpoints", help_text="How many skillpoints were earned in total")
    ultimate_skills = models.IntegerField(blank=True, null=False, verbose_name="Ultimate skills", help_text="How many ultimate skills were achieved")
    highest_skillscore = models.IntegerField(blank=True, null=False, verbose_name="Highest skillscore", help_text="Highest skillscore combo achieved")

    apistats = models.OneToOneField(
        FHStats,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    some_additional_text = RichTextField(null=False, blank=True, verbose_name="Additional text", help_text="Some additional text that is displayed below the stats box")

    content_panels = Page.content_panels + [
        FieldPanel("game"),
        MultiFieldPanel([
            FieldPanel("tunings_released"),
            FieldPanel("designs_released"),
            FieldPanel("events_released"),
        ], heading="1st row"),
        MultiFieldPanel([
            FieldPanel("tunings_downloaded"),
            FieldPanel("designs_downloaded"),
            FieldPanel("events_played"),
        ], heading="2nd row"),
        MultiFieldPanel([
            FieldPanel("tunings_favd"),
            FieldPanel("designs_favd"),
            FieldPanel("events_favd"),
        ], heading="3rd row"),
        MultiFieldPanel([
            FieldPanel("cash"),
            FieldPanel("total_income"),
            FieldPanel("garage_value"),
        ], heading="4th row"),
        MultiFieldPanel([
            FieldPanel("total_skillpoints"),
            FieldPanel("ultimate_skills"),
            FieldPanel("highest_skillscore"),
        ], heading="5th row"),
        FieldPanel("some_additional_text"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, args, kwargs)
        context["curr_page_id"] = self.id
        return context

    class Meta:
        verbose_name = "Forza Stats Page"


class CSGOStats(models.Model):

    total_kills = models.IntegerField(blank=True, null=True, help_text="Total ammount of kills", verbose_name="Total kills")
    total_deaths = models.IntegerField(blank=True, null=True, help_text="Total ammount of deaths", verbose_name="Total deaths")
    total_planted_bombs = models.IntegerField(blank=True, null=True, help_text="Total ammount of planted bombs", verbose_name="Planted bombs")
    total_rescued_hostages = models.IntegerField(blank=True, null=True, help_text="Total ammount of rescued hostages", verbose_name="Rescued hostages")
    total_mvps = models.IntegerField(blank=True, null=True, help_text="Total ammount of MVPs earned", verbose_name="MVPs earned")
    total_money_earned = models.IntegerField(blank=True, null=True, help_text="Total ammount of money earned", verbose_name="Money earned")
    total_wins = models.IntegerField(blank=True, null=True, help_text="Total amount of rounds won", verbose_name="Rounds won")
    total_rounds_played = models.IntegerField(blank=True, null=True, help_text="Total ammount of rounds played", verbose_name="Rounds won")

    total_kills_glock = models.IntegerField(blank=True, null=True, help_text="Total ammount of Glock kills", verbose_name="Glock kills")
    total_kills_hkp2000 = models.IntegerField(blank=True, null=True, help_text="Total ammount of P2000/USP-S kills", verbose_name="P2000/USP-S kills")
    total_kills_elite = models.IntegerField(blank=True, null=True, help_text="Total ammount of Dual Berettas kills", verbose_name="Dual Berettas kills")
    total_kills_p250 = models.IntegerField(blank=True, null=True, help_text="Total ammount of P250/CZ-75 Auto kills", verbose_name="P250 kills")
    total_kills_fiveseven = models.IntegerField(blank=True, null=True, help_text="Total ammount of Five-seveN kills", verbose_name="Five-seveN kills")
    total_kills_tec9 = models.IntegerField(blank=True, null=True, help_text="Total ammount of Tec-9 kills", verbose_name="Tec-9 kills")
    total_kills_deagle = models.IntegerField(blank=True, null=True, help_text="Total ammount of Desert Eagle/R8 Revolver kills", verbose_name="Desert Eagle kills")
    total_kills_nova = models.IntegerField(blank=True, null=True, help_text="Total ammount of Nova kills", verbose_name="Nova kills")
    total_kills_sawedoff = models.IntegerField(blank=True, null=True, help_text="Total ammount of Sawed-off kills", verbose_name="Sawed-off kills")
    total_kills_mag7 = models.IntegerField(blank=True, null=True, help_text="Total ammount of MAG-7 kills", verbose_name="MAG-7 kills")
    total_kills_xm1014 = models.IntegerField(blank=True, null=True, help_text="Total ammount of XM1014 kills", verbose_name="XM1014 kills")
    total_kills_m249 = models.IntegerField(blank=True, null=True, help_text="Total ammount of M249 kills", verbose_name="M249 kills")
    total_kills_negev = models.IntegerField(blank=True, null=True, help_text="Total ammount of Negev kills", verbose_name="Negev kills")
    total_kills_mp9 = models.IntegerField(blank=True, null=True, help_text="Total ammount of MP9 kills", verbose_name="MP9 kills")
    total_kills_mac10 = models.IntegerField(blank=True, null=True, help_text="Total ammount of MAC-10 kills", verbose_name="MAC-10 kills")
    total_kills_ump45 = models.IntegerField(blank=True, null=True, help_text="Total ammount of UMP-45 kills", verbose_name="UMP-45 kills")
    total_kills_bizon = models.IntegerField(blank=True, null=True, help_text="Total ammount of PP-Bizon kills", verbose_name="PP-Bizon kills")
    total_kills_mp7 = models.IntegerField(blank=True, null=True, help_text="Total ammount of MP7/MP5-SD kills", verbose_name="MP7 kills")
    total_kills_p90 = models.IntegerField(blank=True, null=True, help_text="Total ammount of P90 kills", verbose_name="P90 kills")
    total_kills_galilar = models.IntegerField(blank=True, null=True, help_text="Total ammount of Galil AR kills", verbose_name="Galil AR kills")
    total_kills_famas = models.IntegerField(blank=True, null=True, help_text="Total ammount of FAMAS kills", verbose_name="FAMAS kills")
    total_kills_ak47 = models.IntegerField(blank=True, null=True, help_text="Total ammount of AK-47 kills", verbose_name="AK-47 kills")
    total_kills_m4a1 = models.IntegerField(blank=True, null=True, help_text="Total ammount of M4A4/M4A1-S kills", verbose_name="M4A4-M4A1-S kills")
    total_kills_sg556 = models.IntegerField(blank=True, null=True, help_text="Total ammount of SG553 kills", verbose_name="SG553 kills")
    total_kills_aug = models.IntegerField(blank=True, null=True, help_text="Total ammount of AUG kills", verbose_name="AUG kills")
    total_kills_ssg08 = models.IntegerField(blank=True, null=True, help_text="Total ammount of SSG08 kills", verbose_name="SSG08 kills")
    total_kills_awp = models.IntegerField(blank=True, null=True, help_text="Total ammount of AWP kills", verbose_name="AWP kills")
    total_kills_scar20 = models.IntegerField(blank=True, null=True, help_text="Total ammount of SCAR-20 kills", verbose_name="SCAR-20 kills")
    total_kills_g3sg1 = models.IntegerField(blank=True, null=True, help_text="Total ammount of G3SG1 kills", verbose_name="G3SG1 kills")

    total_wins_map_cs_assault = models.IntegerField(blank=True, null=True, help_text="Total amount of rounds won on cs_assault", verbose_name="cs_assault wins")
    total_wins_map_cs_italy = models.IntegerField(blank=True, null=True, help_text="Total amount of rounds won on cs_italy", verbose_name="cs_italy wins")
    total_wins_map_cs_office = models.IntegerField(blank=True, null=True, help_text="Total amount of rounds won on cs_office", verbose_name="cs_office wins")
    total_wins_map_de_aztec = models.IntegerField(blank=True, null=True, help_text="Total amount of rounds won on de_aztec", verbose_name="de_aztec wins")
    total_wins_map_de_cbble = models.IntegerField(blank=True, null=True, help_text="Total amount of rounds won on de_cbble", verbose_name="de_cbble wins")
    total_wins_map_de_dust2 = models.IntegerField(blank=True, null=True, help_text="Total amount of rounds won on de_dust2/others", verbose_name="de_dust2/others wins")
    total_wins_map_de_dust = models.IntegerField(blank=True, null=True, help_text="Total amount of rounds won on de_dust", verbose_name="de_dust wins")
    total_wins_map_de_inferno = models.IntegerField(blank=True, null=True, help_text="Total amount of rounds won on de_inferno", verbose_name="de_inferno wins")
    total_wins_map_de_nuke = models.IntegerField(blank=True, null=True, help_text="Total amount of rounds won on de_nuke", verbose_name="de_nuke wins")
    total_wins_map_de_train = models.IntegerField(blank=True, null=True, help_text="Total amount of rounds won on de_train", verbose_name="de_train wins")
    total_wins_map_de_vertigo = models.IntegerField(blank=True, null=True, help_text="Total amount of rounds won on de_vertigo", verbose_name="de_vertigo wins")


    def __str__(self):
        return str("K-D: " + str(self.total_kills) + "-" + str(self.total_deaths))


    def sort_weapons_after_kills(self) -> list:
        attrs = list(vars(self))
        attrs_and_values = []  # will contain list of tuples containing member name and member values
        sorted_attrs = []
        for attr in attrs:
            if re.match("total_kills_.*", attr):
                attrs_and_values.append((attr, getattr(self, attr)))
        sorted_attrs_and_values = sorted(attrs_and_values, key=lambda attribute: attribute[1])[::-1]
        for attr_and_value in sorted_attrs_and_values:
            sorted_attrs.append(attr_and_value[0])

    def sort_maps_after_wins(self) -> list:
        attrs = list(vars(self))
        attrs_and_values = []  # will contain list of tuples containing member name and member values
        sorted_attrs = []
        for attr in attrs:
            if re.match("total_wins_map_.*", attr):
                attrs_and_values.append((attr, getattr(self, attr)))
        sorted_attrs_and_values = sorted(attrs_and_values, key=lambda attribute: attribute[1])[::-1]
        for attr_and_value in sorted_attrs_and_values:
            sorted_attrs.append(attr_and_value[0])