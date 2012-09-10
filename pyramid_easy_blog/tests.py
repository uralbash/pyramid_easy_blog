import unittest
import transaction

from pyramid import testing
from time import gmtime, strftime

def _initTestingDB():
    from sqlalchemy import create_engine
    from pyramid_easy_blog.models import (
        DBSession,
        Post,
        Base
        )
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    with transaction.manager:
        model = Post('MyTitlle'+str(strftime("%Y-%m-%d %H:%M:%S:%s", gmtime())),
                     'This is the first post content',
                     0, 'tags, many, of ,tags')
        DBSession.add(model)
    return DBSession


def _registerRoutes(config):
    config.add_route('view_blog', '/')
    config.add_route('view_post', '/{postid}')
    config.add_route('add_post', '/add_post/')
    config.add_route('edit_post', '/{postid}/edit_post')


class PostModelTests(unittest.TestCase):

    def setUp(self):
        self.session = _initTestingDB()

    def tearDown(self):
        self.session.remove()

    def _getTargetClass(self):
        from pyramid_easy_blog.models import Post
        return Post

    def _makeOne(self, title='SomeName', content='some data', status=1,
                 tag = 'new tag'):
        return self._getTargetClass()(title, content, status, tag)

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.title, 'SomeName')
        self.assertEqual(instance.content, 'some data')
        self.assertEqual(instance.status, 1)
        self.assertEqual(instance.tags, 'new tag')

'''
class ViewBlogTests(unittest.TestCase):
    #TODO: finish this test
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, request):
        from pyramid_easy_blog.views import view_blog
        return view_blog(request)

    def test_it(self):
        _registerRoutes(self.config)
        request = testing.DummyRequest()
        response = self._callFUT(request)
        #self.assertEqual(response, '')
'''

class ViewPostTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from pyramid_easy_blog.views import view_post
        return view_post(request)

    def test_it(self):
        from pyramid_easy_blog.models import Post
        request = testing.DummyRequest()
        request.matchdict['postid'] = 2
        post = Post('MyTitlle2', 'This is the first post content',
                     1, 'tags, many, of ,tags')
        self.session.add(post)
        _registerRoutes(self.config)
        info = self._callFUT(request)
        #self.assertEqual(info['page'], page)
        '''self.assertEqual(
            info['content'],
            '<div class="document">\n'
            '<p>Hello <a href="http://example.com/add_page/CruelWorld">'
            'CruelWorld</a> '
            '<a href="http://example.com/IDoExist">'
            'IDoExist</a>'
            '</p>\n</div>\n')
        '''
        '''self.assertEqual(info['edit_url'],
            'http://example.com/IDoExist/edit_page')
        '''


class AddPageTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from pyramid_easy_blog.views import add_post
        return add_post(request)

    def test_it_notsubmitted(self):
        _registerRoutes(self.config)
        request = testing.DummyRequest()
        info = self._callFUT(request)
        self.assertEqual(info['post'].content,'')

    def test_it_submitted(self):
        from pyramid_easy_blog.models import Post
        _registerRoutes(self.config)
        request = testing.DummyRequest({'form.submitted':True,
                                        'title': 'New',
                                        'content': 'Hello yo!',
                                        'status': 1,
                                        'tags': 'new, tag'})
        self._callFUT(request)
        post = self.session.query(Post).filter_by(title='New').one()
        self.assertEqual(post.content, 'Hello yo!')

class EditPostTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from pyramid_easy_blog.views import edit_post
        return edit_post(request)

    def test_it_notsubmitted(self):
        from pyramid_easy_blog.models import Post
        _registerRoutes(self.config)
        request = testing.DummyRequest()
        request.matchdict = {'postid': 1}
        post = Post('abc', 'hello', 1, 'a, b, c')
        self.session.add(post)
        info = self._callFUT(request)

    def test_it_submitted(self):
        from pyramid_easy_blog.models import Post
        _registerRoutes(self.config)
        request = testing.DummyRequest({'form.submitted':True,
                                        'title': 'New',
                                        'content': 'Hello yo!',
                                        'status': 1,
                                        'tags': 'new, tag'})

        request.matchdict = {'postid': 1}
        post = Post('New', 'Hello yo!', 1, 'new, tag')
        self.session.add(post)
        response = self._callFUT(request)
        self.assertEqual(post.content, 'Hello yo!')

class FunctionalTests(unittest.TestCase):

    viewer_login = '/login?login=viewer&password=viewer' \
                   '&came_from=/&form.submitted=Login'
    viewer_wrong_login = '/login?login=viewer&password=incorrect' \
                   '&came_from=/&form.submitted=Login'
    editor_login = '/login?login=editor&password=editor' \
                   '&came_from=/&form.submitted=Login'

    def setUp(self):
        from pyramid_easy_blog import main
        settings = { 'sqlalchemy.url': 'sqlite://'}
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
        _initTestingDB()

    def tearDown(self):
        del self.testapp
        from pyramid_easy_blog.models import DBSession
        DBSession.remove()

    def test_root(self):
        res = self.testapp.get('/', status=200)

    def test_unexisting_page(self):
        self.testapp.get('/SomePage', status=404)

    def test_successful_log_in(self):
        res = self.testapp.get(self.viewer_login, status=302)
        self.assertEqual(res.location, 'http://localhost/')

    def test_failed_log_in(self):
        res = self.testapp.get(self.viewer_wrong_login, status=200)
        self.assertTrue(b'login' in res.body)

    def test_logout_link_present_when_logged_in(self):
        self.testapp.get(self.viewer_login, status=302)
        res = self.testapp.get('/', status=200)
        self.assertTrue(b'Logout' in res.body)

    def test_logout_link_not_present_after_logged_out(self):
        self.testapp.get(self.viewer_login, status=302)
        self.testapp.get('/', status=200)
        res = self.testapp.get('/logout', status=302)
        self.assertTrue(b'Logout' not in res.body)

    def test_anonymous_user_cannot_edit(self):
        res = self.testapp.get('/1/edit_post', status=200)
        self.assertTrue(b'Login' in res.body)

    def test_anonymous_user_cannot_add(self):
        res = self.testapp.get('/add_post/', status=200)
        self.assertTrue(b'Login' in res.body)

    def test_viewer_user_cannot_edit(self):
        self.testapp.get(self.viewer_login, status=302)
        res = self.testapp.get('/1/edit_post', status=200)
        self.assertTrue(b'Login' in res.body)

    def test_viewer_user_cannot_add(self):
        self.testapp.get(self.viewer_login, status=302)
        res = self.testapp.get('/add_post/', status=200)
        self.assertTrue(b'Login' in res.body)

    def test_editors_member_user_can_edit(self):
        self.testapp.get(self.editor_login, status=302)
        res = self.testapp.get('/1/edit_post', status=200)
        self.assertTrue(b'Edit post' in res.body)

    def test_editors_member_user_can_add(self):
        self.testapp.get(self.editor_login, status=302)
        res = self.testapp.get('/add_post/', status=200)
        self.assertTrue(b'Edit post' in res.body)

    def test_editors_member_user_can_view(self):
        self.testapp.get(self.editor_login, status=302)
        res = self.testapp.get('/', status=200)
