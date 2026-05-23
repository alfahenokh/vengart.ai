#!/usr/bin/env python3
"""
Property-based tests for data model validation
**Validates: Requirements 3.5**

This module implements property-based tests using Hypothesis to validate that
Pydantic schemas work correctly across a wide range of inputs and ensure
API performance and reliability through comprehensive data validation.
"""
import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal, InvalidOperation
from typing import Dict, Any, List, Optional
from uuid import UUID, uuid4
import json

from hypothesis import given, strategies as st, assume, settings, HealthCheck
from hypothesis.strategies import composite
from pydantic import ValidationError, EmailStr

# Import all schemas to test
# Import schemas directly to avoid database dependency issues
try:
    from app.schemas.user import (
        UserBase, UserCreate, UserUpdate, UserResponse, UserProfile, UserPreferences,
        UserLogin, TokenResponse, UserLoginResponse, PasswordReset, PasswordResetConfirm
    )
    from app.schemas.fleet import (
        FleetUnitBase, FleetUnitCreate, FleetUnitUpdate, FleetUnitResponse,
        GeoLocation, RouteData, MaintenanceRecordBase, MaintenanceRecordCreate,
        MaintenanceRecordUpdate, MaintenanceRecordResponse, FleetStatusSummary
    )
    from app.schemas.analytics import (
        WasteForecastBase, WasteForecastCreate, WasteForecastResponse,
        ForecastPoint, PredictionFactor, KPIMetricBase, KPIMetricCreate,
        KPIMetricResponse, AnalyticsReportBase, AnalyticsReportCreate,
        AnalyticsReportResponse
    )
    from app.schemas.simulation import (
        SimulationScenarioBase, SimulationScenarioCreate, SimulationScenarioUpdate,
        SimulationScenarioResponse, SimulationParameters, SimulationConstraint,
        SimulationExecutionBase, SimulationExecutionCreate, SimulationExecutionResponse,
        SimulationLogBase, SimulationLogResponse, RouteOptimizationBase,
        RouteOptimizationResponse, Waypoint
    )
    from app.models.user import UserRole
    from app.models.fleet import FleetUnitType, FleetUnitStatus, CapacityUnit
except ImportError:
    # Define enums locally if imports fail
    from enum import Enum
    
    class UserRole(str, Enum):
        ADMIN = "admin"
        OPERATOR = "operator"
        ANALYST = "analyst"
        VIEWER = "viewer"
    
    class FleetUnitType(str, Enum):
        COLLECTION = "collection"
        TRANSPORT = "transport"
        PROCESSING = "processing"
    
    class FleetUnitStatus(str, Enum):
        ACTIVE = "active"
        IDLE = "idle"
        MAINTENANCE = "maintenance"
        OFFLINE = "offline"
    
    class CapacityUnit(str, Enum):
        TONS = "tons"
        CUBIC_METERS = "cubic_meters"
    
    # Skip schema imports if they fail
    print("Warning: Could not import schemas due to database dependencies. Skipping schema tests.")


# Custom strategies for domain-specific data types
@composite
def valid_coordinates(draw):
    """Generate valid latitude/longitude coordinates"""
    latitude = draw(st.decimals(min_value=-90, max_value=90, places=8))
    longitude = draw(st.decimals(min_value=-180, max_value=180, places=8))
    return latitude, longitude


@composite
def valid_email_strategy(draw):
    """Generate valid email addresses"""
    username = draw(st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Ll', 'Lu', 'Nd'))))
    domain = draw(st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Ll', 'Lu', 'Nd'))))
    tld = draw(st.sampled_from(['com', 'org', 'net', 'edu', 'gov']))
    return f"{username}@{domain}.{tld}"


@composite
def valid_username_strategy(draw):
    """Generate valid usernames"""
    base = draw(st.text(min_size=3, max_size=50, alphabet=st.characters(whitelist_categories=('Ll', 'Lu', 'Nd'))))
    separators = draw(st.lists(st.sampled_from(['_', '-']), max_size=3))
    # Insert separators randomly
    result = base
    for sep in separators:
        if len(result) < 49:  # Leave room for separator
            pos = draw(st.integers(min_value=1, max_value=len(result)-1))
            result = result[:pos] + sep + result[pos:]
    return result[:50]  # Ensure max length


@composite
def valid_password_strategy(draw):
    """Generate valid passwords meeting strength requirements"""
    # Ensure at least one of each required character type
    upper = draw(st.text(min_size=1, max_size=5, alphabet=st.characters(whitelist_categories=('Lu',))))
    lower = draw(st.text(min_size=1, max_size=5, alphabet=st.characters(whitelist_categories=('Ll',))))
    digit = draw(st.text(min_size=1, max_size=5, alphabet=st.characters(whitelist_categories=('Nd',))))
    
    # Add additional characters to reach minimum length
    additional_length = max(0, 8 - len(upper) - len(lower) - len(digit))
    additional = draw(st.text(min_size=additional_length, max_size=20, 
                             alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc', 'Pd', 'Po'))))
    
    # Combine and shuffle
    all_chars = list(upper + lower + digit + additional)
    draw(st.randoms()).shuffle(all_chars)
    return ''.join(all_chars)[:128]  # Ensure max length


@composite
def valid_decimal_strategy(draw, min_value=None, max_value=None, places=None):
    """Generate valid decimal values"""
    return draw(st.decimals(min_value=min_value, max_value=max_value, places=places, allow_nan=False, allow_infinity=False))


@composite
def valid_json_metadata(draw):
    """Generate valid JSON metadata"""
    return draw(st.dictionaries(
        keys=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Ll', 'Lu', 'Nd'))),
        values=st.one_of(
            st.text(max_size=100),
            st.integers(min_value=-1000000, max_value=1000000),
            st.floats(min_value=-1000000, max_value=1000000, allow_nan=False, allow_infinity=False),
            st.booleans(),
            st.none()
        ),
        max_size=10
    ))


class TestUserSchemas:
    """Property-based tests for user-related schemas"""
    
    @given(
        username=valid_username_strategy(),
        email=valid_email_strategy(),
        role=st.sampled_from(UserRole),
        first_name=st.one_of(st.none(), st.text(min_size=1, max_size=50)),
        last_name=st.one_of(st.none(), st.text(min_size=1, max_size=50)),
        department=st.one_of(st.none(), st.text(min_size=1, max_size=100))
    )
    def test_user_base_validation_property(self, username, email, role, first_name, last_name, department):
        """
        **Validates: Requirements 3.5**
        Property: For any valid user data, UserBase schema SHALL validate successfully
        and normalize username to lowercase
        """
        profile = None
        if first_name or last_name or department:
            profile = UserProfile(
                first_name=first_name,
                last_name=last_name,
                department=department
            )
        
        user = UserBase(
            username=username,
            email=email,
            role=role,
            profile=profile
        )
        
        # Verify username normalization
        assert user.username == username.lower()
        assert user.email == email
        assert user.role == role
        if profile:
            assert user.profile.first_name == first_name
            assert user.profile.last_name == last_name
            assert user.profile.department == department

    @given(
        username=valid_username_strategy(),
        email=valid_email_strategy(),
        password=valid_password_strategy(),
        role=st.sampled_from(UserRole)
    )
    def test_user_create_validation_property(self, username, email, password, role):
        """
        **Validates: Requirements 3.5**
        Property: For any valid user creation data with matching passwords,
        UserCreate schema SHALL validate successfully
        """
        user = UserCreate(
            username=username,
            email=email,
            password=password,
            confirm_password=password,  # Matching password
            role=role
        )
        
        assert user.username == username.lower()
        assert user.email == email
        assert user.password == password
        assert user.confirm_password == password
        assert user.role == role

    @given(
        username=valid_username_strategy(),
        password=valid_password_strategy()
    )
    def test_user_login_validation_property(self, username, password):
        """
        **Validates: Requirements 3.5**
        Property: For any valid username and password, UserLogin schema SHALL validate successfully
        """
        login = UserLogin(
            username=username,
            password=password,
            remember_me=True
        )
        
        assert login.username == username
        assert login.password == password
        assert login.remember_me is True

    @given(st.text(min_size=1, max_size=2))  # Invalid username (too short)
    def test_user_validation_rejects_invalid_username(self, invalid_username):
        """
        **Validates: Requirements 3.5**
        Property: For any invalid username (too short), UserBase SHALL reject with ValidationError
        """
        with pytest.raises(ValidationError):
            UserBase(
                username=invalid_username,
                email="test@example.com",
                role=UserRole.VIEWER
            )

    @given(st.text(min_size=1, max_size=7))  # Invalid password (too short)
    def test_password_validation_rejects_weak_passwords(self, weak_password):
        """
        **Validates: Requirements 3.5**
        Property: For any weak password (less than 8 characters), UserCreate SHALL reject with ValidationError
        """
        with pytest.raises(ValidationError):
            UserCreate(
                username="testuser",
                email="test@example.com",
                password=weak_password,
                confirm_password=weak_password,
                role=UserRole.VIEWER
            )


class TestFleetSchemas:
    """Property-based tests for fleet management schemas"""
    
    @given(
        latitude=st.decimals(min_value=-90, max_value=90, places=8),
        longitude=st.decimals(min_value=-180, max_value=180, places=8),
        address=st.one_of(st.none(), st.text(min_size=1, max_size=255))
    )
    def test_geolocation_validation_property(self, latitude, longitude, address):
        """
        **Validates: Requirements 3.5**
        Property: For any valid coordinates within Earth's bounds, GeoLocation SHALL validate successfully
        """
        location = GeoLocation(
            latitude=latitude,
            longitude=longitude,
            address=address
        )
        
        assert location.latitude == latitude
        assert location.longitude == longitude
        assert location.address == address

    @given(
        identifier=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pd', 'Pc'))),
        fleet_type=st.sampled_from(FleetUnitType),
        status=st.sampled_from(FleetUnitStatus),
        max_capacity=valid_decimal_strategy(min_value=0.01, max_value=1000000, places=2),
        current_capacity=st.one_of(st.none(), valid_decimal_strategy(min_value=0, max_value=1000000, places=2)),
        capacity_unit=st.sampled_from(CapacityUnit)
    )
    def test_fleet_unit_validation_property(self, identifier, fleet_type, status, max_capacity, current_capacity, capacity_unit):
        """
        **Validates: Requirements 3.5**
        Property: For any valid fleet unit data, FleetUnitCreate SHALL validate successfully
        and normalize identifier to uppercase
        """
        # Ensure current capacity doesn't exceed maximum
        if current_capacity is not None:
            current_capacity = min(current_capacity, max_capacity)
        else:
            current_capacity = Decimal('0')
        
        fleet_unit = FleetUnitCreate(
            identifier=identifier,
            type=fleet_type,
            status=status,
            maximum_capacity=max_capacity,
            current_capacity=current_capacity,
            capacity_unit=capacity_unit
        )
        
        # Verify identifier normalization
        assert fleet_unit.identifier == identifier.upper()
        assert fleet_unit.type == fleet_type
        assert fleet_unit.status == status
        assert fleet_unit.maximum_capacity == max_capacity
        assert fleet_unit.current_capacity == current_capacity
        assert fleet_unit.capacity_unit == capacity_unit

    @given(
        latitude=st.decimals(min_value=91, max_value=180, places=8)  # Invalid latitude
    )
    def test_geolocation_rejects_invalid_latitude(self, invalid_latitude):
        """
        **Validates: Requirements 3.5**
        Property: For any latitude outside valid range, GeoLocation SHALL reject with ValidationError
        """
        with pytest.raises(ValidationError):
            GeoLocation(
                latitude=invalid_latitude,
                longitude=Decimal('0')
            )

    @given(
        longitude=st.decimals(min_value=181, max_value=360, places=8)  # Invalid longitude
    )
    def test_geolocation_rejects_invalid_longitude(self, invalid_longitude):
        """
        **Validates: Requirements 3.5**
        Property: For any longitude outside valid range, GeoLocation SHALL reject with ValidationError
        """
        with pytest.raises(ValidationError):
            GeoLocation(
                latitude=Decimal('0'),
                longitude=invalid_longitude
            )


class TestAnalyticsSchemas:
    """Property-based tests for analytics schemas"""
    
    @given(
        name=st.text(min_size=1, max_size=100),
        weight=valid_decimal_strategy(min_value=0, max_value=1, places=4),
        value=valid_decimal_strategy(min_value=-1000000, max_value=1000000, places=2),
        impact=st.text(min_size=1, max_size=200)
    )
    def test_prediction_factor_validation_property(self, name, weight, value, impact):
        """
        **Validates: Requirements 3.5**
        Property: For any valid prediction factor data, PredictionFactor SHALL validate successfully
        """
        factor = PredictionFactor(
            name=name,
            weight=weight,
            value=value,
            impact=impact
        )
        
        assert factor.name == name
        assert factor.weight == weight
        assert factor.value == value
        assert factor.impact == impact

    @given(
        forecast_date=st.dates(min_value=date(2020, 1, 1), max_value=date(2030, 12, 31)),
        predicted_volume=valid_decimal_strategy(min_value=0, max_value=1000000, places=2),
        confidence=valid_decimal_strategy(min_value=0, max_value=100, places=2),
        lower_bound=st.one_of(st.none(), valid_decimal_strategy(min_value=0, max_value=1000000, places=2)),
        upper_bound=st.one_of(st.none(), valid_decimal_strategy(min_value=0, max_value=1000000, places=2))
    )
    def test_forecast_point_validation_property(self, forecast_date, predicted_volume, confidence, lower_bound, upper_bound):
        """
        **Validates: Requirements 3.5**
        Property: For any valid forecast data with proper bounds, ForecastPoint SHALL validate successfully
        """
        # Ensure upper bound is greater than lower bound if both are provided
        if lower_bound is not None and upper_bound is not None:
            if upper_bound <= lower_bound:
                upper_bound = lower_bound + Decimal('1')
        
        forecast_point = ForecastPoint(
            date=forecast_date,
            predicted_volume=predicted_volume,
            confidence=confidence,
            lower_bound=lower_bound,
            upper_bound=upper_bound
        )
        
        assert forecast_point.date == forecast_date
        assert forecast_point.predicted_volume == predicted_volume
        assert forecast_point.confidence == confidence
        assert forecast_point.lower_bound == lower_bound
        assert forecast_point.upper_bound == upper_bound

    @given(
        region=st.text(min_size=1, max_size=100),
        start_date=st.dates(min_value=date(2020, 1, 1), max_value=date(2025, 12, 31)),
        days_ahead=st.integers(min_value=1, max_value=365)
    )
    def test_waste_forecast_date_range_property(self, region, start_date, days_ahead):
        """
        **Validates: Requirements 3.5**
        Property: For any valid date range, WasteForecastBase SHALL validate successfully
        """
        end_date = start_date + timedelta(days=days_ahead)
        
        forecast = WasteForecastBase(
            region=region,
            start_date=start_date,
            end_date=end_date
        )
        
        assert forecast.region == region
        assert forecast.start_date == start_date
        assert forecast.end_date == end_date
        assert forecast.end_date > forecast.start_date

    @given(
        confidence=valid_decimal_strategy(min_value=101, max_value=200, places=2)  # Invalid confidence
    )
    def test_forecast_point_rejects_invalid_confidence(self, invalid_confidence):
        """
        **Validates: Requirements 3.5**
        Property: For any confidence value outside 0-100 range, ForecastPoint SHALL reject with ValidationError
        """
        with pytest.raises(ValidationError):
            ForecastPoint(
                date=date.today(),
                predicted_volume=Decimal('100'),
                confidence=invalid_confidence
            )


class TestSimulationSchemas:
    """Property-based tests for simulation schemas"""
    
    @given(
        constraint_type=st.text(min_size=1, max_size=50),
        parameter=st.text(min_size=1, max_size=50),
        operator=st.sampled_from(['eq', 'lt', 'gt', 'lte', 'gte', 'in', 'not_in']),
        value=st.one_of(st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.text(), st.booleans())
    )
    def test_simulation_constraint_validation_property(self, constraint_type, parameter, operator, value):
        """
        **Validates: Requirements 3.5**
        Property: For any valid constraint data with valid operator, SimulationConstraint SHALL validate successfully
        """
        constraint = SimulationConstraint(
            type=constraint_type,
            parameter=parameter,
            operator=operator,
            value=value
        )
        
        assert constraint.type == constraint_type
        assert constraint.parameter == parameter
        assert constraint.operator == operator
        assert constraint.value == value

    @given(
        operational_mode=st.sampled_from(['efficiency', 'carbon_neutral', 'cost_reduction', 'balanced']),
        spatial_radius=valid_decimal_strategy(min_value=0.1, max_value=1000, places=2),
        fleet_capacity_load=valid_decimal_strategy(min_value=0, max_value=100, places=2),
        time_horizon=st.integers(min_value=1, max_value=168)  # 1 hour to 1 week
    )
    def test_simulation_parameters_validation_property(self, operational_mode, spatial_radius, fleet_capacity_load, time_horizon):
        """
        **Validates: Requirements 3.5**
        Property: For any valid simulation parameters, SimulationParameters SHALL validate successfully
        """
        params = SimulationParameters(
            operational_mode=operational_mode,
            spatial_radius=spatial_radius,
            fleet_capacity_load=fleet_capacity_load,
            time_horizon=time_horizon
        )
        
        assert params.operational_mode == operational_mode
        assert params.spatial_radius == spatial_radius
        assert params.fleet_capacity_load == fleet_capacity_load
        assert params.time_horizon == time_horizon

    @given(
        latitude=st.decimals(min_value=-90, max_value=90, places=8),
        longitude=st.decimals(min_value=-180, max_value=180, places=8),
        stop_type=st.sampled_from(['pickup', 'delivery', 'checkpoint', 'depot', 'maintenance']),
        priority=st.integers(min_value=1, max_value=5)
    )
    def test_waypoint_validation_property(self, latitude, longitude, stop_type, priority):
        """
        **Validates: Requirements 3.5**
        Property: For any valid waypoint data, Waypoint SHALL validate successfully
        """
        waypoint = Waypoint(
            latitude=latitude,
            longitude=longitude,
            stop_type=stop_type,
            priority=priority
        )
        
        assert waypoint.latitude == latitude
        assert waypoint.longitude == longitude
        assert waypoint.stop_type == stop_type
        assert waypoint.priority == priority

    @given(
        invalid_operator=st.text(min_size=1, max_size=20).filter(
            lambda x: x not in ['eq', 'lt', 'gt', 'lte', 'gte', 'in', 'not_in']
        )
    )
    def test_simulation_constraint_rejects_invalid_operator(self, invalid_operator):
        """
        **Validates: Requirements 3.5**
        Property: For any invalid constraint operator, SimulationConstraint SHALL reject with ValidationError
        """
        with pytest.raises(ValidationError):
            SimulationConstraint(
                type="test",
                parameter="test_param",
                operator=invalid_operator,
                value="test_value"
            )

    @given(
        invalid_mode=st.text(min_size=1, max_size=20).filter(
            lambda x: x not in ['efficiency', 'carbon_neutral', 'cost_reduction', 'balanced']
        )
    )
    def test_simulation_parameters_rejects_invalid_mode(self, invalid_mode):
        """
        **Validates: Requirements 3.5**
        Property: For any invalid operational mode, SimulationParameters SHALL reject with ValidationError
        """
        with pytest.raises(ValidationError):
            SimulationParameters(
                operational_mode=invalid_mode,
                spatial_radius=Decimal('10'),
                fleet_capacity_load=Decimal('50'),
                time_horizon=24
            )


class TestCrossSchemaValidation:
    """Property-based tests for cross-schema validation and data consistency"""
    
    @given(
        max_capacity=valid_decimal_strategy(min_value=1, max_value=1000, places=2),
        current_capacity_factor=st.floats(min_value=0, max_value=2, allow_nan=False, allow_infinity=False)
    )
    def test_capacity_constraint_validation_property(self, max_capacity, current_capacity_factor):
        """
        **Validates: Requirements 3.5**
        Property: For any capacity values where current exceeds maximum, 
        FleetUnitCreate SHALL reject with ValidationError
        """
        current_capacity = max_capacity * Decimal(str(current_capacity_factor))
        
        if current_capacity > max_capacity:
            # Should fail validation
            with pytest.raises(ValidationError):
                FleetUnitCreate(
                    identifier="TEST-001",
                    type=FleetUnitType.COLLECTION,
                    maximum_capacity=max_capacity,
                    current_capacity=current_capacity,
                    capacity_unit=CapacityUnit.TONS
                )
        else:
            # Should pass validation
            fleet_unit = FleetUnitCreate(
                identifier="TEST-001",
                type=FleetUnitType.COLLECTION,
                maximum_capacity=max_capacity,
                current_capacity=current_capacity,
                capacity_unit=CapacityUnit.TONS
            )
            assert fleet_unit.current_capacity <= fleet_unit.maximum_capacity

    @given(
        start_date=st.dates(min_value=date(2020, 1, 1), max_value=date(2025, 12, 31)),
        date_offset=st.integers(min_value=-365, max_value=365)
    )
    def test_date_range_constraint_validation_property(self, start_date, date_offset):
        """
        **Validates: Requirements 3.5**
        Property: For any date range where end_date <= start_date,
        WasteForecastBase SHALL reject with ValidationError
        """
        end_date = start_date + timedelta(days=date_offset)
        
        if end_date <= start_date:
            # Should fail validation
            with pytest.raises(ValidationError):
                WasteForecastBase(
                    region="test_region",
                    start_date=start_date,
                    end_date=end_date
                )
        else:
            # Should pass validation
            forecast = WasteForecastBase(
                region="test_region",
                start_date=start_date,
                end_date=end_date
            )
            assert forecast.end_date > forecast.start_date

    @given(
        lower_bound=valid_decimal_strategy(min_value=0, max_value=1000, places=2),
        upper_bound_offset=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False)
    )
    def test_bounds_constraint_validation_property(self, lower_bound, upper_bound_offset):
        """
        **Validates: Requirements 3.5**
        Property: For any bounds where upper_bound <= lower_bound,
        ForecastPoint SHALL reject with ValidationError
        """
        upper_bound = lower_bound + Decimal(str(upper_bound_offset))
        
        if upper_bound <= lower_bound:
            # Should fail validation
            with pytest.raises(ValidationError):
                ForecastPoint(
                    date=date.today(),
                    predicted_volume=Decimal('100'),
                    confidence=Decimal('95'),
                    lower_bound=lower_bound,
                    upper_bound=upper_bound
                )
        else:
            # Should pass validation
            forecast_point = ForecastPoint(
                date=date.today(),
                predicted_volume=Decimal('100'),
                confidence=Decimal('95'),
                lower_bound=lower_bound,
                upper_bound=upper_bound
            )
            assert forecast_point.upper_bound > forecast_point.lower_bound


# Configure Hypothesis settings for property-based tests
settings.register_profile("default", max_examples=100, deadline=5000)
settings.load_profile("default")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])