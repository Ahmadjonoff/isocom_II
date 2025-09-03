#!/usr/bin/env python
"""
JWT Authentication Test
"""

import os
import django
import requests
import json

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isocom_backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def test_jwt_authentication():
    print("🔐 JWT Authentication Test")
    
    base_url = "http://localhost:8000"
    
    # 1. Create test user
    try:
        user, created = User.objects.get_or_create(
            username='jwttest',
            defaults={
                'first_name': 'JWT',
                'last_name': 'Test',
                'email': 'jwt@test.com'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            print("✅ Test user yaratildi")
        else:
            print("✅ Test user mavjud")
            
    except Exception as e:
        print(f"❌ User yaratishda xatolik: {e}")
        return
    
    # 2. Get JWT token
    print("\n🎫 JWT Token olish...")
    try:
        token_response = requests.post(
            f"{base_url}/api/auth/token/",
            json={
                "username": "jwttest",
                "password": "testpass123"
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if token_response.status_code == 200:
            token_data = token_response.json()
            access_token = token_data.get('access')
            refresh_token = token_data.get('refresh')
            
            print("✅ JWT Token olindi")
            print(f"   Access Token: {access_token[:50]}...")
            print(f"   Refresh Token: {refresh_token[:50]}...")
            
        else:
            print(f"❌ Token olishda xatolik: {token_response.status_code}")
            print(f"   Response: {token_response.text}")
            return
            
    except Exception as e:
        print(f"❌ Token request xatolik: {e}")
        return
    
    # 3. Test API without token
    print("\n🚫 Token yo'qligida API test...")
    try:
        response = requests.get(f"{base_url}/api/materials/")
        if response.status_code == 401:
            print("✅ Token yo'q - 401 Unauthorized")
        else:
            print(f"❌ Kutilmagan javob: {response.status_code}")
    except Exception as e:
        print(f"❌ API test xatolik: {e}")
    
    # 4. Test API with Bearer token
    print("\n🔑 Bearer Token bilan API test...")
    try:
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(f"{base_url}/api/materials/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✅ Bearer Token bilan API ishladi")
            print(f"   Materials count: {data.get('count', 0)}")
        else:
            print(f"❌ Bearer Token test: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Bearer Token test xatolik: {e}")
    
    # 5. Test token refresh
    print("\n🔄 Token Refresh test...")
    try:
        refresh_response = requests.post(
            f"{base_url}/api/auth/token/refresh/",
            json={"refresh": refresh_token},
            headers={'Content-Type': 'application/json'}
        )
        
        if refresh_response.status_code == 200:
            new_token_data = refresh_response.json()
            new_access_token = new_token_data.get('access')
            print("✅ Token refresh ishladi")
            print(f"   New Access Token: {new_access_token[:50]}...")
        else:
            print(f"❌ Token refresh: {refresh_response.status_code}")
            print(f"   Response: {refresh_response.text}")
            
    except Exception as e:
        print(f"❌ Token refresh xatolik: {e}")
    
    # 6. Test token verify
    print("\n✅ Token Verify test...")
    try:
        verify_response = requests.post(
            f"{base_url}/api/auth/token/verify/",
            json={"token": access_token},
            headers={'Content-Type': 'application/json'}
        )
        
        if verify_response.status_code == 200:
            print("✅ Token verify ishladi - token valid")
        else:
            print(f"❌ Token verify: {verify_response.status_code}")
            print(f"   Response: {verify_response.text}")
            
    except Exception as e:
        print(f"❌ Token verify xatolik: {e}")
    
    # Cleanup
    print("\n🧹 Test ma'lumotlarini tozalash...")
    try:
        User.objects.filter(username='jwttest').delete()
        print("✅ Test user o'chirildi")
    except Exception as e:
        print(f"❌ Cleanup xatolik: {e}")
    
    print("\n🎉 JWT Authentication test yakunlandi!")

if __name__ == "__main__":
    test_jwt_authentication()
