from . import local

@local.route('/')
def home():
    return '/local'
