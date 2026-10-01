import streamlit as st

from core.database import SessionLocal
from core.session import SessionManager
from services.hospital_service import HospitalService
from services.medicine_service import MedicineService
from services.inventory_service import InventoryService
from services.reservation_service import ReservationService
from translations.languages import t


def show_reports():

    language = st.session_state.get(
        "language",
        "English"
    )

    SessionManager.require_admin()

    st.title(
        f"📊 {t('reports', language)}"
    )

    db = SessionLocal()

    try:

        # ==========================================
        # FETCH DATA
        # ==========================================

        hospitals = HospitalService.get_all_hospitals(db)
        medicines = MedicineService.get_all_medicines(db)
        inventory = InventoryService.get_all_inventory(db)

        reservations = (
            ReservationService.get_all_reservations(
                db,
                is_admin=True
            )
        )

        # ==========================================
        # OVERVIEW
        # ==========================================

        st.subheader(
            f"📈 {t('overview', language)}"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                f"🏥 {t('hospitals', language)}",
                len(hospitals)
            )

        with col2:
            st.metric(
                f"💊 {t('medicines', language)}",
                len(medicines)
            )

        with col3:
            st.metric(
                f"📦 {t('inventory', language)}",
                len(inventory)
            )

        with col4:
            st.metric(
                f"📋 {t('reservations', language)}",
                len(reservations)
            )

        st.divider()

        # ==========================================
        # INVENTORY REPORT
        # ==========================================

        st.subheader(
            f"📦 {t('inventory_report', language)}"
        )

        if not inventory:

            st.info(
                t("no_inventory", language)
            )

        else:

            inventory_data = []

            for item in inventory:

                hospital_name = (
                    item.hospital.hospital_name
                    if item.hospital
                    else t("unknown", language)
                )

                medicine_name = (
                    item.medicine.medicine_name
                    if item.medicine
                    else t("unknown", language)
                )

                if item.quantity <= item.reorder_level:

                    stock_status = (
                        f"🔴 {t('low_stock', language)}"
                    )

                else:

                    stock_status = (
                        f"🟢 {t('in_stock', language)}"
                    )

                inventory_data.append(
                    {
                        t("hospital", language):
                            hospital_name,

                        t("medicine", language):
                            medicine_name,

                        t("quantity", language):
                            item.quantity,

                        t("reorder_level", language):
                            item.reorder_level,

                        t("status", language):
                            stock_status
                    }
                )

            st.dataframe(
                inventory_data,
                use_container_width=True,
                hide_index=True
            )

        st.divider()

        # ==========================================
        # RESERVATION REPORT
        # ==========================================

        st.subheader(
            f"📋 {t('reservation_report', language)}"
        )

        if not reservations:

            st.info(
                t("no_reservations", language)
            )

        else:

            pending_count = sum(
                1
                for r in reservations
                if r.status == "Pending"
            )

            approved_count = sum(
                1
                for r in reservations
                if r.status == "Approved"
            )

            completed_count = sum(
                1
                for r in reservations
                if r.status == "Completed"
            )

            cancelled_count = sum(
                1
                for r in reservations
                if r.status == "Cancelled"
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    f"⏳ {t('pending', language)}",
                    pending_count
                )

            with col2:
                st.metric(
                    f"✅ {t('approved', language)}",
                    approved_count
                )

            with col3:
                st.metric(
                    f"🏁 {t('completed', language)}",
                    completed_count
                )

            with col4:
                st.metric(
                    f"❌ {t('cancelled', language)}",
                    cancelled_count
                )

            st.divider()

            reservation_data = []

            for reservation in reservations:

                hospital_name = (
                    reservation.hospital.hospital_name
                    if reservation.hospital
                    else t("unknown", language)
                )

                medicine_name = (
                    reservation.medicine.medicine_name
                    if reservation.medicine
                    else t("unknown", language)
                )

                reservation_data.append(
                    {
                        t("hospital", language):
                            hospital_name,

                        t("medicine", language):
                            medicine_name,

                        t("quantity", language):
                            reservation.quantity,

                        t("status", language):
                            reservation.status,

                        t("reserved_at", language):
                            reservation.reserved_at
                    }
                )

            st.dataframe(
                reservation_data,
                use_container_width=True,
                hide_index=True
            )

    finally:
        db.close()