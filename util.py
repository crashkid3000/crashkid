import urllib.request as request
from http.client import HTTPResponse
import json
from urllib.error import HTTPError


def get_GET_options(url=""):
    """Returns a dict containing all GET options of a given url."""
    GET_options = dict()
    if url.count('?') > 0:  # if there is a querystring to begin with
        query_string = url.split('?')[1]
        if query_string is not "":
            key_value_pairs = query_string.split('&')
            for kvp in key_value_pairs:
                GET_options[kvp.split('=')[0]] = kvp.split('=')[1]
    return GET_options

def retrieve_github_repo(user, repo):
    """ Asks GitHub about the state of a publicaly-available repository.
    Returns the HTTP status code and the response body as a dict (with nested keys, if necessary).
    If the repo cannot be accessed (authorization error/service unavailable/typo/...), the dict will be left empty, except for th HTTP status code.
    The HTTP status code can be accessed via the 'status' key."""
    req = request.Request('https://api.github.com/repos/' + user + '/' + repo, method='GET')
    retVal = {}
    try:
        resp = request.urlopen(req)
        retVal = json.loads(resp.read())
        retVal['status'] = resp.getheader('status')
    except HTTPError as err:
        retVal['status'] = str(err.code) + " " + err.reason
    return retVal

def convert_github_private_status(status):
    if status:
        return 'public'
    else:
        return 'privat'


