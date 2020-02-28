import json

from haystack import indexes

import apps.user.serializers
from apps.blog import serializers
from apps.blog.models import Article
from helpers.search_indexes import BaseIndex


class ArticleIndex(BaseIndex, indexes.Indexable):
    model = Article

    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')
    image = indexes.CharField()
    categories = indexes.CharField()
    author = indexes.CharField()

    # If you’re working with Asian languages or want to be able to autocomplete across word
    # boundaries, NgramField should be what you use
    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_image(obj):
        image_url = obj.image
        if image_url:
            return 'media/{}'.format(image_url)
        return ''

    @staticmethod
    def prepare_categories(obj):
        return json.dumps(serializers.CategoryMinimalSerializer(obj.categories.all(), many=True).data)

    @staticmethod
    def prepare_author(obj):
        return json.dumps(apps.user.serializers.UserMinimalSerializer(obj.author).data)

    @staticmethod
    def prepare_autocomplete(obj):
        return obj.title
