import streamlit as st

from core.database import SessionLocal
from services.dashboard_service import DashboardService


def show_dashboard():

    st.title("📊 Dashboard")

    db = SessionLocal()

    try:

        stats = DashboardService.get_statistics(db)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "🏥 Hospitals",
                stats["hospitals"]
            )

        with col2:
            st.metric(
                "💊 Medicines",
                stats["medicines"]
            )

        with col3:
            st.metric(
                "📦 Inventory",
                stats["inventory"]
            )

        with col4:
            st.metric(
                "🚨 Low Stock",
                stats["low_stock"]
            )

        st.divider()

        st.subheader("🚨 Low Stock Medicines")

        low_stock = DashboardService.get_low_stock(db)

        if not low_stock:

            st.success("🎉 No medicines are currently low in stock.")

        else:

            table = []

            for item in low_stock:

                table.append({

                    "Hospital": item.hospital.hospital_name,
                    "Medicine": item.medicine.medicine_name,
                    "Available": item.quantity,
                    "Reorder Level": item.reorder_level

                })

            st.dataframe(
                table,
                use_container_width=True,
                hide_index=True
            )

    finally:

        db.close()