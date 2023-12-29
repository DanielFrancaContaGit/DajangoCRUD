from django.shortcuts import render
from django.contrib.auth.models import User, Group
from core.models import Cliente 
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import UserSerializer, GroupSerializers, ClienteSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializers
    permission_classes = [permissions.IsAuthenticated]

class ClienteViewSet(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        data = {
            'name': request.data.get('name'),
            'email': request.data.get('email')
        }

        dataSerializer = ClienteSerializer(data=data)

        if dataSerializer.is_valid():
            dataSerializer.save()
            return Response(dataSerializer.data, status=status.HTTP_201_CREATED)

        return Response(dataSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        clienteList = Cliente.objects.all()
        clienteListSerialer = ClienteSerializer(clienteList, many=True)
        return Response(clienteListSerialer.data, status=status.HTTP_200_OK)

    def put(self, request):

        data = {
            'name': request.data.get('name'),
            'email': request.data.get('email')
        }

        old_email = request.data.get('old_email')

        if old_email:
            try:
                cliente_instance = Cliente.objects.get(email= old_email)
            except Cliente.DoesNotExist:
                cliente_instance = None
                
            if not cliente_instance:
                return Response(
                    {"res": "Email náo existe"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )   
            
            serializer = ClienteSerializer(instance=cliente_instance, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"res": "Email não encontrado"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        email = request.data.get('email')

        if email:
            try:
                cliente_instance = Cliente.objects.get(email= email)
            except Cliente.DoesNotExist:
                cliente_instance = None

            if not cliente_instance:
                return Response(
                    {"res": "Cliente náo encontrado"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            cliente_instance.delete()
            return Response({"res": "Cliente deletado"}, status=status.HTTP_200_OK)
         
        return Response({"res": "email não encontrado"}, status=status.HTTP_400_BAD_REQUEST)