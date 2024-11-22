import itertools
import re
from .common import InfoExtractor
from ..utils import parse_qs, traverse_obj


class ABCNewsIE(InfoExtractor):
    IE_NAME = 'abcnews'
    IE_DESC = 'abcnews.com'
    _VALID_URL = r'https?://(?:www\.)?abcnews\.go\.com/[^/]+/[^/]+/story\?id=(?P<id>\d+)'
    _NETRC_MACHINE = 'abcnews'

    _TESTS = [{
        'url': 'https://abcnews.go.com/International/world-leaders-react-president-trump-lady-test-positive/story?id=73382673',
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
        json_data = self._html_search_regex(
            r"window\['__abcnews__'\]\s*=\s*(\{.*?\});",
            webpage, 'abcnews json', default='{}', flags=re.DOTALL)
        parsed_data = self._parse_json(json_data, None, fatal=False)
        story_item = traverse_obj(parsed_data, ('page', 'content', 'story', 'story'))
        items = traverse_obj(story_item, ('leadMediaVideo', 'video', 'video', 'streams', 'm3u8', ...))
        formats = []
        if items:
            formats.extend(self._extract_m3u8_formats(
                items, video_id, 'mp4', entry_protocol='m3u8_native',
                m3u8_id='hls', fatal=False))
        return {
            'id': video_id,
            'formats': formats,
            'title': story_item.get('title', {}),
            'description': story_item.get('description', {}),
            'thumbnail': self._og_search_thumbnail(webpage, default=None),
        }


class ABCNewsSearchBaseIE(InfoExtractor):
    _SEARCH_TYPE = 'search'
    _API_URL = 'https://abcnews.go.com/meta/api/search?limit=10&sort=&type=&section=&totalrecords=true&offset=%s&q=%s'
    _API_HEADERS = {
        'Referer': 'https://abcnews.go.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    def _entries(self, url, item_id, query=None, note='Downloading page %(page)s'):
        query = query or {}
        pages = [query['page']] if 'page' in query else itertools.count(0)
        for page_num in pages:
            query['page'] = str(page_num)
            api_url = self._API_URL % (page_num, item_id)
            json_parsed = self._download_json(
                api_url,
                item_id,
                headers=self._API_HEADERS,
                note=note % {'page': page_num})

            findlist = json_parsed['item']
            if not findlist:
                return
            for url_items in findlist:
                yield self.url_result(url_items['link'])

    def _search_results(self, query, url):
        return self._entries(url, query)


class ABCNewsSearchURLIE(ABCNewsSearchBaseIE):
    IE_DESC = 'abcnews Video search'
    IE_NAME = 'abcnews:search_url'
    _VALID_URL = r'https?://(?:www\.)?abcnews\.go\.com/search\?searchtext=(?P<id>[^&#]+)'
    _TESTS = [{
        'url': 'https://abcnews.go.com/search?searchtext=trump',
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
        query = (qs.get('searchtext') or qs.get('q'))[0]
        return self.playlist_result(self._entries(url, query), query, query)
