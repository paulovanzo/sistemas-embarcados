from django.http import JsonResponse

def sensor(request):
    return JsonResponse({'teste':'Rota encontrada'})
