import time

from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.urls import reverse

SESSION_IDLE_TIMEOUT = getattr(settings, 'SESSION_IDLE_TIMEOUT', 1800)


class SessionIdleTimeout:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        """Middleware class to timeout a session after a specified time period.
        """

        # Timeout is done only for authenticated logged in users.
        if request.user.is_authenticated and not request.user.is_superuser:
            current_timestamp = int(time.time())

            # Timeout if idle time period is exceeded.
            if request.session.has_key('last_activity') and \
                (current_timestamp - request.session['last_activity']) > SESSION_IDLE_TIMEOUT:
                logout(request)
                messages.add_message(request, messages.ERROR,
                                     _('Your session has been timed out.'))
                return HttpResponseRedirect(reverse('index_page'))
            else:
                request.session['last_activity'] = current_timestamp
        response = self.get_response(request)
        return response
