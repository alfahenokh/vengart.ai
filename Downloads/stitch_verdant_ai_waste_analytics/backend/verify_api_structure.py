"""
Manual Verification Script for Task 6.1
Tests the API structure without requiring database connection
"""
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def verify_imports():
    """Verify all modules can be imported"""
    print("=" * 60)
    print("TASK 6.1 VERIFICATION: FastAPI Application Structure")
    print("=" * 60)
    print()
    
    print("1. Verifying module imports...")
    try:
        from app.middleware import LoggingMiddleware, ErrorHandlerMiddleware, RequestIDMiddleware
        print("   ✓ Middleware modules imported successfully")
    except ImportError as e:
        print(f"   ✗ Failed to import middleware: {e}")
        return False
    
    try:
        from app.api.v1.api import api_router
        print("   ✓ API router imported successfully")
    except ImportError as e:
        print(f"   ✗ Failed to import API router: {e}")
        return False
    
    try:
        from app.api.v1.endpoints import health
        print("   ✓ Health endpoints imported successfully")
    except ImportError as e:
        print(f"   ✗ Failed to import health endpoints: {e}")
        return False
    
    print()
    return True


def verify_structure():
    """Verify directory structure"""
    print("2. Verifying directory structure...")
    
    required_files = [
        "app/api/__init__.py",
        "app/api/v1/__init__.py",
        "app/api/v1/api.py",
        "app/api/v1/endpoints/__init__.py",
        "app/api/v1/endpoints/health.py",
        "app/middleware/__init__.py",
        "app/middleware/request_id.py",
        "app/middleware/logging.py",
        "app/middleware/error_handler.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = backend_dir / file_path
        if full_path.exists():
            print(f"   ✓ {file_path}")
        else:
            print(f"   ✗ {file_path} - NOT FOUND")
            all_exist = False
    
    print()
    return all_exist


def verify_middleware_classes():
    """Verify middleware classes are properly defined"""
    print("3. Verifying middleware classes...")
    
    try:
        from app.middleware.request_id import RequestIDMiddleware
        from app.middleware.logging import LoggingMiddleware
        from app.middleware.error_handler import ErrorHandlerMiddleware
        from starlette.middleware.base import BaseHTTPMiddleware
        
        # Check if they inherit from BaseHTTPMiddleware
        if issubclass(RequestIDMiddleware, BaseHTTPMiddleware):
            print("   ✓ RequestIDMiddleware properly defined")
        else:
            print("   ✗ RequestIDMiddleware does not inherit from BaseHTTPMiddleware")
            return False
        
        if issubclass(LoggingMiddleware, BaseHTTPMiddleware):
            print("   ✓ LoggingMiddleware properly defined")
        else:
            print("   ✗ LoggingMiddleware does not inherit from BaseHTTPMiddleware")
            return False
        
        if issubclass(ErrorHandlerMiddleware, BaseHTTPMiddleware):
            print("   ✓ ErrorHandlerMiddleware properly defined")
        else:
            print("   ✗ ErrorHandlerMiddleware does not inherit from BaseHTTPMiddleware")
            return False
        
        print()
        return True
    except Exception as e:
        print(f"   ✗ Error verifying middleware classes: {e}")
        print()
        return False


def verify_api_router():
    """Verify API router configuration"""
    print("4. Verifying API router configuration...")
    
    try:
        from app.api.v1.api import api_router
        from fastapi import APIRouter
        
        if isinstance(api_router, APIRouter):
            print("   ✓ api_router is a FastAPI APIRouter instance")
        else:
            print("   ✗ api_router is not a FastAPI APIRouter instance")
            return False
        
        # Check if health router is included
        if len(api_router.routes) > 0:
            print(f"   ✓ API router has {len(api_router.routes)} route(s) configured")
        else:
            print("   ✗ API router has no routes configured")
            return False
        
        print()
        return True
    except Exception as e:
        print(f"   ✗ Error verifying API router: {e}")
        print()
        return False


def verify_health_endpoints():
    """Verify health endpoints are defined"""
    print("5. Verifying health endpoints...")
    
    try:
        from app.api.v1.endpoints.health import router
        from fastapi import APIRouter
        
        if isinstance(router, APIRouter):
            print("   ✓ Health router is a FastAPI APIRouter instance")
        else:
            print("   ✗ Health router is not a FastAPI APIRouter instance")
            return False
        
        # Check routes
        routes = [route.path for route in router.routes]
        print(f"   ✓ Health router has {len(routes)} endpoint(s):")
        for route in routes:
            print(f"      - {route}")
        
        print()
        return True
    except Exception as e:
        print(f"   ✗ Error verifying health endpoints: {e}")
        print()
        return False


def main():
    """Run all verifications"""
    results = []
    
    results.append(("Module Imports", verify_imports()))
    results.append(("Directory Structure", verify_structure()))
    results.append(("Middleware Classes", verify_middleware_classes()))
    results.append(("API Router", verify_api_router()))
    results.append(("Health Endpoints", verify_health_endpoints()))
    
    print("=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name:.<40} {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All verifications passed! Task 6.1 implementation is complete.")
        print()
        print("Next steps:")
        print("1. Start the server: python main.py")
        print("2. Visit http://localhost:8000/api/docs for API documentation")
        print("3. Test endpoints:")
        print("   - GET http://localhost:8000/")
        print("   - GET http://localhost:8000/health")
        print("   - GET http://localhost:8000/api/v1/health")
        print("   - GET http://localhost:8000/api/v1/status")
    else:
        print("❌ Some verifications failed. Please review the errors above.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
