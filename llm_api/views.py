# Django imports
from django.shortcuts import render

# Rest Framework imports
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

# Local imports
from .providers.loader import get_provider
from .serializers import RegisterSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def welcome_view(request):
    return Response({"message": "Welcome to the LLM API!"})

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SupportedModelsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        provider_name = request.query_params.get("provider", "openai")
        provider = get_provider(provider_name)
        models = provider.list_models()
        return Response(models)
