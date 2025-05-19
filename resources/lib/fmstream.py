import time
import requests
import xbmc


def gen_api_key():
    keya = "0xb554"
    keyb = "0x0f99"
    key = int(keya, 16) * int(time.time()) + int(keyb, 16)
    api_key = format(key, "x")
    return api_key


class FMStreamAPI:
    def __init__(self, hq):
        self.hq = int(hq)

        self.api = "https://fmstream.org/index.php"

    def make_request(self, url, params=None, headers=None):
        if not headers:
            headers = {"accept": "application/json", "user-agent": "xbox-fmstream"}

        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code != 200:
                xbmc.log("FMStream.org API returned error:", response.status_code)
                return None
            return response.json()
        except Exception:
            xbmc.log("FMStream.org API returned error", level=xbmc.LOGERROR)
        return None

    def get_countries(self):
        return self.make_request("https://fmstream.org/itu.php")

    def get_languages(self):
        return self.make_request("https://fmstream.org/la.php")

    def fetch(self, c=None, l=None, n=None, o=None, s=None, style=None):
        """
        Input:
            Check https://fmstream.org/api.htm to learn what each letter represents
        Output:
            None: if error was encountered
            Dictionary: that represents response from FMStream API
        """

        params = {"key": gen_api_key()}
        params["hq"] = str(self.hq)

        if c:
            params["c"] = str(c)
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

        return self.make_request(self.api, params)
