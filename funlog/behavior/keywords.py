from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from plone.directives import form
from zope.component import adapts
from zope.interface import alsoProvides, implements

from funlog.behavior import MessageFactory as _


class IKeywords(model.Schema):
    """
       Marker/Form interface for Keywords
    """
    form.fieldset(
        'Keywords',
        label=_(u"Keywords"),
        fields=['keywords'],
        description=_(u"Setup keywords for this content."),
    )

    keywords = schema.TextLine(
        title=_(u"Keywords"),
        description=_(u"Separated by commas, for example: 'travel,taipei,outdoor'."),
        required=False,
    )


alsoProvides(IKeywords, IFormFieldProvider)

def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name, value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)


class Keywords(object):
    """
       Adapter for Keywords
    """
    implements(IKeywords)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    keywords = context_property('keywords')
