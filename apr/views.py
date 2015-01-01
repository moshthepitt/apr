from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'appointments/home.html'

home = HomeView.as_view()
