import os
from django.shortcuts import render
from django.http import JsonResponse


def health(request):
    return JsonResponse({
        "status": "ok",
        "version": os.getenv("APP_VERSION", "unknown")
    })