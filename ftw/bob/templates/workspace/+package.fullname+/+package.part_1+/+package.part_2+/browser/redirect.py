from Products.Five.browser import BrowserView


class RedirectToWorkspaces(BrowserView):

    def __call__(self):
        return self.request.RESPONSE.redirect(
            self.context.workspaces.absolute_url())
