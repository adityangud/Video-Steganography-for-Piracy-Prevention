from tornado import template
import tornado.web
import json


class UploadsHandler(tornado.web.RequestHandler):

    loader = template.Loader('./web')

    def post(self):
        self.loader = template.Loader('./web')
        num_uploads = self.get_argument('num_uploads')
        html_data = self.loader.load('uploads.html').generate(num_uploads=num_uploads)
        data = json.dumps({'html': html_data})
        self.write(data)

