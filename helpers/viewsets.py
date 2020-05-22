from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.mixins import DetailSerializerMixin


# noinspection PyUnresolvedReferences
class ChangeCreateSerializerMixin:
    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_detail_class
        return super().get_serializer_class()


class UpdateOnlyModelViewSet(DetailSerializerMixin,
                             mixins.UpdateModelMixin,
                             GenericViewSet):
    """
    A viewset that provides default `update()` and `partial_update()` actions.
    """
    pass


class CreateOnlyModelViewSet(DetailSerializerMixin,
                             ChangeCreateSerializerMixin,
                             mixins.CreateModelMixin,
                             GenericViewSet):
    """
    A viewset that provides default `create()` actions.
    """
    pass


class WriteOnlyModelViewSet(UpdateOnlyModelViewSet,
                            CreateOnlyModelViewSet):
    """
    A viewset that provides default `update()`, `partial_update()`
    and `create()` actions.
    """
    pass


class RetrieveOnlyModelViewSet(mixins.RetrieveModelMixin,
                               GenericViewSet):
    """
    A viewset that provides default `retrieve()` actions.
    """
    pass


class ListOnlyModelViewSet(mixins.ListModelMixin,
                           GenericViewSet):
    """
    A viewset that provides default `list()` actions.
    """
    pass


class ReadOnlyModelViewSet(RetrieveOnlyModelViewSet,
                           ListOnlyModelViewSet):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    """
    pass


class DestroyOnlyModelViewSet(mixins.DestroyModelMixin,
                              GenericViewSet):
    """
    A viewset that provides default `destroy()` actions.
    """
    pass


class ModelViewSet(WriteOnlyModelViewSet,
                   ReadOnlyModelViewSet,
                   DestroyOnlyModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass
