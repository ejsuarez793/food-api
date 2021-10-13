import scrapy

from crawlers.parsers.recetas_gratis_parser import RecetasGratisParser


class RecipeSpider(scrapy.Spider):
    name = 'recipe'

    def start_requests(self):
        urls = [
            'https://www.recetasgratis.net/busqueda?q=desayunos'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = RecetasGratisParser.get_recipe_detail_link(response)

        for link in links:
            yield link
            # yield response.follow(link, callback=self.detail_parse)

        #next page
        # ToDo implementar luego
        """for a in response.css('a.andes-pagination__link'):
            yield response.follow(a, callback=self.parse)"""

    def detail_parse(self, response):
        recipe = RecetasGratisParser.parse_recipe(response)
        yield recipe