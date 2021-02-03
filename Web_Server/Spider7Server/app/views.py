from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics

from app.models import Proxies
from app.serializers import CommSerializers


class IPList(generics.ListAPIView):
    queryset = Proxies.objects.all()
    serializer_class = CommSerializers

