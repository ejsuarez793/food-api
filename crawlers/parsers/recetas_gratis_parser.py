

class RecetasGratisParser:

    def __init__(self):
        self.name = 'recetas_gratis'
        self.base_url = 'https://www.recetasgratis.net'
        self.search_url = '/busqueda?q='
        self.dishes = ['desayunos', 'almuerzos', 'cenas', 'batidos']

    @staticmethod
    def get_recipe_detail_link(response):
        return response\
            .css('.resultado.link')\
            .css('.titulo.titulo--resultado')\
            .css('a::attr(href)')\
            .getall()

    @staticmethod
    def parse_recipe(self):
        pass