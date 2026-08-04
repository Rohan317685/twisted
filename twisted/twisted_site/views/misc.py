import json
import os
import requests
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from ..models import Project, UploadedFile
from django.contrib.auth.decorators import login_required


@login_required
def upload_file(request):
    """
    Makdown image upload for uploading to imgur.com
    and represent as json to markdown editor.
    """

    if request.method == "POST":
        if "file" in request.FILES:
            image = request.FILES["file"]
            max_file_mb = float(request.POST.get("max_mb", 1))

            image_size = image.size / (1024 * 1024)
            if image_size > max_file_mb:
                return JsonResponse(
                    {"status": "error", "reason": f"File size exceeds {max_file_mb}MB!"}
                )

            response_data = file_uploader(request, image)
            return JsonResponse(response_data)
        return JsonResponse(
            {"status": "error", "reason": "Invalid request: no image found"}
        )
    return JsonResponse(
        {"status": "error", "reason": "Invalid request: method not POST"}
    )


def file_uploader(request, image):
    """
    Basic imgur uploader return as json data.
    :param `image` is from `request.FILES['markdown-image-upload']`
    :return json response
    """
    api_url = "https://cdn.hackclub.com/api/v4/upload"
    headers = {"Authorization": "Bearer " + os.environ["HACKCLUB_CDN_API_KEY"]}
    response = requests.post(api_url, headers=headers, files={"file": image})

    if response.status_code in [200, 201]:
        response_data = response.json()
        UploadedFile.objects.create(
            uploaded_by=request.user,
            link=response_data["url"],
            cdn_response=response_data,
            uploaded_thru=request.POST.get("ref", "unknown"),
            filesize=response_data["size"],
        )
        return {
            "status": "ok",
            "link": response_data["url"],
            "name": response_data["filename"],
            "response": response_data,
        }

    return {
        "status": response.status_code,
        "error": response.content.decode("utf-8"),
    }
