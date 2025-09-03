#!/usr/bin/env python
"""
Final Comprehensive Test - Complete Project Validation
Butun loyihaning barcha qismlarini tekshiradi
"""

import os
import django
import requests
import time
from decimal import Decimal

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isocom_backend.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from apps.material.models import Material
from apps.product.models import Product, ProductComponent
from apps.workcenter.models import WorkCenter
from apps.warehouse.models import Warehouse, Location
from apps.stock.models import StockLevel, InventoryMovementLog
from apps.production.models import Order, ProductionStep, ProductionStepExecution, UsedMaterial, ProductionOutput

User = get_user_model()

class FinalTest:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.base_url = "http://localhost:8000"
        
    def log_success(self, test):
        print(f"   ✅ {test}")
        self.passed += 1
        
    def log_error(self, test, error):
        print(f"   ❌ {test}: {error}")
        self.failed += 1

    def test_server_status(self):
        """Test if development server is running"""
        print("🌐 Server Status Testi")
        
        try:
            response = requests.get(f"{self.base_url}/admin/", timeout=5)
            if response.status_code in [200, 302]:  # 302 = redirect to login
                self.log_success("Development server ishlayapti")
            else:
                self.log_error("Server status", f"Status code: {response.status_code}")
        except requests.exceptions.ConnectionError:
            self.log_error("Server connection", "Server ishlamayapti yoki ulanib bo'lmayapti")
        except Exception as e:
            self.log_error("Server test", str(e))

    def test_api_documentation(self):
        """Test API documentation endpoints"""
        print("\n📚 API Documentation Testi")
        
        endpoints = [
            ("/api/schema/", "OpenAPI Schema"),
            ("/api/docs/", "Swagger UI"),
            ("/api/redoc/", "ReDoc")
        ]
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    self.log_success(f"{name} mavjud")
                else:
                    self.log_error(f"{name}", f"Status: {response.status_code}")
            except Exception as e:
                self.log_error(f"{name}", str(e))

    def test_admin_panel(self):
        """Test admin panel functionality"""
        print("\n👤 Admin Panel Testi")
        
        try:
            # Create superuser
            user, created = User.objects.get_or_create(
                username='finaltest',
                defaults={
                    'is_staff': True,
                    'is_superuser': True,
                    'first_name': 'Final',
                    'last_name': 'Test'
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
            
            # Test admin login
            client = Client()
            login_data = {
                'username': 'finaltest',
                'password': 'testpass123',
                'next': '/admin/'
            }
            
            response = client.post('/admin/login/', login_data)
            if response.status_code in [200, 302]:
                self.log_success("Admin login ishlayapti")
            else:
                self.log_error("Admin login", f"Status: {response.status_code}")
            
            # Test admin pages
            admin_pages = [
                '/admin/',
                '/admin/material/',
                '/admin/product/',
                '/admin/workcenter/',
                '/admin/warehouse/',
                '/admin/stock/',
                '/admin/production/',
                '/admin/user/',
            ]
            
            for page in admin_pages:
                try:
                    response = client.get(page)
                    if response.status_code == 200:
                        self.log_success(f"Admin page: {page}")
                    else:
                        self.log_error(f"Admin page: {page}", f"Status: {response.status_code}")
                except Exception as e:
                    self.log_error(f"Admin page: {page}", str(e))
                    
        except Exception as e:
            self.log_error("Admin panel test", str(e))

    def test_complete_workflow(self):
        """Test complete manufacturing workflow"""
        print("\n🏭 To'liq Ishlab Chiqarish Workflow Testi")
        
        try:
            # 1. Create materials
            plastic = Material.objects.create(
                name="Final Test Plastic",
                code="FTP001",
                type="GRANULA",
                unit_of_measure="KG",
                price=Decimal("12.50")
            )
            
            additive = Material.objects.create(
                name="Final Test Additive", 
                code="FTA001",
                type="OTHER",
                unit_of_measure="KG",
                price=Decimal("25.00")
            )
            self.log_success("Materiallar yaratildi")
            
            # 2. Create products
            semi_product = Product.objects.create(
                name="Final Test Semi Product",
                code="FTSP001",
                type="SEMI_FINISHED"
            )
            
            finished_product = Product.objects.create(
                name="Final Test Finished Product",
                code="FTFP001", 
                type="FINISHED"
            )
            
            # Create product component
            ProductComponent.objects.create(
                finished_product=finished_product,
                semi_finished_product=semi_product
            )
            self.log_success("Mahsulotlar va komponentlar yaratildi")
            
            # 3. Create warehouse and workcenters
            warehouse = Warehouse.objects.create(name="Final Test Warehouse")
            
            warehouse_loc = Location.objects.create(
                name="Final Test WH Location",
                location_type="WAREHOUSE",
                warehouse=warehouse
            )
            
            extruder = WorkCenter.objects.create(
                name="Final Test Extruder",
                type="EXTRUDER",
                capacity_per_hour=150
            )
            
            extruder_loc = Location.objects.create(
                name="Final Test Extruder Location",
                location_type="WORKCENTER",
                work_center=extruder
            )
            self.log_success("Warehouse va WorkCenter yaratildi")
            
            # 4. Add stock
            StockLevel.objects.create(
                material=plastic,
                location=warehouse_loc,
                quantity=Decimal("2000.00")
            )
            
            StockLevel.objects.create(
                material=additive,
                location=warehouse_loc,
                quantity=Decimal("500.00")
            )
            self.log_success("Stock qo'shildi")
            
            # 5. Transfer materials to workcenter
            InventoryMovementLog.objects.create(
                material=plastic,
                quantity=Decimal("1000.00"),
                from_location=warehouse_loc,
                to_location=extruder_loc
            )
            
            InventoryMovementLog.objects.create(
                material=additive,
                quantity=Decimal("100.00"),
                from_location=warehouse_loc,
                to_location=extruder_loc
            )
            self.log_success("Materiallar workcenter ga ko'chirildi")
            
            # 6. Create production order
            order = Order.objects.create(
                produced_product=finished_product,
                unit_of_measure="KG",
                produced_quantity=Decimal("800.00"),
                status="PENDING",
                description="Final test production order"
            )
            
            # Create production steps
            order.create_production_steps()
            step_count = order.step_executions.count()
            self.log_success(f"Production order va {step_count} ta step yaratildi")
            
            # 7. Execute first step (Extrusion)
            first_step = order.get_current_step()
            if first_step:
                first_step.status = "IN_PROGRESS"
                first_step.work_center = extruder
                first_step.save()
                
                # Use materials
                UsedMaterial.objects.create(
                    order=order,
                    material=plastic,
                    quantity=Decimal("750.00"),
                    step_execution=first_step
                )
                
                UsedMaterial.objects.create(
                    order=order,
                    material=additive,
                    quantity=Decimal("50.00"),
                    step_execution=first_step
                )
                
                # Create output
                ProductionOutput.objects.create(
                    step_execution=first_step,
                    product=semi_product,
                    unit_of_measure="KG",
                    quantity=Decimal("780.00"),
                    weight=Decimal("780.500"),
                    quality_status="PASSED"
                )
                
                # Complete step
                first_step.status = "COMPLETED"
                first_step.save()
                
                self.log_success("Birinchi step (Extrusion) bajarildi")
            
            # 8. Check final status
            completion = order.get_completion_percentage()
            self.log_success(f"Order completion: {completion}%")
            
            # Check stock levels
            plastic_stock = StockLevel.objects.get(material=plastic, location=extruder_loc)
            additive_stock = StockLevel.objects.get(material=additive, location=extruder_loc)
            
            expected_plastic = Decimal("1000.00") - Decimal("750.00")  # 250
            expected_additive = Decimal("100.00") - Decimal("50.00")   # 50
            
            if plastic_stock.quantity == expected_plastic:
                self.log_success(f"Plastic stock to'g'ri: {plastic_stock.quantity} kg")
            else:
                self.log_error("Plastic stock", f"Expected {expected_plastic}, got {plastic_stock.quantity}")
                
            if additive_stock.quantity == expected_additive:
                self.log_success(f"Additive stock to'g'ri: {additive_stock.quantity} kg")
            else:
                self.log_error("Additive stock", f"Expected {expected_additive}, got {additive_stock.quantity}")
                
        except Exception as e:
            self.log_error("Complete workflow", str(e))

    def test_model_relationships(self):
        """Test model relationships and foreign keys"""
        print("\n🔗 Model Relationships Testi")
        
        try:
            # Test material relationships
            materials = Material.objects.filter(name__startswith="Final Test")
            if materials.exists():
                material = materials.first()
                
                # Check stock levels
                stock_levels = material.stocklevel_set.all()
                if stock_levels.exists():
                    self.log_success("Material -> StockLevel relationship")
                
                # Check used materials
                used_materials = material.usedmaterial_set.all()
                if used_materials.exists():
                    self.log_success("Material -> UsedMaterial relationship")
            
            # Test order relationships
            orders = Order.objects.filter(description__contains="Final test")
            if orders.exists():
                order = orders.first()
                
                # Check step executions
                if order.step_executions.exists():
                    self.log_success("Order -> ProductionStepExecution relationship")
                
                # Check used materials
                if order.used_materials.exists():
                    self.log_success("Order -> UsedMaterial relationship")
            
            # Test location relationships
            locations = Location.objects.filter(name__startswith="Final Test")
            for location in locations:
                if hasattr(location, 'stocklevel_set') and location.stocklevel_set.exists():
                    self.log_success(f"Location -> StockLevel relationship ({location.location_type})")
                    
        except Exception as e:
            self.log_error("Model relationships", str(e))

    def cleanup_final_test(self):
        """Clean up final test data"""
        print("\n🧹 Final test ma'lumotlarini tozalash...")
        
        try:
            # Delete in correct order
            ProductionOutput.objects.filter(product__name__startswith="Final Test").delete()
            UsedMaterial.objects.filter(material__name__startswith="Final Test").delete()
            ProductionStepExecution.objects.filter(order__description__contains="Final test").delete()
            Order.objects.filter(description__contains="Final test").delete()
            InventoryMovementLog.objects.filter(material__name__startswith="Final Test").delete()
            StockLevel.objects.filter(material__name__startswith="Final Test").delete()
            ProductComponent.objects.filter(finished_product__name__startswith="Final Test").delete()
            Location.objects.filter(name__startswith="Final Test").delete()
            WorkCenter.objects.filter(name__startswith="Final Test").delete()
            Warehouse.objects.filter(name__startswith="Final Test").delete()
            Product.objects.filter(name__startswith="Final Test").delete()
            Material.objects.filter(name__startswith="Final Test").delete()
            User.objects.filter(username='finaltest').delete()
            
            self.log_success("Final test ma'lumotlari tozalandi")
            
        except Exception as e:
            self.log_error("Final cleanup", str(e))

    def run_final_tests(self):
        """Run all final tests"""
        print("🎯 ISOCOM II - FINAL COMPREHENSIVE TEST")
        print("=" * 50)
        
        # Run all tests
        self.test_server_status()
        self.test_api_documentation()
        self.test_admin_panel()
        self.test_complete_workflow()
        self.test_model_relationships()
        
        # Final results
        print(f"\n📊 FINAL TEST NATIJALARI:")
        print(f"   ✅ Muvaffaqiyatli testlar: {self.passed}")
        print(f"   ❌ Muvaffaqiyatsiz testlar: {self.failed}")
        total = self.passed + self.failed
        if total > 0:
            success_rate = (self.passed / total) * 100
            print(f"   📈 Muvaffaqiyat darajasi: {success_rate:.1f}%")
        
        if self.failed == 0:
            print("\n🎉 BARCHA TESTLAR MUVAFFAQIYATLI!")
            print("🚀 Loyiha to'liq tayyor va ishga tushirishga yaroqli!")
        else:
            print(f"\n⚠️  {self.failed} ta test muvaffaqiyatsiz tugadi.")
            print("🔧 Ushbu muammolarni hal qilish tavsiya etiladi.")
        
        # Cleanup
        self.cleanup_final_test()
        
        print("\n" + "=" * 50)
        print("FINAL TEST YAKUNLANDI")

if __name__ == "__main__":
    final_test = FinalTest()
    final_test.run_final_tests()
