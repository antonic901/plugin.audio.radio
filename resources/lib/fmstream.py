import time
import requests
import xbmc

HEADERS = {"accept": "application/json", "user-agent": "xbox-fmstream"}


def gen_api_key():
    keya = "0xb554"
    keyb = "0x0f99"
    key = int(keya, 16) * int(time.time()) + int(keyb, 16)
    api_key = format(key, "x")
    return api_key


class FmStreamApi:
    def __init__(self, hq):
        self.hq = int(hq)

        self.api = "http://fmstream.org/api"

    def make_request(self, url, headers, params):
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                return None
            return response.json()
        except Exception:
            xbmc.log("FMStream.org API returned error", level=xbmc.LOGERROR)
        return None

    def getCountries(self):
        return self.make_request("http://fmstream.org/itu.php", HEADERS, {})

    def getLanguages(self):
        return self.make_request("http://fmstream.org/la.php", HEADERS, {})

    def fetch(self, c=None, l=None, n=None, o=None, s=None, style=None):
        """
        Input:
            Check http://fmstream.org/api.htm to learn what each letter represents
        Output:
            None: if error was encountered
            Dictionary: that represents response from FMStream API
        """

        params = {"key": gen_api_key()}
        if c:
            params["c"] = str(c)
        params["hq"] = str(self.hq)
        if l:
            params["l"] = str(l)
        if n:
            params["n"] = str(n)
        if o:
            params["o"] = str(o)
        if s:
            params["s"] = str(s)
        if style:
            params["style"] = str(style)

        return self.make_request(self.api, headers=HEADERS, params=params)
