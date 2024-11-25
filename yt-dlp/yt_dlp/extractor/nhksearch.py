import re
from ..utils import parse_qs, traverse_obj
from .common import InfoExtractor, ExtractorError
import itertools


class NHKSearchIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www3\.)?nhk\.or\.jp/news/html/(?:[^/]+/)*(?P<id>k\d+)\.html'

    _TESTS = [{
        'url':  'https://www3.nhk.or.jp/news/html/20240726/k10014524661000.html',
        'info_dict': {
            'id': 'V8cFcYMxTHaMcEiiYVr39A',
            'ext': 'flv',
            'title': 'Apple Unveils the New IPhone 13, Stock Doesn\'t Move Much',
        },
        'params': {
            'format': 'best[format_id^=hds]',
        },
    }]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }
    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id, headers=self.headers)
        json_ld = self._html_search_regex(
            r'<script type="application/ld\+json">\s*(\{[^{}]*?"@type":\s*"VideoObject"[^{}]*?\})\s*</script>',
            webpage, 'json_ld', default='{}', flags=re.DOTALL)

        parsed_data = self._parse_json(json_ld, None, fatal=False)
        formats = []
        if parsed_data:
            formats.extend(self._extract_m3u8_formats(
                parsed_data['contentUrl'], video_id, 'mp4', entry_protocol='m3u8_native',
                m3u8_id='hls', fatal=False))
        return {
           'id': video_id,
            'formats': formats,
            'title': parsed_data.get('name', '-'),
            'description': parsed_data.get('description', '-'),
            'thumbnail': parsed_data.get('thumbnailUrl', '-'),
        }


class NHKSearchBaseIE(InfoExtractor):
    _SEARCH_TYPE = 'search'
    _API_URL = 'https://noa-api.nhk.jp/r1/db/_search?q=%28%22{query}%22%29&index=news&fields=title%2Cdescription%2Cdetail&_source=link%2CpubDate%2Ctitle%2Cdescription&sortkey=pubDate&order=desc&from={index}&limit=10'
    _API_HEADERS = {
        'Referer': 'https://www3.nhk.or.jp',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    def _entries(self, url, item_id, query=None, note='Downloading page %(page)s'):
        query = query or {}
        pages = [query['page']] if 'page' in query else itertools.count(0)
        for page_num in pages:
            query['page'] = str(page_num)
            api_url = self._API_URL.format(query=item_id, index=page_num*10)
            json_parsed = self._download_json(
                api_url,
                item_id,
                headers=self._API_HEADERS,
                note=note % {'page': page_num})
            # Find the data
            findlist = json_parsed['result']
            if not findlist:
                return
            for url_items in findlist:
                url_base = 'https://www3.nhk.or.jp/news/'
                full_url = url_base + url_items['link']
                yield self.url_result(full_url)

    def _search_results(self, query, url):
        return self._entries(url, query)


class NHKSearchURLIE(NHKSearchBaseIE):

    IE_DESC = 'NHK Video search'
    IE_NAME = 'nhk:search_url'
    _VALID_URL = r'https?://(?:www3\.)?nhk\.or\.jp/news/nsearch/\?qt=(?P<id>[^&#]+)'
    _TESTS = [{
        'url': 'https://www3.nhk.or.jp/news/nsearch/?qt=trump',
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
        query = (qs.get('qt') or qs.get('q'))[0]
        return self.playlist_result(self._entries(url, query), query, query)
