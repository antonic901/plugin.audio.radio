import requests
from fmstream_key import gen_api_key

HEADERS = {'accept': 'application/json', 'user-agent': 'xbox-fmstream'}

class FmStreamApi():
    def __init__(self, plugin):
        self.plugin = plugin
        self.API = plugin.get_setting('api', unicode)
        self.hq = int(plugin.get_setting('sort-streams', bool))

    def make_request(self, URL, HEADERS, PARAMS):
        response = requests.get(URL, headers=HEADERS, params=PARAMS)
        if response.status_code != 200:
            self.plugin.notify('FMStream API returned: {}'.format(response.status_code), title="FMStream API error")
            return None
        return response.json()

    def getCountries(self):
        return self.make_request('http://fmstream.org/itu.php', HEADERS, {})

    def getLanguages(self):
        return self.make_request('http://fmstream.org/la.php', HEADERS, {})

    """
    Input:
        Check http://fmstream.org/api.htm to learn what each letter represents
    Output:
        None: if error was encountered
        Dictionary: that represents response from FMStream API
    """
    def fetch(self, c=None, l=None, n=None, o=None, s=None, style=None):
        PARAMS = {'key': gen_api_key()}
        if c:
            PARAMS['c'] = str(c)
        PARAMS['hq'] = str(self.hq)
        if l:
            PARAMS['l'] = str(l)
        if n:
            PARAMS['n'] = str(n)
        if o:
            PARAMS['o'] = str(o)
        if s:
            if self.plugin.get_setting('search-format', bool):
                s = s.replace(" ", "").lower()
            PARAMS['s'] = str(s)
        if style:
            PARAMS['style'] = str(style)
        return self.make_request(self.API, HEADERS, PARAMS)