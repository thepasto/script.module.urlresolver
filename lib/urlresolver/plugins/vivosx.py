'''
vivo.sx urlresolver plugin
Copyright (C) 2015 y2000j

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import re
import base64
import json
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError


class VivosxResolver(UrlResolver):
    name = "vivosx"
    domains = ["vivo.sx"]
    pattern = '(?://|\.)(vivo\.sx)/([0-9a-zA-Z]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):

        web_url = self.get_url(host, media_id)

        resp = self.net.http_GET(web_url, headers={'Referer': web_url})
        html = resp.content

        r = re.search(r'data-stream\s*=\s*(["\'])(?P<url>(?:(?!\1).)+)\1', html)

        if not r:
            raise ResolverError('page structure changed')

        r_url = base64.b64decode(r.group('url')).decode('utf-8')

        if re.match(r'^(?:[a-zA-Z][\da-zA-Z.+-]*:)?//', r_url):
            stream_url = r_url
        else:
            stream_url = None

        if stream_url:
            return stream_url
        else:
            raise ResolverError('video not found')

    def get_url(self, host, media_id):
        return 'http://vivo.sx/%s' % media_id
