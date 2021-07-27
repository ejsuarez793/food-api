import datetime
import logging
from typing import List

log = logging.getLogger(__name__)


def validate_date_range(str_date_from: str, str_date_to: str):
    try:
        date_from = datetime.datetime.strptime(str_date_from, '%Y-%m-%d')
        date_to = datetime.datetime.strptime(str_date_to, '%Y-%m-%d')
        if date_from > date_to:
            error_msg = 'param \'date_from\' cant be greater than \'date_to\''
            return None, None, error_msg

        return date_to, date_from, None
    except Exception as e:
        log.error('there was an error parsing date params [error:{}]'.format(str(e)))
        error_msg = 'invalid dates format, please send date in YYYY-MM-DD format'
        return None, None, error_msg


def validate_ids(str_ids: str):
    try:
        ids = [int(_id) for _id in str_ids.split(',')]
        return ids, None
    except Exception as e:
        log.error('there was an error parsing ids params [error:{}]'.format(str(e)))
        error_msg = 'there was an error parsing \'ids\', ids must be integers'
        return None, error_msg


def validate_pagination_params(offset: str, limit: str):
    try:
        offset = int(offset) if offset is not None else 0
        limit = int(limit) if limit is not None else 10

        # we do not raise error for bad limit and offset params, we adjust them
        offset = 0 if offset < 0 else offset
        limit = 10 if limit <= 0 or limit > 10 else limit
        return offset, limit, None
    except Exception as e:
        log.error('there was an error parsing pagination params [error:{}]'.format(str(e)))
        error_msg = 'invalid \'offset\' and \'limit\' params'
        return None, None, error_msg


def validate_sort_by_params(sort_by: str, asc: str, str_columns: List[str], numeric_columns: List[str]):
    error_msg = None

    str_sort = True if sort_by in str_columns else False
    numeric_sort = True if sort_by in numeric_columns else False
    if not str_sort and not numeric_sort:
        error_msg = 'param \'sort_by\' is not a valid sort attribute'

    if asc is not None:
        valid_bool = asc.lower() in ['true', 'false']
        if not valid_bool:
            if error_msg:
                error_msg += ' and invalid \'asc\' params'
            else:
                error_msg = 'invalid \'asc\' params'

    return sort_by, str_sort, asc, error_msg