import urllib.request as request
from http.client import HTTPResponse
import json
import configparser
from urllib.error import HTTPError
import crashkid.settings.base as settings


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
    """Converts the 'private' status of a GitHub repo request to an internally used mapping"""
    if status is True:
        return 'privat'
    else:
        return 'public'


def format_number(num, lang=settings.LANGUAGE_CODE):
    """Converts a number to a sting, including decimal separators. Accepted language codes: de-*, en-*, fr-* (*=wildcard)"""
    zero_counter = 0
    nustring = ""  # new string
    code = lang.split("-")[0]  # the language code we will use to search in teh number config INI file
    cfg = configparser.ConfigParser()
    cfg.read('numseps.ini')
    thousands = cfg[code]['thousands'].replace('"', '')
    decimal = cfg[code]['decimal'].replace('"', '')
    num_parts = str(num).split('.')  # split at the '.' character, as that's the decimal separator hard-coded into python for float
    reverse_first_part = num_parts[0][::-1]
    for i in range(len(reverse_first_part)):
        nustring += reverse_first_part[i]
        if reverse_first_part[i] == '0':
            zero_counter += 1
        if zero_counter == 3:
            zero_counter = 0
            nustring += thousands
    retVal = nustring[::-1]
    if len(num_parts) > 1:
        retVal += decimal + num_parts[1]
    return retVal


