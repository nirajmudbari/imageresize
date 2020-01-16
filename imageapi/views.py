from io import BytesIO, StringIO

from django.http import HttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from imageapi.onlyopencv import getBase64ResizeAndReturnBase64


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def fetchandresize(request):
    if request.method == "POST":
        base64 = request.body.decode('ascii')
        bufferstr = StringIO()
        bufferstr.write(base64)
        return HttpResponse(getBase64ResizeAndReturnBase64(bufferstr.getvalue()))
