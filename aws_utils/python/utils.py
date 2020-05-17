import decimal
import json


class DecimalEncoder(json.JSONEncoder):
    """ makes json serialize decimal (for boto3) """

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def validate_params(**kwargs):
    return [v if v is not None else dict() for v in kwargs.values()]


def success(**kwargs):
    status_code = kwargs.get('status_code', 200)
    body = kwargs.get('body') if isinstance(kwargs.get('body'), str) else str(kwargs.get('body'))
    return {"statusCode": status_code, "body": body}


def failure(**kwargs):
    status_code = kwargs.get('status_code', 500)
    body = kwargs.get('body') if isinstance(kwargs.get('body'), str) else str(kwargs.get('body'))
    return {"statusCode": status_code, "body": body}
