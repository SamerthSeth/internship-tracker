"""
File upload utilities with local storage abstraction
"""

import secrets
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class FileUploadManager:
    """Manages file uploads and storage"""
    
    def __init__(self):
        """Initialize file manager"""
        configured_dir = Path(settings.FILE_UPLOAD_DIRECTORY)
        self.upload_dir = configured_dir if configured_dir.is_absolute() else PROJECT_ROOT / configured_dir
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.max_file_size = settings.MAX_FILE_SIZE
        self.allowed_types = {
            file_type.strip().lower()
            for file_type in settings.ALLOWED_FILE_TYPES.split(",")
            if file_type.strip()
        }
    
    def get_file_extension(self, filename: str) -> str:
        """
        Get file extension
        
        Args:
            filename: Name of the file
        
        Returns:
            File extension
        """
        return Path(filename).suffix.lower().lstrip(".")
    
    def validate_file(self, file: UploadFile) -> bool:
        """
        Validate uploaded file
        
        Args:
            file: Uploaded file to validate
        
        Returns:
            True if file is valid
        
        Raises:
            HTTPException: If file is invalid
        """
        # Check file extension
        extension = self.get_file_extension(file.filename)
        if extension not in self.allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed types: {', '.join(self.allowed_types)}"
            )
        
        # File size check is done in route with max_size parameter
        return True
    
    async def save_file(self, file: UploadFile, subdirectory: str = "") -> str:
        """
        Save uploaded file to disk
        
        Args:
            file: File to save
            subdirectory: Subdirectory within upload directory
        
        Returns:
            File path relative to upload directory
        
        Raises:
            HTTPException: If file save fails
        """
        try:
            # Validate file
            self.validate_file(file)
            
            # Create subdirectory if specified
            if subdirectory:
                target_dir = self.upload_dir / subdirectory
                target_dir.mkdir(parents=True, exist_ok=True)
            else:
                target_dir = self.upload_dir
            
            # Generate secure filename
            extension = self.get_file_extension(file.filename)
            secure_filename = f"{secrets.token_hex(8)}.{extension}"
            
            # Save file
            file_path = target_dir / secure_filename
            contents = await file.read()
            
            with open(file_path, "wb") as f:
                f.write(contents)
            
            # Return a path relative to the upload directory for DB storage
            return str(file_path.relative_to(self.upload_dir)).replace("\\", "/")
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save file: {str(e)}"
            )
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete file from storage
        
        Args:
            file_path: Path to file
        
        Returns:
            True if deleted successfully
        """
        try:
            normalized = file_path.replace("\\", "/").lstrip("/")
            if normalized.startswith("uploads/"):
                normalized = normalized[len("uploads/") :]
            full_path = self.upload_dir / normalized
            if full_path.exists():
                full_path.unlink()
                return True
            return False
        except Exception:
            return False
    
    def get_file_url(self, file_path: str) -> str:
        """
        Get URL for accessing file
        
        Args:
            file_path: Stored file path
        
        Returns:
            File URL for access
        """
        return f"/uploads/{file_path.lstrip('/')}"


# Global instance
file_manager = FileUploadManager()
