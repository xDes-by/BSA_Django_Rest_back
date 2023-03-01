from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
# from steamauth import auth, get_uid
from django.http import HttpResponseNotFound
from .models import *
from .serializers import UserSerializer
from allauth.socialaccount.models import SocialAccount
import logging
import json

def index(request):
    return render(request, 'index.html')

def home(request):
    id = request.user.id
    social_account = SocialAccount.objects.get(id=id)
    user_data = UserProfile.objects.filter(user__steamID=social_account.uid)
    return render(request, 'index.html', context={'sid':user_data})


def profile(request):
    id = request.user.id
    social_account = SocialAccount.objects.get(uid=request.user.first_name)
    user_profile = UserProfile.objects.filter(user__steamID=social_account.uid)
    user_statistic = UserStatistic.objects.filter(user__steamID=social_account.uid)
    statistic = user_statistic[0]
    # a = user_statistic[0].user.steamID
    # sid = a - 61197960265728
  
    try:
        kda_creep = user_statistic[0].creep_kill / (user_statistic[0].creep_kill + user_statistic[0].creep_denay) * 100
    except:
        kda_creep = 100

    try:
        kda = user_statistic[0].kill / (user_statistic[0].kill + user_statistic[0].death) * 100
    except:
        kda = 100

    try:
        damage_kda = user_statistic[0].damage_deal / (user_statistic[0].damage_deal + user_statistic[0].damage_take) * 100
    except:
        damage_kda = 100    
        
    try:
        winrate = user_statistic[0].wins / user_statistic[0].games * 100
    except:
        winrate = 0   
        
    try:
        mvp = user_statistic[0].mvp / user_statistic[0].games * 100
    except:
        mvp = 0          

    context = {
        'winrate': winrate,
        'mvp': mvp,
        'damage': damage_kda,
        'kill_death': kda,
        'creep_kill_death': kda_creep,
        'profile': user_profile,
        # 'sid': sid,
        'statistic': statistic,
        'extra':social_account.extra_data
    }
    return render(request, 'profile.html', context=context)

# /////////////////////////////////////////////////////


def get_extra_data(user, provider):
    if not user or not provider:
        return None
    social_account = SocialAccount.objects.filter(user=user, provider=provider).first()
    return social_account.extra_data if social_account else None


# /////////////////////////////////////////////////////

class UserProfileView(APIView):
    def get(self, request):
        sid = get_uid(request.GET)
        user = User.objects.filter(steamID=sid).first()
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({"error": "User not found"}, status=404)


class UserListView(APIView):
    
    renderer_classes = (JSONRenderer, )
    
    def get(self, request):
        Users = User.objects.all()
        serializer = UserSerializer(Users, many=True)
        return Response(serializer.data)

    def post(self, request):
        key = request.GET.get('key')
        logging.basicConfig(filename='server.log', level=logging.INFO)
        logging.info('Received key: %s', key)
        try:
            arr_str = request.POST.get('arr')
            arr = json.loads(arr_str)
        except:
            return Response({"error": "Invalid JSON in arr"})
        if key == '6ACB961EA9ABE491C62B68EBCE65DF2FFF36FA94':
            results = []
            for k, v in arr.items():
                sid = v['sid']
                user, created = User.objects.get_or_create(steamID=sid)
                serializer = UserSerializer(user)
                results.append(serializer.data)
            return Response(results)
        else:
            return Response({"error": "Invalid key"})

# /////////////////////////////////////////////////////

class BuyItemView(APIView):
    renderer_classes = (JSONRenderer, )

    def post(self, request):
        key = request.GET.get('key')
        logging.basicConfig(filename='server.log', level=logging.INFO)
        logging.info('Received key: %s', key)
        try:
            arr_str = request.POST.get('arr')
            arr = json.loads(arr_str)
        except:
            return Response({"error": "Invalid JSON in arr"})
        if key == '6ACB961EA9ABE491C62B68EBCE65DF2FFF36FA94':
            sid = arr['sid']
            name = arr['name']
            count = arr['count']
            price = arr['price']
            currency = arr['currency']  

            user = User.objects.filter(steamID=sid).first()
            if currency == 'don':
                user.coins -= price
            else:
                user.rp -= price    
            user.save()
            product = Product.objects.get(name=name)
            UserItems.objects.create(user=user, count = count, product=product)            
        return Response({"status": "OK"})
            
def login(request):
    return auth('/callback/', use_ssl=False)