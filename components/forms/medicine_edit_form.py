
import streamlit as st

from translations.languages import t


class MedicineEditForm:

    @staticmethod
    def render(medicine):

        language = st.session_state.get(
            "language",
            "English"
        )

        categories = [
            "Tablet",
            "Capsule",
            "Syrup",
            "Injection",
            "Cream",
            "Ointment",
            "Drops",
            "Inhaler",
            "Other"
        ]

        translated_categories = [
            t("tablet", language),
            t("capsule", language),
            t("syrup", language),
            t("injection", language),
            t("cream", language),
            t("ointment", language),
            t("drops", language),
            t("inhaler", language),
            t("other", language)
        ]

        with st.form(
            f"edit_medicine_{medicine.id}"
        ):

            st.subheader(
                f"✏️ {t('edit_medicine', language)}"
            )

            medicine_name = st.text_input(
                t("medicine_name", language),
                value=medicine.medicine_name
            )

            generic_name = st.text_input(
                t("generic_name", language),
                value=medicine.generic_name
            )

            current_category_index = (
                categories.index(medicine.category)
                if medicine.category in categories
                else 8
            )

            category = st.selectbox(
                t("category", language),
                translated_categories,
                index=current_category_index
            )

            # Convert translated category back to
            # the original database value.
            category = categories[
                translated_categories.index(category)
            ]

            manufacturer = st.text_input(
                t("manufacturer", language),
                value=medicine.manufacturer
            )

            unit_price = st.number_input(
                t("unit_price", language),
                value=float(medicine.unit_price),
                min_value=0.0,
                step=1.0
            )

            description = st.text_area(
                t("description", language),
                value=medicine.description or ""
            )

            # ==========================================
            # PRESCRIPTION REQUIREMENT
            # ==========================================

            prescription_required = st.selectbox(
                "📄 Prescription Required?",
                ["No", "Yes"],
                index=(
                    1
                    if medicine.prescription_required
                    else 0
                )
            )

            prescription_required = (
                prescription_required == "Yes"
            )

            # ==========================================
            # SAVE
            # ==========================================

            save = st.form_submit_button(
                f"💾 {t('save_changes', language)}",
                use_container_width=True
            )

        return (
            medicine_name,
            generic_name,
            category,
            manufacturer,
            unit_price,
            description,
            prescription_required,
            save
        )

