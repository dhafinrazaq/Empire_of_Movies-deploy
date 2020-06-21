from django.views.generic import TemplateView
class HomePageView(TemplateView):
    template_name = 'home.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'privacy_policy.html'