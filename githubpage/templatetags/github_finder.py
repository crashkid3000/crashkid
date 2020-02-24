from django import template
import util
register = template.Library()


@register.simple_tag(takes_context=True)
def reload_github_repo(user="", repo=""):
    """Refreshes/created data for a GitHubRepoPage using the GitHub API."""
    github_data = util.retrieve_github_repo(user, repo)
