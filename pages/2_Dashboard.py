
import streamlit as st
import pandas as pd
import plotly.express as px

from core.session import SessionManager
from core.database import SessionLocal

from services.dashboard_service import DashboardService
from services.analytics_service import AnalyticsService
from services.reservation_service import ReservationService


# ==================================================
# AUTHENTICATION
# ==================================================

if not SessionManager.is_logged_in():

    st.error("Please login first.")
    st.stop()


user = SessionManager.get_user()

db = SessionLocal()


try:

    # ==================================================
    # HEADER
    # ==================================================

    st.title("📊 Dashboard")

    st.success(
        f"Welcome, {user['name']} 👋"
    )

    st.write(
        f"**Email:** {user['email']}"
    )

    st.write(
        f"**Role:** {user['role']}"
    )

    st.divider()


    # ==================================================
    # BASIC STATISTICS
    # ==================================================

    stats = DashboardService.get_statistics(db)

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🏥 Hospitals",
            stats["hospitals"]
        )

    with col2:

        st.metric(
            "💊 Medicines",
            stats["medicines"]
        )

    with col3:

        st.metric(
            "📦 Inventory",
            stats["inventory"]
        )

    with col4:

        st.metric(
            "🚨 Low Stock",
            stats["low_stock"]
        )


    st.divider()


    # ==================================================
    # LOW STOCK MEDICINES
    # ==================================================

    st.subheader(
        "🚨 Low Stock Medicines"
    )

    low_stock = DashboardService.get_low_stock(db)

    if low_stock:

        table = []

        for item in low_stock:

            hospital_name = (
                item.hospital.hospital_name
                if item.hospital
                else "Unknown"
            )

            medicine_name = (
                item.medicine.medicine_name
                if item.medicine
                else "Unknown"
            )

            table.append({

                "Hospital":
                    hospital_name,

                "Medicine":
                    medicine_name,

                "Available":
                    item.quantity,

                "Reorder Level":
                    item.reorder_level

            })

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "🎉 No medicines are currently low in stock."
        )


    st.divider()


    # ==================================================
    # RESERVATION DATA
    # ==================================================

    st.subheader(
        "📌 Reservation Overview"
    )

    reservations = (
        ReservationService.get_all_reservations(db)
    )

    pending = 0
    approved = 0
    completed = 0
    cancelled = 0

    for reservation in reservations:

        if reservation.status == "Pending":

            pending += 1

        elif reservation.status == "Approved":

            approved += 1

        elif reservation.status == "Completed":

            completed += 1

        elif reservation.status == "Cancelled":

            cancelled += 1


    # ==================================================
    # RESERVATION CARDS
    # ==================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🟡 Pending",
            pending
        )

    with col2:

        st.metric(
            "🟢 Approved",
            approved
        )

    with col3:

        st.metric(
            "🏁 Completed",
            completed
        )

    with col4:

        st.metric(
            "🔴 Cancelled",
            cancelled
        )


    # ==================================================
    # RESERVATION CHART
    # ==================================================

    reservation_data = pd.DataFrame({

        "Status": [
            "Pending",
            "Approved",
            "Completed",
            "Cancelled"
        ],

        "Count": [
            pending,
            approved,
            completed,
            cancelled
        ]

    })


    fig = px.bar(

        reservation_data,

        x="Status",

        y="Count",

        title="Reservation Status",

        labels={
            "Status": "Reservation Status",
            "Count": "Number of Reservations"
        }

    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.divider()


    # ==================================================
    # ANALYTICS DASHBOARD
    # ==================================================

    st.subheader(
        "📈 Analytics Dashboard"
    )


    # ==================================================
    # INVENTORY BY HOSPITAL
    # ==================================================

    inventory_data = (
        AnalyticsService.inventory_by_hospital(db)
    )


    if inventory_data:

        hospitals = [
            row[0]
            for row in inventory_data
        ]

        quantities = [
            row[1]
            for row in inventory_data
        ]


        fig = px.bar(

            x=hospitals,

            y=quantities,

            labels={
                "x": "Hospital",
                "y": "Inventory"
            },

            title="Inventory Distribution by Hospital"

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ==================================================
    # MEDICINE CATEGORIES
    # ==================================================

    category_data = (
        AnalyticsService
        .medicine_category_distribution(db)
    )


    if category_data:

        labels = [
            row[0]
            for row in category_data
        ]

        values = [
            row[1]
            for row in category_data
        ]


        fig = px.pie(

            names=labels,

            values=values,

            title="Medicine Categories"

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ==================================================
    # STOCK HEALTH
    # ==================================================

    stock = (
        AnalyticsService
        .stock_status_distribution(db)
    )


    if stock:

        fig = px.pie(

            names=list(
                stock.keys()
            ),

            values=list(
                stock.values()
            ),

            hole=0.5,

            title="Stock Health"

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.divider()


    # ==================================================
    # LOGOUT
    # ==================================================

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        SessionManager.logout()

        st.switch_page(
            "pages/0_Login.py"
        )


finally:

    db.close()

