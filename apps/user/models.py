from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.material.models import BaseModel


class User(BaseModel, AbstractUser):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("DIRECTOR", "Director"),
        ("HISOBCHI", "Hisobchi"),
        ("TEXNOLOG", "Texnolog"),
        ("WAREHOUSE", "Warehouse"),
        ("SMENA_BOSHLIGI", "Smena Boshlig'i"),
        ("KATTA_MUTAXASSIS", "Katta Mutaxassis"),
        ("KICHIK_MUTAXASSIS", "Kichik Mutaxassis"),
        ("STAJER", "Stajer"),
        ("WORKER", "Worker"),
    )

    SHIFT_CHOICES = (
        ("DAY", "Day"),
        ("NIGHT", "Night"),
    )

    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, null=True, blank=True)
    employee_id = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_role_display_uz(self):
        """Get role display in Uzbek"""
        role_map = {
            "ADMIN": "Administrator",
            "DIRECTOR": "Direktor", 
            "HISOBCHI": "Hisobchi",
            "TEXNOLOG": "Texnolog",
            "WAREHOUSE": "Omborchi",
            "SMENA_BOSHLIGI": "Smena Boshlig'i",
            "KATTA_MUTAXASSIS": "Katta Mutaxassis", 
            "KICHIK_MUTAXASSIS": "Kichik Mutaxassis",
            "STAJER": "Stajer",
            "WORKER": "Ishchi",
        }
        return role_map.get(self.role, self.role)
    
    def is_operator(self):
        """Check if user is an operator (can be assigned to production steps)"""
        operator_roles = [
            "SMENA_BOSHLIGI", 
            "KATTA_MUTAXASSIS", 
            "KICHIK_MUTAXASSIS", 
            "STAJER", 
            "WORKER"
        ]
        return self.role in operator_roles
    
    def is_supervisor(self):
        """Check if user is a supervisor"""
        supervisor_roles = ["SMENA_BOSHLIGI", "KATTA_MUTAXASSIS"]
        return self.role in supervisor_roles
    
    def is_specialist(self):
        """Check if user is a specialist"""
        specialist_roles = ["KATTA_MUTAXASSIS", "KICHIK_MUTAXASSIS"]
        return self.role in specialist_roles
    
    def get_role_level(self):
        """Get role hierarchy level (higher number = higher authority)"""
        role_levels = {
            "ADMIN": 10,
            "DIRECTOR": 9,
            "TEXNOLOG": 8,
            "HISOBCHI": 7,
            "WAREHOUSE": 6,
            "SMENA_BOSHLIGI": 5,
            "KATTA_MUTAXASSIS": 4,
            "KICHIK_MUTAXASSIS": 3,
            "STAJER": 2,
            "WORKER": 1,
        }
        return role_levels.get(self.role, 0)
    
    def can_supervise(self, other_user):
        """Check if this user can supervise another user"""
        return self.get_role_level() > other_user.get_role_level()


