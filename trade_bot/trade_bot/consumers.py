
from user_exchanges.models import BotStop,LogsModel
from user_exchanges.serializer import BotStopSerial,LogSerials

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    PatchModelMixin,
)


class BotStatus(ListModelMixin, GenericAsyncAPIConsumer):
    queryset = BotStop.objects.all()
    serializer_class = BotStopSerial
    #permission_classes = (permissions.IsAuthenticated,)

class LogsChannel(ListModelMixin,GenericAsyncAPIConsumer):
    queryset = LogsModel.objects.all()
    serializer_class = LogSerials


