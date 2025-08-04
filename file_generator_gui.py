import streamlit as st
import pandas as pd
import os
import shutil
import tempfile
from io import BytesIO

st.title("YDOC Firmware Update File Generator (.bin)")

csv_file = st.file_uploader("Upload CSV File", type="csv")
template_file = st.file_uploader("Upload Template File (.bin)", type=["bin"])

if csv_file and template_file:
    df = pd.read_csv(csv_file)

    if "Borehole ID" not in df.columns or "Current YDoc S/N" not in df.columns:
        st.error("CSV must contain 'Borehole ID' and 'Current YDoc S/N' columns.")
    else:
        with tempfile.TemporaryDirectory() as temp_dir:
            for _, row in df.iterrows():
                borehole_id = str(row["Borehole ID"]).strip()
                serial_raw = row["Current YDoc S/N"]
                serial = str(int(float(serial_raw))) if pd.notna(serial_raw) else ""

                if not borehole_id or not serial:
                    continue

                # Create subfolder per Borehole ID
                folder_path = os.path.join(temp_dir, borehole_id)
                os.makedirs(folder_path, exist_ok=True)

                # Write the file with .bin extension
                file_path = os.path.join(folder_path, f"YDOC_{serial}.bin")
                with open(file_path, "wb") as f:
                    f.write(template_file.getvalue())

            # Zip the entire output structure
            zip_path = shutil.make_archive(os.path.join(temp_dir, "ydoc_output"), 'zip', temp_dir)

            with open(zip_path, "rb") as zip_file:
                st.download_button("Download All Files as ZIP", zip_file, file_name="ydoc_files.zip")
