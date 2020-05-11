import urllib.request as request
from http.client import HTTPResponse
import json
import re
import configparser
import os
from urllib.error import HTTPError
import crashkid.settings.base as settings
import crashkid.settings.local as local


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


def retrieve_xboxlive_stats_crashkid(gameid):
    """Asks an unofficial Xbox API about the stats of crashkid3000s achievements/stats for a specified Xbox Live game"""
    # because the official API sucks
    cfg = configparser.ConfigParser()
    cfg.read(local.LOCAL_API_KEYS_FILE)
    if len(cfg.items()) > 0:  # if we could read the dict specified at that address, and there was actually some data in it (see behavior of ConfigParser.read() for more info ony why this is necessary)
        auth_key = cfg["xbapi"]["auth_key"]
        xuid = cfg["xbapi"]["xuid"]
        print("auth_key: " + auth_key)
        req = request.Request('https://xboxapi.com/v2/' + str(xuid) + '/game-stats/' + str(gameid))
        req.add_header('X-Auth', auth_key)
        try:
            resp = request.urlopen(req)
            retVal = json.loads(resp.read())
            retVal['req_success'] = True
            return retVal
        except HTTPError as err:
            print("HTTP Error! " + str(err))
            print("---> returning error dict")
            return {'req_success': False}
    else:
        print("Could not read API keys file, or it is empty! Returning and empty dict...")
        return {}


def improve_dict_access_for_fh_stats(stats):
    """Improves the atrocious handling of the response comiing from crashkid's Forza Horizon 4 player stats"""
    retVal = {}
    counter = 0
    for counter in range(len(stats['groups'][0]['statlistscollection'][0]['stats'])):
        retVal[counter] = {}
        retVal[counter]['name'] = stats['groups'][0]['statlistscollection'][0]['stats'][counter]['name']
        try:
            retVal[counter]['value'] = stats['groups'][0]['statlistscollection'][0]['stats'][counter]['value']
        except KeyError:
            retVal[counter]['value'] = None
        retVal[counter]['display'] = stats['groups'][0]['statlistscollection'][0]['stats'][counter]['groupproperties']['DisplayName']
    retVal_LenAfterFirstLoop = len(retVal)
    for counter in range(len(stats['statlistscollection'][0]['stats'])):
        retVal[counter + retVal_LenAfterFirstLoop] = {}
        retVal[counter + retVal_LenAfterFirstLoop]['name'] = stats['statlistscollection'][0]['stats'][counter]['name']
        try:
            retVal[counter + retVal_LenAfterFirstLoop]['value'] = stats['statlistscollection'][0]['stats'][counter]['value']
        except KeyError:
            retVal[counter + retVal_LenAfterFirstLoop]['value'] = None
        name_wordlist = re.findall('[A-Z][^A-Z]*', stats['statlistscollection'][0]['stats'][counter]['name'])  # finds all words in CamelCase and puts them in a seperate list entry
        retVal[counter + retVal_LenAfterFirstLoop]['display'] = ' '.join(name_wordlist)

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
    cfg.read(local.LOCAL_NUMBER_FORMATS_FILE)
    thousands = cfg[code]['thousands'].replace('"', '')
    decimal = cfg[code]['decimal'].replace('"', '')
    num_parts = str(num).split('.')  # split at the '.' character, as that's the decimal separator hard-coded into python for float
    reverse_first_part = num_parts[0][::-1]
    for i in range(len(reverse_first_part)):
        nustring += reverse_first_part[i]
        if reverse_first_part[i].isdigit():
            zero_counter += 1
        if zero_counter == 3 and i + 1 < len(reverse_first_part):
            zero_counter = 0
            nustring += thousands
    retVal = nustring[::-1]
    if len(num_parts) > 1:
        retVal += decimal + num_parts[1]
    return retVal


