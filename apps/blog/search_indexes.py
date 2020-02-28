import json

from haystack import indexes

from apps.blog.models import Article
from apps.blog import serializers


class BaseIndex(indexes.SearchIndex):
    model = None

    text = indexes.CharField(document=True, use_template=False)  # django-haystack need this in all index models
    id = indexes.CharField(model_attr='id')

    def get_model(self):
        return self.model

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


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
        return json.dumps(serializers.UserMinimalSerializer(obj.author).data)

    @staticmethod
    def prepare_autocomplete(obj):
        return obj.title
