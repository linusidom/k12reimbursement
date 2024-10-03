from django.views.generic import TemplateView
from django.shortcuts import render

class IndexTemplateView(TemplateView):
	template_name = 'index.html'

# def handler404(request, exception, template_name="404.html"):
#     response = render(template_name)
#     response.status_code = 404
#     return response

# def handler500(request, template_name="500.html", *args, **argv):
#     response = render(template_name)
#     response.status_code = 500
#     return response