from five import grok
from plone import api
from plone.app.content.interfaces import INameFromTitle
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from plone.directives import form
from zope.component import adapts
from zope.interface import alsoProvides, implements, Invalid, Interface
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from DateTime import DateTime
import urllib
from Products.CMFPlone.utils import safe_unicode

from funlog.behavior import MessageFactory as _


def checkContentUrl(value):
    if not value.replace('-', '').isalnum():
        raise Invalid(_(u"Wrong value, only allow english character, number and '-' "))
    return True


class INamedFromTimeStamp(INameFromTitle):
    """
       Marker/Form interface for NamedFromTimeStamp
    """

    form.fieldset('Content URL',
            label=u"Set content url",
            fields=['contentUrl', 'title']
        )

    contentUrl = schema.TextLine(
        title=_(u'Content url'),
        description=_(u'help_contentUrl',
                       default=u"only allow english, number and '-', default value is time stamp, if this url already in use, than don't change."),
        required=False,
        constraint=checkContentUrl
    )

    form.omitted('title')
    title = schema.TextLine(
        title=_(u'title'),
        required=False,
    )


alsoProvides(INamedFromTimeStamp, IFormFieldProvider)

def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name, value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)


class NamedFromTimeStamp(object):
    """
       Adapter for NamedFromTimeStamp
    """
    implements(INamedFromTimeStamp)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    @property
    def title(self):
        context = self.context
        if context.contentUrl is not None:
            return context.contentUrl
        timeString = DateTime().strftime("%Y%m%d%H%M")
        return timeString

    contentUrl = context_property('contentUrl')


@grok.subscribe(Interface, IObjectModifiedEvent)
def object_edited(context, event):
    if not hasattr(context, 'contentUrl'):
        return
    if context.contentUrl is None:
        urlString = str(DateTime().strftime("%Y%m%d%H%M"))
    elif context.getId() != context.contentUrl:
        urlString = context.contentUrl
    else:
        return
    try:
        api.content.rename(obj=context, new_id=str(urlString))
    except:
        pass
