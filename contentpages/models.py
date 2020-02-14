from django.db import models

# Create your models here.
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel

from contentpages.blocks import (TitleAndParagraphWithImage, TitleAndParagraphBlock)


class RichTextPage(Page):
    """A simple page containing a title and a rich text field"""
    template = "contentpages/rich_text_page.html"

    alt_title = models.CharField(max_length=200, blank=True, null=True, verbose_name="Optional alternate title", help_text="An optional alternative title differing from teh given one")
    subheading = models.CharField(max_length=200, blank=True, null=True, verbose_name="Subheading", help_text="A subheading that further expands on either title")
    use_both_titles = models.BooleanField(blank=False, null=False, default=False, verbose_name="Use both titles",
                                          help_text="Whether both titles shall be used if both are present. If both titles are set adn this is not checked, only the secondary title will be seen.")

    content = RichTextField(blank=False, null=True, verbose_name="Page content", help_text="The actual textual content of this page")


    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("alt_title"),
            FieldPanel("use_both_titles"),
            FieldPanel("subheading"),
        ], heading="title options"),
        FieldPanel("content")
    ]


class ExtendableContentPage(Page):
    """A page supporting more and more content using StreamFields"""
    template = "contentpages/streamfield_page.html"

    alt_title = models.CharField(max_length=200, blank=True, null=True, verbose_name="Optional alternate title",
                                 help_text="An optional alternative title differing from teh given one")
    subheading = models.CharField(max_length=200, blank=True, null=True, verbose_name="Subheading",
                                  help_text="A subheading that further expands on either title")
    use_both_titles = models.BooleanField(blank=False, null=False, default=False, verbose_name="Use both titles",
                                          help_text="Whether both titles shall be used if both are present. If both titles are set adn this is not checked, only the secondary title will be seen.")

    contents = StreamField([
        ("title_and_paragraph", TitleAndParagraphBlock()),
        ("title_and_paragraph_with_imnage", TitleAndParagraphWithImage()),
    ], blank=True, verbose_name="Content of teh page")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("alt_title"),
            FieldPanel("use_both_titles"),
            FieldPanel("subheading"),
        ], heading="title options"),
        StreamFieldPanel("contents")
    ]




