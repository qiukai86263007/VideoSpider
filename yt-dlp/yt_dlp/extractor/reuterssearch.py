import itertools
import re
import json
from .common import InfoExtractor
from ..utils import parse_qs
from .common import InfoExtractor
from ..utils import (
    urlencode_postdata,
    get_element_by_class,
    clean_html,
    ExtractorError,
)


class ReutersSearchBaseIE(InfoExtractor):
    _SEARCH_TYPE = 'search'
    _NETRC_MACHINE = 'reuters'
    _API_HEADERS = {
        'Referer': 'https://www.reuters.com/',
        'Origin': 'https://www.reuters.com',
    }
    def _entries(self, url, item_id, query=None, note='Downloading page %(page)s'):
        query = query or {}
        pages = [query['p']] if 'p' in query else itertools.count(1)
        for page_num in pages:
            query['p'] = str(page_num)
            webpage = self._download_webpage(
                url, item_id, query=query, note=note % {'page': page_num})
            findlist = list(set(re.findall(
                r'<a[^>]*data-testid="TitleLink"[^>]*aria-label="[^"]*includes video[^"]*"[^>]*href="([^"]*)"[^>]*>',
                webpage)))
            for url_items in findlist:
                yield self.url_result(url_items)

            if not findlist:
                return

    def _search_results(self, query, url):
        return self._entries(url, query)

    def _perform_login(self, username, password):
        login_response = self._download_json(
            'https://api-reuters-reuters-prod.cdn.arcpublishing.com/identity/public/v1/auth/login', None, note='Logging in',
            data=json.dumps({
                'userName': username,
                'password': password,
                'grantType': 'password',
                'rememberMe': 'true',
            }).encode(), headers={
                'Origin': 'https://www.reuters.com/',
                'Referer': 'https://www.reuters.com',
                'Content-Type': 'application/json',
            })
        # judge is login success
        if login_response.get('code'):
            if login_response.get('message'):
                raise ExtractorError(f'Unable to log in: {self.IE_NAME} said: {login_response["message"]}', expected=True)
            else:
                raise ExtractorError('Unable to log in')


class ReutersSearchURLIE(ReutersSearchBaseIE):
    IE_DESC = 'Reuters Video search'
    IE_NAME = 'reuters:search_url'
    _VALID_URL = r'https?://(?:www\.)?reuters\.com/site-search/\?(?:.*?[&;])?query=(?P<id>[^&#]+)'
    _TESTS = [{
        'url': 'https://www.reuters.com/site-search/?query=trump',
        'info_dict': {
            'id': 'kevin',
            'title': 'kevin is nice man',
        },
        'playlist_mincount': 45,
        'params': {
            'playlistend': 45,
        },
    }]
    _PAGE_SIZE = 100

    def _real_extract(self, url):
        qs = parse_qs(url)
        query = (qs.get('query') or qs.get('q'))[0]
        return self.playlist_result(self._entries(url, query), query, query)
