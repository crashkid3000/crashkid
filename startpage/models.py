from django.db import models

# Create your models here.
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from contentpages.blocks import TitleAndParagraphBlock, TitleAndParagraphWithImage


class StartPage(Page):
    template = "crashpage/homepage.html"
    max_count = 1

    banner_title = models.CharField(max_length=100, null=False, blank=False, help_text="The big text on the jumbotron-style banner", verbose_name="Banner Title")
    banner_text = RichTextField(blank=False, default="",
                                     features=["bold", "italic", "hr", "h3", "h4", "h5", "blockquote", "link", ],
                                     verbose_name="Banner Text", help_text="The main text present on the banner")
    banner_bg_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        help_text="The background image behind the jumbotron banner",
        verbose_name="background image",
    )
    banner_is_bg_dark = models.BooleanField(blank=False, null=False, default=False, verbose_name="Background dark?", help_text="Whether the background (image/solid color) is dark")
    banner_text_sub = RichTextField(blank=True,
                                    features=["bold", "italic", "hr", "h3", "h4", "h5", "blockquote", "link", ],
                                    verbose_name="Seondary Banner Text", help_text="A possible secondary text")
    paragraphs = StreamField([
        ("title_and_text", TitleAndParagraphBlock()),
        ("title_and_text_with_image", TitleAndParagraphWithImage()),
    ], blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("banner_title"),
            FieldPanel("banner_text"),
            FieldPanel("banner_text_sub"),
            ImageChooserPanel("banner_bg_image"),
            FieldPanel("banner_is_bg_dark"),
        ], heading="Banner Settings"),
        StreamFieldPanel("paragraphs"),
    ]

    search_fields = [
        index.SearchField('banner_title'),
        index.SearchField('banner_text'),
        index.SearchField('paragraphs'),
    ]

    class Meta:
        verbose_name = "custom Startpage"

