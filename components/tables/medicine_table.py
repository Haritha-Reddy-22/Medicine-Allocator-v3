import streamlit as st

from components.forms.medicine_edit_form import MedicineEditForm
from services.medicine_service import MedicineService


class MedicineTable:

    @staticmethod
    def render(db, medicines):

        if not medicines:
            st.info("No medicines found.")
            return

        # Initialize session state
        if "edit_medicine" not in st.session_state:
            st.session_state.edit_medicine = None

        for medicine in medicines:

            with st.container(border=True):

                col1, col2, col3 = st.columns([6, 2, 2])

                with col1:

                    st.markdown(f"""
### 💊 {medicine.medicine_name}

🧪 Generic : {medicine.generic_name}

📂 Category : {medicine.category}

🏭 Manufacturer : {medicine.manufacturer}

💰 Price : ₹{medicine.unit_price:.2f}

📅 Expiry : {medicine.expiry_date}
""")

                with col2:

                    if st.button(
                        "✏️ Edit",
                        key=f"edit_med_{medicine.id}"
                    ):
                        st.session_state.edit_medicine = medicine.id
                        st.rerun()

                with col3:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_med_{medicine.id}"
                    ):

                        success, message = MedicineService.delete_medicine(
                            db,
                            medicine.id
                        )

                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

                # Show edit form
                if st.session_state.edit_medicine == medicine.id:

                    (
                        medicine_name,
                        generic_name,
                        category,
                        manufacturer,
                        unit_price,
                        description,
                        save
                    ) = MedicineEditForm.render(medicine)

                    if save:

                        success, message = MedicineService.update_medicine(
                            db=db,
                            medicine_id=medicine.id,
                            medicine_name=medicine_name,
                            generic_name=generic_name,
                            category=category,
                            manufacturer=manufacturer,
                            unit_price=unit_price,
                            description=description
                        )

                        if success:
                            st.success(message)
                            st.session_state.edit_medicine = None
                            st.rerun()
                        else:
                            st.error(message)