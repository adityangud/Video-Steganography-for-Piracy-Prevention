import os
import tornado.ioloop
import tornado.web
from tornado import template
import json


class VideoProcessingHandler(tornado.web.RequestHandler):
    loader = template.Loader('./web')
    def post(self):
        html = self.loader.load('video_processing.html').generate()
        self.write(json.dumps({'html': html}))


