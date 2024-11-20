import itertools
import re
from .common import InfoExtractor
from ..utils import parse_qs


class ApnewsIE(InfoExtractor):
    IE_NAME = 'apnews'
    IE_DESC = 'apnews.com'
    _VALID_URL = r'https://apnews\.com/video/(?P<id>[^/]+)'
    _NETRC_MACHINE = 'apnews'

    _TESTS = [{
        'url': 'https://apnews.com/video/judge-delays-ruling-in-trumps-hush-money-case-0000019322bdd461ad9f7efd37520000',
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
        video_url = self._html_search_meta('og:video', webpage, 'og:video')
        formats = []
        if video_url:
            formats.extend(self._extract_m3u8_formats(
                video_url, video_id, 'mp4', entry_protocol='m3u8_native',
                m3u8_id='hls', fatal=False))
        return {
            'id': video_id,
            'formats': formats,
            'title': self._generic_title('', webpage, default='video'),
            'description': self._og_search_description(webpage, default=None),
            'thumbnail': self._og_search_thumbnail(webpage, default=None),
        }


class ApnewsSearchBaseIE(InfoExtractor):
    _SEARCH_TYPE = 'search'

    def _entries(self, url, item_id, query=None, note='Downloading page %(page)s'):
        query = query or {}
        pages = [query['p']] if 'p' in query else itertools.count(1)
        for page_num in pages:
            query['p'] = str(page_num)
            webpage = self._download_webpage(
                url, item_id, query=query, note=note % {'page': page_num})
            findlist = list(set(re.findall(r'https://apnews\.com/video/[^"]+', webpage)))
            for url_items in findlist:
                yield self.url_result(url_items)

            if not findlist:
                return

    def _search_results(self, query, url):
        return self._entries(url, query)


class ApnewsSearchURLIE(ApnewsSearchBaseIE):
    IE_DESC = 'Apnews Video search'
    IE_NAME = 'apnews:search_url'
    _VALID_URL = r'https?://(?:www\.)?apnews\.com/search(?:/(?P<filter>communities|users|games))?(?:\?|\#!?)(?:.*?[&;])??q=(?P<id>(?:[^&#]+)+)'
    _TESTS = [{
        'url': 'https://apnews.com/search?q=trump&p=2',
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
        query = (qs.get('search_query') or qs.get('q'))[0]
        return self.playlist_result(self._entries(url, query), query, query)
