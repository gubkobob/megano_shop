from app_catalog.models import Category
from jinja2 import Environment


class get_categories(Environment):
    def __init__(self,**kwargs):
        super(get_categories, self).__init__(**kwargs)
        self.globals['categories'] = Category.objects.all()
