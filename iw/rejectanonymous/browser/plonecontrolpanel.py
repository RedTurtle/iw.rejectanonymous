# -*- coding: utf-8 -*-
# Copyright (C) 2008 Ingeniweb

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""Add a new "Private Site" control panel to manage the new option
"""
from iw.rejectanonymous import _
from iw.rejectanonymous import IPrivateSite
from iw.rejectanonymous import logger
from plone import api
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.supermodel import model
from Products.Five.utilities.marker import mark, erase
from z3c.form import button
from zope import schema


class IPrivateSiteSchema(model.Schema):
    private_site = schema.Bool(
        title=_(u'Private site'),
        description=_(u"Users must login to view the site. Anonymous users are presented the login form."),  # noqa
        default=False,
        required=False,
    )


class IPrivateSiteSettings(IPrivateSiteSchema):
    """
    Marker interface for settings
    """


class PrivateSiteSettingsEditForm(RegistryEditForm):
    schema = IPrivateSiteSettings
    label = _(u"Reject Anonymous settings")

    @button.buttonAndHandler(_(u"Save"), name='save')
    def handleSave(self, action):
        private_selected = not api.portal.get_registry_record('iw.rejectanonymous.browser.plonecontrolpanel.IPrivateSiteSettings.private_site')  # noqa
        site = api.portal.get()
        if private_selected:
            mark(site, IPrivateSite)
            logger.info("The site has been set private.")
        else:
            erase(site, IPrivateSite)
            logger.info("The site has been set public.")

        super(PrivateSiteSettingsEditForm, self).handleSave(self, action)

    @button.buttonAndHandler(_(u"Cancel"), name='cancel')
    def handleCancel(self, action):
        super(PrivateSiteSettingsEditForm, self).handleCancel(self, action)


class PrivateSiteSettingsView(ControlPanelFormWrapper):
    form = PrivateSiteSettingsEditForm
