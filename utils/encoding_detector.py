import chardet

class EncodingDetector:
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
    
    @staticmethod
    def suggest_encoding(file_path):
        """Suggest multiple encoding options"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
            result = chardet.detect(raw_data)
            confidence = result['confidence']
            encoding = result['encoding']
            
            suggestions = [encoding]
            if confidence < 0.8:
                suggestions.extend(['utf-8', 'latin-1', 'iso-8859-1'])
            
            return list(set(suggestions))
        except:
            return ['utf-8', 'latin-1', 'iso-8859-1']
    
    @staticmethod
    def validate_encoding(file_path, encoding):
        """Validate if file can be read with specific encoding"""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read()
            return True
        except:
            return False
