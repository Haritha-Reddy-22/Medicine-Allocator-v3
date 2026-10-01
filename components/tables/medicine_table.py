
import streamlit as st

from components.forms.medicine_edit_form import MedicineEditForm
from core.session import SessionManager
from services.medicine_service import MedicineService
from translations.languages import t


class MedicineTable:

    @staticmethod
    def render(db, medicines):

        language = st.session_state.get(
            "language",
            "English"
        )

        is_admin = SessionManager.is_admin()

        if not medicines:
            st.info(
                t("no_medicines_found", language)
            )
            return

        for medicine in medicines:

            with st.container(border=True):

                # ==========================================
                # MEDICINE DETAILS
                # ==========================================

                col1, col2, col3 = st.columns(
                    [2, 2, 1]
                )

                with col1:
                    st.markdown(
                        f"### 💊 {medicine.medicine_name}"
                    )

                    st.write(
                        f"**{t('generic_name', language)}:** "
                        f"{medicine.generic_name}"
                    )

                    st.write(
                        f"**{t('category', language)}:** "
                        f"{medicine.category}"
                    )

                with col2:
                    st.write(
                        f"**{t('manufacturer', language)}:** "
                        f"{medicine.manufacturer}"
                    )

                    st.write(
                        f"**{t('unit_price', language)}:** "
                        f"₹{medicine.unit_price:.2f}"
                    )

                    prescription_status = (
                        "Yes"
                        if getattr(
                            medicine,
                            "prescription_required",
                            False
                        )
                        else "No"
                    )

                    st.write(
                        f"📄 **Prescription Required:** "
                        f"{prescription_status}"
                    )

                with col3:

                    if is_admin:

                        if st.button(
                            "✏️ Edit",
                            key=f"edit_medicine_{medicine.id}",
                            use_container_width=True
                        ):
                            st.session_state.edit_medicine = medicine.id
                            st.rerun()

                # ==========================================
                # EDIT MEDICINE
                # ==========================================

                if (
                    is_admin
                    and st.session_state.get(
                        "edit_medicine"
                    ) == medicine.id
                ):

                    st.divider()

                    (
                        medicine_name,
                        generic_name,
                        category,
                        manufacturer,
                        unit_price,
                        description,
                        prescription_required,
                        save
                    ) = MedicineEditForm.render(
                        medicine
                    )

                    if save:

                        success, message = (
                            MedicineService.update_medicine(
                                db=db,
                                medicine_id=medicine.id,
                                medicine_name=medicine_name,
                                generic_name=generic_name,
                                category=category,
                                manufacturer=manufacturer,
                                unit_price=unit_price,
                                description=description,
                                prescription_required=prescription_required
                            )
                        )

                        if success:

                            st.success(message)

                            st.session_state.edit_medicine = None

                            st.rerun()

                        else:

                            st.error(message)

                    if st.button(
                        "❌ Cancel",
                        key=f"cancel_edit_{medicine.id}",
                        use_container_width=True
                    ):

                        st.session_state.edit_medicine = None
                        st.rerun()

                # ==========================================
                # EXTRA DETAILS
                # ==========================================

                with st.expander(
                    "ℹ️ View Details"
                ):

                    st.write(
                        f"**Batch Number:** "
                        f"{medicine.batch_number}"
                    )

                    st.write(
                        f"**Expiry Date:** "
                        f"{medicine.expiry_date}"
                    )

                    st.write(
                        f"**Description:** "
                        f"{medicine.description or 'N/A'}"
                    )

                    prescription_status = (
                        "Yes"
                        if getattr(
                            medicine,
                            "prescription_required",
                            False
                        )
                        else "No"
                    )

                    st.write(
                        f"📄 **Prescription Required:** "
                        f"{prescription_status}"
                    )
