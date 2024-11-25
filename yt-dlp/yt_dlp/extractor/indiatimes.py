import re
import urllib

from ..utils import parse_qs, traverse_obj
from .common import InfoExtractor, ExtractorError
import itertools
from bs4 import BeautifulSoup


class IndiaTimesIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?timesofindia\.indiatimes\.com/videos(?:/[^/]+)*/videoshow/(?P<id>\d+)\.cms'

    _TESTS = [{
        'url': 'https://timesofindia.indiatimes.com/videos/entertainment/english/will-trump-grant-presidential-pardon-to-diddy-former-bodyguard-dismisses-speculation/videoshow/115488740.cms',
        'info_dict': {
            'id': 'V8cFcYMxTHaMcEiiYVr39A',
            'ext': 'flv',
            'title': 'Apple Unveils the New IPhone 13, Stock Doesn\'t Move Much',
        },
        'params': {
            'format': 'best[format_id^=hds]',
        },
    }]
    API_URL = 'https://tvid.in/api/mediainfo/vs/em/1xvsem896u/1xvsem896u.json?vj=105&apikey=toi371web5awj999ou6&k=1xvsem896u&mse=1&aj=31&ajbit=00000&pw=680&ph=383&chs={chs}&msid={msgid}&url={url}&tpl={tpl}&sw=2560&sh=1440&cont=toiPlayerContainer&gdprn=2&skipanalytics=2&map=1&sdk=1&viewportvr=100'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        pattern = r'https?://(?:www\.)?timesofindia\.indiatimes\.com/videos/(?P<level1>[^/]+)/(?P<level2>[^/]+)/.*(?P<videoshow>videoshow)/\d+\.cms'

        match = re.search(pattern, url)
        if match:
            level1 = match.group('level1')
            level2 = match.group('level2')
            videoshow = match.group('videoshow')
        send_url = self.API_URL.format(msgid=video_id, chs=level1 + '/' + level2, url=urllib.parse.quote(url, safe=''),
                                       tpl=videoshow)
        parsed_data = self._download_json(send_url, video_id, headers=self.headers)
        formats = []
        if parsed_data:
            formats.extend(self._extract_m3u8_formats(
                parsed_data['flavors'][0]['url'], video_id, 'mp4', entry_protocol='m3u8_native',
                m3u8_id='hls', fatal=False))
        return {
            'id': video_id,
            'formats': formats,
            'title': parsed_data.get('name', '-'),
            'description': parsed_data.get('description', '-'),
            'thumbnail': 'https:' + parsed_data.get('thumb', '-'),
        }


class IndiaTimesSearchBaseIE(InfoExtractor):
    _SEARCH_TYPE = 'search'
    _API_HEADERS = {
        'Referer': 'https://www3.nhk.or.jp',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    def _entries(self, url, item_id, query=None, note='Downloading page %(page)s'):
        query = query or {}
        pages = [query['page']] if 'page' in query else itertools.count(0)
        for page_num in pages:
            query['page'] = str(page_num)
            webpage = self._download_webpage(url, item_id, query=query, headers=self._API_HEADERS,
                                             note=note % {'page': page_num})
            soup = BeautifulSoup(webpage, 'html.parser')
            div_list_result = soup.find(class_='qBZe4')
            if not div_list_result:
                raise ExtractorError('No div with id "divListResult" found', expected=True)
            findlist = []
            items = div_list_result.find_all(class_='UnPlE')
            for item in items:
                a_tag = item.find('a')
                if a_tag and 'href' in a_tag.attrs:
                    findlist.append(a_tag['href'])
            if not findlist:
                return
            for url_items in findlist:
                yield self.url_result(url_items)
            break

    def _search_results(self, query, url):
        return self._entries(url, query)


class IndiaTimesSearchURLIE(IndiaTimesSearchBaseIE):
    IE_DESC = 'Indiatimes Video search'
    IE_NAME = 'indiatimes:search_url'
    _VALID_URL = r'https?://(?:www\.)?timesofindia\.indiatimes\.com/topic/(?P<id>[^/]+)/videos'
    _TESTS = [{
        'url': 'https://timesofindia.indiatimes.com/topic/trump/videos',
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
