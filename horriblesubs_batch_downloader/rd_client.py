import requests
import json


class RDClient:
    _base_url = "https://api.real-debrid.com/rest/1.0/{endpoint}"

    def __init__(self, api_token):
        self.api_token = api_token

    # ========================================================================
    #       URL helpers
    # ========================================================================

    def build_url(self, endpoint):
        """
        Format the base url with endpoint.
        """

        return self._base_url.format(endpoint=endpoint)

    def add_auth_header(self, headers):
        """
        Add an auth header to a headers dict.
        """

        headers["Authorization"] = "Bearer {}".format(self.api_token)

    # ========================================================================
    #       Endpoints
    # ========================================================================

    def add_magnet(self, magnet):
        """
        Add a magnet link (/torrents/addMagnet).
        """

        endpoint = "torrents/addMagnet"
        payload = {"magnet": magnet}
        headers = {}
        self.add_auth_header(headers)

        resp = requests.post(self.build_url(endpoint),
                             data=payload, headers=headers)

        return resp.json()
    
    def active_count(self):
        """
        (/torrents/activeCount)
        """

        endpoint = "torrents/activeCount"
        headers = {}
        self.add_auth_header(headers)

        resp = requests.get(self.build_url(endpoint),
                            headers=headers)

        return resp.json()
    
    def select_files(self, id):
        """
        (/torrents/selectFiles/{id})
        """

        endpoint = "torrents/selectFiles/{}".format(id)
        headers = {}
        payload = {"files": "all"}
        self.add_auth_header(headers)

        resp = requests.post(self.build_url(endpoint),
                             data=payload, headers=headers)
        
        return resp.status_code