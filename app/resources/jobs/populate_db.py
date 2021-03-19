"""
PopulateDb Resource entrypoint that starts the jobs that
populate database
"""

import logging
from flask_restx import Resource

from app.repositories.jobs.populate_db import read_recipes, read_ingredients

log = logging.getLogger(__name__)


class PopulateDb(Resource):
    """
    PopulateDb class that only uses post method
    """

    @staticmethod
    def post():
        """
        post method that runs read_recipes and read_ingredients methods
        :return: response with status of the job run
        """

        log.info("Starting db populate job...")
        response, err = read_recipes()
        if err:
            return err, err['status_code']

        response, err = read_ingredients()
        if err:
            return err, err['status_code']
        return response, 200
