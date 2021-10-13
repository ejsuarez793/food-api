import logging
from flask_restx import Resource

log = logging.getLogger(__name__)


class RecipeCrawlerJob(Resource):

    @staticmethod
    def post():
        log.info("Starting crawler...")
        #links = RecipeSpider().start_requests()
        #for link in links:
        #    print('procesando...')
        response, err = "", None
        if err:
            return err, err['status_code']
        return response, 200
