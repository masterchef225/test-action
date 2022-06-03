from django.conf import settings
from django.conf.urls import url
from drf_yasg import openapi
from drf_yasg.inspectors.view import SwaggerAutoSchema
from drf_yasg.utils import force_real_str, is_list_view
from drf_yasg.views import get_schema_view
from rest_framework import exceptions
from rest_framework import permissions
from rest_framework import status


class ErrorResponseAutoSchema(SwaggerAutoSchema):
    def get_generic_error_schema(self):
        return openapi.Schema(
            "Generic API Error",
            type=openapi.TYPE_OBJECT,
            properties={
                "detail": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Error description"
                ),
                "errors": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Error messages",
                    items=openapi.Items(type=openapi.TYPE_STRING),
                ),
            },
            required=["detail"],
        )

    def get_response_serializers(self):
        responses = super().get_response_serializers()
        definitions = self.components.with_scope(
            openapi.SCHEMA_DEFINITIONS
        )  # type: openapi.ReferenceResolver

        definitions.setdefault("GenericError", self.get_generic_error_schema)

        if self.get_request_serializer() or self.get_query_serializer():
            responses.setdefault(
                exceptions.ValidationError.status_code,
                openapi.Response(
                    description=force_real_str(
                        exceptions.ValidationError.default_detail
                    ),
                    schema=openapi.SchemaRef(definitions, "GenericError"),
                ),
            )

        security = self.get_security()
        if security is None or len(security) > 0:
            # Note: 401 error codes are coerced  into 403 see rest_framework/views.py:433:handle_exception
            # This is b/c the API uses token auth which doesn't have WWW-Authenticate header
            responses.setdefault(
                status.HTTP_403_FORBIDDEN,
                openapi.Response(
                    description="Authentication credentials were invalid, absent or insufficient.",
                    schema=openapi.SchemaRef(definitions, "GenericError"),
                ),
            )
        if not is_list_view(self.path, self.method, self.view):
            responses.setdefault(
                exceptions.PermissionDenied.status_code,
                openapi.Response(
                    description="Permission denied.",
                    schema=openapi.SchemaRef(definitions, "GenericError"),
                ),
            )
            responses.setdefault(
                exceptions.NotFound.status_code,
                openapi.Response(
                    description="Object does not exist or caller has insufficient permissions to access it.",
                    schema=openapi.SchemaRef(definitions, "GenericError"),
                ),
            )

        responses.setdefault(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            openapi.Response(
                description="Internal server error.",
                schema=openapi.SchemaRef(definitions, "GenericError"),
            ),
        )

        return responses


scheme = "http" if settings.DEBUG else "https"
hostname = settings.HOSTNAME

schema_view = get_schema_view(
    openapi.Info(
        title="GMOP API",
        default_version="v1",
        description="GMOP API",
        license=openapi.License(name="Proprietary"),
    ),
    url=f"{scheme}://{hostname}",
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(),
)

urlpatterns = [
    url(
        r"^swagger(?P<format>\.json)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
