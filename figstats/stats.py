from os.path import join

# from ldcoolp.curation.api.figshare import FigshareInstituteAdmin

from .commons import issue_request


class Figshare:
    """
    Purpose:
      A Python interface to work with Figshare statistics endpoint

    """

    def __init__(self, token='', institution=False, institute=''):

        self.baseurl = 'https://stats.figshare.com'
        self.institution = institution
        if institute:
            self.institute = institute
            self.baseurl_institute = join(self.baseurl, self.institute)
        self.token = token
        self.headers = {'Content-Type': 'application/json'}
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'

    def endpoint(self, link, institution=False):
        if institution:
            return join(self.baseurl_institute, link)
        else:
            return join(self.baseurl, link)

    def get_totals(self, item_id, item='article', institution=False):
        total_dict = {}
        for counter in ['views', 'downloads', 'shares']:
            # Using non-institution one since that seems to give correct stats
            url = self.endpoint(join('total', counter, item, str(item_id)),
                                institution=institution)
            print(url)
            result = issue_request('GET', url, headers=self.headers)
            total_dict[counter] = result['totals']
        return total_dict
