#!/usr/bin/env python
from AccessControl.SecurityManagement import newSecurityManager
from Testing.makerequest import makerequest
from ftw.inflator.bundle import get_bundles
from ftw.lawgiver.interfaces import IUpdater
from ftw.lawgiver.interfaces import IWorkflowSpecificationDiscovery
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.hooks import setSite

ZOPE_URL = 'http://localhost:8080'
PLONE_URL = '{}/platform'.format(ZOPE_URL)

app=makerequest(app)

bundle = get_bundles()[0]

plone = app.unrestrictedTraverse('platform', None)
if not plone:
    plone = bundle.install(app, 'platform', title='Thor Odinson', language="en")

user = app.acl_users.getUser('admin')
user = user.__of__(app.acl_users)
newSecurityManager(app, user)

#setup site
setSite(plone)

discovery = getMultiAdapter((plone, plone.REQUEST), IWorkflowSpecificationDiscovery)
updater = getUtility(IUpdater)
updater.write_workflow(discovery.discover()[0])
