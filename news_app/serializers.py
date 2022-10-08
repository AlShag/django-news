from rest_framework import serializers

from .models import News
from .models import Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'pk',
            'name',
        )


class NewsSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    pk = serializers.HyperlinkedIdentityField(view_name='news-detail')

    class Meta:
        model = News
        fields = (
            'pk',
            'title',
            'body',
            'thumbnail',
            'tags',
        )

