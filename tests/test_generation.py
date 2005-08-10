#
#  test_generation
#
#  Created by Ben Bangert on 2005-08-08.
#  Copyright (c) 2005 Parachute. All rights reserved.
#

import routes
import unittest
from routes import Mapper

class TestGeneration(unittest.TestCase):
    def test_all_static_no_reqs(self):
        m = Mapper()
        m.connect('hello/world')
        
        self.assertEqual('/hello/world', m.generate())
    
    def test_basic_dynamic(self):
        m = Mapper()
        m.connect('hi/:fred')
        
        self.assertEqual('/hi/index', m.generate(fred='index'))
        self.assertEqual('/hi/show', m.generate(fred='show'))
        self.assertEqual('/hi/list+people', m.generate(fred='list people'))
        self.assertEqual(None, m.generate())
    
    def test_dynamic_with_default(self):
        m = Mapper()
        m.connect('hi/:action')
        
        self.assertEqual('/hi', m.generate(action='index'))
        self.assertEqual('/hi/show', m.generate(action='show'))
        self.assertEqual('/hi/list+people', m.generate(action='list people'))
        self.assertEqual('/hi', m.generate())
    
    def test_dynamic_with_regexp_condition(self):
        m = Mapper()
        m.connect('hi/:name', requirements = {'name':'[a-z]+'})
        
        self.assertEqual('/hi/index', m.generate(name='index'))
        self.assertEqual(None, m.generate(name='fox5'))
        self.assertEqual(None, m.generate(name='something_is_up'))
        self.assertEqual('/hi/abunchofcharacter', m.generate(name='abunchofcharacter'))
        self.assertEqual(None, m.generate())
    
    def test_dynamic_with_default_and_regexp_condition(self):
        m = Mapper()
        m.connect('hi/:action', requirements = {'action':'[a-z]+'})
        
        self.assertEqual('/hi', m.generate(action='index'))
        self.assertEqual(None, m.generate(action='fox5'))
        self.assertEqual(None, m.generate(action='something_is_up'))
        self.assertEqual(None, m.generate(action='list people'))
        self.assertEqual('/hi/abunchofcharacter', m.generate(action='abunchofcharacter'))
        self.assertEqual('/hi', m.generate())
    
    def test_path(self):
        m = Mapper()
        m.connect('hi/*file')
        
        self.assertEqual('/hi', m.generate(file=None))
        self.assertEqual('/hi/books/learning_python.pdf', m.generate(file='books/learning_python.pdf'))
        self.assertEqual('/hi/books/development%26whatever/learning_python.pdf', m.generate(file='books/development&whatever/learning_python.pdf'))
    
    def test_path_backwards(self):
        m = Mapper()
        m.connect('*file/hi')

        self.assertEqual('/hi', m.generate(file=None))
        self.assertEqual('/books/learning_python.pdf/hi', m.generate(file='books/learning_python.pdf'))
        self.assertEqual('/books/development%26whatever/learning_python.pdf/hi', m.generate(file='books/development&whatever/learning_python.pdf'))
    
    def test_controller(self):
        m = Mapper()
        m.connect('hi/:controller')
        
        self.assertEqual(None, m.generate())
        self.assertEqual('/hi/content', m.generate(controller='content'))
        self.assertEqual('/hi/admin/user', m.generate(controller='admin/user'))
    
    def test_standard_route(self):
        m = Mapper()
        m.connect(':controller/:action/:id')
        
        self.assertEqual('/content', m.generate(controller='content', action='index'))
        self.assertEqual('/content/list', m.generate(controller='content', action='list'))
        self.assertEqual('/content/show/10', m.generate(controller='content', action='show', id ='10'))
        
        self.assertEqual('/admin/user', m.generate(controller='admin/user', action='index'))
        self.assertEqual('/admin/user/list', m.generate(controller='admin/user', action='list'))
        self.assertEqual('/admin/user/show/10', m.generate(controller='admin/user', action='show', id='10'))
    
    def test_multiroute(self):
        m = Mapper()
        m.connect('archive/:year/:month/:day', controller='blog', action='view', month=None, day=None,
                            requirements={'month':'\d{1,2}','day':'\d{1,2}'})
        m.connect('viewpost/:id', controller='post', action='view')
        m.connect(':controller/:action/:id')
        
        self.assertEqual('/blog/view', m.generate(controller='blog', action='view', year=2004, month='blah'))
        self.assertEqual('/archive/2004', m.generate(controller='blog', action='view', year=2004))
        self.assertEqual('/viewpost/3', m.generate(controller='post', action='view', id=3))
    
    def test_static(self):
        m = Mapper()
        m.connect('hello/world',known='known_value',controller='content',action='index')
        
        self.assertEqual('/hello/world', m.generate(controller='content',action= 'index',known ='known_value'))
        self.assertEqual('/hello/world', m.generate(controller='content',action='index',known='known_value',extra='hi'))
        
        self.assertEqual(None, m.generate(known='foo'))
    
    def test_dynamic(self):
        m = Mapper()
        m.connect('hello/:name', controller='content', action='show_person')
        
        self.assertEqual('/hello/rails', m.generate(controller='content', action='show_person',name='rails'))
        self.assertEqual('/hello/Alfred+Hitchcock', m.generate(controller='content', action='show_person',name='Alfred Hitchcock'))
        
        self.assertEqual(None, m.generate(controller='content', action='show_dude', name='rails'))
        self.assertEqual(None, m.generate(controller='content', action='show_person'))
        self.assertEqual(None, m.generate(controller='admin/user', action='show_person', name='rails'))
    
    def test_typical(self):
        m = Mapper()
        m.connect(':controller/:action/:id', action = 'index', id = None)
        
        self.assertEqual('/content', m.generate(controller='content', action='index'))
        self.assertEqual('/content/list', m.generate(controller='content', action='list'))
        self.assertEqual('/content/show/10', m.generate(controller='content', action='show', id=10))
        
        self.assertEqual('/admin/user', m.generate(controller='admin/user', action='index'))
        self.assertEqual('/admin/user', m.generate(controller='admin/user'))
        self.assertEqual('/admin/user/show/10', m.generate(controller='admin/user', action='show', id=10))
        
        self.assertEqual('/content', m.generate(controller='content'))
    
    def test_route_with_fixnum_default(self):
        m = Mapper()
        m.connect('page/:id', controller='content', action='show_page', id =1)
        m.connect(':controller/:action/:id')
        
        self.assertEqual('/page', m.generate(controller='content', action='show_page'))
        self.assertEqual('/page', m.generate(controller='content', action='show_page', id=1))
        self.assertEqual('/page', m.generate(controller='content', action='show_page', id='1'))
        self.assertEqual('/page/10', m.generate(controller='content', action='show_page', id=10))
        
        self.assertEqual('/blog/show/4', m.generate(controller='blog', action='show', id=4))
        self.assertEqual('/page', m.generate(controller='content'))
        self.assertEqual('/page/4', m.generate(controller='content',id=4))
        self.assertEqual('/content/show', m.generate(controller='content', action='show'))
    
    def test_uppercase_recognition(self):
        m = Mapper()
        m.connect(':controller/:action/:id')

        self.assertEqual('/Content', m.generate(controller='Content', action='index'))
        self.assertEqual('/Content/list', m.generate(controller='Content', action='list'))
        self.assertEqual('/Content/show/10', m.generate(controller='Content', action='show', id='10'))

        self.assertEqual('/Admin/NewsFeed', m.generate(controller='Admin/NewsFeed', action='index'))
    
    def test_backwards(self):
        m = Mapper()
        m.connect('page/:id/:action', controller='pages', action='show')
        m.connect(':controller/:action/:id')

        self.assertEqual('/page/20', m.generate(id=20))
        self.assertEqual('/page/20', m.generate(controller='pages', id=20, action='show'))
        self.assertEqual('/pages/boo', m.generate(controller='pages', action='boo'))
    
    def test_both_requirement_and_optional(self):
        m = Mapper()
        m.connect('test/:year', controller='post', action='show', year=None, requirements = {'year':'\d{4}'})

        self.assertEqual('/test', m.generate(controller='post', action='show'))
        self.assertEqual('/test', m.generate(controller='post', action='show', year=None))
    
    def test_set_to_nil_forgets(self):
        m = Mapper()
        m.connect('pages/:year/:month/:day', controller='content', action='list_pages', month=None, day=None)
        m.connect(':controller/:action/:id')

        self.assertEqual('/pages/2005', m.generate(controller='content', action='list_pages', year=2005))
        self.assertEqual('/pages/2005/6', m.generate(controller='content', action='list_pages', year=2005, month=6))
        self.assertEqual('/pages/2005/6/12', m.generate(controller='content', action='list_pages', year=2005, month=6, day=12))
    
    def test_url_with_no_action_specified(self):
        m = Mapper()
        m.connect('', controller='content')
        m.connect(':controller/:action/:id')

        self.assertEqual('/', m.generate(controller='content', action='index'))
        self.assertEqual('/', m.generate(controller='content'))
    

if __name__ == '__main__':
    unittest.main()