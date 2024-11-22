import itertools
import re
from .common import InfoExtractor
from ..utils import parse_qs

"""
javaScript 反爬虫 需要用到 selenium？
"""
class NBCNewsIE(InfoExtractor):
    IE_NAME = 'nbcnews'
    IE_DESC = 'nbcnews.com'
    _VALID_URL = r'https://nbcnews\.com/video/(?P<id>[^/]+)'
    _NETRC_MACHINE = 'nbcnews'

    _TESTS = [{
        'url': 'https://nbcnews.com/video/judge-delays-ruling-in-trumps-hush-money-case-0000019322bdd461ad9f7efd37520000',
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


class NBCNewsSearchBaseIE(InfoExtractor):
    _SEARCH_TYPE = 'search'

    def _entries(self, url, item_id, query=None, note='Downloading page %(page)s'):
        query = query or {}
        pages = [query['p']] if 'p' in query else itertools.count(1)
        for page_num in pages:
            query['p'] = str(page_num)
            webpage = self._download_webpage(
                url, item_id, query=query, note=note % {'page': page_num})
            findlist = list(set(re.findall(r'https://nbcnews\.com/video/[^"]+', webpage)))
            if not findlist:
                return
            for url_items in findlist:
                yield self.url_result(url_items)

    def _search_results(self, query, url):
        return self._entries(url, query)


class NBCNewsSearchURLIE(NBCNewsSearchBaseIE):
    IE_DESC = 'nbcnews Video search'
    IE_NAME = 'nbcnews:search_url'
    _VALID_URL = r'https?://(?:www\.)?nbcnews\.com/search/\?q=(?P<id>[^&#]+)'
    _TESTS = [{
        'url': 'https://www.nbcnews.com/search/?q=trump',
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
