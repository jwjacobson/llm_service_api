# Python imports
import json

# Django imports
from django.http import StreamingHttpResponse, JsonResponse
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

class ChatCompletionsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        provider_name = request.query_params.get("provider", "openai")
        provider = get_provider(provider_name)

        model = request.data.get("model")
        messages = request.data.get("messages")
        stream = request.data.get("stream", False)

        if not model or not messages:
            return Response(
                {"error": "Both 'model' and 'messages' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = provider.chat_completion(
                model=model,
                messages=messages,
                stream=stream
            )

            if not stream:
                return Response(result)

            def stream_response():
                for chunk in result:
                    if hasattr(chunk, "text"):
                        data = chunk.text
                    elif hasattr(chunk, "choices") and chunk.choices:
                        data = chunk.choices[0].delta.get("content", "")
                    else:
                        data = str(chunk)

                    yield f"data: {json.dumps({'content': data})}\n\n"

            return StreamingHttpResponse(
                stream_response(),
                content_type="text/event-stream"
            )


        except Exception as e:
            return Response({"error": str(e)}, status=500)
