from time import strftime
from django.views import generic
from django.shortcuts import get_object_or_404, render
from rest_framework import mixins
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .forms import NewsViewsForm
from .models import News, Tag, NewsViews
from .serializers import NewsSerializer


class NewsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        NewsViews.objects.get_or_create(session_key=session_key, news=instance)
        return Response(serializer.data)


class NewsList(generic.ListView):
    template_name = 'home.html'
    queryset = News.objects.all()


class NewsByTag(generic.ListView):
    template_name = 'home.html'

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        return News.objects.filter(tags=self.tag)


class NewsDetail(generic.DetailView):
    template_name = 'detail.html'
    model = News

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        NewsViews.objects.get_or_create(session_key=session_key, news=self.object)
        return self.render_to_response(context)


def get_views_stats(request):
    if request.method == 'POST':
        from_date = strftime(request.POST.get('from_date'))
        to_date = strftime(request.POST.get('to_date'))
        news_views = NewsViews.objects.filter(
            date__gte=from_date,
            date__lte=to_date,
        )
        total_views = news_views.count()

        context = {
            'from_date': from_date,
            'to_date': to_date,
            'total_views': total_views,
        }
        return render(request, 'stats.html', context)

    else:
        form = NewsViewsForm()

    return render(request, 'stats.html', {'form': form})
