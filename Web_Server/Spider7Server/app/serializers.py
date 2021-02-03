from rest_framework import serializers
from app.models import Proxies

class CommSerializers(serializers.ModelSerializer):

    class Meta:
        model = Proxies
        fields = ('ip', 'port', 'type', 'uptime')


