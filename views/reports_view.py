import pandas as pd
import streamlit as st

from core.database import SessionLocal
from core.session import SessionManager
from services.report_service import ReportService


def show_reports():

    # ==========================================
    # ADMIN ACCESS ONLY
    # ==========================================

    SessionManager.require_admin()

    # ==========================================
    # PAGE TITLE
    # ==========================================

    st.title("📊 Reports")

    st.write(
        "Download reports for hospitals, medicines, "
        "inventory and alerts."
    )

    db = SessionLocal()

    try:

        # ==========================================
        # HOSPITAL REPORT
        # ==========================================

        st.subheader("🏥 Hospital Report")

        hospitals = ReportService.get_hospital_report(db)

        hospital_data = []

        for hospital in hospitals:

            hospital_data.append({
                "Hospital": hospital.hospital_name,
                "City": hospital.city,
                "State": hospital.state,
                "Contact": hospital.contact_number,
                "Email": hospital.email
            })

        hospital_df = pd.DataFrame(hospital_data)

        st.download_button(
            label="📥 Download Hospital Report",
            data=hospital_df.to_csv(index=False),
            file_name="hospital_report.csv",
            mime="text/csv"
        )

        st.divider()

        # ==========================================
        # MEDICINE REPORT
        # ==========================================

        st.subheader("💊 Medicine Report")

        medicines = ReportService.get_medicine_report(db)

        medicine_data = []

        for medicine in medicines:

            medicine_data.append({
                "Medicine": medicine.medicine_name,
                "Generic": medicine.generic_name,
                "Category": medicine.category,
                "Manufacturer": medicine.manufacturer,
                "Expiry": medicine.expiry_date,
                "Price": medicine.unit_price
            })

        medicine_df = pd.DataFrame(medicine_data)

        st.download_button(
            label="📥 Download Medicine Report",
            data=medicine_df.to_csv(index=False),
            file_name="medicine_report.csv",
            mime="text/csv"
        )

        st.divider()

        # ==========================================
        # INVENTORY REPORT
        # ==========================================

        st.subheader("📦 Inventory Report")

        inventory = ReportService.get_inventory_report(db)

        inventory_data = []

        for item in inventory:

            inventory_data.append({
                "Hospital": (
                    item.hospital.hospital_name
                    if item.hospital
                    else "Unknown"
                ),
                "Medicine": (
                    item.medicine.medicine_name
                    if item.medicine
                    else "Unknown"
                ),
                "Quantity": item.quantity,
                "Reorder Level": item.reorder_level
            })

        inventory_df = pd.DataFrame(inventory_data)

        st.download_button(
            label="📥 Download Inventory Report",
            data=inventory_df.to_csv(index=False),
            file_name="inventory_report.csv",
            mime="text/csv"
        )

        st.divider()

        # ==========================================
        # LOW STOCK REPORT
        # ==========================================

        st.subheader("🚨 Low Stock Report")

        low_stock = ReportService.get_low_stock_report(db)

        low_stock_data = []

        for item in low_stock:

            low_stock_data.append({
                "Hospital": (
                    item.hospital.hospital_name
                    if item.hospital
                    else "Unknown"
                ),
                "Medicine": (
                    item.medicine.medicine_name
                    if item.medicine
                    else "Unknown"
                ),
                "Available": item.quantity,
                "Reorder Level": item.reorder_level
            })

        low_stock_df = pd.DataFrame(low_stock_data)

        st.download_button(
            label="📥 Download Low Stock Report",
            data=low_stock_df.to_csv(index=False),
            file_name="low_stock_report.csv",
            mime="text/csv"
        )

        st.divider()

        # ==========================================
        # EXPIRED MEDICINES REPORT
        # ==========================================

        st.subheader("⏳ Expired Medicines")

        expired = ReportService.get_expired_report(db)

        expired_data = []

        for item in expired:

            expired_data.append({
                "Hospital": (
                    item.hospital.hospital_name
                    if item.hospital
                    else "Unknown"
                ),
                "Medicine": (
                    item.medicine.medicine_name
                    if item.medicine
                    else "Unknown"
                ),
                "Expiry": item.medicine.expiry_date,
                "Quantity": item.quantity
            })

        expired_df = pd.DataFrame(expired_data)

        st.download_button(
            label="📥 Download Expired Medicines Report",
            data=expired_df.to_csv(index=False),
            file_name="expired_medicines_report.csv",
            mime="text/csv"
        )

    finally:

        db.close()