from django.utils.deprecation import MiddlewareMixin

from common.utils import GlobalVariable

class LogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """This method is called before the view is called."""

        user_id = request.user.uuid if request.user.is_authenticated else None
        GlobalVariable().set_val('user_id', user_id)
