from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=False, null=False)
    thumbnail = models.ImageField(blank=False, null=False, upload_to='%Y/%m/%d')
    tags = models.ManyToManyField(
        'news_app.Tag',
        blank=False,
        related_name='news',
    )

    @property
    def views_count(self) -> int:
        return NewsViews.objects.filter(news=self).count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pk']


class NewsViews(models.Model):
    session_key = models.CharField(max_length=32)
    date = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey(
        'news_app.News',
        on_delete=models.CASCADE
    )
