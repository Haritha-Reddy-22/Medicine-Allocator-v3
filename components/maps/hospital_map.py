import folium
from streamlit_folium import st_folium
import streamlit as st


class HospitalMap:

    @staticmethod
    def render(results):
        # st.write(results)

        if not results:
            return

        # Center map on first hospital
        center_lat = results[0].hospital.latitude
        center_lon = results[0].hospital.longitude

        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=11
        )

        for item in results:

            popup = f"""
            <b>{item.hospital.hospital_name}</b><br>

            Medicine :
            {item.medicine.medicine_name}<br>

            Stock :
            {item.quantity}<br>

            City :
            {item.hospital.city}
            """

            if item.quantity > 100:

                color = "green"

            elif item.quantity > item.reorder_level:

                color = "orange"

            else:

                color = "red"

            folium.Marker(

                location=[
                    item.hospital.latitude,
                    item.hospital.longitude
                ],

                popup=popup,

                tooltip=item.hospital.hospital_name,

                icon=folium.Icon(
                    color=color,
                    icon="plus-sign"
                )

            ).add_to(m)

        st_folium(
            m,
            width=None,
            height=500
        )