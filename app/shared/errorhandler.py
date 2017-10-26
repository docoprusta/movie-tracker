import flask
from flask import json, request


def internal_server_error(func):
    def func_wrapper(*args, **kwargs):
        from app.shared.response import ResponseCreator
        from app.authentication.model import User
        response_creator = ResponseCreator()

        try:
            User.query.count()
            return func(*args, **kwargs)
        except:
            return response_creator.internal_server_error()
    return func_wrapper


def user_already_exists(func):
    def func_wrapper(*args, **kwargs):
        from app.shared.response import ResponseCreator
        from app.authentication.model import User
        response_creator = ResponseCreator()

        request_body_dict = request.json

        try:
            User.query.filter_by(username=request_body_dict['username']).first()
            return func(*args, **kwargs)
        except:
            return response_creator.user_already_exists()
    return func_wrapper


def unauthorized(func):
    def func_wrapper(*args, **kwargs):
        from app.shared.response import ResponseCreator
        from app.authentication.model import User
        response_creator = ResponseCreator()

        request_body_dict = request.json

        user_object = User.query.filter_by(username=request_body_dict['username']).first()

        if user_object is None:
            return response_creator.unauthorized()

        return func(*args, **kwargs)

    return func_wrapper


def user_does_not_exist(func):
    def func_wrapper(*args, **kwargs):
        from app.shared.response import ResponseCreator
        from app.authentication.model import User
        response_creator = ResponseCreator()

        username = flask.request.args['username']

        user_object = User.query.filter_by(username=username).first()

        if user_object is None:
            return response_creator.user_does_not_exist()

        return func(*args, **kwargs)

    return func_wrapper


def api_key_does_not_exist(func):
    def func_wrapper(*args, **kwargs):
        from app.shared.response import ResponseCreator
        from app.authentication.model import User
        response_creator = ResponseCreator()

        api_key = flask.request.args['api-key']

        user_object = User.query.filter_by(api_key=api_key).first()

        if user_object is None:
            return response_creator.api_key_does_not_exist()

        return func(*args, **kwargs)

    return func_wrapper
