from haystack import indexes


class BaseIndex(indexes.SearchIndex):
    model = None

    text = indexes.CharField(document=True, use_template=False)  # django-haystack need this in all index models
    id = indexes.CharField(model_attr='id')

    def get_model(self):
        return self.model

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
