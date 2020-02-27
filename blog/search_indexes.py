from django.utils import timezone
from haystack import indexes
from blog.models import BlogPost


class BaseIndex(indexes.SearchIndex):
    model = None

    text = indexes.CharField(document=True, use_template=False)  # django-haystack need this in all index models
    content_type = indexes.CharField()

    def get_model(self):
        return self.model

    def index_queryset(self, using=None):
        # Unpublished posts don't need to be indexed
        return self.get_model().objects.filter(create_time__lte=timezone.now())

    # noinspection PyUnusedLocal
    def prepare_content_type(self, obj):
        return self.model.__name__.lower()


class BlogPostIndex(BaseIndex, indexes.Indexable):
    model = BlogPost

    title = indexes.CharField(model_attr='title')
    image = indexes.CharField()
    # categories = indexes.MultiValueField(model_attr='categories')

    @staticmethod
    def prepare_image(obj):
        image_url = obj.image
        if image_url:
            return 'media/{}'.format(image_url)
        return ''

    # def prepare_image(self, obj):
    #     image_url = obj.image
    #     if image_url:
    #         return 'media/{}'.format(image_url)
    #     return ''

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.title, obj.author.username
        ))
