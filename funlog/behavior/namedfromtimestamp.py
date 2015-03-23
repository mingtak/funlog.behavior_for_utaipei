from plone.app.content.interfaces import INameFromTitle
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapts
from zope.interface import alsoProvides, implements

from DateTime import DateTime
import urllib
from Products.CMFPlone.utils import safe_unicode

from funlog.behavior import MessageFactory as _


class INamedFromTimeStamp(INameFromTitle):
    """
       Marker/Form interface for NamedFromTimeStamp
    """

    # -*- Your Zope schema definitions here ... -*-


class NamedFromTimeStamp(object):
    """
       Adapter for NamedFromTimeStamp
    """
    implements(INamedFromTimeStamp)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    @property
    def title(self):
        timeString = DateTime().strftime("%Y%m%d%H%M")
        return timeString
