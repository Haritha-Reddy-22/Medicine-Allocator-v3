import streamlit as st
import pandas as pd

from core.database import SessionLocal

from services.hospital_service import HospitalService
from services.medicine_service import MedicineService
from services.inventory_service import InventoryService
from services.reservation_service import ReservationService


def show_dashboard():

    st.title("📊 Medicine Allocator Dashboard")

    db = SessionLocal()

    try:

        # --------------------------------------------------
        # FETCH DATA
        # --------------------------------------------------

        hospitals = HospitalService.get_all_hospitals(db)
        medicines = MedicineService.get_all_medicines(db)
        inventory_items = InventoryService.get_all_inventory(db)
        low_stock_items = InventoryService.get_low_stock_inventory(db)
        reservations = ReservationService.get_all_reservations(db)

        # --------------------------------------------------
        # CALCULATE SUMMARY
        # --------------------------------------------------

        total_hospitals = len(hospitals)
        total_medicines = len(medicines)
        total_inventory = sum(
            item.quantity
            for item in inventory_items
        )

        total_reservations = len(reservations)

        pending_reservations = sum(
            1
            for reservation in reservations
            if reservation.status == "Pending"
        )

        approved_reservations = sum(
            1
            for reservation in reservations
            if reservation.status == "Approved"
        )

        completed_reservations = sum(
            1
            for reservation in reservations
            if reservation.status == "Completed"
        )

        cancelled_reservations = sum(
            1
            for reservation in reservations
            if reservation.status == "Cancelled"
        )

        # --------------------------------------------------
        # SUMMARY CARDS
        # --------------------------------------------------

        st.subheader("📌 Overview")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric(
                "🏥 Hospitals",
                total_hospitals
            )

        with col2:
            st.metric(
                "💊 Medicines",
                total_medicines
            )

        with col3:
            st.metric(
                "📦 Total Stock",
                total_inventory
            )

        with col4:
            st.metric(
                "📌 Reservations",
                total_reservations
            )

        with col5:
            st.metric(
                "🔴 Low Stock",
                len(low_stock_items)
            )

        st.divider()

        # --------------------------------------------------
        # RESERVATION STATUS
        # --------------------------------------------------

        st.subheader("📌 Reservation Status")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "🟡 Pending",
                pending_reservations
            )

        with col2:
            st.metric(
                "🟢 Approved",
                approved_reservations
            )

        with col3:
            st.metric(
                "🏁 Completed",
                completed_reservations
            )

        with col4:
            st.metric(
                "🔴 Cancelled",
                cancelled_reservations
            )

        if reservations:

            status_data = pd.DataFrame({
                "Status": [
                    "Pending",
                    "Approved",
                    "Completed",
                    "Cancelled"
                ],
                "Count": [
                    pending_reservations,
                    approved_reservations,
                    completed_reservations,
                    cancelled_reservations
                ]
            })

            st.bar_chart(
                status_data.set_index("Status")
            )

        st.divider()

        # --------------------------------------------------
        # LOW STOCK
        # --------------------------------------------------

        st.subheader("⚠️ Low Stock Medicines")

        if not low_stock_items:

            st.success("No low-stock medicines currently.")

        else:

            low_stock_table = []

            for item in low_stock_items:

                hospital_name = (
                    item.hospital.hospital_name
                    if item.hospital
                    else "Unknown"
                )

                medicine_name = (
                    item.medicine.medicine_name
                    if item.medicine
                    else "Unknown"
                )

                low_stock_table.append({
                    "Hospital": hospital_name,
                    "Medicine": medicine_name,
                    "Current Stock": item.quantity,
                    "Reorder Level": item.reorder_level
                })

            st.dataframe(
                low_stock_table,
                use_container_width=True,
                hide_index=True
            )

        st.divider()

        # --------------------------------------------------
        # INVENTORY BY HOSPITAL
        # --------------------------------------------------

        st.subheader("🏥 Hospital-wise Inventory")

        if not inventory_items:

            st.info("No inventory data available.")

        else:

            hospital_inventory = {}

            for item in inventory_items:

                hospital_name = (
                    item.hospital.hospital_name
                    if item.hospital
                    else "Unknown"
                )

                if hospital_name not in hospital_inventory:
                    hospital_inventory[hospital_name] = 0

                hospital_inventory[hospital_name] += item.quantity

            inventory_data = pd.DataFrame(
                list(hospital_inventory.items()),
                columns=[
                    "Hospital",
                    "Total Stock"
                ]
            )

            st.bar_chart(
                inventory_data.set_index("Hospital")
            )

    finally:

        db.close()