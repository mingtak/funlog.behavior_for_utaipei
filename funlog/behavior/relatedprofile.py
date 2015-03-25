from five import grok
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from plone.directives import form
from zope.component import adapts
from zope.interface import alsoProvides, implements
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from zope.schema.interfaces import IContextSourceBinder
#from z3c.relationfield.relation import RelationValue


from funlog.behavior import MessageFactory as _

#from funlog.content.profile import IProfile


@grok.provider(IContextSourceBinder)
def getProfileBinder(context):
    return ObjPathSourceBinder(Type="Profile", Creator=context.owner_info()["id"]).__call__(context)

class IRelatedProfile(model.Schema):
    """
       Marker/Form interface for RelatedProfile
    """
    form.omitted("relatedProfile")
    relatedProfile = RelationChoice(
        title=_(u"Related profile"),
        source=getProfileBinder,
        required=False,
    )


alsoProvides(IRelatedProfile, IFormFieldProvider)

def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name, value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)


class RelatedProfile(object):
    """
       Adapter for RelatedProfile
    """
    implements(IRelatedProfile)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    relatedProfile = context_property('relatedProfile')
