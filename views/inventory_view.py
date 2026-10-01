import streamlit as st

from components.forms.inventory_form import InventoryForm
from core.database import SessionLocal
from core.session import SessionManager
from services.hospital_service import HospitalService
from services.inventory_service import InventoryService
from services.medicine_service import MedicineService
from translations.languages import t


def show_inventory():

    language = st.session_state.get(
        "language",
        "English"
    )

    # ==========================================
    # ADMIN ACCESS ONLY
    # ==========================================

    SessionManager.require_admin()

    # ==========================================
    # PAGE TITLE
    # ==========================================

    st.title(
        f"📦 {t('inventory_management', language)}"
    )

    db = SessionLocal()

    try:

        # ==========================================
        # GET HOSPITALS & MEDICINES
        # ==========================================

        hospitals = HospitalService.get_all_hospitals(db)
        medicines = MedicineService.get_all_medicines(db)

        if not hospitals:

            st.warning(
                t("add_hospital_first", language)
            )

            return

        if not medicines:

            st.warning(
                t("add_medicine_first", language)
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

        st.subheader(
            f"📋 {t('inventory_list', language)}"
        )

        inventory_items = InventoryService.get_all_inventory(
            db
        )

        if not inventory_items:

            st.info(
                t("no_inventory", language)
            )

        else:

            table = []

            for item in inventory_items:

                # ==================================
                # STOCK STATUS
                # ==================================

                if item.quantity <= item.reorder_level:

                    status = (
                        f"🔴 "
                        f"{t('low_stock', language)}"
                    )

                else:

                    status = (
                        f"🟢 "
                        f"{t('in_stock', language)}"
                    )

                # ==================================
                # TABLE ROW
                # ==================================

                table.append({

                    t("hospital", language):
                        (
                            item.hospital.hospital_name
                            if item.hospital
                            else t(
                                "unknown",
                                language
                            )
                        ),

                    t("medicine", language):
                        (
                            item.medicine.medicine_name
                            if item.medicine
                            else t(
                                "unknown",
                                language
                            )
                        ),

                    t("quantity", language):
                        item.quantity,

                    t("reorder_level", language):
                        item.reorder_level,

                    t("status", language):
                        status
                })

            # ==========================================
            # DISPLAY TABLE
            # ==========================================

            st.dataframe(
                table,
                use_container_width=True,
                hide_index=True
            )

    finally:

        db.close()