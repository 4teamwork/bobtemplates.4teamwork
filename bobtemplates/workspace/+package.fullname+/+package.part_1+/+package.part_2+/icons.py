from ftw.upgrade.interfaces import IPostUpgrade
from plone import api
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


def remove_icon_expressions():
    types_tool = api.portal.get_tool(name='portal_types')

    for fti in types_tool.objectValues():
        if fti.icon_expr:
            fti.manage_changeProperties(icon_expr='')


def remove_icon_expressions_when_profile_installed(portal):
    remove_icon_expressions()


@implementer(IPostUpgrade)
@adapter(IPloneSiteRoot, Interface)
def post_upgrade_remove_icon_expression_factory(context, request):
    return remove_icon_expressions
