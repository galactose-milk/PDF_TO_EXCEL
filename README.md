# PDF to Excel Converter 📄➡️📊  

A Python script that extracts tables from PDF files and converts them into Excel format using OCR and table extraction libraries.  

## 🚀 Features  
- Extracts text and tables from PDFs  
- Converts extracted data to Excel format (`.xlsx`)  
- Uses **OCR (Tesseract)** for scanned PDFs  
- Supports structured table extraction with **Camelot**  
- Works with both **image-based and text-based PDFs**  

## 🛠️ Installation  

### **1️⃣ Prerequisites**  
Ensure you have **Python 3.7+** installed.  
You'll also need **Tesseract-OCR** installed on your system:  
- **Windows**: [Download Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)  
- **Linux**: Install via package manager:
  ```sh
  sudo apt install tesseract-ocr
  ```
- **Mac**: Install via Homebrew:
  ```sh
  brew install tesseract
  ```

### **2️⃣ Install Dependencies**  
Clone this repository and install required Python packages:  

```sh
git clone https://github.com/your-username/PDF-to-Excel-Converter.git
cd PDF-to-Excel-Converter
pip install -r requirements.txt
```

## 📌 Usage  

### **Command Line Usage**
Run the script with:  

```sh
python pdf_to_excel.py input.pdf output.xlsx
```

### **Example**  
```sh
python pdf_to_excel.py sample.pdf result.xlsx
```
This extracts tables from `sample.pdf` and saves them in `result.xlsx`.

## 🧩 How It Works  
1. **PDF Processing**  
   - If the PDF is text-based, `Camelot` extracts tables directly.  
   - If the PDF is scanned (image-based), `pytesseract` (OCR) extracts text.  
   - `pdf2image` converts scanned PDFs into images for better OCR accuracy.  

2. **Data Processing**  
   - Extracted text is parsed using **pandas**.  
   - Cleaned data is structured into a DataFrame.  

3. **Excel Conversion**  
   - The final data is saved as an `.xlsx` file using **pandas**.  

## 🛠 Dependencies  
- `pytesseract` – OCR for scanned PDFs  
- `opencv-python` – Image processing  
- `pandas` – Data handling  
- `camelot-py` – Table extraction  
- `numpy` – Array operations  
- `pdf2image` – Converts PDFs to images  
- `anthropic` – AI model integration (if needed)  

Install all dependencies via:  
```sh
pip install -r requirements.txt
```

## ❓ Troubleshooting  

### **Common Issues & Fixes**  

- **Tesseract Not Found**:  
  Ensure Tesseract is installed and added to your system PATH.  
  ```sh
  tesseract -v  # Should display the version
  ```

- **Camelot Not Extracting Tables?**  
  Ensure your PDF has text-based tables. If it's scanned, use OCR.  

- **ImportError for pdf2image?**  
  Install poppler:
  - Windows: [Download Poppler](https://blog.alivate.com.au/poppler-windows/)
  - Linux:
    ```sh
    sudo apt install poppler-utils
    ```
  - Mac:
    ```sh
    brew install poppler
    ```

## 🎯 Future Enhancements  
✅ GUI version with a user-friendly interface  
✅ Batch processing for multiple PDFs  
✅ More AI-based table extraction  

## 🤝 Contributing  
Contributions are welcome! Fork the repo, make your changes, and submit a pull request.  

## 📜 License  
This project is licensed under the **MIT License**.  

## ⭐ Show Some Love  
If you find this project useful, please ⭐ star this repository!  
