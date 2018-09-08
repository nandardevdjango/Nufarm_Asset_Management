from django.http import JsonResponse
from django.views.generic import View

from .models import NANotifications


class NANotificationView(View):

    def __init__(self, *args, **kwargs):
        super(NANotificationView, self).__init__(*args, **kwargs)
        self.queryset = NANotifications.objects.filter(
            is_active=True
        )

    def get(self, request):
        name = request.GET.get('name')
        notifications = self.queryset.filter(
            name=name,
            user=request.user
        )
        result = []
        for notif in notifications:
            result.append({
                'title': notif.title,
                'data': notif.data
            })
        return JsonResponse(result, safe=False)

