from rest_framework import routers
from core.user.viewsets import UserViewSet
from core.auth.viewsets.login import LoginViewSet
from core.auth.viewsets.register import RegisterViewSet
from core.auth.viewsets.refresh import RefreshViewSet
from core.post.viewsets import PostViewSet



router = routers.SimpleRouter()

# Auth
router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewSet, basename="auth-login")
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')


# user
router.register(r"user", UserViewSet, basename='user')

# post
router.register(r'post', PostViewSet, basename='post')

app_name="core"

urlpatterns = [
    *router.urls,
]