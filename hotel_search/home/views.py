from django.shortcuts import render
from .models import *
from django.http import JsonResponse

# Create your views here.

def home(request):
    return render(request, 'home.html')

def get_hotel(request):
    try:
        Ans_objs = GFG.objects.all()

        if request.GET.get('sort_by'):
            sort_by_value = request.GET.get('sort_by')
            if sort_by_value == 'asc':
                Ans_objs = Ans_objs.order_by('hotel_price')
            elif sort_by_value == 'dsc':
                Ans_objs = Ans_objs.order_by('-hotel_price')

            if request.GET.get('amount'):
                amount = request.GET.get('amount')
                Ans_objs = Ans_objs.filter(hotel_price__lte=amount)

        payload = []
        for Ans_obj in Ans_objs:
            payload.append({
                'name': Ans_objs.hotel_name,
                'price': Ans_objs.hotel_price,
                'description': Ans_objs.hotel_description,
            })
        return JsonResponse(payload, safe=False)
    
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'Something went wrong'})