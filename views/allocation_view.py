import streamlit as st

from core.database import SessionLocal
from services.allocation_service import AllocationService
from components.maps.hospital_map import HospitalMap


def show_allocation():

    st.title("🔍 Smart Medicine Allocator")

    st.write(
        "Search for a medicine to find hospitals where it is available."
    )

    keyword = st.text_input(
        "💊 Medicine Name",
        placeholder="Example: Paracetamol"
    )

    if not keyword.strip():
        return

    db = SessionLocal()

    try:

        results = AllocationService.search_medicine(
            db,
            keyword
        )

        if not results:

            st.warning(
                "No hospitals found with this medicine."
            )

            return

        st.subheader(
            f"Results ({len(results)})"
        )

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

                    st.markdown(f"""
### 🏥 {item.hospital.hospital_name}

💊 **Medicine:** {item.medicine.medicine_name}

📍 **City:** {item.hospital.city}

📦 **Available Stock:** {item.quantity}

🚦 **Status:** {status}
""")

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