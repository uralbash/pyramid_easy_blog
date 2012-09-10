# coding=utf8
import os
import json

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.view import view_config
from pyramid.security import authenticated_userid

from .models import (
    DBSession,
    Post,
    )

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    )

from .security import USERS

from sqlalchemy import desc

@view_config(route_name='view_blog', renderer='templates/index.jinja2')
def view_blog(request):
    posts = DBSession.query(Post).filter(Post.status != 0).order_by(desc(Post.id))
    return dict(posts=posts, logged_in=authenticated_userid(request))


@view_config(route_name='view_post', renderer='templates/view.jinja2')
def view_post(request):
    postid = request.matchdict['postid']
    post = DBSession.query(Post).filter_by(id=postid).first()
    if (post is None) or post.status == 0:
        return HTTPNotFound('No such page')

    title = post.title
    content = post.content
    tags = post.tags
    return dict(title=title, content=content, tags=tags,
                logged_in=authenticated_userid(request))


@view_config(route_name='add_post', renderer='templates/edit.jinja2',
             permission='edit')
def add_post(request):
    if 'form.submitted' in request.params:
        title = request.params['title']
        content = request.params['content']
        status = request.params['status']
        tags = request.params['tags']
        post = Post(title, content, status, tags)
        DBSession.add(post)
        return HTTPFound(location=request.route_url('view_blog'))
    post = Post('', '', '', '')
    return dict(post=post, logged_in=authenticated_userid(request))


@view_config(route_name='edit_post', renderer='templates/edit.jinja2',
             permission='edit')
def edit_post(request):
    postid = request.matchdict['postid']
    post = DBSession.query(Post).filter_by(id=postid).one()
    if 'form.submitted' in request.params:
        post.title = request.params['title']
        post.content = request.params['content']
        post.status = request.params['status']
        post.tags = request.params['tags']
        DBSession.add(post)
        return HTTPFound(location=request.route_url('view_post',
                                                    postid=post.id))
    return dict(post=post, logged_in=authenticated_userid(request))


@view_config(route_name='login', renderer='templates/login.jinja2')
@forbidden_view_config(renderer='templates/login.jinja2')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'  # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        if USERS.get(login) == password:
            headers = remember(request, login)
            return HTTPFound(location=came_from,
                             headers=headers)
        message = 'Failed login'

    return dict(
        message=message,
        url=request.application_url + '/login',
        came_from=came_from,
        login=login,
        password=password,
        )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('view_blog'),
                     headers=headers)


@view_config(route_name='connector',
             permission='edit', renderer='json')
def upload_photo(request):
    path =request.registry.settings.get('redactor_images')

    filename = request.POST['file'].filename
    input_file = request.POST['file'].file

    # Using the filename like this without cleaning it is very
    # insecure so please keep that in mind when writing your own
    # file handling.
    file_path = os.path.join(path, filename)
    output_file = open(file_path, 'wb')

    # Finally write the data to the output file
    input_file.seek(0)
    while 1:
        data = input_file.read(2<<16)
        if not data:
            break
        output_file.write(data)
    output_file.close()

    # TODO: брать путь из конфига
    return {"filelink": "/static/uploaded/images/"+filename}


import os, glob
@view_config(route_name='images_json',
             permission='edit', renderer='json')
def upload_file(request):
    path =request.registry.settings.get('redactor_images')
    types = ('*.jpg', '*.jpeg', '*.gif') # the tuple of file types

    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(path+"/"+files))
    resp = []
    for file in files_grabbed:
        file = file.replace(path, "")
        resp.append({"thumb": "/static/uploaded/images/"+file,
             "image": "/static/uploaded/images/"+file,
             "title": file, "folder": "images"})

    return resp
