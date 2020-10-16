import datetime

def validate_dates(str_date_from: str, str_date_to: str):
    try:
        date_from = datetime.datetime.strptime(str_date_from, '%Y-%m-%d')
        date_to = datetime.datetime.strptime(str_date_to, '%Y-%m-%d')
        if date_from > date_to:
            raise ValueError("param 'date_from' can't be greater than 'date_to'")
    except ValueError:
        raise ValueError("incorrect data format, should be YYYY-MM-DD")

def validate_offset(str_num: str):
    try:
        if str_num is None:
            return 0

        num = int(str_num)
        if num < 0:
            return 0

        return num
    except:
        raise ValueError("incorrect 'offset' value, not a number")


def validate_limit(str_num: str):
    try:
        if str_num is None:
            return 10
        num = int(str_num)
        if num < 0:
            return 10
        if num > 20:
            return 20
        return num
    except:
        raise ValueError("incorrect 'limit' value, not a number")