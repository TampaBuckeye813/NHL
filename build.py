"""
Build script for NHL Game Predictor
Creates a single-file .exe for Windows
"""

import subprocess
import sys
import os
import shutil


def install_requirements():
    """Install required packages"""
    print("=" * 60)
    print("Installing required packages...")
    print("=" * 60)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("\n✓ Requirements installed successfully!\n")


def build_exe():
    """Build the executable using PyInstaller"""
    print("=" * 60)
    print("Building executable...")
    print("=" * 60)

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",              # Single file
        "--windowed",             # No console window
        "--name", "NHL_Game_Predictor",
        "--clean",                # Clean cache
        "src/main.py"
    ]

    subprocess.check_call(cmd)
    print("\n✓ Build completed successfully!\n")


def cleanup():
    """Clean up build artifacts"""
    print("Cleaning up build artifacts...")

    # Remove build folder
    if os.path.exists("build"):
        shutil.rmtree("build")

    # Remove spec file
    if os.path.exists("NHL_Game_Predictor.spec"):
        os.remove("NHL_Game_Predictor.spec")

    print("✓ Cleanup complete!\n")


def main():
    """Main build process"""
    print("\n" + "=" * 60)
    print("NHL GAME PREDICTOR - BUILD SCRIPT")
    print("=" * 60 + "\n")

    try:
        # Step 1: Install requirements
        install_requirements()

        # Step 2: Build executable
        build_exe()

        # Step 3: Cleanup
        cleanup()

        # Success message
        print("=" * 60)
        print("BUILD SUCCESSFUL!")
        print("=" * 60)
        print(f"\nYour executable is ready:")
        print(f"  → dist/NHL_Game_Predictor.exe")
        print(f"\nYou can copy this file to your desktop or any folder.")
        print(f"Double-click it to run - no installation needed!")
        print("=" * 60 + "\n")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
