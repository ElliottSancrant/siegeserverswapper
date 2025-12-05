"""
Module to locate and modify GameSettings.ini files for Rainbow Six Siege
"""

import os
from pathlib import Path
import configparser


def get_user_documents_paths():
    """
    Get potential paths to Documents folders (regular and OneDrive)
    Searches multiple locations including custom Documents folder locations
    
    Returns:
        list: List of potential Documents paths
    """
    paths = []
    checked_paths = set()  # Avoid duplicates
    
    # Method 1: Use Windows shell folder (if available)
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        documents_path = shell.SpecialFolders("MyDocuments")
        if documents_path:
            doc_path = Path(documents_path)
            if doc_path.exists():
                paths.append(doc_path)
                checked_paths.add(str(doc_path.resolve()))
    except (ImportError, Exception):
        pass
    
    # Method 2: Use os.path.expanduser (works on Windows)
    try:
        home = Path(os.path.expanduser("~"))
        doc_paths = [
            home / "Documents",
            home / "OneDrive" / "Documents",
        ]
        for doc_path in doc_paths:
            if doc_path.exists():
                resolved = str(doc_path.resolve())
                if resolved not in checked_paths:
                    paths.append(doc_path)
                    checked_paths.add(resolved)
    except Exception:
        pass
    
    # Method 3: Check USERPROFILE environment variable
    userprofile = os.getenv('USERPROFILE')
    if userprofile:
        doc_paths = [
            Path(userprofile) / "Documents",
            Path(userprofile) / "OneDrive" / "Documents",
        ]
        for doc_path in doc_paths:
            if doc_path.exists():
                resolved = str(doc_path.resolve())
                if resolved not in checked_paths:
                    paths.append(doc_path)
                    checked_paths.add(resolved)
    
    # Method 4: Search all drives for Documents folders
    # Check common drive letters (C: through Z:)
    username = os.getenv('USERNAME') or os.getenv('USER', '')
    
    for drive in "CDEFGHIJKLMNOPQRSTUVWXYZ":
        potential_paths = [
            Path(f"{drive}:/Documents"),  # Direct Documents on drive (like D:/Documents)
        ]
        
        if username:
            potential_paths.extend([
                Path(f"{drive}:/Users/{username}/Documents"),
                Path(f"{drive}:/Users/{username}/OneDrive/Documents"),
            ])
        
        for doc_path in potential_paths:
            if doc_path.exists():
                resolved = str(doc_path.resolve())
                if resolved not in checked_paths:
                    paths.append(doc_path)
                    checked_paths.add(resolved)
    
    return paths


def find_game_settings_files(ubisoft_id: str = None):
    """
    Find GameSettings.ini file(s) for Rainbow Six Siege
    
    Args:
        ubisoft_id: Optional Ubisoft ID to find specific account's file.
                   If None, finds all GameSettings.ini files.
    
    Returns:
        list: List of Path objects to GameSettings.ini files
    """
    game_settings_files = []
    base_folder_name = "Rainbow Six - Siege"
    settings_filename = "GameSettings.ini"
    
    documents_paths = get_user_documents_paths()
    
    for docs_path in documents_paths:
        siege_folder = docs_path / "My Games" / base_folder_name
        
        if not siege_folder.exists():
            continue
        
        if ubisoft_id:
            # Look for specific account
            account_folder = siege_folder / ubisoft_id
            settings_file = account_folder / settings_filename
            
            if settings_file.exists():
                game_settings_files.append(settings_file)
        else:
            # Find all accounts
            for account_folder in siege_folder.iterdir():
                if account_folder.is_dir():
                    settings_file = account_folder / settings_filename
                    if settings_file.exists():
                        game_settings_files.append(settings_file)
    
    return game_settings_files


def update_server_setting(file_path: Path, server_value: str) -> bool:
    """
    Update the DataCenterHint setting in a GameSettings.ini file
    
    Args:
        file_path: Path to the GameSettings.ini file
        server_value: Value to set for DataCenterHint (e.g., "default", "playfab/westus1")
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Find and update DataCenterHint line
        updated = False
        for i, line in enumerate(lines):
            if line.strip().startswith('DataCenterHint='):
                lines[i] = f'DataCenterHint={server_value}\n'
                updated = True
                break
        
        # If DataCenterHint doesn't exist, add it at the end
        if not updated:
            # Remove empty lines at the end
            while lines and lines[-1].strip() == '':
                lines.pop()
            lines.append(f'DataCenterHint={server_value}\n')
        
        # Write the file back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        return True
        
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

