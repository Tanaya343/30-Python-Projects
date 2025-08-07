import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import PyPDF2
import os


# ========== SPLIT PDF FUNCTION ==========
def split_pdf(): #defines split function
    file_path = filedialog.askopenfilename( 
        title="Select PDF to Split", filetypes=[("PDF Files", "*.pdf")]
    ) #opens a file selection dialog
    #only shows .pdf files as we have set fileNames = Pdf files, .pdf
    #stores selected file path in file_path

    if not file_path:
        return
    #if the user cancels the diaog, exits the function immediately

    try:
        pdf = PyPDF2.PdfReader(file_path) #opens the pdf file in read mode using PyPDF2's PdfReader
        total_pages = len(pdf.pages) #pdf.pages is a list of all pages in the pdf
        #total_pages counts the number of pages
        
        # Check if single-page PDF 
        if total_pages == 1: #if pdf has only 1 page - no splitting
            messagebox.showinfo(
                "Single Page PDF", "This PDF has only 1 page. No need to split."
            ) #shows popup msg and stops
            return

        # Ask user for split mode
        split_type = messagebox.askquestion(
            "Split Mode",
            "Do you want to split by custom page ranges?\n\nYes = Custom Ranges (e.g., 1-4, 5-7, 8)\nNo = Every page separately",
        ) #asks user how they want tp split
        #yes = custom range
        #no = individual pdfs per page

        output_dir = filedialog.askdirectory(title="Select Output Folder")
        if not output_dir:
            return #asks user where to save split files, if cancel, exit

        if split_type == "yes": #if user cooses yes
            # Custom range input
            ranges_input = simpledialog.askstring(
                "Custom Ranges",
                f"Enter page ranges (1-{total_pages}) separated by commas.\nExample: 1-4, 5-7, 8",
            ) #Prompt for custom ranges
            if not ranges_input:
                return

            try:
                ranges = ranges_input.split(",") #splits the input string by comms to get each ranges
                for idx, r in enumerate(ranges, start=1): #loops over each range
                    #idx used for naming output files
                    r = r.strip()
                    writer = PyPDF2.PdfWriter()

                    if "-" in r:
                        start, end = map(int, r.split("-"))
                        if start < 1 or end > total_pages or start > end:
                            raise ValueError("Invalid range")
                        for p in range(start - 1, end):
                            writer.add_page(pdf.pages[p])
                    else:
                        page_num = int(r)
                        if page_num < 1 or page_num > total_pages:
                            raise ValueError("Invalid page number")
                        writer.add_page(pdf.pages[page_num - 1])

                    output_filename = os.path.join(
                        output_dir, f"split_part_{idx}.pdf"
                    )
                    with open(output_filename, "wb") as f:
                        writer.write(f)

                messagebox.showinfo(
                    "Success", f"PDF split successfully into {len(ranges)} parts!"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        else:
            # Split into individual pages
            for i in range(total_pages):
                writer = PyPDF2.PdfWriter()
                writer.add_page(pdf.pages[i])

                output_filename = os.path.join(
                    output_dir, f"page_{i+1}.pdf"
                )
                with open(output_filename, "wb") as f:
                    writer.write(f)

            messagebox.showinfo(
                "Success", f"PDF split into {total_pages} single pages!"
            )

    except Exception as e:
        messagebox.showerror("Error", f"Failed to split PDF: {e}")


# ========== MERGE PDF FUNCTION ==========
def merge_pdfs():
    files = filedialog.askopenfilenames(
        title="Select PDFs to Merge", filetypes=[("PDF Files", "*.pdf")]
    )

    if not files or len(files) < 2:
        messagebox.showerror("Error", "Select at least 2 PDF files to merge.")
        return

    output_path = filedialog.asksaveasfilename(
        title="Save Merged PDF As",
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
    )
    if not output_path:
        return

    try:
        merger = PyPDF2.PdfMerger()

        messagebox.showinfo(
            "Order Info",
            "PDFs will be merged in the order you selected them.\nIf you want a different order, re-select accordingly.",
        )

        for pdf_file in files:
            merger.append(pdf_file)

        with open(output_path, "wb") as f:
            merger.write(f)

        messagebox.showinfo("Success", "PDFs merged successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to merge PDFs: {e}")


# ========== MAIN GUI ==========
root = tk.Tk()
root.title("PDF Utility Tool")
root.geometry("400x200")
root.config(bg="#f0f0f0")

tk.Label(root, text="📄 PDF Utility Tool", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

tk.Button(root, text="Split PDF", font=("Arial", 12), width=20, command=split_pdf).pack(pady=10)
tk.Button(root, text="Merge PDFs", font=("Arial", 12), width=20, command=merge_pdfs).pack(pady=10)

root.mainloop()
