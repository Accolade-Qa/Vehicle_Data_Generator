param(
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

$python = if (Test-Path ".\.venv\Scripts\python.exe") {
    ".\.venv\Scripts\python.exe"
} else {
    "python"
}

Write-Host "Using Python: $python"
& $python -m pip install pyinstaller

$args = @(
    "-m", "PyInstaller",
    "--noconfirm",
    "--windowed",
    "--onefile",
    "--name", "VehicleDataGenerator",
    "--paths", "src",
    "run_desktop.py"
)

if ($Clean) {
    $args += "--clean"
}

& $python @args

Write-Host ""
Write-Host "Build complete."
Write-Host "Executable: dist\VehicleDataGenerator.exe"
