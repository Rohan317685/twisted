import json
import os
import requests
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from ..models import Project, UploadedFile
from django.contrib.auth.decorators import login_required
import boto3
from pathlib import Path
from uuid import uuid4
from botocore.exceptions import ClientError, BotoCoreError

s3 = boto3.client(
    "s3",
    endpoint_url=os.environ["R2_ENDPOINT"],
    aws_access_key_id=os.environ["R2_ACCESS_KEY"],
    aws_secret_access_key=os.environ["R2_SECRET_KEY"],
    region_name="auto",
)

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
            # Handle upload errors
            if response_data.get("status") == "error":
                return JsonResponse(response_data)
            return JsonResponse({
                "status": "ok",
                "link": response_data["url"],
                "name": response_data["filename"],
                "response": response_data,
            })
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
    try:
        ext = Path(image.name).suffix.lower()
        filename = f"{uuid4().hex}{ext}"
        s3.upload_fileobj(
            image,
            os.environ["R2_BUCKET"],
            filename,
            ExtraArgs={
                "ContentType": image.content_type,
            },
        )

        return {
            "url": f"{os.environ['R2_PUBLIC_URL']}/{filename}",
            "filename": filename,
            "size": image.size,
        }

    except (ClientError, BotoCoreError) as e:
        return {
                "status": "Error Occured", 
                "error": str(e)
            }

    except Exception as e:
        return {
            "status": "Error Occurred", 
            "error": f"Unknown Error Occurred: {str(e)}",
        }
