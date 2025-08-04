import streamlit as st
import pandas as pd
import os
import shutil
import tempfile

st.set_page_config(page_title="YDOC File Generator", layout="centered")
st.title("📁 YDOC Firmware Update File Generator (.bin)")

# Step 1: Upload CSV
st.markdown("""
### Step 1: Upload CSV File
Upload a `.csv` file containing columns for Borehole IDs and YDOC serial numbers.
""")
csv_file = st.file_uploader("Choose your CSV file", type="csv")

if csv_file:
    df = pd.read_csv(csv_file)
    column_options = list(df.columns)

    # Step 2: Select Columns
    st.markdown("### Step 2: Select Column Headers")
    bore_col = st.selectbox("Select the column for Logger ID", column_options, key="bore_id_col")
    serial_col = st.selectbox("Select the column for YDOC Serial Number", column_options, key="serial_col")

    # Step 3: Upload Template
    st.markdown("""
    ### Step 3: Upload Template File
    Upload the firmware `.bin` file that will be duplicated and renamed for each serial number.
    """)
    template_file = st.file_uploader("Choose your Template (.bin) file", type=["bin"])

    if template_file:
        with tempfile.TemporaryDirectory() as temp_dir:
            for _, row in df.iterrows():
                borehole_id = str(row[bore_col]).strip()
                serial_raw = row[serial_col]
                serial = str(int(float(serial_raw))) if pd.notna(serial_raw) else ""

                if not borehole_id or not serial:
                    continue

                # Create a folder for the borehole
                folder_path = os.path.join(temp_dir, borehole_id)
                os.makedirs(folder_path, exist_ok=True)

                # Copy template file with new name
                file_path = os.path.join(folder_path, f"YDOC_{serial}.bin")
                with open(file_path, "wb") as f:
                    f.write(template_file.getvalue())

            # Zip the result
            zip_path = shutil.make_archive(os.path.join(temp_dir, "ydoc_output"), 'zip', temp_dir)

            st.markdown("### Step 4: Download Result")
            with open(zip_path, "rb") as zip_file:
                st.download_button("📦 Download ZIP of Files", zip_file, file_name="YDOC_Files.zip")
