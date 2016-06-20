from plone.app.layout.viewlets.content import DocumentBylineViewlet


class BaselDocumentBylineViewlet(DocumentBylineViewlet):

    def show(self):
        if self.request.get('disable_border', False):
            return False
        return super(BaselDocumentBylineViewlet, self).show()
