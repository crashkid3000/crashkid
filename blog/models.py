from django.db import models
from django.core.paginator import (EmptyPage, PageNotAnInteger, Paginator)
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from contentpages.blocks import (TitleAndParagraphWithImage, TitleAndParagraphBlock)
# Create your models here.


class BlogListingPage(Page):
    """List all Blog Detail Pages"""

    template = "blog/blog_listing_page.html"
    max_count = 1

    content_panels = Page.content_panels + [

    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, args, kwargs)
        all_blogs = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        paginator = Paginator(all_blogs, 10)  # 10 posts per page
        page_no = request.GET.get("page")
        try:
            blogs = paginator.page(page_no)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
        context["blogs"] = blogs
        return context



class BlogDetailPage(Page):
    """A blog page with some detailed information about a topic. Hopefully."""

    template = "blog/blog.html"

    title_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Title image",
        help_text="Image used in the title to introduce the user to the topic"
    )

    paragraphs = StreamField([
        ("title_and_text", TitleAndParagraphBlock()),
        ("title_and_text_with_image", TitleAndParagraphWithImage())
    ])

    summary = RichTextField(null=False, blank=True, help_text="A short summary to get the user into reading more", verbose_name="Blog summary")

    content_panels = Page.content_panels + [
        ImageChooserPanel("title_image"),
        StreamFieldPanel("paragraphs"),
        FieldPanel("summary"),
    ]
