import streamlit as st
from mercator2equirectangular import mercator_to_equirectangular

st.title("Convert Mercator Projection Maps to Equirectangular Projection")

st.write('For best results, use the so-called "Web Mercator" (also called the "Google Mercator" or "Pseudo-Mercator") projection, which projects onto a sphere instead of an ellipsoid and terminates the map at approximately ±85.05°.')
st.write("If your Mercator map is approximately square, chances are you're using this projection!")

uploaded_file = st.file_uploader("Upload your Mercator map here...", accept_multiple_files=False, max_upload_size=1000)


if uploaded_file is not None:

    if any("." in i for i in uploaded_file.name.split(".")):
        st.error('Filename cannot include more than one "." character!')
    else:
        extension=uploaded_file.name.split(".")[1]

        with open(f"./map.{extension}", "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.write("You uploaded this Mercator map:")
        st.image(f"./map.{extension}")

        output_path = "converted_map.jpg"
        mercator_to_equirectangular(f"./map.{extension}", output_path)

        st.write("Here is your converted Equirectangular map:")
        st.image(output_path)

        with open(output_path, "rb") as f:
            image_bytes = f.read()

        st.download_button("Download", image_bytes, file_name=output_path, mime="image/jpeg")

        st.write("Have a nice day!")

