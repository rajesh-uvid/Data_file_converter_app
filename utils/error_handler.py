class ErrorHandler:
    ERROR_SOLUTIONS = {
        'UnicodeDecodeError': 'Try selecting a different encoding (UTF-8, Latin-1, ISO-8859-1)',
        'ParserError': 'Check delimiter and file format',
        'FileNotFoundError': 'Ensure file path is correct',
        'PermissionError': 'Check file permissions',
        'MemoryError': 'File is too large, try batch processing',
    }
    
    @staticmethod
    def format_error_message(error):
        """Format error message for display"""
        error_type = type(error).__name__
        error_msg = str(error)
        
        return f"Error: {error_msg}"
    
    @staticmethod
    def get_error_solution(error):
        """Get solution for common errors"""
        error_type = type(error).__name__
        
        for key, solution in ErrorHandler.ERROR_SOLUTIONS.items():
            if key in error_type:
                return solution
        
        return "Check the file format and try again"
    
    @staticmethod
    def log_error(error, context=""):
        """Log error for debugging"""
        error_type = type(error).__name__
        error_msg = str(error)
        
        log_message = f"[{error_type}] {context}: {error_msg}"
        print(log_message)
        
        return log_message
