import pandas as pd

class CSVHandler:
    @staticmethod
    def read(file_path, **kwargs):
        return pd.read_csv(file_path, **kwargs)
    
    @staticmethod
    def write(df, output_path, **kwargs):
        df.to_csv(output_path, index=False, **kwargs)

class ExcelHandler:
    @staticmethod
    def read(file_path, **kwargs):
        return pd.read_excel(file_path, **kwargs)
    
    @staticmethod
    def write(df, output_path, **kwargs):
        df.to_excel(output_path, index=False, **kwargs)

class JSONHandler:
    @staticmethod
    def read(file_path, **kwargs):
        return pd.read_json(file_path, **kwargs)
    
    @staticmethod
    def write(df, output_path, **kwargs):
        df.to_json(output_path, **kwargs)

class ParquetHandler:
    @staticmethod
    def read(file_path, **kwargs):
        return pd.read_parquet(file_path, **kwargs)
    
    @staticmethod
    def write(df, output_path, **kwargs):
        df.to_parquet(output_path, **kwargs)

class FeatherHandler:
    @staticmethod
    def read(file_path, **kwargs):
        return pd.read_feather(file_path, **kwargs)
    
    @staticmethod
    def write(df, output_path, **kwargs):
        df.to_feather(output_path, **kwargs)
