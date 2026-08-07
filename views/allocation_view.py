import streamlit as st

from core.database import SessionLocal
from services.allocation_service import AllocationService
from components.maps.hospital_map import HospitalMap


def show_allocation():

    st.title("🔍 Smart Medicine Allocator")

    st.write(
        "Search for a medicine and optionally provide your location to find the nearest hospital."
    )

    keyword = st.text_input(
        "💊 Medicine Name",
        placeholder="Example: Paracetamol"
    )

    st.subheader("📍 Your Location (Optional)")

    col1, col2 = st.columns(2)

    with col1:
        user_latitude = st.number_input(
            "Latitude",
            value=0.0,
            format="%.6f"
        )

    with col2:
        user_longitude = st.number_input(
            "Longitude",
            value=0.0,
            format="%.6f"
        )

    if not keyword.strip():
        return

    db = SessionLocal()

    try:

        if user_latitude == 0.0 and user_longitude == 0.0:

            results = AllocationService.search_medicine(
                db,
                keyword
            )

        else:

            results = AllocationService.search_medicine(
                db,
                keyword,
                user_latitude,
                user_longitude
            )

        if not results:

            st.warning(
                "No hospitals found with this medicine."
            )

            return

        # ----------------------------
        # Recommended Hospital
        # ----------------------------

        if hasattr(results[0], "distance"):

            nearest = results[0]

            st.success(
                f"⭐ Recommended Hospital: "
                f"{nearest.hospital.hospital_name} "
                f"({nearest.distance} km away)"
            )

        st.subheader(
            f"Results ({len(results)})"
        )

        # ----------------------------
        # Hospital Cards
        # ----------------------------

        for item in results:

            if item.quantity > 100:
                status = "🟢 High Stock"

            elif item.quantity > item.reorder_level:
                status = "🟡 Medium Stock"

            else:
                status = "🔴 Low Stock"

            with st.container(border=True):

                col1, col2 = st.columns([4, 1])

                with col1:

                    text = f"""
### 🏥 {item.hospital.hospital_name}

💊 **Medicine:** {item.medicine.medicine_name}

📍 **City:** {item.hospital.city}

📦 **Available Stock:** {item.quantity}

🚦 **Status:** {status}
"""

                    if hasattr(item, "distance"):

                        text += f"\n📏 **Distance:** {item.distance} km"

                    st.markdown(text)

                with col2:

                    st.metric(
                        "Stock",
                        item.quantity
                    )

        st.divider()

        st.subheader("🗺️ Hospital Locations")

        HospitalMap.render(results)

    finally:

        db.close()