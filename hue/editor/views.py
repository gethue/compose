from django.shortcuts import render
from editor.api import execute
from rest_framework.decorators import api_view


from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_field,
    extend_schema_serializer,
    extend_schema_view,
    inline_serializer,
)


@extend_schema(
    # Json https://github.com/tfranzel/drf-spectacular/issues/279
    # Should define properly json POST attributes
    parameters=[
        OpenApiParameter(
            name="snippet",
            type={
                "type": "json",
                "minItems": 4,
                "maxItems": 6,
                "items": {"type": "number"},
            },
            location=OpenApiParameter.QUERY,
            required=False,
            style="form",
            explode=False,
        )
    ],
    responses=OpenApiTypes.OBJECT,
)
@api_view(["POST"])
def query(request, dialect=None):
    print(request.data)
    print(request.POST)
    data = execute(request)
    return data
