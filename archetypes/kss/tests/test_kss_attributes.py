from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from kss.core.BeautifulSoup import BeautifulSoup
from Products.Five.testbrowser import Browser

class TestKSSAttributes(ptc.FunctionalTestCase):
    
    BeautifulSoup = BeautifulSoup

    def afterSetUp(self):
        self.folder.invokeFactory('Document', 'page')
        self.page = self.folder.page
        self.page.setTitle('My title')
        self.page.setDescription('My description')
        self.page.setText('<p>My text</p>')
        self.user = ptc.default_user
        self.password = ptc.default_password
        self.browser = Browser()

class TestForKSSInlineEditing:
      
    def test_notLogged():
        r"""
        
        We call the page
        
          >>> self.browser.open(self.page.absolute_url())
          >>> soup = self.BeautifulSoup(self.browser.contents)
        
        We find the title tag
        
          >>> title = soup.find('h1', attrs=dict(id='parent-fieldname-title'))
          >>> title is not None
          True
        
        We see that the KSS hooks shouldn't be there because we're not
        logged in!
        
          >>> 'kssattr-atfieldname-' in title['class']
          False
          >>> 'kssattr-templateId-' in title['class']
          False
          >>> 'kssattr-macro-' in title['class']
          False
        """

    def test_logged():
        r"""
        
        Okay, we don't go straight away for the page but we actually
        do authenticate
        
          >>> self.browser.addHeader(
          ...    'Authorization', 'Basic %s:%s' % (self.user, self.password))
          >>> self.browser.open(self.page.absolute_url())
          >>> soup = self.BeautifulSoup(self.browser.contents)
        
        We find the title
        
          >>> title = soup.find('h1', dict(id='parent-fieldname-title'))
          >>> title is not None
          True
        
        We check everything is in now, especially that
        ``kssattr-fieldname-`` matched the right field, and is not
        only there, but actually makes some sense
        
          >>> 'kssattr-atfieldname-title' in title['class']
          True
          >>> 'kssattr-templateId-' in title['class']
          True
          >>> 'kssattr-macro-' in title['class']
          True
        
        Rerun, description now! (which is not a Francis Ford Coppola's
        movie)
        
          >>> description = soup.find(
          ...    'p', dict(id='parent-fieldname-description'))
          >>> description is not None
          True
          >>> 'kssattr-atfieldname-description' in description['class']
          True
          >>> 'kssattr-templateId-' in description['class']
          True
          >>> 'kssattr-macro-' in description['class']
          True
        
        Now, time for the text
        
          >>> text = soup.find('div', attrs=dict(id='parent-fieldname-text'))
          >>> text is not None
          True
          >>> 'kssattr-atfieldname-text' in text['class']
          True
          >>> 'kssattr-templateId-' in text['class']
          True
          >>> 'kssattr-macro-' in text['class']
          True
        """

class TestContentsTabs:
    def test_tab_ids():
        """
        Okay, we don't go straight away for the page but we actually
        do authenticate
        
          >>> self.browser.addHeader(
          ...    'Authorization', 'Basic %s:%s' % (self.user, self.password))
          >>> self.browser.open(self.page.absolute_url())
          >>> soup = self.BeautifulSoup(self.browser.contents)
        
        The content tabs must have li tags with special ids:

          >>> li = soup.find('li', attrs=dict(id='contentview-folderContents'))
          >>> li is not None
          True
	"""

def test_suite():
    suite = ztc.FunctionalDocTestSuite(test_class=TestKSSAttributes)
    suite.layer = PloneSite
    return suite
