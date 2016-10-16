import tornado.web
from tornado import template
import json

class OverviewHandler(tornado.web.RequestHandler):
    loader = template.Loader('./web')
    def post(self):
        print "got request for overview"
        html = self.loader.load('preprocessed_overview.html').generate()
        data = json.dumps({'html': html})
        self.write(data)

