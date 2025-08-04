import os
import csv
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def create_files_from_template(csv_path, template_path, output_folder):
    try:
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            records = [(row["Borehole ID"].strip(), row["Current YDoc S/N"].strip()) for row in reader if row["Current YDoc S/N"].strip()]

        for borehole_id, serial in records:
            borehole_folder = os.path.join(output_folder, borehole_id)
            os.makedirs(borehole_folder, exist_ok=True)
            new_filepath = os.path.join(borehole_folder, f"{serial}.bin")
            shutil.copyfile(template_path, new_filepath)

        return f"✅ Successfully created {len(records)} .bin files in subfolders."
    except Exception as e:
        return f"❌ Error: {e}"

def run_gui():
    root = tk.Tk()
    root.title("YDoc File Generator")

    def select_csv():
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            csv_entry.delete(0, tk.END)
            csv_entry.insert(0, path)

    def select_template():
        path = filedialog.askopenfilename(filetypes=[("BIN Files", "*.bin"), ("All Files", "*.*")])
        if path:
            template_entry.delete(0, tk.END)
            template_entry.insert(0, path)

    def select_output():
        path = filedialog.askdirectory()
        if path:
            output_entry.delete(0, tk.END)
            output_entry.insert(0, path)

    def on_run():
        csv_path = csv_entry.get()
        template_path = template_entry.get()
        output_folder = output_entry.get()
        if not all([csv_path, template_path, output_folder]):
            messagebox.showerror("Missing Info", "Please select all required files and folder.")
            return
        result = create_files_from_template(csv_path, template_path, output_folder)
        messagebox.showinfo("Result", result)

    tk.Label(root, text="CSV File:").grid(row=0, column=0, sticky="e")
    csv_entry = tk.Entry(root, width=50)
    csv_entry.grid(row=0, column=1)
    tk.Button(root, text="Browse", command=select_csv).grid(row=0, column=2)

    tk.Label(root, text="Template .bin File:").grid(row=1, column=0, sticky="e")
    template_entry = tk.Entry(root, width=50)
    template_entry.grid(row=1, column=1)
    tk.Button(root, text="Browse", command=select_template).grid(row=1, column=2)

    tk.Label(root, text="Output Folder:").grid(row=2, column=0, sticky="e")
    output_entry = tk.Entry(root, width=50)
    output_entry.grid(row=2, column=1)
    tk.Button(root, text="Browse", command=select_output).grid(row=2, column=2)

    tk.Button(root, text="Generate Files", command=on_run, bg="green", fg="white").grid(row=3, column=1, pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
