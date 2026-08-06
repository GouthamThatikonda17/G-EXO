"""
=========================================================
Project G-EXO Apps Tool
Version : 1.2
Developer : Thatikonda Goutham Teja
=========================================================
"""
import platform
import subprocess
import shutil
import os
from tools.models import ToolResult
from tools.app_metadata import SUPPORTED_APPS

# Internal mapping mapping application keys to typical OS executable names
_EXE_MAP = {
    "chrome": {"windows": "chrome.exe", "darwin": "Google Chrome", "linux": "google-chrome"},
    "notepad": {"windows": "notepad.exe", "darwin": "TextEdit", "linux": "gedit"},
    "calculator": {"windows": "calc.exe", "darwin": "Calculator", "linux": "gnome-calculator"},
    "vscode": {"windows": "code.cmd", "darwin": "Visual Studio Code", "linux": "code"},
    "explorer": {"windows": "explorer.exe", "darwin": "Finder", "linux": "xdg-open"},
    "paint": {"windows": "mspaint.exe", "darwin": "Paintbrush", "linux": "kolourpaint"},
    "cmd": {"windows": "cmd.exe", "darwin": "Terminal", "linux": "gnome-terminal"}
}

def _resolve_command(app_id: str, system: str) -> list[str] | None:
    """
    Platform-aware executable resolution strategy.
    Attempts standard PATH discovery, falling back to OS-specific mechanisms.
    """
    exe_name = _EXE_MAP.get(app_id, {}).get(system)
    if not exe_name:
        return None

    if system == "windows":
        # 1. Attempt standard PATH resolution
        path = shutil.which(exe_name)
        
        # 2. Fallback to Windows Registry (App Paths)
        if not path:
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rf"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{exe_name}") as key:
                    found_path, _ = winreg.QueryValueEx(key, "")
                    if found_path and os.path.exists(found_path):
                        path = found_path
            except Exception:
                pass
                
        # 3. Final fallback: Core Windows utilities natively resolvable by Popen
        if not path and exe_name in ["calc.exe", "notepad.exe", "explorer.exe", "cmd.exe", "mspaint.exe"]:
            path = exe_name
            
        if not path:
            return None
            
        cmd = [path]
        if app_id == "explorer":
            cmd.append(".")
        return cmd

    elif system == "darwin":
        # macOS native discovery mechanism via 'open'
        if app_id == "explorer":
            return ["open", "."]
        return ["open", "-a", exe_name]

    elif system == "linux":
        # Linux standard PATH discovery
        path = shutil.which(exe_name)
        if not path:
            return None
            
        cmd = [path]
        if app_id == "explorer":
            cmd.append(".")
        return cmd
        
    return None

def open_app(app_name: str) -> ToolResult:
    """
    Executes a requested application safely via a strict whitelist and 
    a platform-aware resolution strategy.
    """
    if not app_name:
        return ToolResult(
            success=False, 
            message="No application name provided."
        )
        
    app_id = app_name.lower().strip()
    
    if app_id not in SUPPORTED_APPS:
        return ToolResult(
            success=False, 
            message=f"Application '{app_id}' is not recognized."
        )
        
    system = platform.system().lower()
    command = _resolve_command(app_id, system)
    
    if not command:
        return ToolResult(
            success=False, 
            message=f"Could not locate '{SUPPORTED_APPS[app_id]}' on your system. Ensure it is installed."
        )
        
    try:
        # Secure, direct executable invocation without shell=True
        subprocess.Popen(command)
        return ToolResult(
            success=True, 
            message=f"Opening {SUPPORTED_APPS[app_id]}..."
        )
    except FileNotFoundError:
        return ToolResult(
            success=False, 
            message=f"Executable for {SUPPORTED_APPS[app_id]} not found. Ensure it is in your system PATH."
        )
    except Exception as e:
        return ToolResult(
            success=False, 
            message=f"Failed to launch {SUPPORTED_APPS[app_id]}: {str(e)}"
        )