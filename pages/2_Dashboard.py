import streamlit as st
import plotly.express as px

from core.session import SessionManager
from core.database import SessionLocal
from services.dashboard_service import DashboardService
from services.analytics_service import AnalyticsService


st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------
# Authentication
# --------------------------

if not SessionManager.is_logged_in():

    st.error("Please login first.")
    st.stop()

user = SessionManager.get_user()

db = SessionLocal()

try:

    # --------------------------
    # Dashboard Header
    # --------------------------

    st.title("📊 Dashboard")

    st.success(f"Welcome, {user['name']} 👋")

    st.write(f"**Email:** {user['email']}")
    st.write(f"**Role:** {user['role']}")

    st.divider()

    # --------------------------
    # Statistics
    # --------------------------

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

    # --------------------------
    # Low Stock Medicines
    # --------------------------

    st.subheader("🚨 Low Stock Medicines")

    low_stock = DashboardService.get_low_stock(db)

    if low_stock:

        table = []

        for item in low_stock:

            table.append({

                "Hospital": item.hospital.hospital_name,
                "Medicine": item.medicine.medicine_name,
                "Available": item.quantity,
                "Reorder Level": item.reorder_level

            })

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success("🎉 No medicines are currently low in stock.")

    st.divider()

    # --------------------------
    # Analytics
    # --------------------------

    st.subheader("📈 Analytics Dashboard")

    # Inventory by Hospital

    inventory_data = AnalyticsService.inventory_by_hospital(db)

    if inventory_data:

        hospitals = [row[0] for row in inventory_data]
        quantities = [row[1] for row in inventory_data]

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

    # Medicine Categories

    category_data = AnalyticsService.medicine_category_distribution(db)

    if category_data:

        labels = [row[0] for row in category_data]
        values = [row[1] for row in category_data]

        fig = px.pie(
            names=labels,
            values=values,
            title="Medicine Categories"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Stock Health

    stock = AnalyticsService.stock_status_distribution(db)

    fig = px.pie(
        names=list(stock.keys()),
        values=list(stock.values()),
        hole=0.5,
        title="Stock Health"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # --------------------------
    # Logout
    # --------------------------

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        SessionManager.logout()

        st.switch_page("app.py")

finally:

    db.close()