from pathlib import Path
from wsgiref.util import FileWrapper

from pandas import DataFrame

from django.http import HttpResponse
from django.utils.encoding import smart_str
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.virtual_assistant.main.report_generator import (
    build_report_filters,
    make_report,
    get_report_dir,
    get_datetime_range,
    get_issues_for_report,
)
from apps.extractor.main.connector import get_issues


class ReportDownloadView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, filename):
        file_path = get_report_dir().joinpath(filename)

        file = open(file_path, "r")
        response = HttpResponse(
            FileWrapper(file), content_type="application/force-download"
        )
        response[
            "Content-Disposition"
        ] = f"attachment; filename={smart_str(filename)}"
        response["X-Sendfile"] = smart_str(file_path)

        return response


class ReportCreatorView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        from_date, to_date = get_datetime_range(request.data.get("date"))

        filters = build_report_filters(
            field="Created", period=(from_date, to_date)
        )
        fields = [
            "Project",
            "Key",
            "Status",
            "Priority",
            "Created",
            "Reporter",
            "Assignee",
        ]

        new_issues = get_issues_for_report(fields, filters)

        filters = build_report_filters(
            field="Resolved", period=(from_date, to_date)
        )
        fields.insert(5, "Resolved")

        closed_issues = get_issues_for_report(fields, filters)

        report = make_report(new_issues, closed_issues, from_date)

        return Response(report)
