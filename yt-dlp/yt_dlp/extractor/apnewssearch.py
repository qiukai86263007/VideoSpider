import itertools
import re
import urllib.parse
from .common import InfoExtractor
from ..utils import parse_qs


class ApnewsSearchBaseIE(InfoExtractor):
    _SEARCH_TYPE = 'search'

    def _entries(self, url, item_id, query=None, note='Downloading page %(page)s'):
        query = query or {}
        # pages = [query['page']] if 'page' in query else itertools.count(1)
        # for page_num in pages:
        #     query['page'] = str(page_num)
        #     webpage = self._download_webpage(url, item_id, query=query, note=note % {'page': page_num})
        #     results = re.findall(r'(?<=data-video-id=)["\']?(?P<videoid>.*?)(?=["\'])', webpage)
        #     for item in results:
        #         yield self.url_result(f'https://www.nicovideo.jp/watch/{item}', 'Niconico', item)
        #     if not results:
        #         break
        pages = [query['p']] if 'p' in query else itertools.count(1)
        for page_num in pages:
            query['p'] = str(page_num)
            webpage = self._download_webpage(
                url, item_id,query=query,note=note % {'page': page_num})
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

    # def _search_results(self, query, url):
    #     for pagenum in itertools.count():
    #         webpage = self._download_webpage(
    #             url, query,
    #             note=f'Downloading result page {pagenum + 1}',
    #             query={
    #                 'q': query
    #             })
    #         findlist = re.findall(r'href="https://apnews\.com/video/[^"]+"', webpage)
    #         for url in list(set(findlist)):
    #             yield self.url_result(url)
    #
    #         if not re.search(r'id="pnnext"', webpage):
    #             return

    def _real_extract(self, url):
        qs = parse_qs(url)
        query = (qs.get('search_query') or qs.get('q'))[0]
        return self.playlist_result(self._entries(url, query), query, query)
