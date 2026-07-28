import streamlit as st
from mercator2equirectangular import mercator_to_equirectangular

st.title("Convert Mercator Projection Maps to Equirectangular Projection")

st.write('For best results, use the so-called "Web Mercator" or "Google Mercator" projection, which terminates the map at approximately ±89.05°.')
st.write("If your Mercator map is approximately square, chances are you're using this projection!")

uploaded_file = st.file_uploader("Upload your Mercator map here...")


if uploaded_file is not None:

    if any("." in i for i in uploaded_file.name.split(".")):
        st.error('Filename cannot include more than one "." character!')
    else:
        extension=uploaded_file.name.split(".")[1]

        with open(f"./map.{extension}", "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.write("You uploaded this Mercator map:")
        st.image(f"./map.{extension}")

        mercator_to_equirectangular(f"./map.{extension}", f"converted_map.{extension}")

        st.write("Here is your converted Equirectangular map:")
        st.image(f"converted_map.{extension}")

        st.write("Have a nice day!")

