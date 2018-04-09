import os
from collections import defaultdict

import six

import tw2.core as twc
from tw2.core import Link, Param


_external_ = False
_variant_ = None


class CDNLink(Link):

    external = Param("(boolean) True if you would like to grab the file from a"
                     " CDN instead of locally.  Default: {!r}".format(
                         _external_), default=_external_, request_local=False)

    cdn_handle = Param("(string) handle of the CDN to pick if external == True"
                       " and cdn_url is a dict mapping handles to URLs.",
                       default=None, request_local=False)

    cdn_url = Param("(dict(string: string) or string) URL of the resource on a"
                    " CDN, or dict mapping CDN handles (see `cdn_handle`) to"
                    " their URLs.", default=None, request_local=False)

    version = Param("(string) Specify the version of the resource to use.",
                    default=None, request_local=False)

    variant = Param("(string) File variant, e.g. 'min' for minified.  Default:"
                    " {!r}".format(_variant_), default=_variant_,
                    request_local=False)

    cdn_url = Param(
        "(dict(string: string) or string) URL of the resource on a CDN, "
        "or dict mapping CDN handles (see `external`) to their URLs.",
        request_local=False)

    def __init__(self, *p, **k):
        self._expanded_filename = None
        self._expanded_cdn_url = None
        self._link = None
        self._expansions = defaultdict(str)
        super(CDNLink, self).__init__(*p, **k)
        for param in ('version', 'variant'):
            value = getattr(self, param)
            if not value:
                continue
            self._expansions[param] = value
            for sep, sepname in (
                    (".", "dot"), ("-", "dash"), ("_", "underscore"),
                    ("/", "slash")):
                self._expansions[sepname + "_" + param] = sep + value
                self._expansions[param + "_" + sepname] = value + sep

    def prepare(self):
        if not self.external:
            modname = self.modname or self.__module__
            twc.register_resource(
                modname, os.path.dirname(self.filename),
                whole_dir=self.whole_dir)
        super(CDNLink, self).prepare()

    def expand_string(self, string):
        return string.format(**self._expansions)

    @property
    def expanded_filename(self):
        if self._expanded_filename is None:
            self._expanded_filename = self.expand_string(self.filename)
        return self._expanded_filename

    def pick_cdn_url(self):
        assert len(self.cdn_url)
        if isinstance(self.cdn_url, six.text_type):
            return self.cdn_url

        # assume dict/mapping
        if self.external in self.cdn_url:
            return self.cdn_url[self.external]
        else:
            # use any CDN (unspecified which one)
            return next(iter(self.cdn_url.values()))

    @property
    def expanded_cdn_url(self):
        if self._expanded_cdn_url is None:
            self._expanded_cdn_url = self.expand_string(self.pick_cdn_url())
        return self._expanded_cdn_url

    @property
    def link(self):
        if self._link is None:
            if self.external:
                self._link = self.expanded_cdn_url
            else:
                rl = twc.core.request_local()
                mw = rl['middleware']
                self._link = "/" + "/".join(filter(None, (
                    mw.config.script_name.strip("/"),
                    mw.config.res_prefix.strip("/"),
                    self.modname,
                    self.expanded_filename))).replace("//", "/")
        return self._link


class CSSCDNLink(CDNLink, twc.CSSLink):

    pass


class JSCDNLink(CDNLink, twc.JSLink):

    pass
