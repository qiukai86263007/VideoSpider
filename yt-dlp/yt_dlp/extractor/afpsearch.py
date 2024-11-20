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


class AfpIE(InfoExtractor):
    IE_NAME = 'afpnews'
    IE_DESC = 'afpnews.com'
    _VALID_URL = r'https://www\.afp\.com/en/(?!search/).+/(?P<id>[^/]+)'
    _NETRC_MACHINE = 'afpnews'
    _EMBED_REGEX = [r'<iframe[^>]+src=[\'"](?P<url>https?://[^\'"]+)[\'"]']
    _TESTS = [{
        'url': 'https://www.afp.com/en/inside-afp/10-most-popular-videos-afps-youtube-channel-week-august-29-4-september-2022',
        'info_dict': {
            'id': 'kevin',
            'title': 'kevin is nice man',
        },
        'playlist_mincount': 45,
        'params': {
            'playlistend': 45,
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage, urlh = self._download_webpage_handle(url, video_id)
        if not self._match_valid_url(urlh.url):
            return self.url_result(urlh.url)
        iframe_src = self._search_regex(
            r'<iframe[^>]+src=[\'"](?P<url>https?://www\.youtube\.com[^\'"]+)[\'"]',
            webpage, 'iframe src', group='url')

        formats = []
        if iframe_src:
            formats.extend(self._extract_m3u8_formats(
                iframe_src, video_id, 'mp4', entry_protocol='m3u8_native',
                m3u8_id='hls', fatal=False))
        return {
            'id': video_id,
            'formats': formats,
            'title': self._generic_title('', webpage, default='video'),
            'description': self._og_search_description(webpage, default=None),
            'thumbnail': self._og_search_thumbnail(webpage, default=None),
        }


class AfpSearchBaseIE(InfoExtractor):
    _SEARCH_TYPE = 'search'
    _NETRC_MACHINE = 'afp'
    _API_HEADERS = {
        'Referer': 'https://www.afp.com/',
        'Origin': 'https://www.afp.com',
    }

    def _entries(self, url, item_id, query=None, note='Downloading page %(page)s'):
        query = query or {}
        pages = [query['page']] if 'page' in query else itertools.count(0)
        for page_num in pages:
            query['page'] = str(page_num)
            webpage = self._download_webpage(
                url, item_id, query=query, note=note % {'page': page_num})
            findlist = list(set(re.findall(
                r'<div[^>]*class="[^"]*search_result_item[^"]*"[^>]*>.*?<a[^>]*href="(https://www\.afp\.com/en/[^"]*)"[^>]*>.*?</a>',
                webpage, re.DOTALL)))
            for url_items in findlist:
                yield self.url_result(url_items)

            if not findlist:
                return

    def _search_results(self, query, url):
        return self._entries(url, query)

    # def _perform_login(self, username, password):
    #     login_response = self._download_json(
    #         'https://api-reuters-reuters-prod.cdn.arcpublishing.com/identity/public/v1/auth/login', None, note='Logging in',
    #         data=json.dumps({
    #             'userName': username,
    #             'password': password,
    #             'grantType': 'password',
    #             'rememberMe': 'true',
    #         }).encode(), headers={
    #             'Origin': 'https://www.reuters.com/',
    #             'Referer': 'https://www.reuters.com',
    #             'Content-Type': 'application/json',
    #         })
    #     # judge is login success
    #     if login_response.get('code'):
    #         if login_response.get('message'):
    #             raise ExtractorError(f'Unable to log in: {self.IE_NAME} said: {login_response["message"]}', expected=True)
    #         else:
    #             raise ExtractorError('Unable to log in')


class AfpSearchURLIE(AfpSearchBaseIE):
    IE_DESC = 'Afp Video search'
    IE_NAME = 'afp:search_url'
    _VALID_URL = r'https?://(?:www\.)?afp\.com/en/search/results/(?P<id>[^&#]+)'
    _TESTS = [{
        'url': 'https://www.afp.com/en/search/results/trump',
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
        query = self._match_id(url)
        return self.playlist_result(self._entries(url, query), query, query, query)
