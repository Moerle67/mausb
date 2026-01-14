from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.

class MyLoginView(LoginView):
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('start') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

def start(request):
    return HttpResponse("Startseite")