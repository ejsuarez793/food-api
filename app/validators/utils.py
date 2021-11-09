import datetime
import logging
from typing import List, Dict

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


def validate_ids(str_ids: str, int_ids: bool, max_multiget_length: int):
    try:
        ids = [_id for _id in str_ids.split(',')]
        if int_ids:
            [int(_id) for _id in ids]  # validate correct int str
        if len(ids) > max_multiget_length:
            return None, f'max number of ids to search is {max_multiget_length} but {len(ids)} was given'
        return ids, None
    except Exception as e:
        log.error('there was an error parsing ids params [error:{}]'.format(str(e)))
        error_msg = 'there was an error parsing \'ids\''
        return None, error_msg


def validate_pagination_params(offset: str, limit: str, max_limit: int):
    try:
        offset = int(offset) if offset is not None else 0
        limit = int(limit) if limit is not None else 10

        # we do not raise error for bad limit and offset params, we adjust them
        offset = 0 if offset < 0 else offset
        limit = 10 if limit <= 0 or limit > max_limit else limit
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


def valid_filter_value(param: str, filters_data_types: Dict, operator: str, value: str):
    try:
        if param in filters_data_types['integer_values']:
            int(value) if operator != 'between' else (int(value.split(',')[0]), int(value.split(',')[1]))
        if param in filters_data_types['real_values']:
            float(value) if operator != 'between' else (float(value.split(',')[0]), float(value.split(',')[1]))
        if param in filters_data_types['date_values']:
            float(datetime.datetime.strptime(value, '%Y-%m-%d')) if operator != 'between' \
                else \
                    (datetime.datetime.strptime(value.split(',')[0], '%Y-%m-%d'), \
                    datetime.datetime.strptime(value.split(',')[1], '%Y-%m-%d'))
        if param in filters_data_types['discrete_values']:
            if value not in filters_data_types['discrete_values'][param]:
                raise ValueError('error validating filter value')
        if param in filters_data_types['boolean_values']:
            if value.lower() not in ['true', 'false']:
                raise ValueError('error validating filter value')
    except ValueError:
        log.error(f'there was an error checking filter \'{param}\' value, value {value} not valid')
        return False

    return True


def validate_filters(request, valid_filters: Dict, filters_data_types: Dict):
    filters = []
    errors = {}

    for key in request.args:
        splitted_key = key.split('[')
        is_lhs_filter_param = len(splitted_key) == 2
        if is_lhs_filter_param:
            param, operator = splitted_key[0], splitted_key[1][:-1]
            if operator in valid_filters and param in valid_filters[operator] and valid_filter_value(param, filters_data_types, operator,
                                                                                                     request.args[key]):
                filters.append({'field': param, 'operator': operator, 'value': request.args[key]})
            else:
                errors[param] = f'filter for field \'{param}\' and operator \'{operator}\' is not supported or has an invalid value'

    return filters, errors


def validate_fields(fields: str, valid_fields: Dict):

    splitted_fields = fields.split(',')
    errors = {}

    for field in splitted_fields:
        if field not in valid_fields:
            errors['fields'] = f'field \'{field}\' in fields query params is not supported'

    return splitted_fields, errors
