class CommonTitleMixin:
    title = None

    def det_context_data(self, **kwargs):
        context = super(CommonTitleMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context
