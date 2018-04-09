from nose.tools import eq_, assert_in

import tw2.core as twc
from tw2.core.testbase import WidgetTest as _WidgetTest

import tw2.cdnlink as twl

def setUp():
    _rl = {}
    def fake_rl():
        return _rl
    twc.core.request_local = fake_rl
    rl = twc.core.request_local()
    rl['middleware'] = twc.middleware.make_middleware(None, {})


# basic tests

class SimpleCDNLink(twl.CDNLink):

    modname = 'simple'
    filename = "static/simple"
    cdn_url = "//code.somecdn.net/path/simple"


class ComplicatedCDNLink(twl.CDNLink):

    modname = 'complicated'
    filename = "static/complicated/{version}/complicated{dot_variant}.js"
    cdn_url = {
        'cdn1': "//code.cdn1.com/complicated{dash_version}{dot_variant}.js",
        'cdn2': "https://cdn2.net/ajax/libs/complicated/{version}/complicated{dot_variant}.js"
        }


class TestSimple(object):

    def test_local(self):
        simple = SimpleCDNLink()
        the_link = "/resources/simple/static/simple"
        eq_(simple.req().link, the_link)

    def test_external(self):
        simple = SimpleCDNLink(external=True)
        the_link = "//code.somecdn.net/path/simple"
        eq_(simple.req().link, the_link)


class TestComplicated(object):

    def test_local(self):
        complicated = ComplicatedCDNLink(version="1.0.0", variant="min")
        the_link = "/resources/complicated/static/complicated/1.0.0/complicated.min.js"
        eq_(complicated.req().link, the_link)

    def test_external(self):
        complicated = ComplicatedCDNLink(
            version="1.0.0", variant="min", external='cdn1')
        eq_(complicated.req().link, "//code.cdn1.com/complicated-1.0.0.min.js")

    def test_external_random(self):
        complicated = ComplicatedCDNLink(
            version="1.0.0", variant="min", external=True)
        assert_in(complicated.req().link, (
            "//code.cdn1.com/complicated-1.0.0.min.js",
            "https://cdn2.net/ajax/libs/complicated/1.0.0/complicated.min.js"))

# widget tests

class WidgetTest(_WidgetTest):

    #engines = ['mako', 'jinja', 'genshi']
    pass


class TestJSCDNLink(twl.JSCDNLink):

    modname = 'jsmod'
    version = '1.0.0'
    filename = "static{slash_version}/javascript.js"
    cdn_url = "//code.somecdn.net/path/jsmod/javascript{dash_version}.js"


class TestJSCDNLinkLocal(WidgetTest):

    widget = TestJSCDNLink
    expected = """<script type="text/javascript"
    src="/resources/jsmod/static/1.0.0/javascript.js"></script>"""


class TestJSCDNLinkExternal(WidgetTest):

    widget = TestJSCDNLink
    params = {'external': True}
    expected = """<script type="text/javascript"
    src="//code.somecdn.net/path/jsmod/javascript-1.0.0.js"></script>"""
