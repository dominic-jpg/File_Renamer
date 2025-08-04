import streamlit as st
import pandas as pd
import os
import shutil
from io import BytesIO

st.title("YDoc File Generator")

# Upload CSV
csv_file = st.file_uploader("Upload CSV file", type="csv")

# Upload template file
template_file = st.file_uploader("Upload Template File (.bin)", type=["bin", "txt"])

# Process when both files are uploaded
if csv_file and template_file:
    df = pd.read_csv(csv_file)
    
    # Validate required columns
    if "Borehole ID" not in df.columns or "Current YDoc S/N" not in df.columns:
        st.error("CSV must contain 'Borehole ID' and 'Current YDoc S/N' columns.")
    else:
        output_zip = BytesIO()
        with shutil.make_archive("ydoc_output", 'zip', root_dir=None) as archive:
            for _, row in df.iterrows():
                borehole_id = str(row["Borehole ID"]).strip()
                serial = str(row["Current YDoc S/N"]).strip()

                if not serial:
                    continue

                # Create in-memory subfolder and file
                folder_path = f"{borehole_id}"
                filename = f"{serial}.bin"
                file_path = os.path.join(folder_path, filename)

                os.makedirs(folder_path, exist_ok=True)
                with open(file_path, "wb") as f:
                    f.write(template_file.getbuffer())

            # Zip the entire structure
            shutil.make_archive("ydoc_output", 'zip', ".")

        with open("ydoc_output.zip", "rb") as zip_file:
            st.download_button("Download ZIP", zip_file, file_name="ydoc_files.zip")

