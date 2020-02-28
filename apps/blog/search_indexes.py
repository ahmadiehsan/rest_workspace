import json

from haystack import indexes

from apps.blog.models import Article
from helpers.search_indexes import BaseIndex


class ArticleIndex(BaseIndex, indexes.Indexable):
    model = Article

    title = indexes.CharField(model_attr='title')
    modify_time = indexes.CharField(model_attr='modify_time')
    image = indexes.CharField()
    author = indexes.CharField()
    author_index = indexes.CharField()
    categories = indexes.CharField()
    categories_index = indexes.MultiValueField()

    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_image(obj):
        image_url = obj.image
        if image_url:
            return 'media/{}'.format(image_url)
        return ''

    @staticmethod
    def prepare_author(obj):
        from apps.user.serializers import UserMinimalSerializer
        return json.dumps(UserMinimalSerializer(obj.author).data)

    @staticmethod
    def prepare_author_index(obj):
        return '{} {}'.format(obj.author.first_name, obj.author.last_name)

    @staticmethod
    def prepare_categories(obj):
        from apps.blog.serializers import CategoryMinimalSerializer
        return json.dumps(CategoryMinimalSerializer(obj.categories.all(), many=True).data)

    @staticmethod
    def prepare_categories_index(obj):
        return [category.title for category in obj.categories.all()]

    # for searching with elasticsearch autocomplete feature
    # /?autocomplete=<wrong word>
    @staticmethod
    def prepare_autocomplete(obj):
        return obj.title
