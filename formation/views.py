from django.views import generic


class IndexView(generic.RedirectView):
    url = '/forms/'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
