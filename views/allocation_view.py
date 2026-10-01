import os
import uuid

import streamlit as st

from components.maps.hospital_map import HospitalMap
from core.database import SessionLocal
from core.session import SessionManager
from services.allocation_service import AllocationService
from services.reservation_service import ReservationService
from translations.languages import t


# ==========================================
# PRESCRIPTION UPLOAD DIRECTORY
# ==========================================

PRESCRIPTION_DIR = os.path.join(
    "data",
    "prescriptions"
)

os.makedirs(
    PRESCRIPTION_DIR,
    exist_ok=True
)


def save_prescription(uploaded_file):

    if uploaded_file is None:
        return None

    file_extension = os.path.splitext(
        uploaded_file.name
    )[1].lower()

    allowed_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".pdf"
    ]

    if file_extension not in allowed_extensions:
        return None

    unique_name = (
        f"{uuid.uuid4().hex}"
        f"{file_extension}"
    )

    file_path = os.path.join(
        PRESCRIPTION_DIR,
        unique_name
    )

    with open(
        file_path,
        "wb"
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )

    return file_path


def show_allocation():

    language = st.session_state.get(
        "language",
        "English"
    )

    # ==========================================
    # USER / ADMIN ACCESS
    # ==========================================

    SessionManager.require_user()

    current_user_id = (
        SessionManager.get_user_id()
    )

    # ==========================================
    # PAGE TITLE
    # ==========================================

    st.title(
        f"🔍 {t('medicine_allocator', language)}"
    )

    st.write(
        t(
            "allocator_description",
            language
        )
    )

    # ==========================================
    # MEDICINE SEARCH
    # ==========================================

    keyword = st.text_input(
        f"💊 {t('medicine_name', language)}",
        placeholder=t(
            "medicine_search_placeholder",
            language
        )
    )

    # ==========================================
    # LOCATION
    # ==========================================

    st.subheader(
        f"📍 {t('select_location', language)}"
    )

    col1, col2 = st.columns(2)

    with col1:

        user_latitude = st.number_input(
            t(
                "latitude",
                language
            ),
            value=0.0,
            format="%.6f"
        )

    with col2:

        user_longitude = st.number_input(
            t(
                "longitude",
                language
            ),
            value=0.0,
            format="%.6f"
        )

    if not keyword.strip():
        return

    db = SessionLocal()

    try:

        # ==========================================
        # SEARCH MEDICINE
        # ==========================================

        if (
            user_latitude == 0.0
            and user_longitude == 0.0
        ):

            results = (
                AllocationService.search_medicine(
                    db,
                    keyword
                )
            )

        else:

            results = (
                AllocationService.search_medicine(
                    db,
                    keyword,
                    user_latitude,
                    user_longitude
                )
            )

        # ==========================================
        # NO RESULTS
        # ==========================================

        if not results:

            st.warning(
                t(
                    "no_hospitals_medicine",
                    language
                )
            )

            return

        # ==========================================
        # RECOMMENDED HOSPITAL
        # ==========================================

        if hasattr(
            results[0],
            "distance"
        ):

            nearest = results[0]

            st.success(
                f"⭐ "
                f"{t('nearest_hospital', language)}: "
                f"{nearest.hospital.hospital_name} "
                f"({nearest.distance} km)"
            )

        # ==========================================
        # RESULTS
        # ==========================================

        st.subheader(
            f"📋 "
            f"{t('results', language)} "
            f"({len(results)})"
        )

        # ==========================================
        # HOSPITAL CARDS
        # ==========================================

        for index, item in enumerate(results):

            # ======================================
            # STOCK STATUS
            # ======================================

            if item.quantity > 100:

                status = (
                    f"🟢 "
                    f"{t('high_stock', language)}"
                )

            elif (
                item.quantity
                > item.reorder_level
            ):

                status = (
                    f"🟡 "
                    f"{t('medium_stock', language)}"
                )

            else:

                status = (
                    f"🔴 "
                    f"{t('low_stock', language)}"
                )

            with st.container(
                border=True
            ):

                col1, col2 = st.columns(
                    [4, 1]
                )

                with col1:

                    text = f"""
### 🏥 {item.hospital.hospital_name}

💊 **{t('medicine', language)}:** {item.medicine.medicine_name}

📍 **{t('city', language)}:** {item.hospital.city}

📦 **{t('available_stock', language)}:** {item.quantity}

🚦 **{t('status', language)}:** {status}
"""

                    if hasattr(
                        item,
                        "distance"
                    ):

                        text += (
                            f"\n📏 **"
                            f"{t('distance', language)}:** "
                            f"{item.distance} km"
                        )

                    st.markdown(text)

                with col2:

                    st.metric(
                        t(
                            "stock",
                            language
                        ),
                        item.quantity
                    )

                # ======================================
                # RESERVATION
                # ======================================

                st.divider()

                quantity = st.number_input(
                    t(
                        "reservation_quantity",
                        language
                    ),
                    min_value=1,
                    max_value=item.quantity,
                    value=1,
                    step=1,
                    key=(
                        f"reservation_quantity_"
                        f"{index}"
                    )
                )

                # ======================================
                # PRESCRIPTION CHECK
                # ======================================

                prescription_required = bool(
                    getattr(
                        item.medicine,
                        "prescription_required",
                        False
                    )
                )

                if prescription_required:

                    st.warning(
                        "📄 This medicine requires "
                        "a prescription."
                    )

                    st.info(
                        "Please upload a clear "
                        "prescription before submitting "
                        "your reservation."
                    )

                    prescription_file = (
                        st.file_uploader(
                            "Upload Prescription",
                            type=[
                                "jpg",
                                "jpeg",
                                "png",
                                "pdf"
                            ],
                            key=(
                                f"prescription_"
                                f"{index}"
                            ),
                            help=(
                                "Accepted formats: "
                                "JPG, JPEG, PNG and PDF."
                            )
                        )
                    )

                else:

                    prescription_file = None

                # ======================================
                # RESERVE BUTTON
                # ======================================

                if st.button(
                    f"📌 "
                    f"{t('reserve_medicine', language)}",
                    key=(
                        f"reserve_{index}"
                    ),
                    use_container_width=True
                ):

                    # ==================================
                    # PRESCRIPTION VALIDATION
                    # ==================================

                    if (
                        prescription_required
                        and prescription_file is None
                    ):

                        st.error(
                            "❌ A prescription is "
                            "required for this medicine."
                        )

                        continue

                    # ==================================
                    # SAVE PRESCRIPTION
                    # ==================================

                    prescription_path = None

                    if prescription_file:

                        prescription_path = (
                            save_prescription(
                                prescription_file
                            )
                        )

                        if not prescription_path:

                            st.error(
                                "❌ Invalid prescription "
                                "file."
                            )

                            continue

                    # ==================================
                    # CREATE RESERVATION
                    # ==================================

                    success, message = (
                        ReservationService
                        .add_reservation(
                            db=db,
                            user_id=current_user_id,
                            hospital_id=(
                                item.hospital.id
                            ),
                            medicine_id=(
                                item.medicine.id
                            ),
                            quantity=quantity,
                            prescription_path=(
                                prescription_path
                            )
                        )
                    )

                    # ==================================
                    # RESULT
                    # ==================================

                    if success:

                        st.success(
                            message
                        )

                        if prescription_required:

                            st.info(
                                "📄 Your prescription "
                                "has been submitted for "
                                "review. The reservation "
                                "will proceed after "
                                "administrative approval."
                            )

                        else:

                            st.info(
                                t(
                                    "reservation_pending_message",
                                    language
                                )
                            )

                    else:

                        # If reservation creation failed
                        # after the file was saved, remove
                        # the unused prescription file.

                        if prescription_path:

                            try:

                                if os.path.exists(
                                    prescription_path
                                ):

                                    os.remove(
                                        prescription_path
                                    )

                            except Exception:
                                pass

                        st.error(
                            message
                        )

        # ==========================================
        # HOSPITAL MAP
        # ==========================================

        st.divider()

        st.subheader(
            f"🗺️ "
            f"{t('hospital_locations', language)}"
        )

        HospitalMap.render(
            results
        )

    finally:

        db.close()