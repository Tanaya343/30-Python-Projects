## 📄 PDF Utility Tool (Python Project)
A lightweight Python-based GUI application to split and merge PDF files — built using PyPDF2 and tkinter. Designed to be user-friendly, flexible, and offline-ready!

## Features

✅ Split PDF files by:

Single pages

Custom page ranges (e.g., 1-3, 4-5, 6)

✅ Merge multiple PDFs in a selected order

 Smart Validations:

Warns if splitting a single-page PDF

Handles incorrect or overlapping page ranges gracefully

Simple GUI — no terminal or code knowledge needed

Built with readability and learnability in mind


## Reqirements

Python 3.7+

Modules:

PyPDF2

tkinter (usually bundled with Python)

## Installation
Clone this repo or download the .py file

Install dependencies
Run the app

## How to use
🔹 Split PDF
Click Split PDF

Choose the PDF you want to split

Enter ranges:

For single pages: 1, 2, 3

For custom ranges: 1-4, 5-6, 7

The app will generate separate files for each range

⚠️ Files will be named like: split_part_1.pdf, split_part_2.pdf, etc.

🔹 Merge PDFs
Click Merge PDFs

Select multiple PDF files in the desired merge order

The merged file will be saved as merged.pdf

🔔 Make sure to select files in the order you want them to appear in the final merged file.

## 📌 Notes
The app warns if you try to split a single-page PDF

Empty or incorrect inputs are handled gracefully

All output files are saved in the same directory as the original PDF

## ✨ Future Improvements
Add PDF preview panel

Password-protected PDF support

Drag & drop interface

Dark mode

## Learning Outcomes
Practical use of PyPDF2 for file manipulation

GUI creation with tkinter

Robust input handling and validation

File dialogs and saving via tkinter.filedialog

## 🐍 Made with Python & 💙



