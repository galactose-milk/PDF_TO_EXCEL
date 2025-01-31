import pytesseract
import cv2
import pandas as pd
import camelot
import numpy as np
from pdf2image import convert_from_path
from anthropic import Anthropic  # Updated import for newer API
from io import StringIO
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFTableExtractor:
    def __init__(self, api_key):
        """Initialize with Claude API key."""
        self.client = Anthropic(api_key=api_key)  # Updated client initialization
        
    def preprocess_image(self, image):
        """Preprocess image for better OCR results."""
        try:
            if isinstance(image, np.ndarray):
                img_array = image
            else:
                img_array = np.array(image)
                
            gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
            thresh = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11, 2
            )
            kernel = np.ones((3, 3), np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
            return opening
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            return image

    def extract_table_data(self, pdf_path):
        """Extract tables from PDF using both Camelot and OCR."""
        try:
            images = convert_from_path(pdf_path)
            all_tables = []

            for page_num, img in enumerate(images, 1):
                preprocessed_img = self.preprocess_image(img)
                
                # Try Camelot first
                try:
                    tables = camelot.read_pdf(
                        pdf_path,
                        pages=str(page_num),
                        flavor='stream'
                    )
                    if len(tables) > 0:
                        for table in tables:
                            if table.df.size > 0:  # Check if table contains data
                                all_tables.append(table.df)
                                continue
                    
                    # If no tables found with stream, try lattice
                    tables = camelot.read_pdf(
                        pdf_path,
                        pages=str(page_num),
                        flavor='lattice'
                    )
                    for table in tables:
                        if table.df.size > 0:
                            all_tables.append(table.df)
                
                except Exception as e:
                    logger.warning(f"Camelot failed on page {page_num}, trying OCR: {e}")
                    # OCR fallback
                    extracted_text = pytesseract.image_to_string(preprocessed_img)
                    if extracted_text.strip():  # Check if text was extracted
                        all_tables.append(pd.DataFrame([line.split() for line in extracted_text.splitlines()]))
            
            return all_tables

        except Exception as e:
            logger.error(f"Error in table extraction: {e}")
            return []

    def process_with_claude(self, table_string):
        """Clean and structure table data using Claude."""
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",  # Updated model
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": f"""Clean and structure this table data. Output as CSV format.
                    If there are headers, preserve them. Make best effort to maintain table structure.
                    Table data:
                    {table_string}
                    """
                }]
            )
            return message.content
        except Exception as e:
            logger.error(f"Claude API Error: {e}")
            return None

    def process_pdf_tables(self, pdf_path, output_excel_path):
        """Main processing function."""
        try:
            extracted_tables = self.extract_table_data(pdf_path)
            if not extracted_tables:
                logger.warning("No tables extracted from PDF")
                return False

            all_cleaned_dfs = []
            for i, table_df in enumerate(extracted_tables, 1):
                table_string = table_df.to_string()
                claude_output = self.process_with_claude(table_string)

                if claude_output:
                    try:
                        cleaned_df = pd.read_csv(StringIO(claude_output))
                        all_cleaned_dfs.append(cleaned_df)
                        logger.info(f"Successfully processed table {i}")
                    except pd.errors.ParserError as e:
                        logger.warning(f"Error parsing Claude output for table {i}: {e}")
                        all_cleaned_dfs.append(table_df)
                else:
                    logger.warning(f"Using original table {i} (Claude processing failed)")
                    all_cleaned_dfs.append(table_df)

            # Save to Excel
            with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
                for i, df in enumerate(all_cleaned_dfs, 1):
                    df.to_excel(writer, sheet_name=f"Table_{i}", index=False)
            
            logger.info(f"Successfully saved tables to {output_excel_path}")
            return True

        except Exception as e:
            logger.error(f"Error processing PDF tables: {e}")
            return False

# Example usage
if __name__ == "__main__":
    API_KEY = "your-api-key-please"  # Replace with actual key
    PDF_PATH = "/media/galactose/Partition2/ML_PROGRAMMING/rag_anal/table.pdf"
    OUTPUT_PATH = "output_tables.xlsx"
    
    extractor = PDFTableExtractor(API_KEY)
    success = extractor.process_pdf_tables(PDF_PATH, OUTPUT_PATH)
