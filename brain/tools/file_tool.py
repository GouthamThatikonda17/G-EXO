# brain/tools/file_tool.py
"""
=========================================================
Project G-EXO File Tool
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""
import os
import shutil
from pathlib import Path
from config import DATA_DIR
from tools.models import ToolResult

WORKSPACE_DIR = Path(DATA_DIR) / "workspace"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB limit for reading text

def _secure_path(relative_path: str) -> Path | ToolResult:
    """
    Resolves the target path and ensures it does not escape the workspace sandbox.
    Protects against directory traversal attacks (e.g., '../../etc/passwd').
    """
    if not relative_path:
        relative_path = ""
    try:
        WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
        # Resolve to absolute real path (following symlinks)
        target = (WORKSPACE_DIR / str(relative_path)).resolve()
        workspace_real = WORKSPACE_DIR.resolve()
        
        if not target.is_relative_to(workspace_real):
            return ToolResult(
                success=False, 
                message=f"Security Error: Access to '{relative_path}' is denied. Sandbox violation."
            )
        return target
    except Exception as e:
        return ToolResult(success=False, message=f"Path resolution error: {str(e)}")

def create_file(path: str) -> ToolResult:
    target = _secure_path(path)
    if isinstance(target, ToolResult): return target
    try:
        if target.exists():
            return ToolResult(success=False, message=f"File already exists: {path}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.touch()
        return ToolResult(success=True, message=f"File created successfully: {path}")
    except Exception as e:
        return ToolResult(success=False, message=f"Failed to create file: {str(e)}")

def create_folder(path: str) -> ToolResult:
    target = _secure_path(path)
    if isinstance(target, ToolResult): return target
    try:
        if target.exists():
            return ToolResult(success=False, message=f"Folder already exists: {path}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.mkdir()
        return ToolResult(success=True, message=f"Folder created: {path}")
    except Exception as e:
        return ToolResult(success=False, message=f"Failed to create folder: {str(e)}")

def delete_file(path: str) -> ToolResult:
    target = _secure_path(path)
    if isinstance(target, ToolResult): return target
    try:
        if not target.exists():
            return ToolResult(success=False, message=f"File not found: {path}")
        if not target.is_file():
            return ToolResult(success=False, message=f"Path is not a file: {path}")
        target.unlink()
        return ToolResult(success=True, message=f"File deleted: {path}")
    except Exception as e:
        return ToolResult(success=False, message=f"Failed to delete file: {str(e)}")

def delete_folder(path: str) -> ToolResult:
    target = _secure_path(path)
    if isinstance(target, ToolResult): return target
    try:
        if not target.exists():
            return ToolResult(success=False, message=f"Folder not found: {path}")
        if not target.is_dir():
            return ToolResult(success=False, message=f"Path is not a folder: {path}")
        shutil.rmtree(target)
        return ToolResult(success=True, message=f"Folder deleted: {path}")
    except Exception as e:
        return ToolResult(success=False, message=f"Failed to delete folder: {str(e)}")

def rename(path: str, new_path: str) -> ToolResult:
    target = _secure_path(path)
    if isinstance(target, ToolResult): return target
    new_target = _secure_path(new_path)
    if isinstance(new_target, ToolResult): return new_target
    try:
        if not target.exists():
            return ToolResult(success=False, message=f"Path not found: {path}")
        if new_target.exists():
            return ToolResult(success=False, message=f"Destination already exists: {new_path}")
        new_target.parent.mkdir(parents=True, exist_ok=True)
        target.rename(new_target)
        return ToolResult(success=True, message=f"Renamed '{path}' to '{new_path}'")
    except Exception as e:
        return ToolResult(success=False, message=f"Failed to rename: {str(e)}")

def move(source: str, destination: str) -> ToolResult:
    src = _secure_path(source)
    if isinstance(src, ToolResult): return src
    dst = _secure_path(destination)
    if isinstance(dst, ToolResult): return dst
    try:
        if not src.exists():
            return ToolResult(success=False, message=f"Source not found: {source}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        return ToolResult(success=True, message=f"Moved to: {destination}")
    except Exception as e:
        return ToolResult(success=False, message=f"Failed to move: {str(e)}")

def copy(source: str, destination: str) -> ToolResult:
    src = _secure_path(source)
    if isinstance(src, ToolResult): return src
    dst = _secure_path(destination)
    if isinstance(dst, ToolResult): return dst
    try:
        if not src.exists():
            return ToolResult(success=False, message=f"Source not found: {source}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)
        return ToolResult(success=True, message=f"Copied to: {destination}")
    except Exception as e:
        return ToolResult(success=False, message=f"Failed to copy: {str(e)}")

def read_text(path: str) -> ToolResult:
    target = _secure_path(path)
    if isinstance(target, ToolResult): return target
    try:
        if not target.exists():
            return ToolResult(success=False, message=f"File not found: {path}")
        if not target.is_file():
            return ToolResult(success=False, message=f"Path is not a file: {path}")
        if target.stat().st_size > MAX_FILE_SIZE:
            return ToolResult(success=False, message=f"File exceeds maximum size limit ({MAX_FILE_SIZE/(1024*1024)}MB).")
        content = target.read_text(encoding="utf-8")
        return ToolResult(success=True, message=f"Read file: {path}", data=content)
    except UnicodeDecodeError:
        return ToolResult(success=False, message=f"File is not valid UTF-8 text: {path}")
    except Exception as e:
        return ToolResult(success=False, message=f"Failed to read file: {str(e)}")

def write_text(path: str, content: str, overwrite: bool = False) -> ToolResult:
    target = _secure_path(path)
    if isinstance(target, ToolResult): return target
    try:
        if target.exists() and not overwrite:
            return ToolResult(success=False, message=f"File already exists and overwrite is False: {path}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return ToolResult(success=True, message=f"Wrote to file: {path}")
    except Exception as e:
        return ToolResult(success=False, message=f"Failed to write file: {str(e)}")

def append_text(path: str, content: str) -> ToolResult:
    target = _secure_path(path)
    if isinstance(target, ToolResult): return target
    try:
        if not target.exists():
            return ToolResult(success=False, message=f"File not found: {path}")
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as f:
            f.write(content)
        return ToolResult(success=True, message=f"Appended to file: {path}")
    except Exception as e:
        return ToolResult(success=False, message=f"Failed to append to file: {str(e)}")

def list_directory(path: str = "") -> ToolResult:
    target = _secure_path(path)
    if isinstance(target, ToolResult): return target
    try:
        if not target.exists():
            return ToolResult(success=False, message=f"Path not found: {path}")
        if not target.is_dir():
            return ToolResult(success=False, message=f"Path is not a directory: {path}")
        items = []
        for item in target.iterdir():
            item_type = "Folder" if item.is_dir() else "File"
            items.append(f"[{item_type}] {item.name}")
        return ToolResult(success=True, message=f"Directory listing for '{path or '/'}'", data=items)
    except Exception as e:
        return ToolResult(success=False, message=f"Failed to list directory: {str(e)}")

def search_by_filename(filename: str, path: str = "") -> ToolResult:
    target = _secure_path(path)
    if isinstance(target, ToolResult): return target
    try:
        if not target.exists() or not target.is_dir():
            return ToolResult(success=False, message=f"Search path not valid: {path}")
        matches = []
        for p in target.rglob(f"*{filename}*"):
            try:
                matches.append(str(p.relative_to(WORKSPACE_DIR)))
            except ValueError:
                continue
        return ToolResult(success=True, message=f"Found {len(matches)} matches for '{filename}'", data=matches)
    except Exception as e:
        return ToolResult(success=False, message=f"Failed to search: {str(e)}")