import streamlit as st


class MedicineEditForm:

    @staticmethod
    def render(medicine):

        with st.form(f"edit_medicine_{medicine.id}"):

            st.subheader("✏️ Edit Medicine")

            medicine_name = st.text_input(
                "Medicine Name",
                value=medicine.medicine_name
            )

            generic_name = st.text_input(
                "Generic Name",
                value=medicine.generic_name
            )

            category = st.selectbox(
                "Category",
                [
                    "Tablet",
                    "Capsule",
                    "Syrup",
                    "Injection",
                    "Cream",
                    "Ointment",
                    "Drops",
                    "Inhaler",
                    "Other"
                ],
                index=[
                    "Tablet",
                    "Capsule",
                    "Syrup",
                    "Injection",
                    "Cream",
                    "Ointment",
                    "Drops",
                    "Inhaler",
                    "Other"
                ].index(medicine.category)
                if medicine.category in [
                    "Tablet",
                    "Capsule",
                    "Syrup",
                    "Injection",
                    "Cream",
                    "Ointment",
                    "Drops",
                    "Inhaler",
                    "Other"
                ] else 8
            )

            manufacturer = st.text_input(
                "Manufacturer",
                value=medicine.manufacturer
            )

            unit_price = st.number_input(
                "Unit Price",
                value=float(medicine.unit_price),
                min_value=0.0,
                step=1.0
            )

            description = st.text_area(
                "Description",
                value=medicine.description or ""
            )

            save = st.form_submit_button(
                "💾 Save Changes",
                use_container_width=True
            )

        return (
            medicine_name,
            generic_name,
            category,
            manufacturer,
            unit_price,
            description,
            save
        )