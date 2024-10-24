from rest_framework.routers import DefaultRouter
from task.views import TaskViewSet

router = DefaultRouter()
router.register(r'', TaskViewSet, basename='task')

urlpatterns = router.urls