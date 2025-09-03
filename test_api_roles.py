#!/usr/bin/env python
"""
Test User API with new roles
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

def test_user_api():
    print("🌐 User API Test with New Roles")
    
    base_url = "http://localhost:8000"
    
    # 1. Create test user and get token
    try:
        user, created = User.objects.get_or_create(
            username='apitestuser',
            defaults={
                'first_name': 'API',
                'last_name': 'Tester',
                'role': 'ADMIN',
                'email': 'api@test.com'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
        
        # Get JWT token
        token_response = requests.post(
            f"{base_url}/api/auth/token/",
            json={"username": "apitestuser", "password": "testpass123"}
        )
        
        if token_response.status_code == 200:
            access_token = token_response.json()['access']
            print("✅ JWT token obtained")
        else:
            print(f"❌ Token error: {token_response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # 2. Create test users with new roles
    print("\n📝 Creating users with new roles via API...")
    
    test_users = [
        {
            "username": "smena_bosh_api",
            "first_name": "Smena",
            "last_name": "Boshligi",
            "role": "SMENA_BOSHLIGI",
            "shift": "DAY",
            "employee_id": "SB001"
        },
        {
            "username": "katta_mut_api", 
            "first_name": "Katta",
            "last_name": "Mutaxassis",
            "role": "KATTA_MUTAXASSIS",
            "shift": "NIGHT",
            "employee_id": "KM001"
        },
        {
            "username": "stajer_api",
            "first_name": "Stajer",
            "last_name": "User",
            "role": "STAJER",
            "shift": "DAY",
            "employee_id": "ST001"
        }
    ]
    
    created_user_ids = []
    
    for user_data in test_users:
        try:
            response = requests.post(
                f"{base_url}/api/users/",
                json=user_data,
                headers=headers
            )
            
            if response.status_code == 201:
                user_info = response.json()
                created_user_ids.append(user_info['id'])
                print(f"   ✅ {user_data['username']} ({user_data['role']}) created")
                print(f"      - Role Display: {user_info.get('role_display')}")
                print(f"      - Role Display UZ: {user_info.get('role_display_uz')}")
                print(f"      - Is Operator: {user_info.get('is_operator')}")
                print(f"      - Is Supervisor: {user_info.get('is_supervisor')}")
                print(f"      - Role Level: {user_info.get('role_level')}")
            else:
                print(f"   ❌ {user_data['username']} creation failed: {response.status_code}")
                print(f"      Response: {response.text}")
                
        except Exception as e:
            print(f"   ❌ API error for {user_data['username']}: {e}")
    
    # 3. Test filtering operators
    print("\n🔍 Testing operator filtering...")
    try:
        # Get all users
        response = requests.get(f"{base_url}/api/users/", headers=headers)
        if response.status_code == 200:
            users_data = response.json()
            all_users = users_data.get('results', [])
            
            operators = [u for u in all_users if u.get('is_operator')]
            supervisors = [u for u in all_users if u.get('is_supervisor')]
            specialists = [u for u in all_users if u.get('is_specialist')]
            
            print(f"   ✅ Total users: {len(all_users)}")
            print(f"   ✅ Operators: {len(operators)}")
            print(f"      - {[u['username'] for u in operators]}")
            print(f"   ✅ Supervisors: {len(supervisors)}")
            print(f"      - {[u['username'] for u in supervisors]}")
            print(f"   ✅ Specialists: {len(specialists)}")
            print(f"      - {[u['username'] for u in specialists]}")
        else:
            print(f"   ❌ Users list error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Filtering error: {e}")
    
    # 4. Test role filtering
    print("\n🎭 Testing role-based filtering...")
    try:
        # Filter by role
        response = requests.get(
            f"{base_url}/api/users/?role=SMENA_BOSHLIGI", 
            headers=headers
        )
        if response.status_code == 200:
            smena_users = response.json().get('results', [])
            print(f"   ✅ Smena Boshligi users: {len(smena_users)}")
            for user in smena_users:
                print(f"      - {user['username']}: {user['role_display_uz']}")
        else:
            print(f"   ❌ Role filtering error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Role filtering error: {e}")
    
    # 5. Cleanup
    print("\n🧹 Cleaning up...")
    try:
        # Delete created users
        for user_id in created_user_ids:
            response = requests.delete(
                f"{base_url}/api/users/{user_id}/",
                headers=headers
            )
            if response.status_code == 204:
                print(f"   ✅ User {user_id} deleted")
        
        # Delete test user
        User.objects.filter(username='apitestuser').delete()
        print("   ✅ Test user deleted")
        
    except Exception as e:
        print(f"   ❌ Cleanup error: {e}")
    
    print("\n🎉 User API test completed!")

if __name__ == "__main__":
    test_user_api()
