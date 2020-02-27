from haystack import indexes

from blog.models import BlogPost


class BaseIndex(indexes.SearchIndex):
    model = None

    text = indexes.CharField(document=True, use_template=False)  # django-haystack need this in all index models
    id = indexes.CharField(model_attr='id')

    def get_model(self):
        return self.model

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class BlogPostIndex(BaseIndex, indexes.Indexable):
    model = BlogPost

    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')
    image = indexes.CharField()
    category_ids = indexes.MultiValueField()
    author_id = indexes.MultiValueField()

    @staticmethod
    def prepare_image(obj):
        image_url = obj.image
        if image_url:
            return 'media/{}'.format(image_url)
        return ''

    @staticmethod
    def prepare_category_ids(obj):
        return [category.id for category in obj.categories.all()]

    @staticmethod
    def prepare_author_id(obj):
        return obj.id

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.title, obj.author.username
        ))
