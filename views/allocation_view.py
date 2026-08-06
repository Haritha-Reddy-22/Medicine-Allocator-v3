import streamlit as st

from core.database import SessionLocal
from services.allocation_service import AllocationService


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

        st.divider()

        if not results:

            st.warning("No hospitals found with this medicine.")

            return

        st.subheader(f"Results ({len(results)})")

        for item in results:

            if item.quantity > 100:
                status = "🟢 High Stock"
            elif item.quantity > 30:
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

    finally:

        db.close()