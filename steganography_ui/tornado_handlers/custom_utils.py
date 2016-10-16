import os
import time
import types
import transformations

__UPLOADS__ = './uploads/'

AVAILABLE_TRANSFORMATIONS = [ t for t in dir(transformations)
                              if type(getattr(transformations, t)) == types.FunctionType
                              and not t.startswith('_') ]



file_not_supported = lambda x: {'name': x + "_NOT_SUPPORTED", 'link': os.path.join(__UPLOADS__, x), 'compatiable': False, 'image_link': '/images/not_found.jpg'}
file_not_found = lambda x: {'name': x + "_NOT_FOUND", 'link': '#', 'compatiable': False, 'image_link': '/images/not_found.jpg'}
file_supported = lambda x: {'name': x, 'link': os.path.join(__UPLOADS__, x), 'compatiable': True}




def file_info(filename):
    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(__UPLOADS__ + filename)
    return_data = {"name": filename, "size": size, "last-modified": time.ctime(mtime)}
    return return_data;


def get_documents():
    return map(file_info, os.listdir('./uploads'))


def renderable_as_graph(filename):
    fp = open(os.path.join(__UPLOADS__, filename))
    try:
        data = eval(fp.read())
        one_element = data[0]
        fp.close()
    except Exception as exception:
        fp.close()
        return False

    return True
