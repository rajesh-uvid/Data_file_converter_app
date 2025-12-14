import pandas as pd
import chardet
from io import BytesIO

class ConversionUtils:
    """Core utilities for format conversion"""
    
    @staticmethod
    def read_csv_advanced(file_path, delimiter=',', encoding='utf-8', skip_rows=0, header=0, dtype_dict=None, na_values=None):
        """Read CSV with advanced options"""
        try:
            df = pd.read_csv(
                file_path,
                sep=delimiter,
                encoding=encoding,
                skiprows=skip_rows,
                header=header,
                dtype=dtype_dict,
                na_values=na_values or ['NA', 'N/A', '']
            )
            return df, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def read_excel_advanced(file_path, sheet_name=0, header=0, skip_rows=0):
        """Read Excel with advanced options"""
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=header, skiprows=skip_rows)
            return df, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def read_json_advanced(file_path, orient='records'):
        """Read JSON with advanced options"""
        try:
            df = pd.read_json(file_path, orient=orient)
            return df, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def convert_format(df, output_fmt, options=None):
        """Convert DataFrame to target format"""
        try:
            output = BytesIO()
            
            if output_fmt == 'csv':
                df.to_csv(output, index=False)
            elif output_fmt == 'excel':
                df.to_excel(output, index=False)
            elif output_fmt == 'json':
                df.to_json(output, orient='records')
            elif output_fmt == 'parquet':
                df.to_parquet(output)
            elif output_fmt == 'feather':
                df.to_feather(output)
            
            output.seek(0)
            return output, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def detect_encoding(file_path):
        """Auto-detect file encoding"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding']
        except:
            return 'utf-8'
