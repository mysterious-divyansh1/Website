from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
import feedparser


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        feeds1 = feedparser.parse('http://feeds.bbci.co.uk/news/world/rss.xml')
        feeds = feedparser.parse('http://johnsmallman.wordpress.com/author/johnsmallman/feed/')
        ctx = {'feeds': feeds1}
        return render(request, self.template_name, ctx)


class AboutView(View):
    template_name = "about.html"

    def get(self, request):
        return render(request, self.template_name)


class SupportView(View):
    template_name = "support.html"

    def get(self, request):
        return render(request, self.template_name)


class AccountView(View):
    template_name = "support.html"

    def get(self, request):
        return render(request, self.template_name)


class SigninView(View):
    template_name = "signin.html"

    def get(self, request):
        return render(request, self.template_name)