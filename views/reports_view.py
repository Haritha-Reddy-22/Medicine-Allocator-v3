import pandas as pd
import streamlit as st

from core.database import SessionLocal
from services.report_service import ReportService


def show_reports():

    st.title("📊 Reports")

    st.write(
        "Download reports for hospitals, medicines, inventory and alerts."
    )

    db = SessionLocal()

    try:

        # -----------------------------------
        # Hospital Report
        # -----------------------------------

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

        # -----------------------------------
        # Medicine Report
        # -----------------------------------

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

        # -----------------------------------
        # Inventory Report
        # -----------------------------------

        st.subheader("📦 Inventory Report")

        inventory = ReportService.get_inventory_report(db)

        inventory_data = []

        for item in inventory:

            inventory_data.append({

                "Hospital": item.hospital.hospital_name,
                "Medicine": item.medicine.medicine_name,
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

        # -----------------------------------
        # Low Stock Report
        # -----------------------------------

        st.subheader("🚨 Low Stock Report")

        low_stock = ReportService.get_low_stock_report(db)

        low_stock_data = []

        for item in low_stock:

            low_stock_data.append({

                "Hospital": item.hospital.hospital_name,
                "Medicine": item.medicine.medicine_name,
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

        # -----------------------------------
        # Expired Medicines Report
        # -----------------------------------

        st.subheader("⏳ Expired Medicines")

        expired = ReportService.get_expired_report(db)

        expired_data = []

        for item in expired:

            expired_data.append({

                "Hospital": item.hospital.hospital_name,
                "Medicine": item.medicine.medicine_name,
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