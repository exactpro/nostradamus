from django.http import HttpResponse
from django.utils.encoding import smart_str
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from io import BytesIO

from apps.extractor.main.connector import get_unique_values, get_issue_count
from apps.virtual_assistant.main.report_generator import (
    build_report_filters,
    make_report,
    get_report_dir,
    get_issues_for_report,
    REPORT_FIELDS,
    parse_field,
)


class ReportDownloadView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, filename):
        file_path = get_report_dir().joinpath(filename)

        file = open(file_path, "rb")
        response = HttpResponse(
            BytesIO(file.read()), content_type="application/force-download"
        )
        response[
            "Content-Disposition"
        ] = f"attachment; filename={smart_str(filename)}"
        response["X-Sendfile"] = smart_str(file_path)

        return response


class ReportCreatorView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from_date, to_date = request.data.pop("period")
        date_filter = build_report_filters(
            **parse_field("created", (from_date, to_date))
        )

        filters = []
        for field in request.data:
            filters += build_report_filters(
                **parse_field(field, request.data.get(field))
            )

        new_issues = get_issues_for_report(
            REPORT_FIELDS, filters + date_filter
        )

        date_filter[0]["name"] = "Resolved"
        REPORT_FIELDS.insert(5, "Resolved")

        closed_issues = get_issues_for_report(
            REPORT_FIELDS, filters + date_filter
        )

        if closed_issues.empty and new_issues.empty:
            return Response({})

        report = make_report(new_issues, closed_issues, to_date)

        return Response(report)


class RequestValuesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        field = request.GET.get("field")
        values = get_unique_values(field)

        return Response({"values": values})


class IssuesCheckerView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        issues_count = get_issue_count()

        return Response({"issues_loaded": bool(issues_count)})
