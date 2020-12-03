from os.path import join

# from ldcoolp.curation.api.figshare import FigshareInstituteAdmin

from .commons import issue_request


class Figshare:
    """
    Purpose:
      A Python interface to work with Figshare statistics endpoint

    """

    def __init__(self, api_token='', basic_token='', institution=False, institute=''):

        # For stats API
        self.stats_baseurl = 'https://stats.figshare.com'
        self.institution = institution
        if institute:
            self.institute = institute
            self.stats_baseurl_institute = join(self.stats_baseurl, self.institute)

        # Base64 token
        self.basic_headers = {'Content-Type': 'application/json'}
        self.basic_token = basic_token
        if self.basic_token:
            self.basic_headers['Authorization'] = f'Basic {self.basic_token}'

        # API token
        self.api_headers = {'Content-Type': 'application/json'}
        self.api_token = api_token
        if self.api_token:
            self.api_headers['Authorization'] = f'token {self.api_token}'

    def stats_endpoint(self, link, institution=False):
        if institution:
            return join(self.stats_baseurl_institute, link)
        else:
            return join(self.stats_baseurl, link)

    def get_totals(self, item_id, item='article', institution=False):
        """
        Retrieve totals of views, downloads, and share for an "item"
        Item can be 'article', 'author', 'collection', 'group' or 'project'
        Note: This does not require authenticating credentials for institution accounts

        See: https://docs.figshare.com/#stats_totals
        """

        if item not in ['article', 'author', 'collection', 'group', 'project']:
            raise ValueError("Incorrect item type")

        total_dict = {}
        for counter in ['views', 'downloads', 'shares']:
            # Using non-institution one since that seems to give correct stats
            url = self.stats_endpoint(join('total', counter, item, str(item_id)),
                                      institution=institution)
            result = issue_request('GET', url, headers=self.basic_headers)
            total_dict[counter] = result['totals']
        return total_dict

    def get_user_totals(self, author_id):
        """
        Retrieve an author's total using get_totals()

        :param author_id: This is not the same as the institution_user_id for institutional accounts
        :return: total_dict: dict containing total views, downloads, and shares
        Note: This does not require authenticating credentials for institution accounts
        """
        total_dict = self.get_totals(author_id, item='author',
                                     institution=False)
        return total_dict

    def get_timeline(self, item_id, item='article', granularity='day',
                     institution=False):
        total_dict = {}
        for counter in ['views', 'downloads', 'shares']:
            # Using non-institution one since that seems to give correct stats
            urls = ['timeline', granularity, counter, item, str(item_id)]
            url = self.stats_endpoint(join(*urls), institution=institution)
            result = issue_request('GET', url, headers=self.basic_headers)
            total_dict[counter] = result['timeline']
        return total_dict
