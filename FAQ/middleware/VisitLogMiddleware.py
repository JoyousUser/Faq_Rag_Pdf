from authentication.models import VisitLog

class VisitLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            VisitLog.objects.create(
                user=request.user,
                url=request.path,
                timestamp=request.timestamp if hasattr(request, 'timestamp') else None
            )

        return response