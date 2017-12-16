from django.http.response import Http404
from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponse, HttpResponseRedirect

from django.views import View

from analytics.models import ClickEvent

from .models import ShortURL
from .forms import SubmitUrlForm

class HomeView(View):

    def get(self, request, *args, **kwargs):
        the_form = SubmitUrlForm()
        context = {
            "title": "Short.com",
            "form": the_form
        }
        return render(request, "shortener/home.html", context)

    def post(self, request, *args, **kwargs):
        the_form = SubmitUrlForm(request.POST)

        context = {
            "title": "Short.com",
            "form": the_form
        }
        template = "shortener/home.html"

        if the_form.is_valid():
            new_url =  the_form.cleaned_data.get("url")
            obj, created = ShortURL.objects.get_or_create(url=new_url)

            context = {
                "object": obj,
                "created": created
            }

            if created:
                template = "shortener/success.html"
            else:
                template = "shortener/already-created.html"

        return render(request, template, context)

class ShortRedirectView(View):

    def get(self, request, shortcode=None, *args, **kwargs):
        qs = ShortURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        ClickEvent.objects.create_event(obj)
        return HttpResponseRedirect(obj.url)