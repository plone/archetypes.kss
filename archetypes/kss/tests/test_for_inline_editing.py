from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from kss.core.BeautifulSoup import BeautifulSoup
from Products.Five.testbrowser import Browser

ZOPE_DEPS = []
PLONE_DEPS = []
#ZOPE_DEPS = ['MyZopeProductDependecy']
#PLONE_DEPS = ['MyPloneProduct',
#              'MyPloneDependency']

for x in ZOPE_DEPS + PLONE_DEPS:
    ztc.installProduct(x)
ptc.setupPloneSite(products=PLONE_DEPS)

class TestForKSSInlineEditing(ptc.FunctionalTestCase):
    """
    Ok, this is a strange case of doctest: actually, we are able to use
    self inside the doctests, but the import stuff is still quite broken,
    hence the abundance of function that do just one libne of code or so
    (take a look at Daniel Nouri's blog for more details)
    """
    
    
    def afterSetUp(self):
        self.folder.invokeFactory('Document', 'page')
        self.page = self.folder.page
        self.page.setTitle('My title')
        self.page.setDescription('My description')
        self.page.setText('<p>My text</p>')
        self.user = ptc.default_user
        self.password = ptc.default_password
        self.browser = Browser()
      
    def test_notLogged():
        r"""
        
        We import some stuff, else we're not gonna go anywhere
        cause the import is more broken than Saddam's neck
        
          >>> from kss.core.BeautifulSoup import BeautifulSoup
        
        We call the page
        
          >>> self.browser.open(self.page.absolute_url())
          >>> soup = BeautifulSoup(self.browser.contents)
        
        We find the title tag
        
          >>> title = soup.find('h1', attrs = { 'id': 'parent-fieldname-title' })
          >>> title is not None
          True
        
        We see that the KSS hooks shouldn't be there because we're not logged in!
        
          >>> 'kssattr-atfieldname-' in title['class']
          False
          >>> 'kssattr-templateId-' in title['class']
          False
          >>> 'kssattr-macro-' in title['class']
          False
        """

    def test_logged():
        r"""
        
        All the usual setup
        
          >>> from kss.core.BeautifulSoup import BeautifulSoup
        
        Okay, we don't go straight away for the page but we actually do authenticate
        
          >>> self.browser.addHeader('Authorization', 'Basic %s:%s' % (self.user, self.password))
          >>> self.browser.open(self.page.absolute_url())
          >>> soup = BeautifulSoup(self.browser.contents)
        
        We find the title
        
          >>> title = soup.find('h1', attrs = { 'id': 'parent-fieldname-title' })
          >>> title is not None
          True
        
        We check everything is in now, especially that kssattr-fieldname- matched the right field,
        and is not only there, but actually makes some sense
        
          >>> 'kssattr-atfieldname-title' in title['class']
          True
          >>> 'kssattr-templateId-' in title['class']
          True
          >>> 'kssattr-macro-' in title['class']
          True
        
        Rerun, description now! (which is not a Francis Ford Coppola's movie)
        
          >>> description = soup.find('p', attrs = { 'id': 'parent-fieldname-description' })
          >>> description is not None
          True
          >>> 'kssattr-atfieldname-description' in description['class']
          True
          >>> 'kssattr-templateId-' in description['class']
          True
          >>> 'kssattr-macro-' in description['class']
          True
        
        Now, time for the text
        
          >>> text = soup.find('div', attrs = { 'id': 'parent-fieldname-text' })
          >>> text is not None
          True
          >>> 'kssattr-atfieldname-text' in text['class']
          True
          >>> 'kssattr-templateId-' in text['class']
          True
          >>> 'kssattr-macro-' in text['class']
          True
        """

def test_suite():
    suite = ztc.FunctionalDocTestSuite(test_class=TestForKSSInlineEditing)
    suite.layer = PloneSite
    return suite
