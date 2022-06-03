import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("project")


class LogRequestMiddleware(MiddlewareMixin):
    """Middleware to log every request/response.
    Is not triggered when the request/response is managed using the cache
    """

    def _log_request(self, request):
        """Log the request"""
        user = str(getattr(request, "user", ""))
        method = str(getattr(request, "method", "")).upper()
        request_path = str(getattr(request, "path", ""))
        query_params = str(["%s=%s" % (k, v) for k, v in request.GET.items()])
        query_params = query_params if query_params else ""
        body = getattr(request, "body", b"").decode("utf-8").replace("\n", " ")

        if body and ("auth" in request_path):
            body = "****"

        logger.info(
            f"({user}) request: {method} {request_path} params: {query_params} payload: {body}"
        )

    def _log_response(self, request, response):
        """Log the response using values from the request"""
        user = str(getattr(request, "user", ""))
        method = str(getattr(request, "method", "")).upper()
        status_code = str(getattr(response, "status_code", ""))
        status_text = str(getattr(response, "status_text", ""))
        request_path = str(getattr(request, "path", ""))
        size = str(len(response.content))
        body = str(getattr(response, "data", ""))

        if body and ("auth" in request_path):
            body = "****"

        logger.info(
            f"({user}) response: {method} {request_path} - {status_code} ({status_text} / {size}) body: {body}"
        )

    def __call__(self, request):
        self._log_request(request)
        response = self.get_response(request)
        self._log_response(request, response)
        return response
