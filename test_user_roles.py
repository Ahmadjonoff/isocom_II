#!/usr/bin/env python
"""
Test new user roles and hierarchy
"""

import os
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isocom_backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def test_user_roles():
    print("👥 User Roles Test")
    
    # Create test users with different roles
    test_users = [
        ("admin_user", "ADMIN", "Admin", "User"),
        ("director", "DIRECTOR", "Director", "Manager"),
        ("smena_bosh", "SMENA_BOSHLIGI", "Smena", "Boshligi"),
        ("katta_mut", "KATTA_MUTAXASSIS", "Katta", "Mutaxassis"),
        ("kichik_mut", "KICHIK_MUTAXASSIS", "Kichik", "Mutaxassis"),
        ("stajer_user", "STAJER", "Stajer", "User"),
        ("worker_user", "WORKER", "Worker", "User"),
    ]
    
    created_users = []
    
    print("\n1. Creating test users...")
    for username, role, first_name, last_name in test_users:
        try:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': role,
                    'email': f"{username}@test.com",
                    'shift': 'DAY'
                }
            )
            created_users.append(user)
            if created:
                print(f"   ✅ {username} ({role}) yaratildi")
            else:
                print(f"   ✅ {username} ({role}) mavjud")
        except Exception as e:
            print(f"   ❌ {username} yaratishda xatolik: {e}")
    
    print("\n2. Testing role methods...")
    for user in created_users:
        print(f"\n👤 {user.username} ({user.role}):")
        print(f"   - Role Display: {user.get_role_display()}")
        print(f"   - Role Display UZ: {user.get_role_display_uz()}")
        print(f"   - Full Name: {user.get_full_name()}")
        print(f"   - Is Operator: {user.is_operator()}")
        print(f"   - Is Supervisor: {user.is_supervisor()}")
        print(f"   - Is Specialist: {user.is_specialist()}")
        print(f"   - Role Level: {user.get_role_level()}")
    
    print("\n3. Testing supervision hierarchy...")
    admin = next((u for u in created_users if u.role == 'ADMIN'), None)
    smena_bosh = next((u for u in created_users if u.role == 'SMENA_BOSHLIGI'), None)
    stajer = next((u for u in created_users if u.role == 'STAJER'), None)
    
    if admin and smena_bosh and stajer:
        print(f"   Admin can supervise Smena Bosh: {admin.can_supervise(smena_bosh)}")
        print(f"   Smena Bosh can supervise Stajer: {smena_bosh.can_supervise(stajer)}")
        print(f"   Stajer can supervise Admin: {stajer.can_supervise(admin)}")
    
    print("\n4. Testing operator filtering...")
    operators = [u for u in created_users if u.is_operator()]
    supervisors = [u for u in created_users if u.is_supervisor()]
    specialists = [u for u in created_users if u.is_specialist()]
    
    print(f"   Operators ({len(operators)}): {[u.username for u in operators]}")
    print(f"   Supervisors ({len(supervisors)}): {[u.username for u in supervisors]}")
    print(f"   Specialists ({len(specialists)}): {[u.username for u in specialists]}")
    
    print("\n5. Testing role choices...")
    print("   Available roles:")
    for role_code, role_name in User.ROLE_CHOICES:
        print(f"   - {role_code}: {role_name}")
    
    print("\n🧹 Cleaning up test users...")
    try:
        User.objects.filter(username__in=[u[0] for u in test_users]).delete()
        print("✅ Test users deleted")
    except Exception as e:
        print(f"❌ Cleanup error: {e}")
    
    print("\n✅ User roles test completed!")

if __name__ == "__main__":
    test_user_roles()
