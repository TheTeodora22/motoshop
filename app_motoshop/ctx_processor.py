from django.conf import settings


def procesare(request):
    return {
        "firma": settings.FIRMA,
        "ip": request.ip,
        "copyright": f"© 2026 {settings.FIRMA['nume']}. Toate drepturile rezervate."
    }