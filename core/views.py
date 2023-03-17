from django.shortcuts import render
from django.views import View

# Create your views here.

class HomeView(View):
    template_name = '_welcomepage.html'

    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated:
        #     return ''
        return render(request, self.template_name)
