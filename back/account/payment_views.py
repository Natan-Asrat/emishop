from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
import requests
from decimal import Decimal
from django.db import transaction
import json

def get_paypal_access_token():
    auth_url = "https://api-m.sandbox.paypal.com/v1/oauth2/token" if settings.PAYPAL_MODE == "sandbox" else "https://api-m.paypal.com/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US"
    }
    auth_response = requests.post(
        auth_url,
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
        headers=headers,
        data="grant_type=client_credentials"
    )
    return auth_response.json()["access_token"]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_paypal_order(request):
    try:
        coins = int(request.data.get('coins', 0))
        price = float(request.data.get('price', 0))
        
        if not coins or not price:
            return Response({'error': 'Invalid request data'}, status=400)
        
        access_token = get_paypal_access_token()
        
        api_url = "https://api-m.sandbox.paypal.com/v2/checkout/orders" if settings.PAYPAL_MODE == "sandbox" else "https://api-m.paypal.com/v2/checkout/orders"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "USD",
                    "value": str(price)
                },
                "description": f"Purchase of {coins} coins"
            }]
        }
        
        response = requests.post(api_url, headers=headers, json=payload)
        
        if response.status_code == 201:
            return Response({
                'id': response.json()['id']
            })
        else:
            return Response({
                'error': 'Failed to create PayPal order'
            }, status=400)
            
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def capture_paypal_order(request):
    try:
        order_id = request.data.get('orderId')
        
        if not order_id:
            return Response({'error': 'Order ID is required'}, status=400)
        
        access_token = get_paypal_access_token()
        
        api_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture" if settings.PAYPAL_MODE == "sandbox" else f"https://api-m.paypal.com/v2/checkout/orders/{order_id}/capture"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.post(api_url, headers=headers)
        
        if response.status_code == 201:
            capture_data = response.json()
            amount = Decimal(capture_data['purchase_units'][0]['payments']['captures'][0]['amount']['value'])
            
            # Credit coins to user (1 coin = $1)
            with transaction.atomic():
                user = request.user
                coins_to_credit = int(amount)
                user.coins += coins_to_credit
                user.save()
                
                return Response({
                    'success': True,
                    'coins_credited': coins_to_credit,
                    'new_balance': user.coins
                })
        else:
            return Response({
                'error': 'Payment capture failed'
            }, status=400)
            
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=500)
