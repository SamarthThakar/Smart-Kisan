"""SQLAlchemy ORM Models — Database table definitions"""
from sqlalchemy import Column, String, Boolean, DateTime, Float, Integer, Text, Date, SmallInteger, ForeignKey
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    phone = Column(String(15), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    preferred_language = Column(String(10), default="en")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    profile = relationship("FarmerProfile", back_populates="user", uselist=False)
    disease_predictions = relationship("DiseasePrediction", back_populates="user")
    crop_recommendations = relationship("CropRecommendation", back_populates="user")
    chat_history = relationship("ChatHistory", back_populates="user")
    notifications = relationship("Notification", back_populates="user")


class FarmerProfile(Base):
    __tablename__ = "farmer_profiles"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    state = Column(String(50), nullable=True)
    district = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    land_size_acres = Column(Float, nullable=True)
    primary_crops = Column(JSON, default=list)  # ["rice", "wheat"]
    farmer_category = Column(String(20), nullable=True)  # small/marginal/medium
    soil_type = Column(String(50), nullable=True)

    user = relationship("User", back_populates="profile")


class DiseasePrediction(Base):
    __tablename__ = "disease_predictions"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    image_path = Column(String(500), nullable=True)
    disease_name = Column(String(150), nullable=False)
    confidence = Column(Float, nullable=False)
    top3_results = Column(JSON, default=list)
    treatment_shown = Column(JSON, default=list)
    crop_type = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_rating = Column(SmallInteger, nullable=True)  # 1-5 accuracy rating

    user = relationship("User", back_populates="disease_predictions")


class CropRecommendation(Base):
    __tablename__ = "crop_recommendations"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    input_params = Column(JSON, nullable=False)   # {N, P, K, pH, temp, humid, rain}
    recommended_crops = Column(JSON, nullable=False)  # ranked crop list
    location = Column(String(200), nullable=True)
    season = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="crop_recommendations")


class WeatherCache(Base):
    __tablename__ = "weather_cache"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    lat_lon_key = Column(String(30), unique=True, index=True)  # "18.96_72.83"
    weather_data = Column(JSON, nullable=False)
    farming_advice = Column(JSON, default=list)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class MarketPrice(Base):
    __tablename__ = "market_prices"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    state = Column(String(50), nullable=True)
    district = Column(String(100), nullable=True)
    market_name = Column(String(200), nullable=True)
    commodity = Column(String(100), nullable=False, index=True)
    variety = Column(String(100), nullable=True)
    min_price = Column(Float, nullable=True)
    max_price = Column(Float, nullable=True)
    modal_price = Column(Float, nullable=True)
    price_date = Column(Date, nullable=False)
    source = Column(String(50), default="mock")  # api/mock
    created_at = Column(DateTime, default=datetime.utcnow)


class GovernmentScheme(Base):
    __tablename__ = "government_schemes"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    scheme_name = Column(String(300), nullable=False)
    short_name = Column(String(100), nullable=True)
    ministry = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    benefits = Column(JSON, default=list)
    eligibility_criteria = Column(JSON, default=dict)
    applicable_states = Column(JSON, default=list)  # ["ALL"] or ["MH", "UP"]
    applicable_crops = Column(JSON, default=list)
    farmer_categories = Column(JSON, default=list)  # ["small", "marginal", "all"]
    max_land_acres = Column(Float, nullable=True)
    required_documents = Column(JSON, default=list)
    application_mode = Column(String(50), nullable=True)  # online/offline/both
    official_url = Column(String(500), nullable=True)
    scheme_type = Column(String(50), nullable=True)  # insurance/subsidy/credit/training
    is_active = Column(Boolean, default=True)
    last_verified = Column(Date, nullable=True)


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(String(36), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # user/assistant
    content = Column(Text, nullable=False)
    language = Column(String(10), default="en")
    sources_used = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_history")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    type = Column(String(50), nullable=True)  # weather/market/tip
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")


class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    feature = Column(String(50), nullable=True)  # disease/crop/chat
    prediction_id = Column(String(36), nullable=True)
    rating = Column(SmallInteger, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
