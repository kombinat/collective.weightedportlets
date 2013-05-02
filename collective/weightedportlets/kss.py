from zope.interface import implements, Interface

from Acquisition import aq_inner
from persistent.dict import PersistentDict

from plone.portlets.utils import unhashPortletInfo
from plone.app.portlets.utils import assignment_mapping_from_key
from plone.app.portlets.interfaces import IPortletPermissionChecker

from collective.weightedportlets import ATTR

try:
    from plone.app.kss.interfaces import IPloneKSSView
    from plone.app.portlets.browser.kss import PortletManagerKSS as BasePortletManagerKSS
except ImportError:
    IPloneKSSView = Interface
    BasePortletManagerKSS = object

try:
    from plone.app.portlets.browser.editmanager import ManagePortletAssignments
except ImportError:
    ManagePortletAssignments = object


class PortletManagerNonKSS(ManagePortletAssignments):
    def change_portlet_weight(self, portlethash, viewname, weight):
        try:
            weight = int(weight)
        except ValueError:
            #kss_plone = self.getCommandSet('plone')
            #msg = 'You must enter an integer for the portlet weight.'
            #kss_plone.issuePortalMessage(msg, msgtype='error')
            #return self.render()
            import pdb; pdb.set_trace()

        info = unhashPortletInfo(portlethash)
        assignments = assignment_mapping_from_key(
            self.context, info['manager'], info['category'], info['key']
        )

        IPortletPermissionChecker(assignments.__of__(aq_inner(self.context)))()

        name = info['name']
        if not hasattr(assignments[name], ATTR):
            setattr(assignments[name], ATTR, PersistentDict())
        getattr(assignments[name], ATTR)['weight'] = weight
        return self._render_column(info, viewname)

class PortletManagerKSS(BasePortletManagerKSS):
    """Opertions on portlets done using KSS
    """
    implements(IPloneKSSView)

    def change_portlet_weight(self, portlethash, viewname, weight):
        try:
            weight = int(weight)
        except ValueError:
            kss_plone = self.getCommandSet('plone')
            msg = 'You must enter an integer for the portlet weight.'
            kss_plone.issuePortalMessage(msg, msgtype='error')
            return self.render()

        info = unhashPortletInfo(portlethash)
        assignments = assignment_mapping_from_key(
            self.context, info['manager'], info['category'], info['key']
        )

        IPortletPermissionChecker(assignments.__of__(aq_inner(self.context)))()

        name = info['name']
        if not hasattr(assignments[name], ATTR):
            setattr(assignments[name], ATTR, PersistentDict())
        getattr(assignments[name], ATTR)['weight'] = weight
        return self._render_column(info, viewname)

PortletManager = None
if BasePortletManagerKSS is not object:
    PortletManager = PortletManagerKSS
else:
    PortletManager = PortletManagerNonKSS
