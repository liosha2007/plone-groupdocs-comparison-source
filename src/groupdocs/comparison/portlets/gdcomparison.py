import logging

from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from plone.app.portlets.portlets import base
from zope import schema
from zope.interface import implements
from zope.component import getUtility
from zope.formlib import form

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.portlet.static import PloneMessageFactory as _

logger = logging.getLogger('groupdocs.comparison')


class IGDComparisonPortlet(IPortletDataProvider):
    """A portlet which renders predefined static HTML.

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the GroupDocs Comparison portlet"),
        required=True)

    fileid = schema.TextLine(
        title=_(u"File ID"),
        description=_(u"GUID of the shared file from GroupDocs account"),
        required=True)

    compareKey = schema.TextLine(
        title=_(u"Compare KEY"),
        description=_(u"Compare KEY from GroupDocs account"),
        required=True)

    width = schema.TextLine(
        title=_(u"Width"),
        description=_(u"Width of the Comparison"),
        required=True)
        
    height = schema.TextLine(
        title=_(u"Height"),
        description=_(u"Height of the Comparison"),
        required=True)

    omit_border = schema.Bool(
        title=_(u"Omit portlet border"),
        description=_(u"Tick this box if you want to render the text above "
                      "without the standard header, border or footer."),
        required=True,
        default=False)

    footer = schema.TextLine(
        title=_(u"Portlet footer"),
        description=_(u"Text to be shown in the footer"),
        required=False)

    more_url = schema.ASCIILine(
        title=_(u"Details link"),
        description=_(u"If given, the header and footer "
                      "will link to this URL."),
        required=False)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IGDComparisonPortlet)

    header = _(u"title_gdcomparison_portlet", default=u"GroupDocs Comparison portlet")
    fileid = u""
    compareKey = u""
    width = u""
    height = u""
    omit_border = False
    footer = u""
    more_url = ''

    def __init__(self, header=u"", fileid=u"", compareKey=u"", width=u"", height=u"", omit_border=False, footer=u"",
                 more_url=''):
        self.header = header
        self.fileid = fileid
        self.compareKey = compareKey
        self.width = width
        self.height = height
        self.omit_border = omit_border
        self.footer = footer
        self.more_url = more_url

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('gdcomparison.pt')

    def css_class(self):
        """Generate a CSS class from the portlet header
        """
        header = self.data.header
        normalizer = getUtility(IIDNormalizer)
        return "portlet-static-%s" % normalizer.normalize(header)

    def has_link(self):
        return bool(self.data.more_url)

    def has_footer(self):
        return bool(self.data.footer)

    def transformed(self, mt='text/x-html-safe'):
        """Transform imput data to get iframe code for GroupDocs Embedded Comparison.
        """
        frame_source = '<iframe src="http://apps.groupdocs.com/document-comparison/embed/' + self.data.compareKey + '/' + self.data.fileid + '" frameborder="0" width="' + self.data.width + '" height="' + self.data.height + '"></iframe>'

        if frame_source:
            return frame_source
        return None


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IGDComparisonPortlet)
    label = _(u"title_add_comparison_portlet",
              default=u"Add groupdocs comparison portlet")
    description = _(u"description_comparison_portlet",
                    default=u"A portlet which can display GroupDocs Embedded Viwer.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IGDComparisonPortlet)
    label = _(u"title_edit_comparison_portlet",
              default=u"Edit GroupDocs Comparison portlet")
    description = _(u"description_comparison_portlet",
                    default=u"A portlet which can display GroupDocs Embedded Viwer.")
