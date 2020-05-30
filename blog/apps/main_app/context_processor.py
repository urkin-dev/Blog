def getID(request):
    from django.conf import settings
    id = request.GET.get('id')
    
    if id is not None:
        return {'id': int(id)}

    return {'id': id}