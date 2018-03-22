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
from plone.supermodel import model
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from zope import schema
from z3c.form import group
from z3c.form import field

from zope.component import getGlobalSiteManager
from zope.interface import alsoProvides
from zope.interface import classImplementsOnly
from zope.interface import implementedBy
from zope.interface import noLongerProvides
from z3c.form import field
from zope.interface import Interface
# from zope.formlib.form import FormFields

# from plone.app.controlpanel.security import SecurityControlPanel
from Products.CMFPlone.controlpanel.browser.security import SecurityControlPanel  # noqa

# from plone.app.controlpanel.security import SecurityControlPanelAdapter
from Products.CMFPlone.controlpanel.bbb.security import SecurityControlPanelAdapter  # noqa

# from plone.app.controlpanel.security import ISecuritySchema
from Products.CMFPlone.interfaces import ISecuritySchema


from iw.rejectanonymous import IPrivateSite


class IPrivateSiteSchema(model.Schema):
    private_site = schema.Bool(
        title=u'Private site',
        description=u"Users must login to view the site. Anonymous users "
                    u"are presented the login form",
        default=False,
        required=False,
    )


class PrivateSiteSettingsEditForm(RegistryEditForm):
    schema = IPrivateSiteSchema
    label = u"Private site settings"


class PrivateSiteSettingsView(ControlPanelFormWrapper):
    form = PrivateSiteSettingsEditForm


# add accessors to adapter

def get_private_site(self):
    return IPrivateSite.providedBy(self.portal)


SecurityControlPanelAdapter.get_private_site = get_private_site


def set_private_site(self, value):
    operator = value and alsoProvides or noLongerProvides
    operator(self.portal, IPrivateSite)


SecurityControlPanelAdapter.set_private_site = set_private_site

SecurityControlPanelAdapter.private_site = property(
    SecurityControlPanelAdapter.get_private_site,
    SecurityControlPanelAdapter.set_private_site
)

# re-register adapter with new interface
_decl = implementedBy(SecurityControlPanelAdapter)
_decl -= ISecuritySchema
_decl += IPrivateSiteSchema
classImplementsOnly(SecurityControlPanelAdapter, _decl.interfaces())
del _decl

getGlobalSiteManager().registerAdapter(SecurityControlPanelAdapter)

# re-instanciate form
# SecurityControlPanel.form_fields = FormFields(IPrivateSiteSchema)


# (Pdb) field.Fields(IPrivateSiteSchema).items()
# [('enable_self_reg', <Field 'enable_self_reg'>), ('enable_user_pwd_choice', <Field 'enable_user_pwd_choice'>), ('enable_user_folders', <Field 'enable_user_folders'>), ('allow_anon_views_about', <Field 'allow_anon_views_about'>), ('use_email_as_login', <Field 'use_email_as_login'>), ('use_uuid_as_userid', <Field 'use_uuid_as_userid'>), ('private_site', <Field 'private_site'>)]

SecurityControlPanel.form.fields += field.Fields(IPrivateSiteSchema)
