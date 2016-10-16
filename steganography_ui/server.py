import os
import glob
import tornado.ioloop
import tornado.web
from tornado import template
import json

# from tornado_handlers import overview_handler, uploads_handler, archive_handler, compare_handler, compare_files_handler, transformation_handler

from tornado_handlers import *


### Constants BEGIN
__UPLOADS__ = 'uploads/' # custom_utils.py has one too TODO: one copy
IMAGES_PATH = os.path.join(os.getcwd(), "images")
JS_PATH = os.path.join(os.getcwd(), "js")
CSS_PATH = os.path.join(os.getcwd(), "css")
FONTS_PATH = os.path.join(os.getcwd(), "fonts")
VIDEO_PATH = os.path.join(os.getcwd(), "video")
### Constants END

class Upload(tornado.web.RequestHandler):
    def post(self):
        print "GOT request for upload of a file"
        fileinfo = self.request.files['myFile'][0]
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]

        fh = open(__UPLOADS__ + fname, 'w')
        fh.write(fileinfo['body'])
        self.finish(json.dumps({'name': fname}))

class UploadVideo(tornado.web.RequestHandler):
    loader = template.Loader('./web')
    def post(self):
        print "request to upload a video"
        fileinfo = self.request.files['myVideo'][0]
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]

        fh = open(VIDEO_PATH + "/" + fname, 'w')
        fh.write(fileinfo['body'])

        data = self.loader.load('video_upload.html').generate()
        self.write(json.dumps({'html': data}))

class MainHandler(tornado.web.RequestHandler):
    loader = template.Loader('./web')
    def get(self):
        html = self.loader.load('index.html').generate()
        self.write(html)


def preprocess_stuff():
    print "Creating slides..."
    loader = template.Loader('./web')
    slide_names = glob.glob('./web/slides/slide_*.html')
    slide_names.sort()
    fp = open('./web/preprocessed_overview.html', 'w')
    str_to_write = ''
    if not slide_names:
        str_to_write = loader.load('overview.html')
    else:
        str_to_write = ''
        num_slides = len(slide_names)
        slides = []
        for i in slide_names:
            slide_name = os.path.basename(i)
            slides.append(loader.load('slides/%s' % slide_name).generate())
        str_to_write = loader.load('overview_slide.html').generate(num_slides=num_slides, slides=slides)

    fp.write("%s" % str_to_write)
    fp.close()
    print "done creating slides"


preprocess_stuff()

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/fileupload/", Upload),
    (r"/videoupload/", UploadVideo),
    (r"/overview/", overview_handler.OverviewHandler),
    (r"/uploads/", uploads_handler.UploadsHandler),
    (r"/archives/", archive_handler.ArchiveHandler),
    (r"/compare/", compare_handler.CompareHandler),
    (r"/comparefiles/", compare_files_handler.CompareFilesHandler),
    (r"/transform/", transformation_handler.TransformationHandler),
    (r"/video_processing/", video_processing_handler.VideoProcessingHandler),
    (r"/splitter/", splitter_handler.SplitterHandler),
    (r"/embedder/", embedder_handler.EmbedderHandler),
    (r"/joiner/", joiner_handler.JoinerHandler),
    (r"/detector/", detector_handler.DetectorHandler),
    (r"/do-detection/", detector_handler.DoDetection),
    (r"/images/(.*)", tornado.web.StaticFileHandler, {'path': IMAGES_PATH}),
    (r"/js/(.*)", tornado.web.StaticFileHandler, {'path': JS_PATH}),
    (r"/css/(.*)", tornado.web.StaticFileHandler, {"path": CSS_PATH}),
    (r"/fonts/(.*)", tornado.web.StaticFileHandler, {"path": FONTS_PATH}),
    (r"/video/(.*)", tornado.web.StaticFileHandler, {"path": VIDEO_PATH}),


])

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
