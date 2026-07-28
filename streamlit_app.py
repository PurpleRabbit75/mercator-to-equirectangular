import streamlit as st
from mercator2equirectangular import mercator_to_equirectangular

# Big nasty global of PIL-supported extensions and their MIME types
PIL_WRITE_SUPPORTED_EXTENSIONS = {
    # Normal ones
    ".bmp": "image/bmp",
    ".gif": "image/gif",
    ".ico": "image/x-icon",
    ".jpg": "image/jpeg",
    ".png": "image/png",
    ".tiff": "image/tiff",
    ".webp": "image/webp",
    # Obscure Ones
    ".apng": "image/png",
    ".bw": "image/sgi",
    ".dds": "image/vnd.ms-dds",
    ".dib": "image/bmp",
    ".icb": "image/x-tga",
    ".im": "image/x-im",
    ".j2c": "image/jp2",
    ".j2k": "image/jp2",
    ".jfif": "image/jpeg",
    ".jp2": "image/jp2",
    ".jpc": "image/jp2",
    ".jpe": "image/jpeg",    
    ".jpeg": "image/jpeg",
    ".jpf": "image/jp2",
    ".jpx": "image/jp2",
    ".mpo": "image/mpo",
    ".pbm": "image/x-portable-anymap",
    ".pcx": "image/x-pcx",
    ".pgm": "image/x-portable-anymap",
    ".pnm": "image/x-portable-anymap",
    ".ppm": "image/x-portable-anymap",
    ".rgb": "image/sgi",
    ".rgba": "image/sgi",
    ".sgi": "image/sgi",
    ".tga": "image/x-tga",
    ".tif": "image/tiff",
    ".vda": "image/x-tga",
    ".vst": "image/x-tga",
}


# Force a narrow style (important for embedding)
st.markdown("""
<style>
.block-container {
    max-width: 730px;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)


# Make a nice litte welcome page
st.title("Convert Mercator Projection Maps to Equirectangular Projection")

st.write('For best results, use the so-called "Web Mercator" (also called the "Google Mercator" or "Pseudo-Mercator") projection. This format is characterized by poles truncated at approximately ±85.05°.')
st.write("TL;DR: If your Mercator map is approximately square, chances are you're using this projection!")

# File-uploader widget for the input map
uploaded_file = st.file_uploader("Upload your Mercator map here...", accept_multiple_files=False, max_upload_size=1000)

# Widget for selecting the export file type (easy, since once you pick the extension, PIL does the rest)
output_type = st.selectbox("Export As", list(PIL_WRITE_SUPPORTED_EXTENSIONS), index=4)
output_MIME="/image/jpeg"
if output_type is not None:
    output_MIME = PIL_WRITE_SUPPORTED_EXTENSIONS[output_type]


# All this stuff appears as soon as someone uploads the file
if uploaded_file is not None:

    # This whole thing is to prevent directory traversal attacks. I need to preserve the extension of the input file for PIL, but not the rest of it!
    if any("." in i for i in uploaded_file.name.split(".")):
        st.error('Filename cannot include more than one "." character!')
    else:
        extension=uploaded_file.name.split(".")[1]

        # Dump the file locally
        with open(f"./map.{extension}", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Display it for the user
        st.write("You uploaded this Mercator map:")
        st.image(f"./map.{extension}")

        # Do backend conversion
        output_path = f"converted_map{output_type}"
        mercator_to_equirectangular(f"./map.{extension}", output_path)

        # Display the converted map for the user
        st.write("Here is your converted Equirectangular map:")
        st.image(output_path)

        # Read the converted map into bytes again
        with open(output_path, "rb") as f:
            image_bytes = f.read()

        # Combine bytes, MIME type, and filename into a downloadable file
        st.download_button("Download", image_bytes, file_name=output_path, mime=output_MIME)

        # Bye!
        st.write("Have a nice day!")

