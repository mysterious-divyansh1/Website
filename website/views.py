from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from .forms import AccountForm
from .models import Account, Article
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
import feedparser


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('account')


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        feeds1 = feedparser.parse('http://feeds.bbci.co.uk/news/world/rss.xml')
        feeds = feedparser.parse('http://johnsmallman.wordpress.com/author/johnsmallman/feed/')
        for article in feeds1.entries:
            if not Article.objects.filter(link=article.link):
                item = Article(link=article.link, published=article.published,
                               summary=article.summary, title=article.title, )
                item.save()
        if request.user.is_authenticated:
            account = Account.objects.get(user=request.user)
            account_bookmarks = []
            for link in account.bookmarks.all().values('link'):
                account_bookmarks.append(link['link'])
            ctx = {'feeds': feeds1, 'bookmarks': account_bookmarks}
        else:
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
    template_name = "account.html"

    def get(self, request):
        if request.user.is_authenticated:
            user = Account.objects.get(user=request.user)
            ctx = {'user': user}
            return render(request, self.template_name, ctx)
        else:
            return redirect('login')


class AccountEditView(View):
    template_name = 'account_edit.html'

    def get(self, request):
        account = Account.objects.get(user=request.user)
        form = AccountForm(initial={'first_name': account.first_name, 'last_name': account.last_name})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AccountForm(request.POST, request.FILES)
        if form.is_valid():
            account = Account.objects.get(user=request.user)
            account.first_name = form.cleaned_data.get('first_name')
            account.last_name = form.cleaned_data.get('last_name')
            if form.cleaned_data.get('avatar'):
                account.avatar = form.cleaned_data.get('avatar')
            account.save()
        return redirect('account_edit')


class SearchResultsView(View):
    model = Article
    template_name = 'search_results.html'

    def get(self, request):
        query = request.GET.get('q')
        queryset = list(Article.objects.filter(Q(summary__icontains=query) | Q(title__icontains=query)))
        return render(request, self.template_name, {'entries': queryset})


class BookmarkView(View):
    model = Article
    template_name = 'bookmarks.html'

    def get(self, request):
        if request.user.is_authenticated:
            bookmarks = []
            account = Account.objects.get(user=request.user)
            for bookmark in account.bookmarks.all():
                bookmarks.append(bookmark)
            return render(request, self.template_name, {'bookmarks'})
        return redirect('index')

    def post(self, request):
        account = Account.objects.get(user=request.user)
        bookmark_link = request.POST.get('link')
        article = Article.objects.get(link=bookmark_link)
        account_bookmarks = []
        for link in account.bookmarks.all().values('link'):
            account_bookmarks.append(link['link'])
        if bookmark_link in account_bookmarks:
            account.bookmarks.remove(article)
        else:
            account.bookmarks.add(article)
        account.save()
        return redirect('index')


class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            account = Account(user=user)
            user.save()
            account.save()
            login(request, user)
            return redirect('index')
        return render(request, self.template_name, {'form': form})
