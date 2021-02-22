import os
from django.conf import settings
from django.http import HttpResponse, Http404
from .models import Ticket
from django.views.decorators.csrf import csrf_exempt
import mimetypes
@csrf_exempt 
def download(request,pk):
  if request.method=='POST':
    ticket=Ticket.objects.get(id=pk)
    file_path=ticket.qr_code.path
    if os.path.exists(file_path):
      with open(file_path, 'rb') as fh:
        mime_type, _ = mimetypes.guess_type(file_path)
        response = HttpResponse(fh.read(), content_type=mime_type)
        print(response)
        response['Content-Disposition'] = file_path
        return response
    raise Http404


  
    # response = HttpResponse(fl, content_type=mime_type)
    # response['Content-Disposition'] = "attachment; filename=%s" % filename
    #     return response