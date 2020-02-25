from django import template
from githubpage.models import GitHubRepo, GitHubRepoPage
from datetime import datetime, timezone
import util
register = template.Library()


@register.simple_tag(takes_context=True)
def reload_github_repo(context, user="", repo=""):
    """Refreshes/created data for a GitHubRepoPage using the GitHub API."""

    fetch_new_data = False  # if we need to fetch new data

    _repos = GitHubRepo.objects.filter(owner_name__iexact=user, name__iexact=repo)
    if _repos.count() > 0:
        old_repo = _repos[0]
        if (old_repo.object_last_updated - datetime.utcnow(timezone.utc)).days >= 1:  # if at least 1 day passed since last update
            fetch_new_data = True  # fetch new data, because the one we have is outdated
        print('    repo last updated on: ' + str(old_repo.object_last_updated))
    else:  # if there is no repo matching the given owner and repo name
        fetch_new_data = True  # ...we definitely ned to fetch teh data from the GitHub API
        old_repo = None

    if fetch_new_data:
        ghdata = util.retrieve_github_repo(user, repo)
        if ghdata['status'] == '200 OK':
            repo_status = util.convert_github_private_status(ghdata['private'])
            if old_repo is None:
                new_github_data = GitHubRepo(
                    name=ghdata['name'],
                    owner_name=ghdata['owner']['login'],
                    owner_id=ghdata['owner']['id'],
                    access_status=repo_status,
                    description=ghdata['description'],
                    created_on=ghdata['created_at'],
                    last_updated=ghdata['updated_at'],
                    size=ghdata['size'],
                    language=ghdata['language'],
                    issues=ghdata['open_issues'],
                    forks=ghdata['forks_count'],
                    stargazers=ghdata['stargazers_count'],
                    subscribers=ghdata['subscribers_count'],
                    object_last_updated=datetime.now(),
                    repo_url=ghdata['html_url'],
                )
            else:
                new_github_data = GitHubRepo(
                    id=old_repo.id,
                    name=ghdata['name'],
                    owner_name=ghdata['owner']['login'],
                    owner_id=ghdata['owner']['id'],
                    access_status=repo_status,
                    description=ghdata['description'],
                    created_on=ghdata['created_at'],
                    last_updated=ghdata['updated_at'],
                    size=ghdata['size'],
                    language=ghdata['language'],
                    issues=ghdata['open_issues'],
                    forks=ghdata['forks_count'],
                    stargazers=ghdata['stargazers_count'],
                    subscribers=ghdata['subscribers_count'],
                    object_last_updated=datetime.now(),
                    repo_url=ghdata['html_url'],
                    )
            new_github_data.save()
            curr_page = GitHubRepoPage.objects.filter(id=context["curr_page_id"])[0]
            curr_page.repo = new_github_data
            curr_page.save()
    return ''  # return an empty string, because we cannot return nothing
