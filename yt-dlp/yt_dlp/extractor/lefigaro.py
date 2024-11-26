import json
import math
import itertools
import re
from .common import InfoExtractor, ExtractorError
from ..utils import (
    InAdvancePagedList,
    traverse_obj,
)
from bs4 import BeautifulSoup


class LeFigaroVideoEmbedIE(InfoExtractor):
    _VALID_URL = r'https?://video\.lefigaro\.fr/embed/[^?#]+/(?P<id>[\w-]+)'

    _TESTS = [{
        'url': 'https://video.lefigaro.fr/embed/figaro/video/les-francais-ne-veulent-ils-plus-travailler-suivez-en-direct-le-club-le-figaro-idees/',
        'md5': 'a0c3069b7e4c4526abf0053a7713f56f',
        'info_dict': {
            'id': 'g9j7Eovo',
            'title': 'Les Français ne veulent-ils plus travailler ? Retrouvez Le Club Le Figaro Idées',
            'description': 'md5:862b8813148ba4bf10763a65a69dfe41',
            'upload_date': '20230216',
            'timestamp': 1676581615,
            'duration': 3076,
            'thumbnail': r're:^https?://[^?#]+\.(?:jpeg|jpg)',
            'ext': 'mp4',
        },
    }, {
        'url': 'https://video.lefigaro.fr/embed/figaro/video/intelligence-artificielle-faut-il-sen-mefier/',
        'md5': '319c662943dd777bab835cae1e2d73a5',
        'info_dict': {
            'id': 'LeAgybyc',
            'title': 'Intelligence artificielle : faut-il s’en méfier ?',
            'description': 'md5:249d136e3e5934a67c8cb704f8abf4d2',
            'upload_date': '20230124',
            'timestamp': 1674584477,
            'duration': 860,
            'thumbnail': r're:^https?://[^?#]+\.(?:jpeg|jpg)',
            'ext': 'mp4',
        },
    }]

    _WEBPAGE_TESTS = [{
        'url': 'https://video.lefigaro.fr/figaro/video/suivez-en-direct-le-club-le-figaro-international-avec-philippe-gelie-9/',
        'md5': '6289f9489efb969e38245f31721596fe',
        'info_dict': {
            'id': 'QChnbPYA',
            'title': 'Où en est le couple franco-allemand ? Retrouvez Le Club Le Figaro International',
            'description': 'md5:6f47235b7e7c93b366fd8ebfa10572ac',
            'upload_date': '20230123',
            'timestamp': 1674503575,
            'duration': 3153,
            'thumbnail': r're:^https?://[^?#]+\.(?:jpeg|jpg)',
            'age_limit': 0,
            'ext': 'mp4',
        },
    }, {
        'url': 'https://video.lefigaro.fr/figaro/video/la-philosophe-nathalie-sarthou-lajus-est-linvitee-du-figaro-live/',
        'md5': 'f6df814cae53e85937621599d2967520',
        'info_dict': {
            'id': 'QJzqoNbf',
            'title': 'La philosophe Nathalie Sarthou-Lajus est l’invitée du Figaro Live',
            'description': 'md5:c586793bb72e726c83aa257f99a8c8c4',
            'upload_date': '20230217',
            'timestamp': 1676661986,
            'duration': 1558,
            'thumbnail': r're:^https?://[^?#]+\.(?:jpeg|jpg)',
            'age_limit': 0,
            'ext': 'mp4',
        },
    }]

    def _real_extract(self, url):
        display_id = self._match_id(url)
        webpage = self._download_webpage(url, display_id)

        player_data = self._search_nextjs_data(
            webpage, display_id)['props']['pageProps']['initialProps']['pageData']['playerData']

        return self.url_result(
            f'jwplatform:{player_data["videoId"]}', title=player_data.get('title'),
            description=player_data.get('description'), thumbnail=player_data.get('poster'))


class LeFigaroVideoSectionIE(InfoExtractor):
    _VALID_URL = r'https?://video\.lefigaro\.fr/figaro/(?P<id>[\w-]+)/?(?:[#?]|$)'

    _TESTS = [{
        'url': 'https://video.lefigaro.fr/figaro/le-club-le-figaro-idees/',
        'info_dict': {
            'id': 'le-club-le-figaro-idees',
            'title': 'Le Club Le Figaro Idées',
        },
        'playlist_mincount': 14,
    }, {
        'url': 'https://video.lefigaro.fr/figaro/factu/',
        'info_dict': {
            'id': 'factu',
            'title': 'Factu',
        },
        'playlist_mincount': 519,
    }]

    _PAGE_SIZE = 20

    def _get_api_response(self, display_id, page_num, note=None):
        return self._download_json(
            'https://api-graphql.lefigaro.fr/graphql', display_id, note=note,
            query={
                'id': 'flive-website_UpdateListPage_1fb260f996bca2d78960805ac382544186b3225f5bedb43ad08b9b8abef79af6',
                'variables': json.dumps({
                    'slug': display_id,
                    'videosLimit': self._PAGE_SIZE,
                    'sort': 'DESC',
                    'order': 'PUBLISHED_AT',
                    'page': page_num,
                }).encode(),
            })

    def _real_extract(self, url):
        display_id = self._match_id(url)
        initial_response = self._get_api_response(display_id, page_num=1)['data']['playlist']

        def page_func(page_num):
            api_response = self._get_api_response(display_id, page_num + 1, note=f'Downloading page {page_num + 1}')

            return [self.url_result(
                video['embedUrl'], LeFigaroVideoEmbedIE, **traverse_obj(video, {
                    'title': 'name',
                    'description': 'description',
                    'thumbnail': 'thumbnailUrl',
                })) for video in api_response['data']['playlist']['jsonLd'][0]['itemListElement']]

        entries = InAdvancePagedList(
            page_func, math.ceil(initial_response['videoCount'] / self._PAGE_SIZE), self._PAGE_SIZE)

        return self.playlist_result(entries, playlist_id=display_id, playlist_title=initial_response.get('title'))


class LeFigaroIE(InfoExtractor):
    _VALID_URL = r'https?://www.lefigaro\.fr(?:/[^?#]+)*/(?P<id>[\w-]+)/?(?:[#?]|$)'

    _TESTS = [{
        'url': 'https://www.lefigaro.fr/international/a-butler-les-supporters-de-trump-saluent-son-cran-20241006',
        'info_dict': {
            'id': 'le-club-le-figaro-idees',
            'title': 'Le Club Le Figaro Idées',
        },
        'playlist_mincount': 14,
    }]


    def _real_extract(self, url):
        display_id = self._match_id(url)
        webpage = self._download_webpage(url, display_id)
        json_ld =self._html_search_regex(
            r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
            webpage, 'json_ld', default='{}', flags=re.DOTALL)
        if not json_ld:
            raise ExtractorError('No JSON-LD found', expected=True)
        parsed_data = self._parse_json(json_ld, None, fatal=False)
        urls = parsed_data[-1]['video']['embedUrl']
        return self.url_result(urls)

class LefigaroSearchBaseIE(InfoExtractor):
    _SEARCH_TYPE = 'search'
    _API_HEADERS = {
        'Referer': 'https://recherche.lefigaro.fr/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }
    def _entries(self, url, item_id, query=None, note='Downloading page %(page)s'):
        query = query or {}
        pages = [query['page']] if 'page' in query else itertools.count(1)
        for page_num in pages:
            query['page'] = str(page_num)
            webpage = self._download_webpage(url, item_id, query=query, headers=self._API_HEADERS,
                                             note=note % {'page': page_num})
            soup = BeautifulSoup(webpage, 'html.parser')
            div_list_result = soup.find(id='articles-list')
            if not div_list_result:
                raise ExtractorError('No div with id "divListResult" found', expected=True)
            findlist = []
            items = div_list_result.find_all('article')
            for item in items:
                h2_tag = item.find('h2')
                if not h2_tag:
                    continue
                a_tag = h2_tag.find('a')
                if a_tag and 'href' in a_tag.attrs:
                    findlist.append(a_tag['href'])
            if not findlist:
                return
            for url_items in findlist:
                yield self.url_result(url_items)

    def _search_results(self, query, url):
        return self._entries(url, query)


class LefigaroSearchURLIE(LefigaroSearchBaseIE):
    IE_DESC = 'Lefigaro Video search'
    IE_NAME = 'lefigaro:search_url'
    _VALID_URL = r'https?://(?:www\.)?recherche\.lefigaro\.fr/recherche/(?P<id>[^/]+)/?'
    _TESTS = [{
        'url': 'https://recherche.lefigaro.fr/recherche/trump/',
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
        return self.playlist_result(self._entries(url, query), query, query)
