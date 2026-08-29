import streamlit as st

from components.forms.inventory_form import InventoryForm
from core.database import SessionLocal
from core.session import SessionManager
from services.hospital_service import HospitalService
from services.inventory_service import InventoryService
from services.medicine_service import MedicineService


def show_inventory():

    # ==========================================
    # ADMIN ACCESS ONLY
    # ==========================================

    SessionManager.require_admin()

    # ==========================================
    # PAGE TITLE
    # ==========================================

    st.title("📦 Inventory Management")

    db = SessionLocal()

    try:

        hospitals = HospitalService.get_all_hospitals(db)
        medicines = MedicineService.get_all_medicines(db)

        if not hospitals:

            st.warning(
                "Please add at least one hospital first."
            )

            return

        if not medicines:

            st.warning(
                "Please add at least one medicine first."
            )

            return

        # ==========================================
        # INVENTORY FORM
        # ==========================================

        (
            hospital_id,
            medicine_id,
            quantity,
            reorder_level,
            submitted
        ) = InventoryForm.render(
            hospitals,
            medicines
        )

        # ==========================================
        # ADD INVENTORY
        # ==========================================

        if submitted:

            success, message = InventoryService.add_inventory(
                db=db,
                hospital_id=hospital_id,
                medicine_id=medicine_id,
                quantity=quantity,
                reorder_level=reorder_level
            )

            if success:

                st.success(message)
                st.rerun()

            else:

                st.error(message)

        # ==========================================
        # INVENTORY LIST
        # ==========================================

        st.divider()

        st.subheader("📋 Inventory List")

        inventory_items = InventoryService.get_all_inventory(
            db
        )

        if not inventory_items:

            st.info("No inventory available.")

        else:

            table = []

            for item in inventory_items:

                status = (
                    "🔴 Low Stock"
                    if item.quantity <= item.reorder_level
                    else "🟢 In Stock"
                )

                table.append({
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
                    "Reorder Level": item.reorder_level,
                    "Status": status
                })

            st.dataframe(
                table,
                use_container_width=True,
                hide_index=True
            )

    finally:

        db.close()