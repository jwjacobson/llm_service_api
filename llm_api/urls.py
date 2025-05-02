from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterView,
    welcome_view,
    SupportedModelsView,
    ChatCompletionsView
)

urlpatterns = [
    path('api/', welcome_view, name='welcome'),
    path('api/signup/', RegisterView.as_view(), name='signup'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/supported-models/', SupportedModelsView.as_view(), name='supported-models'),
    path('api/chat/completions/', ChatCompletionsView.as_view(), name='chat-completions'),
]
