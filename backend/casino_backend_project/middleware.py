# Diese Datei regelt gleichzeitige Anfragen (frontend <-> backend) und Sitzungsmanagement (z.B. user löschen).

class DynamicSameSiteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Prüfe, ob der Pfad zum Django-Admin führt
        if request.path.startswith('/admin'):
            # Admin: sichere Cookies für Formulare
            if 'csrftoken' in response.cookies:
                response.cookies['csrftoken']['samesite'] = 'Lax'
            if 'sessionid' in response.cookies:
                response.cookies['sessionid']['samesite'] = 'Lax'
        else:
            # API-Zugriffe (Frontend): Cookies auch Cross-Origin zulassen
            if 'csrftoken' in response.cookies:
                response.cookies['csrftoken']['samesite'] = 'None'
                response.cookies['csrftoken']['secure'] = False  # True bei HTTPS
            if 'sessionid' in response.cookies:
                response.cookies['sessionid']['samesite'] = 'None'
                response.cookies['sessionid']['secure'] = False  # True bei HTTPS

        return response
# Füge diese Middleware in die MIDDLEWARE-Liste in settings.py ein, idealerweise nach der Session- und Auth-Middleware. (gemacht, dient nur dokumentation)