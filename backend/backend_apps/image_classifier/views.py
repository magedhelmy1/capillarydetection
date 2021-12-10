from django.http import HttpResponse
from django.shortcuts import render
import aiohttp


async def hello(request):
    return HttpResponse("Hello, async Django!")


async def example(request):
    async with aiohttp.ClientSession() as session:
        url = "http://64.227.106.224/api/analyze_im/"
        async with session.post(url) as res:
            pokemon = await res.json()

    return render(request, "index.html", {"data": pokemon})
