from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel

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

    tunings_downloaded = models.IntegerField(blank=True, null=False, verbose_name="Tunings released",
                                           help_text="How many tunings were downloaded by others.")
    designs_downloaded = models.IntegerField(blank=True, null=False, verbose_name="Designs released",
                                           help_text="How many designs were downloaded by others.")
    events_played = models.IntegerField(blank=True, null=False, verbose_name="Events released",
                                          help_text="How many events were played by others.")

    tunings_favd = models.IntegerField(blank=True, null=False, verbose_name="Tunings released",
                                           help_text="How many tunings were favored by others.")
    designs_favd = models.IntegerField(blank=True, null=False, verbose_name="Designs released",
                                           help_text="How many designs were favored by others.")
    events_favd = models.IntegerField(blank=True, null=False, verbose_name="Events released",
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
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, args, kwargs)
        context["curr_page_id"] = self.id
        return context

    class Meta:
        verbose_name = "Forza Stats Page"