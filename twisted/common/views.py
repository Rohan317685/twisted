import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
import requests
import json

# Create your views here.
@login_required
def markdown_imgur_uploader(request):
    """
    Makdown image upload for uploading to imgur.com
    and represent as json to markdown editor.
    """

    def is_ajax(request):
        return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"

    if request.method == "POST" and is_ajax(request):
        if "markdown-image-upload" in request.FILES:
            image = request.FILES["markdown-image-upload"]
            response_data = imgur_uploader(image=image)
            return HttpResponse(response_data, content_type="application/json")
        return HttpResponse(_("Invalid request!"))
    return HttpResponse(_("Invalid request!"))

def imgur_uploader(image):
    """
    Basic imgur uploader return as json data.
    :param `image` is from `request.FILES['markdown-image-upload']`
    :return json response
    """
    api_url = "https://cdn.hackclub.com/api/v4/upload"
    headers = {"Authorization": "Bearer " + os.environ['HACKCLUB_CDN_API_KEY']}
    response = requests.post(
        api_url,
        headers=headers,
        files={
            "file": image
        }
    )

    if response.status_code == 200:
        response_data = response.json()
        return json.dumps(
            {
                "status": "ok",
                "link": response_data["url"],
                "name": response_data["filename"],
            }
        )

    return json.dumps(
        {
            "status": response.status_code,
            "error": response.content.decode("utf-8"),
        }
    )