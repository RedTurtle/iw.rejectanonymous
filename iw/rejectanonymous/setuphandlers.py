# -*- coding: utf-8 -*-
from iw.rejectanonymous import IPrivateSite
from iw.rejectanonymous import logger
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from Products.Five.utilities.marker import erase
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'iw.rejectanonymous:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.


def uninstall(context):
    """Uninstall script"""
    site = api.portal.get()
    erase(site, IPrivateSite)
    logger.info("iw.rejectanonymous:uninstall - The site has been set public.")
    # Do something at the end of the uninstallation of this package.
