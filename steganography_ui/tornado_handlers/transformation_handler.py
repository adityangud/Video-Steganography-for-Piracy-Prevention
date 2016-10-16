from tornado import template
import tornado.web
import json
import glob
from custom_utils import *
import plotter

class TransformationHandler(tornado.web.RequestHandler):
    loader = template.Loader('./web')
    def post(self):
        documents = self.get_argument('documents', None)
        transformation = self.get_argument('transformation', None)
        num_selects = self.get_argument('num_selects', None)

        if not documents:
            self.finish(json.dumps({"error": "missing docs"}))
            return

        recieved_documents = json.loads(documents)

        if transformation not in AVAILABLE_TRANSFORMATIONS:
            self.finish(json.dumps({"error": "unknown transformation"}))
            return

        transform = getattr(transformations, transformation)
        documents = []

        for document in recieved_documents:
            doc = glob.glob('uploads/%s' % document['name'])
            if not doc:
                documents.append(file_not_found(document['name']))
                continue

            if not renderable_as_graph(document['name']):
                documents.append(file_not_supported(document['name']))
                continue

            filename = document['name']
            transformed_name = transform('uploads/%s' % filename)
            image_name, ext = os.path.splitext(os.path.basename(transformed_name))
            plotter.plotter(transformed_name, 'images/%s.png' % image_name)
            data = {'name': os.path.basename(transformed_name), 'image_link': 'images/%s.png' % image_name, 'compatiable': True}
            documents.append(data)

        data = self.loader.load('transformed_rows.html').generate(documents=documents, operations=AVAILABLE_TRANSFORMATIONS, num_selects=num_selects)
        data = json.dumps({'html': data})
        self.finish(data)

