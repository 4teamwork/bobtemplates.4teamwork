#!/usr/bin/env python
from Testing.makerequest import makerequest
from ftw.inflator.bundle import get_bundles
import transaction


ZOPE_URL = 'http://localhost:8080'
PLONE_URL = '{}/platform'.format(ZOPE_URL)

app=makerequest(app)

bundle = get_bundles()[0]

plone = app.unrestrictedTraverse('platform', None)

if not plone:
    plone = bundle.install(app, 'platform', title='Thor Odinson', language="en")
    transaction.commit()
