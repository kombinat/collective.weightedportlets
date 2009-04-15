from zope.interface import Interface
from zope.component import getSiteManager
from plone.portlets.interfaces import IPortletManager, IPortletRetriever

def uninstall(portal):
    getSiteManager(context=portal).unregisterAdapter(required=(Interface, IPortletManager), provided=IPortletRetriever)
