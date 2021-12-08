from django.http import HttpResponse
from django.shortcuts import render


async def hello(request):
    return HttpResponse("Hello, async Django!")


