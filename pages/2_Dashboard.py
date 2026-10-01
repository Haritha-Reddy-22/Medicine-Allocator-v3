import streamlit as st
import pandas as pd
import plotly.express as px

from core.session import SessionManager
from core.database import SessionLocal

from services.dashboard_service import DashboardService
from services.analytics_service import AnalyticsService
from services.reservation_service import ReservationService


# ==================================================
# LANGUAGE
# ==================================================

# language = st.session_state.get("language", "English")
language = st.session_state.get("language", "English")

# Convert displayed language names to translation dictionary keys
LANGUAGE_MAP = {
    "English": "English",
    "తెలుగు": "Telugu",
    "हिन्दी": "Hindi",
    "தமிழ்": "Tamil",
    "ಕನ್ನಡ": "Kannada",
}

language = LANGUAGE_MAP.get(language, "English")

DASHBOARD_TEXT = {

    "English": {
        "dashboard": "Dashboard",
        "welcome": "Welcome",
        "email": "Email",
        "role": "Role",
        "welcome_section": "Welcome!",
        "user_info": (
            "You can use the Medicine Availability and "
            "Reservations sections to find medicines and "
            "manage your reservations."
        ),
        "what_you_can_do": "What you can do",
        "find_medicines": "Find Medicines",
        "find_medicines_desc": (
            "Search for medicines and check their "
            "availability at hospitals."
        ),
        "reservations": "Reservations",
        "reservations_desc": (
            "Create and manage your medicine reservations."
        ),
        "logout": "Logout",
        "hospitals": "Hospitals",
        "medicines": "Medicines",
        "inventory": "Inventory",
        "low_stock": "Low Stock",
        "low_stock_medicines": "Low Stock Medicines",
        "hospital": "Hospital",
        "medicine": "Medicine",
        "available": "Available",
        "reorder_level": "Reorder Level",
        "no_low_stock": "🎉 No medicines are currently low in stock.",
        "reservation_overview": "Reservation Overview",
        "pending": "Pending",
        "approved": "Approved",
        "completed": "Completed",
        "cancelled": "Cancelled",
        "reservation_status": "Reservation Status",
        "number_reservations": "Number of Reservations",
        "analytics": "Analytics Dashboard",
        "inventory_distribution": "Inventory Distribution by Hospital",
        "inventory_label": "Inventory",
        "medicine_categories": "Medicine Categories",
        "stock_health": "Stock Health",
        "please_login": "Please login first.",
        "unknown": "Unknown",
    },

    "Telugu": {
        "dashboard": "డాష్‌బోర్డ్",
        "welcome": "స్వాగతం",
        "email": "ఇమెయిల్",
        "role": "పాత్ర",
        "welcome_section": "స్వాగతం!",
        "user_info": (
            "మందుల లభ్యత మరియు రిజర్వేషన్ల విభాగాలను ఉపయోగించి "
            "మందులను కనుగొని, మీ రిజర్వేషన్లను నిర్వహించవచ్చు."
        ),
        "what_you_can_do": "మీరు ఏమి చేయగలరు",
        "find_medicines": "మందులను కనుగొనండి",
        "find_medicines_desc": (
            "మందుల కోసం శోధించి, ఆసుపత్రుల్లో వాటి లభ్యతను చూడండి."
        ),
        "reservations": "రిజర్వేషన్లు",
        "reservations_desc": (
            "మీ మందుల రిజర్వేషన్లను సృష్టించి నిర్వహించండి."
        ),
        "logout": "లాగ్ అవుట్",
        "hospitals": "ఆసుపత్రులు",
        "medicines": "మందులు",
        "inventory": "నిల్వ",
        "low_stock": "తక్కువ నిల్వ",
        "low_stock_medicines": "తక్కువ నిల్వ ఉన్న మందులు",
        "hospital": "ఆసుపత్రి",
        "medicine": "మందు",
        "available": "అందుబాటులో",
        "reorder_level": "మళ్లీ ఆర్డర్ స్థాయి",
        "no_low_stock": "🎉 ప్రస్తుతం తక్కువ నిల్వలో ఉన్న మందులు లేవు.",
        "reservation_overview": "రిజర్వేషన్ల వివరాలు",
        "pending": "పెండింగ్",
        "approved": "ఆమోదించబడింది",
        "completed": "పూర్తయింది",
        "cancelled": "రద్దు చేయబడింది",
        "reservation_status": "రిజర్వేషన్ స్థితి",
        "number_reservations": "రిజర్వేషన్ల సంఖ్య",
        "analytics": "విశ్లేషణ డాష్‌బోర్డ్",
        "inventory_distribution": "ఆసుపత్రుల వారీగా మందుల నిల్వ",
        "inventory_label": "నిల్వ",
        "medicine_categories": "మందుల వర్గాలు",
        "stock_health": "నిల్వ స్థితి",
        "please_login": "దయచేసి ముందుగా లాగిన్ అవ్వండి.",
        "unknown": "తెలియదు",
    },

    "Hindi": {
        "dashboard": "डैशबोर्ड",
        "welcome": "स्वागत है",
        "email": "ईमेल",
        "role": "भूमिका",
        "welcome_section": "स्वागत है!",
        "user_info": (
            "दवाओं की उपलब्धता और आरक्षण अनुभागों का उपयोग करके "
            "दवाएं खोजें और अपने आरक्षण प्रबंधित करें।"
        ),
        "what_you_can_do": "आप क्या कर सकते हैं",
        "find_medicines": "दवाएं खोजें",
        "find_medicines_desc": (
            "दवाओं को खोजें और अस्पतालों में उनकी उपलब्धता देखें।"
        ),
        "reservations": "आरक्षण",
        "reservations_desc": (
            "अपने दवा आरक्षण बनाएं और प्रबंधित करें।"
        ),
        "logout": "लॉग आउट",
        "hospitals": "अस्पताल",
        "medicines": "दवाएं",
        "inventory": "इन्वेंटरी",
        "low_stock": "कम स्टॉक",
        "low_stock_medicines": "कम स्टॉक वाली दवाएं",
        "hospital": "अस्पताल",
        "medicine": "दवा",
        "available": "उपलब्ध",
        "reorder_level": "पुनः ऑर्डर स्तर",
        "no_low_stock": "🎉 वर्तमान में कम स्टॉक वाली कोई दवा नहीं है।",
        "reservation_overview": "आरक्षण विवरण",
        "pending": "लंबित",
        "approved": "स्वीकृत",
        "completed": "पूर्ण",
        "cancelled": "रद्द",
        "reservation_status": "आरक्षण स्थिति",
        "number_reservations": "आरक्षणों की संख्या",
        "analytics": "विश्लेषण डैशबोर्ड",
        "inventory_distribution": "अस्पताल के अनुसार इन्वेंटरी वितरण",
        "inventory_label": "इन्वेंटरी",
        "medicine_categories": "दवा श्रेणियां",
        "stock_health": "स्टॉक स्थिति",
        "please_login": "कृपया पहले लॉगिन करें।",
        "unknown": "अज्ञात",
    },

    "Tamil": {
        "dashboard": "டாஷ்போர்டு",
        "welcome": "வரவேற்கிறோம்",
        "email": "மின்னஞ்சல்",
        "role": "பங்கு",
        "welcome_section": "வரவேற்கிறோம்!",
        "user_info": (
            "மருந்துகளின் கிடைக்கும் நிலை மற்றும் முன்பதிவு பகுதிகளைப் "
            "பயன்படுத்தி மருந்துகளைத் தேடி உங்கள் முன்பதிவுகளை நிர்வகிக்கலாம்."
        ),
        "what_you_can_do": "நீங்கள் என்ன செய்யலாம்",
        "find_medicines": "மருந்துகளைத் தேடுங்கள்",
        "find_medicines_desc": (
            "மருந்துகளைத் தேடி மருத்துவமனைகளில் அவற்றின் கிடைக்கும் நிலையைப் பார்க்கவும்."
        ),
        "reservations": "முன்பதிவுகள்",
        "reservations_desc": (
            "உங்கள் மருந்து முன்பதிவுகளை உருவாக்கி நிர்வகிக்கவும்."
        ),
        "logout": "வெளியேறு",
        "hospitals": "மருத்துவமனைகள்",
        "medicines": "மருந்துகள்",
        "inventory": "சரக்கு",
        "low_stock": "குறைந்த சரக்கு",
        "low_stock_medicines": "குறைந்த சரக்கில் உள்ள மருந்துகள்",
        "hospital": "மருத்துவமனை",
        "medicine": "மருந்து",
        "available": "கிடைக்கும்",
        "reorder_level": "மறுஆர்டர் நிலை",
        "no_low_stock": "🎉 தற்போது குறைந்த சரக்கில் மருந்துகள் எதுவும் இல்லை.",
        "reservation_overview": "முன்பதிவு விவரங்கள்",
        "pending": "நிலுவையில்",
        "approved": "அங்கீகரிக்கப்பட்டது",
        "completed": "முடிந்தது",
        "cancelled": "ரத்து செய்யப்பட்டது",
        "reservation_status": "முன்பதிவு நிலை",
        "number_reservations": "முன்பதிவுகளின் எண்ணிக்கை",
        "analytics": "பகுப்பாய்வு டாஷ்போர்டு",
        "inventory_distribution": "மருத்துவமனை வாரியாக சரக்கு விநியோகம்",
        "inventory_label": "சரக்கு",
        "medicine_categories": "மருந்து வகைகள்",
        "stock_health": "சரக்கு நிலை",
        "please_login": "முதலில் உள்நுழையவும்.",
        "unknown": "தெரியவில்லை",
    },

    "Kannada": {
        "dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "welcome": "ಸ್ವಾಗತ",
        "email": "ಇಮೇಲ್",
        "role": "ಪಾತ್ರ",
        "welcome_section": "ಸ್ವಾಗತ!",
        "user_info": (
            "ಔಷಧ ಲಭ್ಯತೆ ಮತ್ತು ಮೀಸಲಾತಿ ವಿಭಾಗಗಳನ್ನು ಬಳಸಿಕೊಂಡು "
            "ಔಷಧಿಗಳನ್ನು ಹುಡುಕಿ ಮತ್ತು ನಿಮ್ಮ ಮೀಸಲಾತಿಗಳನ್ನು ನಿರ್ವಹಿಸಿ."
        ),
        "what_you_can_do": "ನೀವು ಏನು ಮಾಡಬಹುದು",
        "find_medicines": "ಔಷಧಿಗಳನ್ನು ಹುಡುಕಿ",
        "find_medicines_desc": (
            "ಔಷಧಿಗಳನ್ನು ಹುಡುಕಿ ಮತ್ತು ಆಸ್ಪತ್ರೆಗಳಲ್ಲಿ ಅವುಗಳ ಲಭ್ಯತೆಯನ್ನು ಪರಿಶೀಲಿಸಿ."
        ),
        "reservations": "ಮೀಸಲಾತಿಗಳು",
        "reservations_desc": (
            "ನಿಮ್ಮ ಔಷಧ ಮೀಸಲಾತಿಗಳನ್ನು ರಚಿಸಿ ಮತ್ತು ನಿರ್ವಹಿಸಿ."
        ),
        "logout": "ಲಾಗ್ ಔಟ್",
        "hospitals": "ಆಸ್ಪತ್ರೆಗಳು",
        "medicines": "ಔಷಧಿಗಳು",
        "inventory": "ದಾಸ್ತಾನು",
        "low_stock": "ಕಡಿಮೆ ದಾಸ್ತಾನು",
        "low_stock_medicines": "ಕಡಿಮೆ ದಾಸ್ತಾನು ಇರುವ ಔಷಧಿಗಳು",
        "hospital": "ಆಸ್ಪತ್ರೆ",
        "medicine": "ಔಷಧಿ",
        "available": "ಲಭ್ಯವಿದೆ",
        "reorder_level": "ಮರುಆರ್ಡರ್ ಮಟ್ಟ",
        "no_low_stock": "🎉 ಪ್ರಸ್ತುತ ಕಡಿಮೆ ದಾಸ್ತಾನು ಇರುವ ಔಷಧಿಗಳಿಲ್ಲ.",
        "reservation_overview": "ಮೀಸಲಾತಿ ವಿವರಗಳು",
        "pending": "ಬಾಕಿಯಿದೆ",
        "approved": "ಅನುಮೋದಿಸಲಾಗಿದೆ",
        "completed": "ಪೂರ್ಣಗೊಂಡಿದೆ",
        "cancelled": "ರದ್ದುಗೊಳಿಸಲಾಗಿದೆ",
        "reservation_status": "ಮೀಸಲಾತಿ ಸ್ಥಿತಿ",
        "number_reservations": "ಮೀಸಲಾತಿಗಳ ಸಂಖ್ಯೆ",
        "analytics": "ವಿಶ್ಲೇಷಣೆ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "inventory_distribution": "ಆಸ್ಪತ್ರೆಯ ಪ್ರಕಾರ ದಾಸ್ತಾನು ವಿತರಣೆ",
        "inventory_label": "ದಾಸ್ತಾನು",
        "medicine_categories": "ಔಷಧಿ ವರ್ಗಗಳು",
        "stock_health": "ದಾಸ್ತಾನು ಸ್ಥಿತಿ",
        "please_login": "ದಯವಿಟ್ಟು ಮೊದಲು ಲಾಗಿನ್ ಮಾಡಿ.",
        "unknown": "ತಿಳಿದಿಲ್ಲ",
    }
}


# ==================================================
# GET TRANSLATED TEXT
# ==================================================

text = DASHBOARD_TEXT.get(
    language,
    DASHBOARD_TEXT["English"]
)


# ==================================================
# AUTHENTICATION
# ==================================================

if not SessionManager.is_logged_in():

    st.error(text["please_login"])
    st.stop()


user = SessionManager.get_user()

role = user["role"]


# ==================================================
# USER DASHBOARD
# ==================================================

if role != "ADMIN":

    st.title(f"📊 {text['dashboard']}")

    st.success(
        f"{text['welcome']}, {user['name']} 👋"
    )

    st.write(
        f"**{text['email']}:** {user['email']}"
    )

    st.write(
        f"**{text['role']}:** {user['role']}"
    )

    st.divider()

    st.subheader(
        f"👤 {text['welcome_section']}"
    )

    st.info(
        text["user_info"]
    )

    st.divider()

    st.subheader(
        f"💊 {text['what_you_can_do']}"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            ### 🔎 {text['find_medicines']}

            {text['find_medicines_desc']}
            """
        )

    with col2:

        st.markdown(
            f"""
            ### 📌 {text['reservations']}

            {text['reservations_desc']}
            """
        )

    st.divider()

    if st.button(
        f"🚪 {text['logout']}",
        use_container_width=True
    ):

        SessionManager.logout()

        st.switch_page(
            "pages/0_Login.py"
        )

    st.stop()


# ==================================================
# ADMIN DASHBOARD
# ==================================================

db = SessionLocal()


try:

    # ==================================================
    # HEADER
    # ==================================================

    st.title(
        f"📊 {text['dashboard']}"
    )

    st.success(
        f"{text['welcome']}, {user['name']} 👋"
    )

    st.write(
        f"**{text['email']}:** {user['email']}"
    )

    st.write(
        f"**{text['role']}:** {user['role']}"
    )

    st.divider()


    # ==================================================
    # BASIC STATISTICS
    # ==================================================

    stats = DashboardService.get_statistics(db)

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            f"🏥 {text['hospitals']}",
            stats["hospitals"]
        )

    with col2:

        st.metric(
            f"💊 {text['medicines']}",
            stats["medicines"]
        )

    with col3:

        st.metric(
            f"📦 {text['inventory']}",
            stats["inventory"]
        )

    with col4:

        st.metric(
            f"🚨 {text['low_stock']}",
            stats["low_stock"]
        )


    st.divider()


    # ==================================================
    # LOW STOCK MEDICINES
    # ==================================================

    st.subheader(
        f"🚨 {text['low_stock_medicines']}"
    )

    low_stock = DashboardService.get_low_stock(db)

    if low_stock:

        table = []

        for item in low_stock:

            hospital_name = (
                item.hospital.hospital_name
                if item.hospital
                else text["unknown"]
            )

            medicine_name = (
                item.medicine.medicine_name
                if item.medicine
                else text["unknown"]
            )

            table.append({

                text["hospital"]:
                    hospital_name,

                text["medicine"]:
                    medicine_name,

                text["available"]:
                    item.quantity,

                text["reorder_level"]:
                    item.reorder_level

            })

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            text["no_low_stock"]
        )


    st.divider()


    # ==================================================
    # RESERVATION DATA
    # ==================================================

    st.subheader(
        f"📌 {text['reservation_overview']}"
    )

    reservations = (
        ReservationService.get_all_reservations(db)
    )

    pending = 0
    approved = 0
    completed = 0
    cancelled = 0

    for reservation in reservations:

        if reservation.status == "Pending":

            pending += 1

        elif reservation.status == "Approved":

            approved += 1

        elif reservation.status == "Completed":

            completed += 1

        elif reservation.status == "Cancelled":

            cancelled += 1


    # ==================================================
    # RESERVATION CARDS
    # ==================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            f"🟡 {text['pending']}",
            pending
        )

    with col2:

        st.metric(
            f"🟢 {text['approved']}",
            approved
        )

    with col3:

        st.metric(
            f"🏁 {text['completed']}",
            completed
        )

    with col4:

        st.metric(
            f"🔴 {text['cancelled']}",
            cancelled
        )


    # ==================================================
    # RESERVATION CHART
    # ==================================================

    reservation_data = pd.DataFrame({

        "Status": [
            text["pending"],
            text["approved"],
            text["completed"],
            text["cancelled"]
        ],

        "Count": [
            pending,
            approved,
            completed,
            cancelled
        ]

    })


    fig = px.bar(

        reservation_data,

        x="Status",

        y="Count",

        title=text["reservation_status"],

        labels={
            "Status": text["reservation_status"],
            "Count": text["number_reservations"]
        }

    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.divider()


    # ==================================================
    # ANALYTICS DASHBOARD
    # ==================================================

    st.subheader(
        f"📈 {text['analytics']}"
    )


    # ==================================================
    # INVENTORY BY HOSPITAL
    # ==================================================

    inventory_data = (
        AnalyticsService.inventory_by_hospital(db)
    )


    if inventory_data:

        hospitals = [
            row[0]
            for row in inventory_data
        ]

        quantities = [
            row[1]
            for row in inventory_data
        ]


        fig = px.bar(

            x=hospitals,

            y=quantities,

            labels={
                "x": text["hospital"],
                "y": text["inventory_label"]
            },

            title=text["inventory_distribution"]

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ==================================================
    # MEDICINE CATEGORIES
    # ==================================================

    category_data = (
        AnalyticsService
        .medicine_category_distribution(db)
    )


    if category_data:

        labels = [
            row[0]
            for row in category_data
        ]

        values = [
            row[1]
            for row in category_data
        ]


        fig = px.pie(

            names=labels,

            values=values,

            title=text["medicine_categories"]

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ==================================================
    # STOCK HEALTH
    # ==================================================

    stock = (
        AnalyticsService
        .stock_status_distribution(db)
    )


    if stock:

        fig = px.pie(

            names=list(
                stock.keys()
            ),

            values=list(
                stock.values()
            ),

            hole=0.5,

            title=text["stock_health"]

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.divider()


    # ==================================================
    # LOGOUT
    # ==================================================

    if st.button(
        f"🚪 {text['logout']}",
        use_container_width=True
    ):

        SessionManager.logout()

        st.rerun()


finally:

    db.close()