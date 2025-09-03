#!/usr/bin/env python
"""
Comprehensive test for the entire ISOCOM II project
Bu test barcha asosiy funksionalliklarni tekshiradi
"""

import os
import django
from decimal import Decimal

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isocom_backend.settings')
django.setup()

from django.core.exceptions import ValidationError
from django.db import transaction
from apps.material.models import Material
from apps.product.models import Product, ProductComponent
from apps.workcenter.models import WorkCenter
from apps.warehouse.models import Warehouse, Location
from apps.stock.models import StockLevel, InventoryMovementLog
from apps.production.models import Order, ProductionStep, ProductionStepExecution, UsedMaterial, ProductionOutput
from apps.user.models import User

class ComprehensiveTest:
    def __init__(self):
        self.test_data = {}
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_success(self, test_name):
        print(f"   ✅ {test_name}")
        self.passed_tests += 1
        
    def log_error(self, test_name, error):
        print(f"   ❌ {test_name}: {error}")
        self.failed_tests += 1
        
    def cleanup(self):
        """Clean up all test data"""
        print("🧹 Test ma'lumotlarini tozalash...")
        try:
            # Delete in reverse order to avoid foreign key constraints
            ProductionOutput.objects.filter(product__name__startswith="Test").delete()
            UsedMaterial.objects.filter(material__name__startswith="Test").delete()
            ProductionStepExecution.objects.filter(order__produced_product__name__startswith="Test").delete()
            Order.objects.filter(produced_product__name__startswith="Test").delete()
            ProductionStep.objects.filter(name__startswith="Test").delete()
            InventoryMovementLog.objects.filter(material__name__startswith="Test").delete()
            StockLevel.objects.filter(material__name__startswith="Test").delete()
            ProductComponent.objects.filter(finished_product__name__startswith="Test").delete()
            Location.objects.filter(name__startswith="Test").delete()
            WorkCenter.objects.filter(name__startswith="Test").delete()
            Warehouse.objects.filter(name__startswith="Test").delete()
            Product.objects.filter(name__startswith="Test").delete()
            Material.objects.filter(name__startswith="Test").delete()
            User.objects.filter(username__startswith="test").delete()
            print("✅ Test ma'lumotlari tozalandi")
        except Exception as e:
            print(f"❌ Tozalashda xatolik: {e}")

    def test_material_model(self):
        """Test Material model"""
        print("\n📦 Material Model Testi")
        
        try:
            # Create material
            material = Material.objects.create(
                name="Test Plastic Granules",
                code="TPG001",
                type="GRANULA",
                unit_of_measure="KG",
                description="Test plastic granules for testing",
                price=Decimal("15.50")
            )
            self.test_data['material'] = material
            self.log_success("Material yaratildi")
            
            # Test slug generation
            if material.slug:
                self.log_success("Slug avtomatik yaratildi")
            else:
                self.log_error("Slug yaratilmadi", "slug field empty")
                
            # Test string representation
            expected_str = f"{material.name} ({material.get_type_display()})"
            if str(material) == expected_str:
                self.log_success("String representation to'g'ri")
            else:
                self.log_error("String representation", f"Expected: {expected_str}, Got: {str(material)}")
                
        except Exception as e:
            self.log_error("Material yaratish", str(e))

    def test_product_model(self):
        """Test Product model and components"""
        print("\n🏭 Product Model Testi")
        
        try:
            # Create finished product
            finished_product = Product.objects.create(
                name="Test Finished Product",
                code="TFP001",
                type="FINISHED",
                description="Test finished product"
            )
            self.test_data['finished_product'] = finished_product
            self.log_success("Finished product yaratildi")
            
            # Create semi-finished product
            semi_product = Product.objects.create(
                name="Test Semi Product",
                code="TSP001", 
                type="SEMI_FINISHED",
                description="Test semi-finished product"
            )
            self.test_data['semi_product'] = semi_product
            self.log_success("Semi-finished product yaratildi")
            
            # Create product component relationship
            component = ProductComponent.objects.create(
                finished_product=finished_product,
                semi_finished_product=semi_product
            )
            self.log_success("Product component bog'lanishi yaratildi")
            
        except Exception as e:
            self.log_error("Product yaratish", str(e))

    def test_workcenter_and_location(self):
        """Test WorkCenter and Location models"""
        print("\n🏭 WorkCenter va Location Testi")
        
        try:
            # Create warehouse
            warehouse = Warehouse.objects.create(
                name="Test Main Warehouse",
                description="Test warehouse for testing"
            )
            self.test_data['warehouse'] = warehouse
            self.log_success("Warehouse yaratildi")
            
            # Create warehouse location
            warehouse_location = Location.objects.create(
                name="Test Warehouse Location",
                location_type="WAREHOUSE",
                warehouse=warehouse
            )
            self.test_data['warehouse_location'] = warehouse_location
            self.log_success("Warehouse location yaratildi")
            
            # Create workcenter
            workcenter = WorkCenter.objects.create(
                name="Test Extruder Machine",
                type="EXTRUDER",
                description="Test extruder machine",
                capacity_per_hour=100,
                capacity_unit="KG"
            )
            self.test_data['workcenter'] = workcenter
            self.log_success("WorkCenter yaratildi")
            
            # Create workcenter location
            workcenter_location = Location.objects.create(
                name="Test WorkCenter Location",
                location_type="WORKCENTER",
                work_center=workcenter
            )
            self.test_data['workcenter_location'] = workcenter_location
            self.log_success("WorkCenter location yaratildi")
            
        except Exception as e:
            self.log_error("WorkCenter/Location yaratish", str(e))

    def test_stocklevel_restrictions(self):
        """Test StockLevel model with warehouse restrictions"""
        print("\n📊 StockLevel Model Testi")
        
        try:
            material = self.test_data.get('material')
            warehouse_location = self.test_data.get('warehouse_location')
            workcenter_location = self.test_data.get('workcenter_location')
            
            if not all([material, warehouse_location, workcenter_location]):
                self.log_error("StockLevel test", "Required test data missing")
                return
            
            # Test warehouse location (should work)
            stock_warehouse = StockLevel.objects.create(
                material=material,
                location=warehouse_location,
                quantity=Decimal("1000.00")
            )
            self.test_data['stock_warehouse'] = stock_warehouse
            self.log_success("Warehouse location uchun StockLevel yaratildi")
            
            # Test workcenter location (should work)
            stock_workcenter = StockLevel.objects.create(
                material=material,
                location=workcenter_location,
                quantity=Decimal("500.00")
            )
            self.test_data['stock_workcenter'] = stock_workcenter
            self.log_success("WorkCenter location uchun StockLevel yaratildi")
            
            # Test workshop location (should fail)
            try:
                workshop_location = Location.objects.create(
                    name="Test Workshop Location",
                    location_type="WORKSHOP"
                )
                
                StockLevel.objects.create(
                    material=material,
                    location=workshop_location,
                    quantity=Decimal("100.00")
                )
                self.log_error("Workshop restriction", "Workshop location uchun StockLevel yaratildi (bo'lmasligi kerak edi)")
                
            except ValidationError:
                self.log_success("Workshop location uchun StockLevel restriction ishladi")
            except Exception as e:
                self.log_error("Workshop restriction test", str(e))
                
        except Exception as e:
            self.log_error("StockLevel yaratish", str(e))

    def test_inventory_movement(self):
        """Test InventoryMovementLog"""
        print("\n📋 InventoryMovementLog Testi")
        
        try:
            material = self.test_data.get('material')
            warehouse_location = self.test_data.get('warehouse_location')
            workcenter_location = self.test_data.get('workcenter_location')
            
            if not all([material, warehouse_location, workcenter_location]):
                self.log_error("InventoryMovement test", "Required test data missing")
                return
            
            # Create inventory movement (warehouse to workcenter)
            movement = InventoryMovementLog.objects.create(
                material=material,
                quantity=Decimal("200.00"),
                from_location=warehouse_location,
                to_location=workcenter_location
            )
            self.log_success("InventoryMovementLog yaratildi")
            
            # Check stock levels after movement
            warehouse_stock = StockLevel.objects.get(material=material, location=warehouse_location)
            workcenter_stock = StockLevel.objects.get(material=material, location=workcenter_location)
            
            if warehouse_stock.quantity == Decimal("800.00"):  # 1000 - 200
                self.log_success("Warehouse stock to'g'ri ayrildi")
            else:
                self.log_error("Warehouse stock", f"Expected 800, got {warehouse_stock.quantity}")
                
            if workcenter_stock.quantity == Decimal("700.00"):  # 500 + 200
                self.log_success("WorkCenter stock to'g'ri qo'shildi")
            else:
                self.log_error("WorkCenter stock", f"Expected 700, got {workcenter_stock.quantity}")
                
        except Exception as e:
            self.log_error("InventoryMovement yaratish", str(e))

    def test_production_workflow(self):
        """Test complete production workflow"""
        print("\n🏭 Production Workflow Testi")
        
        try:
            # Create user
            user = User.objects.create(
                username="test_operator",
                first_name="Test",
                last_name="Operator",
                role="WORKER"
            )
            self.test_data['user'] = user
            self.log_success("User yaratildi")
            
            # Create production steps
            steps_data = [
                ("EXTRUSION", "Test Extrusion", 1, 8.0),
                ("DEGASSING", "Test Degassing", 2, 240.0),
                ("PACKAGING", "Test Packaging", 3, 1.0),
                ("QUALITY_CONTROL", "Test Quality Control", 4, 0.5),
            ]
            
            steps = []
            for step_type, name, sequence, duration in steps_data:
                step = ProductionStep.objects.create(
                    step_type=step_type,
                    name=name,
                    order_sequence=sequence,
                    duration_hours=Decimal(str(duration))
                )
                steps.append(step)
            
            self.test_data['production_steps'] = steps
            self.log_success(f"{len(steps)} ta ProductionStep yaratildi")
            
            # Create order
            finished_product = self.test_data.get('finished_product')
            if not finished_product:
                self.log_error("Order yaratish", "Finished product topilmadi")
                return
                
            order = Order.objects.create(
                produced_product=finished_product,
                unit_of_measure="KG",
                produced_quantity=Decimal("100.00"),
                status="PENDING",
                description="Test production order"
            )
            order.operators.add(user)
            self.test_data['order'] = order
            self.log_success("Order yaratildi")
            
            # Create step executions
            workcenter = self.test_data.get('workcenter')
            step_executions = []
            
            for step in steps:
                execution = ProductionStepExecution.objects.create(
                    order=order,
                    production_step=step,
                    status="PENDING",
                    assigned_operator=user,
                    work_center=workcenter
                )
                step_executions.append(execution)
                
            self.test_data['step_executions'] = step_executions
            self.log_success(f"{len(step_executions)} ta ProductionStepExecution yaratildi")
            
        except Exception as e:
            self.log_error("Production workflow yaratish", str(e))

    def test_used_material_logic(self):
        """Test UsedMaterial with workcenter logic"""
        print("\n🔧 UsedMaterial Logic Testi")
        
        try:
            material = self.test_data.get('material')
            order = self.test_data.get('order')
            step_executions = self.test_data.get('step_executions')
            workcenter_location = self.test_data.get('workcenter_location')
            
            if not all([material, order, step_executions, workcenter_location]):
                self.log_error("UsedMaterial test", "Required test data missing")
                return
            
            # Get initial stock
            initial_stock = StockLevel.objects.get(material=material, location=workcenter_location)
            initial_quantity = initial_stock.quantity
            self.log_success(f"Boshlang'ich stock: {initial_quantity} kg")
            
            # Test material usage (should work)
            used_material = UsedMaterial.objects.create(
                order=order,
                material=material,
                quantity=Decimal("50.00"),
                step_execution=step_executions[0]  # Extrusion step
            )
            self.log_success("UsedMaterial yaratildi")
            
            # Check stock after usage
            updated_stock = StockLevel.objects.get(material=material, location=workcenter_location)
            expected_quantity = initial_quantity - Decimal("50.00")
            
            if updated_stock.quantity == expected_quantity:
                self.log_success("Stock to'g'ri ayrildi")
            else:
                self.log_error("Stock ayrilishi", f"Expected {expected_quantity}, got {updated_stock.quantity}")
            
            # Test insufficient material (should fail)
            try:
                UsedMaterial.objects.create(
                    order=order,
                    material=material,
                    quantity=Decimal("1000.00"),  # More than available
                    step_execution=step_executions[1]
                )
                self.log_error("Insufficient material test", "Yetarli bo'lmagan material bilan ham yaratildi")
            except ValidationError:
                self.log_success("Insufficient material validation ishladi")
            except Exception as e:
                self.log_error("Insufficient material test", str(e))
                
        except Exception as e:
            self.log_error("UsedMaterial logic", str(e))

    def test_production_output(self):
        """Test ProductionOutput"""
        print("\n📦 ProductionOutput Testi")
        
        try:
            finished_product = self.test_data.get('finished_product')
            step_executions = self.test_data.get('step_executions')
            
            if not all([finished_product, step_executions]):
                self.log_error("ProductionOutput test", "Required test data missing")
                return
            
            # Create production output
            output = ProductionOutput.objects.create(
                step_execution=step_executions[0],  # Extrusion step
                product=finished_product,
                unit_of_measure="KG",
                quantity=Decimal("45.00"),
                weight=Decimal("45.500"),
                quality_status="PASSED",
                notes="Test production output"
            )
            self.log_success("ProductionOutput yaratildi")
            
            # Test string representation
            expected_str = f"{output.product.name} - {output.quantity} {output.get_unit_of_measure_display()} ({output.get_quality_status_display()})"
            if str(output) == expected_str:
                self.log_success("ProductionOutput string representation to'g'ri")
            else:
                self.log_error("ProductionOutput string", f"Expected: {expected_str}, Got: {str(output)}")
                
        except Exception as e:
            self.log_error("ProductionOutput yaratish", str(e))

    def test_order_helper_methods(self):
        """Test Order helper methods"""
        print("\n📋 Order Helper Methods Testi")
        
        try:
            order = self.test_data.get('order')
            if not order:
                self.log_error("Order helper test", "Order topilmadi")
                return
            
            # Test get_current_step
            current_step = order.get_current_step()
            if current_step:
                self.log_success("get_current_step() ishladi")
            else:
                self.log_error("get_current_step()", "Current step topilmadi")
            
            # Test get_completion_percentage
            completion = order.get_completion_percentage()
            if isinstance(completion, (int, float)) and 0 <= completion <= 100:
                self.log_success(f"get_completion_percentage(): {completion}%")
            else:
                self.log_error("get_completion_percentage()", f"Invalid percentage: {completion}")
                
        except Exception as e:
            self.log_error("Order helper methods", str(e))

    def run_all_tests(self):
        """Run all tests"""
        print("🚀 ISOCOM II - To'liq Loyiha Testi Boshlanmoqda...\n")
        
        # Cleanup first
        self.cleanup()
        
        # Run all tests
        self.test_material_model()
        self.test_product_model()
        self.test_workcenter_and_location()
        self.test_stocklevel_restrictions()
        self.test_inventory_movement()
        self.test_production_workflow()
        self.test_used_material_logic()
        self.test_production_output()
        self.test_order_helper_methods()
        
        # Final results
        print(f"\n📊 Test Natijalari:")
        print(f"   ✅ Muvaffaqiyatli: {self.passed_tests}")
        print(f"   ❌ Xatolik: {self.failed_tests}")
        print(f"   📈 Muvaffaqiyat foizi: {(self.passed_tests / (self.passed_tests + self.failed_tests) * 100):.1f}%")
        
        if self.failed_tests == 0:
            print("\n🎉 BARCHA TESTLAR MUVAFFAQIYATLI!")
        else:
            print(f"\n⚠️  {self.failed_tests} ta test muvaffaqiyatsiz tugadi.")
        
        # Cleanup at the end
        self.cleanup()

if __name__ == "__main__":
    test = ComprehensiveTest()
    test.run_all_tests()
