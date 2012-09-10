from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from sqlalchemy import engine_from_config

from pyramid_easy_blog.security import groupfinder

from .models import DBSession


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings,
                          root_factory='pyramid_easy_blog.models.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("pyramid_easy_blog:templates")
    config.add_static_view('static', 'static', cache_max_age=3600)

    #config.include('pyramid_easy_blog.connector')

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('view_blog', '/')
    config.add_route('add_post', '/add_post/')
    config.add_route('connector', '/connector')
    config.add_route('images_json', '/images_json')
    config.add_route('view_post', '/{postid}')
    config.add_route('edit_post', '/{postid}/edit_post')
    config.scan()
    return config.make_wsgi_app()
