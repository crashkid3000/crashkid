
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
