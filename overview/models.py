from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.core.models import Page
# Create your models here.


class FH4OverviewPage(Page):
    template = "overview/overview_fh4_event.html"
    max_count = 1

    content_panels = Page.content_panels + [

    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, args, kwargs)
        all_events = FH4Track.objects.all().filter(show_in_all_tracks=True).order_by("-id")
        paginator = Paginator(all_events, 6)  # 6 Events per page
        page_no = request.GET.get("page")
        try:
            events = paginator.page(page_no)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)
        context["events"] = events

        event_id = request.GET.get("id")
        if event_id is None:
            context["url_has_id"] = False
        else:
            context["url_has_id"] = True
        return context

    class Meta:
        verbose_name = "FH4 All Events Overview"

class FH4ChampOverviewPage(Page):
    template = "overview/overview_fh4_champ.html"
    max_count = 1

    intro = RichTextField(blank=True, null=True, help_text="And intro text to give readers some context", verbose_name="Intro text")

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, args, kwargs)
        all_champs = FH4Championship.objects.all().order_by("-id")
        paginator = Paginator(all_champs, 5)  # 5 Championships per page
        page_no = request.GET.get("page")
        try:
            champs = paginator.page(page_no)
        except PageNotAnInteger:
            champs = paginator.page(1)
        except EmptyPage:
            champs = paginator.page(paginator.num_pages)
        context["champs"] = champs

        champ_id = request.GET.get("id")
        if champ_id is None:
            context["url_has_id"] = False
        else:
            context["url_has_id"] = True
        return context

    class Meta:
        verbose_name = "FH4 All Championships Overview"


class FH4TuneOverviewPage(Page):
    template = "overview/overview_fh4_tune.html"
    max_count = 1

    intro = RichTextField(blank=True, null=True, help_text="And intro text to give readers some context",
                          verbose_name="Intro text")

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, args, kwargs)
        all_tunes = FH4Tune.objects.all().order_by("-id")
        paginator = Paginator(all_tunes, 6)  # 5 Championships per page
        page_no = request.GET.get("page")
        try:
            tunes = paginator.page(page_no)
        except PageNotAnInteger:
            tunes = paginator.page(1)
        except EmptyPage:
            tunes = paginator.page(paginator.num_pages)
        context["tunes"] = tunes

        tune_id = request.GET.get("id")
        if tune_id is None:
            context["url_has_id"] = False
        else:
            context["url_has_id"] = True
        return context

    class Meta:
        verbose_name = "FH4 All Tunes Overview"


class FH4Track(models.Model):

    CAR_CLASSES = [
        ('X', 'X Klasse'),  # X class
        ('2', 'S2 Klasse'),  # S2 class
        ('1', 'S1 Klasse'),  # S1 class
        ('A', 'A Klasse'),  # A class
        ('B', 'B Klasse'),  # B class
        ('C', 'C Klasse'),  # C class
        ('D', 'D Klasse'),  # D class
        ('-', 'Unbeschränkt'),  # unrestricted
    ]

    SEASONS = [
        ("W", "Winter"),
        ("F", "Frühling"),  # F = Frühling (ger) = Spring
        ("S", "Sommer"),  # Summer
        ("H", "Herbst")  # H = Herbst (ger) = Autumn
    ]

    TIME_OF_DAYS = [
        ('Da', 'Morgengrauen'),  # Dawn
        ('Su', 'Sonnenaufgang'),  # Sunrise
        ('Mo', 'Morgen'),  # Morning
        ('No', 'Mittag'),  # Noon
        ('Af', 'Nachmittag'),  # Afternoon
        ('Se', 'Sonnenuntergang'),  # Sunset
        ('Du', 'Abend'),  # Dusk
        ('Ni', 'Nacht'),  # Night
        ('??', 'Aktuell'),  # Current
    ]

    WEATHERS = [
        ('S ', 'Heiter'),  # Sunny
        ('Sr', 'Heiter (nass)'),  # Sunny (wet)
        ('C ', 'Wolkig'),  # Cloudy
        ('Cr', 'Wolkig (nass)'),  # Cloudy (wet)
        ('O ', 'Bewölkt'),  # Overcast
        ('Lr', 'Leichter Regen'),  # light rain
        ('Ls', 'Leichter Schneefall'),  # light snow
        ('Hr', 'Starker Regen'),  # heavy rain
        ('Hs', 'Starker Schneefall'),  # heavy snow
        ('FB', 'Nebel'),  # fog
        ('Bl', 'Blizzard'),  # Blizzard
        ('??', 'Aktuell'),  # current
    ]
    track = models.ForeignKey(
        'FH4Route',
        null=True,
        blank=False,
        on_delete=models.CASCADE,  # delete this fh4 event too if the track gets deleted
        related_name="+",
        verbose_name="Track",
        help_text="The track on which this event takes place",
    )
    name = models.CharField(max_length=50, blank=False, null=False, help_text="The name of the event", verbose_name="Event name")
    car_power = models.CharField(max_length=1, blank=False, null=True, choices=CAR_CLASSES, default='-', help_text="The recommended/restricted car class for this event", verbose_name="Power limit")
    event_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="event image",
        help_text="The fancy image for an event (if available)",
    )
    description = models.CharField(max_length=300, blank=True, null=True, help_text="Some descriptive text to further inform about the track/event", verbose_name="Event/Track description")
    laps = models.IntegerField(blank=False, null=True, default=1, help_text="How many laps? Note: Use 0 for sprints", verbose_name="Lap count")
    season = models.CharField(max_length=1, blank=False, null=False, choices=SEASONS, help_text="In which season this event takes place", verbose_name="Season")
    car_class = models.CharField(max_length=250, blank=True, null=False, default="Anything Goes", help_text="Which cars are allowed for this race",  verbose_name="Car restriction")
    time_of_day = models.CharField(max_length=2, choices=TIME_OF_DAYS, default='No', blank=False, null=False, help_text="When this race takes place", verbose_name="Time of day")
    weather = models.CharField(max_length=30, blank=False, null=False, choices=WEATHERS, default='S ', help_text="What kind of weather will be present at the event")
    sharecode = models.IntegerField(blank=False, null=False, default=0, help_text="The share code for that event", verbose_name="Share code")
    show_in_all_tracks = models.BooleanField(blank=False, null=False, default=True, help_text='Show track in "FH4 Overview Page"')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "FH4 Event"

    panels = [
        FieldPanel("track"),
        FieldPanel("name"),
        ImageChooserPanel("event_image"),
        FieldPanel("description"),
        FieldRowPanel([
            FieldPanel("laps"),
            FieldPanel("car_class"),
            FieldPanel("show_in_all_tracks"),
        ]),
        FieldRowPanel([
            FieldPanel("season"),
            FieldPanel("time_of_day"),
        ]),
        FieldRowPanel([
            FieldPanel("weather"),
            FieldPanel("car_power"),
        ]),
        FieldPanel("sharecode"),
    ]


class FH4Route(models.Model):
    TYPES = [
        ('r', 'Sprint'),
        ('R', 'Rundkurs'),
        ('d', 'Rallye'),
        ('D', 'Dirt Track'),
        ('c', 'Offroad-Sprint'),
        ('C', 'Offroadkurs')
    ]

    track_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="track image",
        help_text="overview image of the track",
    )
    type = models.CharField(max_length=1, blank=False, null=False, choices=TYPES, help_text="What kind of race this is", verbose_name="Track type")
    length_per_round = models.FloatField(blank=False, null=False, help_text="The length (in km) per lap (for circuits)/per race (for sprints)", verbose_name="Lap length")
    name = models.CharField(max_length = 35, blank=False, null=False, default="DEFAULT", help_text="Name of the route", verbose_name="Route name")

    def __str__(self):
        return self.name + " (" + self.get_type_display() + ")"

    panels = [
        ImageChooserPanel("track_image"),
        FieldPanel("name"),
        FieldRowPanel([
            FieldPanel("type"),
            FieldPanel("length_per_round"),
        ]),
    ]

    class Meta:
        verbose_name = "FH4 Route"


class FH4Championship(models.Model):
    TYPES = [
        ('r', 'Sprint'),
        ('R', 'Rundkurs'),
        ('d', 'Rallye'),
        ('D', 'Dirt Track'),
        ('c', 'Offroad-Sprint'),
        ('C', 'Offroadkurs'),
        ('A', 'Asphalt'),
        ('E', 'Alle Straßenbeläge'),
        ('G', 'Schotter'),
        ('€', 'Offroad'),
        ('S', 'Straßenszene'),
    ]

    name = models.CharField(max_length=50, blank=False, null=False, help_text="The name for this championship", verbose_name="Championship name")
    championship_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Championship image",
        help_text="A pretty image that represents teh championship, instead of just some plain old text",
    )
    description = models.CharField(max_length=250, blank=True, null=False, default="", help_text="A nice little description about this championship", verbose_name="Description")
    type = models.CharField(max_length=1, blank=False, null=False, choices=TYPES, help_text="What kind of championship this is", verbose_name="Championship type")
    prize_money = models.IntegerField(blank=False, null=False, default=0, help_text="The pize money assigned to this championship", verbose_name="Prize money")
    further_prize = models.CharField(max_length=200, blank=True, null=True, help_text="An additional prize given to the winner of the championship", verbose_name="Additional prize")
    events = models.ManyToManyField(FH4Track)

    panels = [
        MultiFieldPanel([
            FieldPanel("name"),
            ImageChooserPanel("championship_image"),
            FieldPanel("type"),
            FieldPanel("description"),
        ], heading="General championship settings"),
        MultiFieldPanel([
            FieldPanel("prize_money"),
            FieldPanel("further_prize"),
        ], heading="Prize settings"),
        FieldPanel("events"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "FH4 Championship"


class FH4Tune(models.Model):
    TUNE_TYPE = [
        ('C', 'Asphalt'),
        ('R', 'Rallye'),
        ('O', 'Offroad'),
        ('d', 'Drag'),
        ('D', 'Drift'),
    ]

    TUNE_CHARACTERISTIC = [
        ('S', 'Geschwindigkeit'),
        ('A', 'Beschleunigung'),
        ('a', 'Aerodynamischer Grip'),
        ('G', 'Grip'),
        ('B', 'Ausgeglichen'),
    ]

    DRIVETRAIN = [
        ('F', 'FF'),
        ('h', 'FR'),
        ('H', 'RR'),
        ('M', 'MR'),
        ('A', 'AWD'),

    ]

    INTAKE = [
        ('/', 'Saugmotor'),
        ('S', 'Kompressor'),
        ('C', 'Zentrifugal-Kompressor'),
        ('t', 'Einzelner Turbo'),
        ('T', 'Zwei Turbos'),
    ]

    name = models.CharField(max_length=50, blank=False, null=False, default="", verbose_name="Tune name", help_text="The name of this setup")
    tune_type = models.CharField(max_length=1, blank=False, null=False, choices=TUNE_TYPE, default='A', verbose_name="Tune type", help_text="For what kind of racing this tune was made for")
    tune_characteristic = models.CharField(max_length=1, blank=False, null=False, choices=TUNE_CHARACTERISTIC, default='B', verbose_name="Tune focus", help_text="What's the focus of this setup? Is it grip, or maybe speed?")
    livery_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Livery name", help_text="The name of the livery that this tune should come with (if available)")
    preview_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Car preview",
        help_text="An Image of the car that this livery comes with",
    )
    car = models.CharField(max_length=150, blank=False, null=True, verbose_name="Car name", help_text="The car this tune was made for")
    pi = models.IntegerField(blank=False, null=False, verbose_name="Performance Index", help_text="The performance index of this tune")

    speed = models.FloatField(blank=False, null=True, verbose_name="Max speed (kph)", help_text="The maximum speed this car can reach")
    accel100 = models.FloatField(blank=False, null=True, verbose_name="0-100kmh Acceleration (s)", help_text="The time it takes for this car to accelerate from 0 to 100")
    grip100 = models.FloatField(blank=False, null=True, verbose_name="Grip at 100 km/h", help_text="The grip that the car develops at 100 km/h")
    accel160 = models.FloatField(blank=False, null=True, verbose_name="0-160kmh Acceleration (s)",
                                 help_text="The time it takes for this car to accelerate from 0 to 160")
    grip160 = models.FloatField(blank=False, null=True, verbose_name="Grip at 160 km/h",
                                help_text="The grip that the car develops at 160 km/h")
    power = models.IntegerField(blank=False, null=True, verbose_name="Power (kW)", help_text="The maximum power output of this car")
    torque = models.IntegerField(blank=False, null=True, verbose_name="Torque (Nm)", help_text="The maximum torque output of this car")
    intake = models.CharField(max_length=1, blank=False, null=True, choices=INTAKE, verbose_name="Intake type", help_text="If/How extra air is forced into the engine")
    weight = models.IntegerField(blank=False, null=True, verbose_name="Weight (kg)", help_text="How much this car weighs")
    weight_distrib = models.IntegerField(blank=True, null=True, verbose_name="Weight distribution (%)", help_text="How much weight lies on the front axle")
    drivetrain = models.CharField(max_length=1, blank=False, null=True, verbose_name="Drivetrain", choices=DRIVETRAIN,
                                  help_text="Where the engine lies and what wheels are driven by it")

    rating_speed = models.IntegerField(blank=False, null=False, default=0.0, verbose_name="Speed rating", help_text="The Forza-internal speed rating")
    rating_handling = models.IntegerField(blank=False, null=False, default=0.0, verbose_name="Handling rating", help_text="The Forza-internal handling rating")
    rating_accel = models.IntegerField(blank=False, null=False, default=0.0, verbose_name="Acceleration handling", help_text="The Forza-internal accelearation rating")
    rating_start = models.IntegerField(blank=False, null=False, default=0.0, verbose_name="Start rating", help_text="The Forza-internal start rating")
    rating_brakes = models.IntegerField(blank=False, null=False, default=0.0, verbose_name="Brakes rating", help_text="The Forza-internal brakes rating")

    panels = [
        MultiFieldPanel([
            FieldPanel("name"),
            FieldPanel("car"),
            FieldPanel("pi"),
            FieldRowPanel([
                FieldPanel("tune_type"),
                FieldPanel("tune_characteristic"),
            ]),
            FieldPanel("livery_name"),
            ImageChooserPanel("preview_image"),
        ], heading="General Tune Settings"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel("rating_speed"),
                FieldPanel("rating_handling"),
            ]),
            FieldRowPanel([
                FieldPanel("rating_accel"),
                FieldPanel("rating_start"),
            ]),
            FieldPanel("rating_brakes"),
        ], heading="Simple Tune Statistics. Note: Entered value must be multiplied by 10"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel("speed"),
                FieldPanel("drivetrain"),
            ]),
            FieldRowPanel([
                FieldPanel("accel100"),
                FieldPanel("grip100"),
            ]),
            FieldRowPanel([
                FieldPanel("accel160"),
                FieldPanel("grip160"),
            ]),
            FieldRowPanel([
                FieldPanel("power"),
                FieldPanel("torque"),
                FieldPanel("intake"),
            ]),
            FieldRowPanel([
                FieldPanel("weight"),
                FieldPanel("weight_distrib"),
            ]),
        ], heading="Detailed Tune Statsistics")
    ]

    def __str__(self):
        return self.name + "(" + self.get_tune_type_display() + ")"

    class Meta:
        verbose_name = "Forza Setup"
