from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.form.interfaces import IEditForm, IAddForm
from zope import schema
from plone.autoform import directives as form
from zope.component import adapts
from zope.interface import alsoProvides, implements

from funlog.behavior import MessageFactory as _


class ISetTitleOnly(model.Schema):
    """
       Marker/Form interface for SetTitleOnly
    """

    # -*- Your Zope schema definitions here ... -*-
    title = schema.TextLine(
        title=_(u'label_title', default=u'Title'),
        required=True
    )

    form.order_before(title='*')

    form.omitted('title')
    form.no_omit(IEditForm, 'title')
    form.no_omit(IAddForm, 'title')




alsoProvides(ISetTitleOnly, IFormFieldProvider)

def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name, value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)



class SetTitleOnly(object):
    """
       Adapter for SetTitleOnly
    """
    implements(ISetTitleOnly)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-

    def _get_title(self):
        return self.context.title

    def _set_title(self, value):
        if isinstance(value, str):
            raise ValueError('Title must be unicode.')
        self.context.title = value
    title = property(_get_title, _set_title)
