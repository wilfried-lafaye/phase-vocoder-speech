"""
Utility functions for file management in the audio vocoder app.

Includes functions to save uploaded files temporarily and to clean up temporary files.
"""

import os
import tempfile

import streamlit as st


def save_uploaded_file(uploaded_file):
    """
    Saves an uploaded Streamlit file to a temporary file.

    Args:
        uploaded_file: Streamlit uploaded file object.

    Returns:
        str or None: Path to the saved temporary file, or None if saving failed.
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except OSError as e:
        st.error(f'Error saving file: {str(e)}')
        return None


def cleanup_temp_files(file_paths):
    """
    Deletes a list of temporary files if they exist.

    Args:
        file_paths (list[str]): List of file paths to delete.
    """
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except OSError:
            pass
