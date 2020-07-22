from django.shortcuts import render
from scrapyd_api import ScrapydAPI
from django.http import HttpResponse
from django.views import View
# Create your views here.
scrapyd = ScrapydAPI('http://localhost:6800')

class SpiderView(View):
    def get(self, request):
        state_dict = scrapyd.list_jobs('DMZJ')
        scrapyd.schedule('DMZJ', 'DMZJ', manhua_url=request.GET.get('manhua_url'), manhua_name=request.GET.get('manhua_name'))
        return HttpResponse(1)