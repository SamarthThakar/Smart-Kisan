"""Seed Government Schemes Database with real Indian agricultural schemes"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from datetime import date
from app.database import SessionLocal, engine, Base
from app.models import GovernmentScheme

# Create tables if not exist
Base.metadata.create_all(bind=engine)

SCHEMES = [
    {
        "scheme_name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "short_name": "PM-KISAN",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "scheme_type": "subsidy",
        "description": "Direct income support of ₹6,000 per year to all eligible land-holding farmer families. Amount is transferred in three equal installments of ₹2,000 every four months directly to farmers' bank accounts.",
        "benefits": [
            "₹6,000 per year direct bank transfer",
            "No intermediaries — money goes directly to farmer",
            "Three installments of ₹2,000 each",
            "Covers all land-holding farmer families"
        ],
        "eligibility_criteria": {
            "land_holding": "Must be a land-holding farmer",
            "exclusions": "Income tax payers, government employees, constitutional post holders, and professionals earning above ₹10,000/month are excluded"
        },
        "applicable_states": ["ALL"],
        "applicable_crops": ["ALL"],
        "farmer_categories": ["all"],
        "max_land_acres": None,
        "required_documents": ["Aadhaar card", "Bank account (linked to Aadhaar)", "Land records/Khatauni", "Mobile number"],
        "application_mode": "both",
        "official_url": "https://pmkisan.gov.in",
        "is_active": True,
        "last_verified": date(2024, 1, 1)
    },
    {
        "scheme_name": "Pradhan Mantri Fasal Bima Yojana",
        "short_name": "PMFBY",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "scheme_type": "insurance",
        "description": "Comprehensive crop insurance scheme providing financial support to farmers suffering crop loss or damage due to unforeseen events like natural calamities, pests and diseases.",
        "benefits": [
            "Insurance for crop loss due to drought, flood, hailstorm, cyclone, fire",
            "Premium as low as 2% for Kharif, 1.5% for Rabi, 5% for commercial/horticultural crops",
            "Full insurance amount paid for crop loss above 25% threshold",
            "Mobile app for crop loss intimation within 72 hours"
        ],
        "eligibility_criteria": {
            "farmers": "All farmers (loanee and non-loanee) growing notified crops",
            "enrollment": "Enroll before cut-off date for each crop season"
        },
        "applicable_states": ["ALL"],
        "applicable_crops": ["rice", "wheat", "maize", "cotton", "sugarcane", "groundnut", "soybean", "onion", "potato"],
        "farmer_categories": ["all"],
        "max_land_acres": None,
        "required_documents": ["Aadhaar card", "Bank passbook", "Land records", "Sowing certificate"],
        "application_mode": "both",
        "official_url": "https://pmfby.gov.in",
        "is_active": True,
        "last_verified": date(2024, 1, 1)
    },
    {
        "scheme_name": "Kisan Credit Card Scheme",
        "short_name": "KCC",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "scheme_type": "credit",
        "description": "Provides farmers with affordable credit for agricultural purposes including crop cultivation, purchase of inputs, consumption requirements, and maintenance of farm assets.",
        "benefits": [
            "Credit limit up to ₹3 lakh at concessional interest rate of 7% per annum",
            "Additional 3% interest subvention for timely repayment (effective 4%)",
            "No collateral required for loans up to ₹1.6 lakh",
            "Covers crop cultivation, equipment purchase, and consumption needs",
            "Valid for 5 years with annual review"
        ],
        "eligibility_criteria": {
            "farmers": "All farmers — individual, joint, tenant farmers, oral lessees, share croppers, SHGs of farmers",
            "minimum_age": "18 years"
        },
        "applicable_states": ["ALL"],
        "applicable_crops": ["ALL"],
        "farmer_categories": ["all"],
        "max_land_acres": None,
        "required_documents": ["Identity proof (Aadhaar/PAN)", "Land records", "Address proof", "Passport photograph"],
        "application_mode": "offline",
        "official_url": "https://www.nabard.org/content1.aspx?id=593&catid=8&mid=530",
        "is_active": True,
        "last_verified": date(2024, 1, 1)
    },
    {
        "scheme_name": "Soil Health Card Scheme",
        "short_name": "SHC",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "scheme_type": "subsidy",
        "description": "Free soil health cards issued to farmers that carry crop-wise recommendations of nutrients and fertilizers required for each farm to improve productivity.",
        "benefits": [
            "Free soil testing at government labs",
            "Crop-wise fertilizer recommendations",
            "Advice on micronutrient deficiencies",
            "Helps reduce input costs by avoiding over-fertilization",
            "Valid for 3 years"
        ],
        "eligibility_criteria": {"farmers": "All farmers across India"},
        "applicable_states": ["ALL"],
        "applicable_crops": ["ALL"],
        "farmer_categories": ["all"],
        "max_land_acres": None,
        "required_documents": ["Aadhaar card", "Land records", "Mobile number"],
        "application_mode": "offline",
        "official_url": "https://soilhealth.dac.gov.in",
        "is_active": True,
        "last_verified": date(2024, 1, 1)
    },
    {
        "scheme_name": "PM Krishi Sinchayee Yojana",
        "short_name": "PMKSY",
        "ministry": "Ministry of Jal Shakti",
        "scheme_type": "irrigation",
        "description": "Achieving convergence of investments in irrigation, ensure complete field level water distribution infrastructure, improve water use efficiency, and sustainable water conservation.",
        "benefits": [
            "Micro-irrigation (drip and sprinkler) subsidized up to 55% for small/marginal farmers",
            "Water source creation support",
            "Distribution network support",
            "Promotes 'More Crop Per Drop'"
        ],
        "eligibility_criteria": {
            "farmers": "All farmers, priority to small and marginal farmers",
            "land": "Farmers with at least 0.5 acres of land"
        },
        "applicable_states": ["ALL"],
        "applicable_crops": ["ALL"],
        "farmer_categories": ["small", "marginal", "medium"],
        "max_land_acres": None,
        "required_documents": ["Aadhaar card", "Land records", "Bank account", "Farm plan"],
        "application_mode": "both",
        "official_url": "https://pmksy.gov.in",
        "is_active": True,
        "last_verified": date(2024, 1, 1)
    },
    {
        "scheme_name": "Paramparagat Krishi Vikas Yojana",
        "short_name": "PKVY",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "scheme_type": "organic",
        "description": "Promotes organic farming in a cluster-based approach. Provides financial assistance for organic inputs, certification, and marketing of organic produce.",
        "benefits": [
            "₹50,000 per hectare over 3 years for organic conversion",
            "Free organic certification (₹10,000 per hectare)",
            "Support for organic input production",
            "Market linkage support",
            "Cluster-based approach (20 or more farmers per cluster)"
        ],
        "eligibility_criteria": {
            "farmers": "Farmers willing to adopt organic farming",
            "cluster": "Minimum 20 farmers forming a cluster of 50+ acres"
        },
        "applicable_states": ["ALL"],
        "applicable_crops": ["ALL"],
        "farmer_categories": ["small", "marginal"],
        "max_land_acres": None,
        "required_documents": ["Aadhaar card", "Land records", "Bank account", "Cluster formation certificate"],
        "application_mode": "offline",
        "official_url": "https://pgsindia-ncof.gov.in/PKVY/Index.aspx",
        "is_active": True,
        "last_verified": date(2024, 1, 1)
    },
    {
        "scheme_name": "National Mission for Sustainable Agriculture",
        "short_name": "NMSA",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "scheme_type": "subsidy",
        "description": "Enhances agricultural productivity especially in rainfed areas through integrated farming, water use efficiency, soil health management, and synergizing resource conservation.",
        "benefits": [
            "Subsidized soil and water conservation structures",
            "Micro-irrigation support",
            "Soil testing and amendment support",
            "Climate-resilient farming practices support"
        ],
        "eligibility_criteria": {"farmers": "All farmers, priority to rainfed areas"},
        "applicable_states": ["ALL"],
        "applicable_crops": ["ALL"],
        "farmer_categories": ["all"],
        "max_land_acres": None,
        "required_documents": ["Aadhaar card", "Land records"],
        "application_mode": "offline",
        "official_url": "https://nmsa.dac.gov.in",
        "is_active": True,
        "last_verified": date(2024, 1, 1)
    },
    {
        "scheme_name": "Agriculture Infrastructure Fund",
        "short_name": "AIF",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "scheme_type": "credit",
        "description": "Medium to long-term debt financing for post-harvest management infrastructure and community farming assets through interest subvention and financial support.",
        "benefits": [
            "Loans up to ₹2 crore at 3% interest subvention",
            "Up to 7 years loan repayment period",
            "For primary agricultural cooperative societies, FPOs, farmers, SHGs",
            "Credit guarantee support through CGTMSE for loans up to ₹2 crore"
        ],
        "eligibility_criteria": {
            "eligible_entities": "Farmers, FPOs, PACS, Marketing Cooperative Societies, SHGs, Startups"
        },
        "applicable_states": ["ALL"],
        "applicable_crops": ["ALL"],
        "farmer_categories": ["all"],
        "max_land_acres": None,
        "required_documents": ["Business plan", "Identity proof", "Land documents", "Bank account"],
        "application_mode": "online",
        "official_url": "https://agriinfra.dac.gov.in",
        "is_active": True,
        "last_verified": date(2024, 1, 1)
    },
    {
        "scheme_name": "PM Kisan Maandhan Yojana",
        "short_name": "PM-KMY",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "scheme_type": "subsidy",
        "description": "Pension scheme for small and marginal farmers providing minimum assured pension of ₹3,000 per month after 60 years of age.",
        "benefits": [
            "₹3,000 per month pension after age 60",
            "50% contribution by farmer, 50% by Government of India",
            "Family pension of 50% in case of death of farmer",
            "Exit flexibility before maturity"
        ],
        "eligibility_criteria": {
            "age": "18-40 years",
            "land": "Farmers with less than 2 hectares (5 acres) of land",
            "not_eligible": "Farmers covered under PM-KISAN (optional for them)"
        },
        "applicable_states": ["ALL"],
        "applicable_crops": ["ALL"],
        "farmer_categories": ["small", "marginal"],
        "max_land_acres": 4.94,
        "required_documents": ["Aadhaar card", "Bank account", "Land records"],
        "application_mode": "offline",
        "official_url": "https://pmkmy.gov.in",
        "is_active": True,
        "last_verified": date(2024, 1, 1)
    },
    {
        "scheme_name": "e-NAM (National Agriculture Market)",
        "short_name": "e-NAM",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "scheme_type": "market",
        "description": "Pan-India electronic trading portal to create a unified national market for agricultural commodities, enabling farmers to get better prices through online auction.",
        "benefits": [
            "Access to buyers across India through online platform",
            "Transparent auction process — no middlemen",
            "Better price discovery for farmers",
            "Quality assaying services available",
            "Payment directly to farmer's bank account"
        ],
        "eligibility_criteria": {"farmers": "Any farmer selling through registered APMC mandis"},
        "applicable_states": ["ALL"],
        "applicable_crops": ["ALL"],
        "farmer_categories": ["all"],
        "max_land_acres": None,
        "required_documents": ["Aadhaar card", "Bank account", "Mobile number", "Valid APMC trader license (optional)"],
        "application_mode": "online",
        "official_url": "https://enam.gov.in",
        "is_active": True,
        "last_verified": date(2024, 1, 1)
    },
]


def seed_schemes():
    """Add government schemes to database if not already present"""
    db = SessionLocal()
    try:
        existing_count = db.query(GovernmentScheme).count()
        if existing_count > 0:
            print(f"[OK] Schemes already seeded ({existing_count} schemes found)")
            return

        print(f"[INFO] Seeding {len(SCHEMES)} government schemes...")
        for scheme_data in SCHEMES:
            scheme = GovernmentScheme(**scheme_data)
            db.add(scheme)

        db.commit()
        print(f"[SUCCESS] Successfully seeded {len(SCHEMES)} government schemes!")
    except Exception as e:
        print(f"[ERROR] Error seeding schemes: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_schemes()
