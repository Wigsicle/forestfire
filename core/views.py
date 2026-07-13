import os
from django.shortcuts import render
from django.http import JsonResponse


def health(request):
    return JsonResponse({
        "status": "ok",
        "version": os.getenv("APP_VERSION", "unknown"),
        "pod": os.getenv("POD_NAME", "unknown"),
        "namespace": os.getenv("POD_NAMESPACE", "unknown"),
        "node": os.getenv("NODE_NAME", "unknown"),
    })