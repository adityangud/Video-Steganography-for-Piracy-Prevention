import tornado.web
from tornado import template
import json

class JoinerHandler(tornado.web.RequestHandler):
    loader = template.Loader('./web')
    def post(self):
        print "got request for joiner"
        html = self.loader.load('joiner.html').generate()
        data = json.dumps({'html': html})
        self.write(data)

