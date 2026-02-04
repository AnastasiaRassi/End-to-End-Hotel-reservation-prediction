import sys
import traceback
from pathlib import Path


class CustomException(Exception):
    def __init__(self, error: Exception, sys_module=None):
        super().__init__(str(error))
        self.original_error = error
        
        # Get traceback info
        if sys_module is None:
            sys_module = sys
            
        exc_type, exc_value, exc_tb = sys_module.exc_info()
        
        if exc_tb:
            self.lineno = exc_tb.tb_lineno
            self.file_name = Path(exc_tb.tb_frame.f_code.co_filename).name
            self.full_traceback = ''.join(traceback.format_tb(exc_tb))
        else:
            self.lineno = None
            self.file_name = None
            self.full_traceback = None

    def __str__(self):
        return (
            f"Error in script '{self.file_name}' at line {self.lineno}: "
            f"{self.original_error.__class__.__name__}: {str(self.original_error)}"
        )
    
    def get_detailed_message(self):
        """Get full traceback for logging."""
        return f"{str(self)}\n\nFull traceback:\n{self.full_traceback}"