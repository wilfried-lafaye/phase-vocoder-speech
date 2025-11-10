"""
Configuration module for the Audio Vocoder application.

This module contains configuration settings and utility methods
for file management and application settings.
"""

import os


class Config:
    """
    Configuration class for Audio Vocoder application.

    This class holds all configuration constants and provides
    utility methods for directory management.
    """

    TEMP_AUDIO_PATH = './temp_audio'
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    SUPPORTED_FORMATS = ['.wav', '.mp3', '.flac']

    @classmethod
    def ensure_directories(cls):
        """
        Ensure all required directories exist.

        Creates the temporary audio directories if they don't exist.
        This includes uploaded and processed subdirectories.
        """
        os.makedirs(cls.TEMP_AUDIO_PATH, exist_ok=True)
        os.makedirs(os.path.join(cls.TEMP_AUDIO_PATH, 'uploaded'), exist_ok=True)
        os.makedirs(os.path.join(cls.TEMP_AUDIO_PATH, 'processed'), exist_ok=True)

    @classmethod
    def is_supported_format(cls, filename):
        """
        Check if the file extension is in the list of supported formats.

        Args:
            filename (str): Name of the file.

        Returns:
            bool: True if format is supported, False otherwise.
        """
        _, ext = os.path.splitext(filename)
        return ext.lower() in cls.SUPPORTED_FORMATS
