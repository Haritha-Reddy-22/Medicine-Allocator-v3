import streamlit as st

from core.session import SessionManager
from services.hospital_service import HospitalService
from services.medicine_service import MedicineService
from services.inventory_service import InventoryService
from services.reservation_service import ReservationService
from core.database import SessionLocal
from translations.languages import t


# ==========================================================
# DASHBOARD-SPECIFIC TRANSLATIONS
# ==========================================================

DASHBOARD_TRANSLATIONS = {

    "English": {
        "recent_reservations": "Recent Reservations",
        "no_reservations": "No reservations available.",
        "admin": "Admin",
        "admin_dashboard_message":
            "You have administrator access to manage hospitals, medicines, inventory, reservations and reports.",
    },

    "Telugu": {
        "recent_reservations": "ఇటీవలి రిజర్వేషన్లు",
        "no_reservations": "రిజర్వేషన్లు అందుబాటులో లేవు.",
        "admin": "అడ్మిన్",
        "admin_dashboard_message":
            "హాస్పిటల్స్, మందులు, నిల్వ, రిజర్వేషన్లు మరియు రిపోర్టులను నిర్వహించడానికి మీకు అడ్మిన్ యాక్సెస్ ఉంది.",
    },

    "Hindi": {
        "recent_reservations": "हाल के आरक्षण",
        "no_reservations": "कोई आरक्षण उपलब्ध नहीं है।",
        "admin": "एडमिन",
        "admin_dashboard_message":
            "आपके पास अस्पताल, दवाएँ, इन्वेंटरी, आरक्षण और रिपोर्ट प्रबंधित करने के लिए एडमिन एक्सेस है।",
    },

    "Tamil": {
        "recent_reservations": "சமீபத்திய முன்பதிவுகள்",
        "no_reservations": "முன்பதிவுகள் எதுவும் கிடைக்கவில்லை.",
        "admin": "நிர்வாகி",
        "admin_dashboard_message":
            "மருத்துவமனைகள், மருந்துகள், சரக்கு, முன்பதிவுகள் மற்றும் அறிக்கைகளை நிர்வகிக்க உங்களுக்கு நிர்வாகி அணுகல் உள்ளது.",
    },

    "Kannada": {
        "recent_reservations": "ಇತ್ತೀಚಿನ ಮೀಸಲಾತಿಗಳು",
        "no_reservations": "ಯಾವುದೇ ಮೀಸಲಾತಿಗಳು ಲಭ್ಯವಿಲ್ಲ.",
        "admin": "ನಿರ್ವಾಹಕರು",
        "admin_dashboard_message":
            "ಆಸ್ಪತ್ರೆಗಳು, ಔಷಧಿಗಳು, ದಾಸ್ತಾನು, ಮೀಸಲಾತಿಗಳು ಮತ್ತು ವರದಿಗಳನ್ನು ನಿರ್ವಹಿಸಲು ನಿಮಗೆ ನಿರ್ವಾಹಕ ಪ್ರವೇಶವಿದೆ.",
    },
}


def dashboard_text(key, language):

    return DASHBOARD_TRANSLATIONS.get(
        language,
        DASHBOARD_TRANSLATIONS["English"]
    ).get(
        key,
        DASHBOARD_TRANSLATIONS["English"].get(key, key)
    )


def show_dashboard():

    language = st.session_state.get(
        "language",
        "English"
    )

    SessionManager.require_user()

    user_name = SessionManager.get_user_name()
    is_admin = SessionManager.is_admin()

    # ==========================================================
    # PAGE TITLE
    # ==========================================================

    st.title(
        f"🏠 {t('dashboard', language)}"
    )

    st.write(
        f"{t('welcome', language)}, "
        f"**{user_name}** 👋"
    )

    db = SessionLocal()

    try:

        # ======================================================
        # GET DATA
        # ======================================================

        hospitals = HospitalService.get_all_hospitals(db)

        medicines = MedicineService.get_all_medicines(db)

        inventory = InventoryService.get_all_inventory(db)

        if is_admin:

            reservations = (
                ReservationService.get_all_reservations(
                    db,
                    is_admin=True
                )
            )

        else:

            user_id = SessionManager.get_user_id()

            reservations = (
                ReservationService.get_user_reservations(
                    db,
                    user_id
                )
            )

        # ======================================================
        # STATISTICS
        # ======================================================

        col1, col2, col3, col4 = st.columns(4)

        # ------------------------------------------------------
        # HOSPITALS
        # ------------------------------------------------------

        with col1:

            st.metric(
                f"🏥 {t('hospitals', language)}",
                len(hospitals)
            )

        # ------------------------------------------------------
        # MEDICINES
        # ------------------------------------------------------

        with col2:

            st.metric(
                f"💊 {t('medicines', language)}",
                len(medicines)
            )

        # ------------------------------------------------------
        # INVENTORY
        # ------------------------------------------------------

        with col3:

            st.metric(
                f"📦 {t('inventory', language)}",
                len(inventory)
            )

        # ------------------------------------------------------
        # RESERVATIONS
        # ------------------------------------------------------

        with col4:

            st.metric(
                f"📋 {t('reservations', language)}",
                len(reservations)
            )

        # ======================================================
        # RECENT RESERVATIONS
        # ======================================================

        st.divider()

        st.subheader(
            f"📋 {dashboard_text('recent_reservations', language)}"
        )

        if not reservations:

            st.info(
                dashboard_text(
                    "no_reservations",
                    language
                )
            )

        else:

            # Show latest 5 reservations
            recent = reservations[:5]

            for reservation in recent:

                # --------------------------------------------------
                # HOSPITAL NAME
                # --------------------------------------------------

                hospital_name = (
                    reservation.hospital.hospital_name
                    if reservation.hospital
                    else t("unknown", language)
                )

                # --------------------------------------------------
                # MEDICINE NAME
                # --------------------------------------------------

                medicine_name = (
                    reservation.medicine.medicine_name
                    if reservation.medicine
                    else t("unknown", language)
                )

                # --------------------------------------------------
                # RESERVATION CARD
                # --------------------------------------------------

                st.markdown(
                    f"""
### 🏥 {hospital_name}

💊 **{t('medicine', language)}:** {medicine_name}

🔢 **{t('quantity', language)}:** {reservation.quantity}

📌 **{t('status', language)}:** {reservation.status}

---
"""
                )

        # ======================================================
        # ADMIN INFORMATION
        # ======================================================

        if is_admin:

            st.divider()

            st.subheader(
                f"👑 {dashboard_text('admin', language)}"
            )

            st.info(
                dashboard_text(
                    "admin_dashboard_message",
                    language
                )
            )

    finally:

        db.close()