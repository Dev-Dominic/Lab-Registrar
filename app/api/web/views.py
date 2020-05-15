from . import web

@web.route('/')
def home():
    return "/web"
