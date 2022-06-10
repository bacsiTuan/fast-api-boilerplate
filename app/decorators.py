# coding: utf8
from functools import wraps

from loguru import logger

from app.config import config_app
from jsonschema import FormatChecker, validate
from jsonschema.exceptions import ValidationError


# def validate_func(**schema):
#     def decorated(func):
#         def validate_required(params):
#             for field in schema["required"]:
#                 if field not in params or not params[field]:
#                     field_name = field
#                     field_name = get_field_name(field_name, field)
#                     raise BadRequest(
#                         message="{field_name} is required".format(field_name=field_name)
#                     )
#
#         def get_field_name(field_name, field):
#             if field_name in schema["properties"]:
#                 if "name" in schema["properties"][field]:
#                     field_name = schema["properties"][field]["name"]
#             return field_name
#
#         def validate_properties(params):
#             try:
#                 validate(instance=params, schema=schema, format_checker=FormatChecker())
#             except ValidationError as exp:
#                 exp_info = list(exp.schema_path)
#                 error_type = ("type", "format", "pattern", "maxLength", "minLength")
#                 if set(exp_info).intersection(set(error_type)):
#                     field = exp_info[1]
#                     field_name = field
#                     field_name = get_field_name(field_name, field)
#                     message = "{field_name} is not valid".format(field_name=field_name)
#                 else:
#                     message = exp.message  # pragma: no cover
#                 raise BadRequest(message=message)
#
#         def parse_params(params):
#             if "enum_type" in schema:
#                 for field in schema["enum_type"]:
#                     if field in params:
#                         if not schema["enum_type"][field].has_value(params[field]):
#                             field_name = field
#                             field_name = get_field_name(field_name, field)
#                             raise BadRequest(
#                                 message="{} not isinstance enum".format(field_name)
#                             )
#                         else:
#                             params[field] = schema["enum_type"][field](params[field])
#             return params
#
#         @wraps(func)
#         def resource_verb(*args, **kwargs):
#             if not schema:
#                 return func(*args, **kwargs)
#
#             req_args = {
#                 k: v for k, v in kwargs.items() if k in schema["properties"].keys()
#             }
#
#             if "required" in schema:
#                 validate_required(req_args)
#
#             validate_properties(req_args)
#
#             new_args = args + (parse_params(req_args),)
#             return func(*new_args, **kwargs)
#
#         return resource_verb
#
#     return decorated


def sqlalchemy_session(db):
    def decorated(func):
        @wraps(func)
        def resource_verb(*args, **kwargs):
            # MANUAL PRE PING
            try:
                db.session.execute("SELECT 1;")
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.close()
                db.session.remove()

            result = None
            exception = None
            try:
                result = func(*args, **kwargs)
                db.session.commit()
            except Exception as exp:
                exception = exp
                if db.session.is_active:
                    db.session.rollback()
            finally:
                db.session.close()
                db.session.remove()

            if exception:
                raise exception
            return result

        return resource_verb

    return decorated
