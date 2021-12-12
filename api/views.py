from rest_framework import viewsets
from api.models import Tree
from api.serializers import TreeSerializer
# Create your views here.
class TreeVs(viewsets.ModelViewSet):
    model=Tree
    serializer_class=TreeSerializer
    queryset=Tree.objects.all()
