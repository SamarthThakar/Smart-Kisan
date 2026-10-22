"""Authentication Router — Register, Login, Profile"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import User, FarmerProfile
from app.schemas.auth import UserRegister, UserLogin, LoginResponse, UserResponse, FarmerProfileUpdate
from app.core.security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()


@router.post("/register", response_model=LoginResponse, status_code=201)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new farmer account"""
    # Check if phone already exists
    existing = db.query(User).filter(User.phone == user_data.phone).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone number already registered. Please login instead."
        )

    # Create user
    user = User(
        phone=user_data.phone,
        full_name=user_data.full_name,
        password_hash=hash_password(user_data.password),
        preferred_language=user_data.preferred_language,
    )
    db.add(user)
    db.flush()  # Get the ID without committing

    # Create empty farmer profile
    profile = FarmerProfile(user_id=user.id)
    db.add(profile)
    db.commit()
    db.refresh(user)

    # Generate JWT
    token = create_access_token({"sub": user.id})
    return LoginResponse(
        access_token=token,
        user=UserResponse.model_validate(user)
    )


@router.post("/login", response_model=LoginResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login with phone and password"""
    user = db.query(User).filter(User.phone == credentials.phone).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password"
        )

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    token = create_access_token({"sub": user.id})
    return LoginResponse(
        access_token=token,
        user=UserResponse.model_validate(user)
    )


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user profile"""
    profile = db.query(FarmerProfile).filter(FarmerProfile.user_id == current_user.id).first()
    return {
        "user": UserResponse.model_validate(current_user),
        "profile": {
            "state": profile.state if profile else None,
            "district": profile.district if profile else None,
            "latitude": profile.latitude if profile else None,
            "longitude": profile.longitude if profile else None,
            "land_size_acres": profile.land_size_acres if profile else None,
            "primary_crops": profile.primary_crops if profile else [],
            "farmer_category": profile.farmer_category if profile else None,
            "soil_type": profile.soil_type if profile else None,
        }
    }


@router.put("/profile")
async def update_profile(
    profile_data: FarmerProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update farmer profile"""
    profile = db.query(FarmerProfile).filter(FarmerProfile.user_id == current_user.id).first()
    if not profile:
        profile = FarmerProfile(user_id=current_user.id)
        db.add(profile)

    for field, value in profile_data.model_dump(exclude_none=True).items():
        setattr(profile, field, value)

    db.commit()
    return {"message": "Profile updated successfully"}
