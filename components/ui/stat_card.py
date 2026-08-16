import streamlit as st


class StatCard:

    @staticmethod
    def render(
        title: str,
        value,
        icon: str = "📊",
        color: str = "#2563EB"
    ):

        st.markdown(
            f"""
            <div style="
                background:white;
                border-radius:16px;
                padding:20px;
                border-left:6px solid {color};
                box-shadow:0 4px 15px rgba(0,0,0,.08);
                margin-bottom:10px;
            ">

                <div style="
                    font-size:30px;
                ">
                    {icon}
                </div>

                <div style="
                    color:#64748B;
                    font-size:15px;
                    margin-top:8px;
                ">
                    {title}
                </div>

                <div style="
                    font-size:34px;
                    font-weight:700;
                    color:#1E293B;
                ">
                    {value}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )