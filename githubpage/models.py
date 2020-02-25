from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, FieldRowPanel

from contentpages.models import ExtendableContentPage
# Create your models here.
from wagtail.core.models import Page


class GitHubRepo(models.Model):
    """A GitHub repository"""
    PRIVATE_STATUS = [
        ('privat', '🔒'),  # "locked lock" emoji
        ('public', '🔓'),  # "unlocked lock" emoji
    ]

    name = models.CharField(max_length=100, blank=False, null=True, verbose_name='Name', help_text='The name of the repository')
    owner_name = models.CharField(max_length=100, blank=False, null=True, verbose_name="Owner", help_text='The name of the owner of this repository')
    owner_id = models.IntegerField(blank=False, null=False, default=-1, verbose_name="Owner ID", help_text='The ID of the repository owner')
    access_status = models.CharField(max_length=6, null=True, blank=False, choices=PRIVATE_STATUS, verbose_name='Access status')
    description = models.CharField(max_length=500, blank=True, null=True, verbose_name="Description", help_text='The description of the repo. NOT the readme file!')
    created_on = models.DateTimeField(blank=True, null=True, verbose_name="Created on", help_text="When this repo was created")
    last_updated = models.DateTimeField(blank=True, null=True, verbose_name="Last updated on", help_text="When the repo recieved it's last update")
    size = models.IntegerField(blank=True, null=True, verbose_name="Size", help_text="Size of the repo in kiB. Divide by 1024 to get the size displayed in github.com/settings/repositories.")
    language = models.CharField(max_length=50, blank=False, null=True, verbose_name='Language', help_text='The programming language used in this repo')
    issues = models.IntegerField(blank=False, null=True, verbose_name="Open issues", help_text="# of open issues for this repo")
    forks = models.IntegerField(blank=False, null=True, verbose_name="Forks", help_text="# of forks for this repo")
    stargazers = models.IntegerField(blank=False, null=True, verbose_name="Stargazers", help_text="# of stargazers")
    subscribers = models.IntegerField(blank=False, null=True, verbose_name="Subscribers", help_text="# of subscribers")
    object_last_updated = models.DateTimeField(auto_now_add=True, blank=False, null=False, verbose_name="last update of object", help_text="When this object was last updated")
    repo_url = models.URLField(max_length=200, blank=False, null=True, verbose_name="Link to the repo", help_text="A link to the repo")

    panels = [
        FieldPanel("name"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel("owner_name"),
                FieldPanel("owner_id"),
            ]),
        ], heading="Owner settings"),
        FieldPanel("repo_url"),
        FieldPanel("description"),
        FieldPanel("access_status"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel("created_on"),
                FieldPanel("last_updated"),
            ]),
        ], heading="Date stuff"),
        FieldPanel("language"),
        MultiFieldPanel([
            FieldPanel("size"),
            FieldRowPanel([
                FieldPanel("issues"),
                FieldPanel("forks"),
            ]),
            FieldRowPanel([
                FieldPanel("stargazers"),
                FieldPanel("subscribers"),
            ])
        ], heading="Numbers and all"),
        FieldPanel("object_last_updated")
    ]


class GitHubRepoPage(ExtendableContentPage):
    """A page describing a GitHub repository. Extends ExtendableContentPage for code simplicity."""

    template = "githubpage/githubpage.html"

    repo = models.OneToOneField(  # will be lazily initialized when the page is loaded, using a template tag
        GitHubRepo,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    # Basic data about the repository, which we will use to aks the GitHub API if it knows more about said repository
    repo_owner = models.CharField(max_length=100, blank=False, null=True, verbose_name="Owner", help_text='The name of the owner of this repository')
    repo_name = models.CharField(max_length=100, blank=False, null=True, verbose_name='Name', help_text='The name of the repository')

    content_panels = ExtendableContentPage.content_panels + [
        MultiFieldPanel([
            FieldPanel("repo_owner"),
            FieldPanel("repo_name"),
        ], heading="Basic GitHub Repo information"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, args, kwargs)
        context["curr_page_id"] = self.id
        return context

    class Meta:
        verbose_name = "GitHub Repo Page"

