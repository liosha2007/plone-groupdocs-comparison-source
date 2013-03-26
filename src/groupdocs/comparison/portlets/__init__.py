from zope.i18nmessageid import MessageFactory
PloneMessageFactory = MessageFactory('plone')

from Products.CMFCore.permissions import setDefaultRoles
setDefaultRoles('comparison.portlets.gdcomparison: Add GroupDocs Comparison portlet',
                ('Manager', 'Site Administrator', 'Owner',))
