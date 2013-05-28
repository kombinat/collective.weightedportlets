from Acquisition import aq_inner
from Products.Five import BrowserView
from collective.weightedportlets import ATTR, ATTR
from collective.weightedportlets.utils import ReplacingViewPageTemplateFile
from persistent.dict import PersistentDict
from plone.app.portlets.browser import manage as base
from plone.app.portlets.browser.editmanager import ManagePortletAssignments
from plone.app.portlets.interfaces import IPortletPermissionChecker
from plone.app.portlets.utils import assignment_mapping_from_key
from plone.portlets.utils import unhashPortletInfo
from zope.interface import implements, Interface
import plone.app.portlets.browser


class PortletWeightInfo(BrowserView):

    def portlet_weight(self, renderer, portlet_index):
        assignments = renderer._lazyLoadAssignments(renderer.manager)
        assignment = assignments[portlet_index]
        return getattr(assignment, ATTR, {}).get('weight', 50)


class ManageContextualPortlets(base.ManageContextualPortlets):

    index = ReplacingViewPageTemplateFile(
        module=plone.app.portlets.browser,
        filename='templates/edit-manager-macros.pt',
        regexp=r'<span class="managedPortletActions">',
        replacement="""
<span class="managedPortletActions">
<input type="text" size="1" class="weight" title="Portlet Weight"
    tal:define="weight_info nocall:context/@@portlet-weight-info"
    tal:attributes="value python:weight_info.portlet_weight(view, repeat['portlet'].index)"
    i18n:domain="collective.weightedportlets"
    i18n:attributes="title"/>
        """
    )


class PortletManager(ManagePortletAssignments):
    def change_portlet_weight(self, portlethash, viewname, weight):
        try:
            weight = int(weight)
        except ValueError:
            return self._render_column()

        info = unhashPortletInfo(portlethash)
        assignments = assignment_mapping_from_key(
            self.context, info['manager'], info['category'], info['key']
        )

        IPortletPermissionChecker(assignments.__of__(aq_inner(self.context)))()

        name = info['name']
        if not hasattr(assignments[name], ATTR):
            setattr(assignments[name], ATTR, PersistentDict())
        getattr(assignments[name], ATTR)['weight'] = weight
        return "done"
