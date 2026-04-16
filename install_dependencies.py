#!/usr/bin/env python3
"""
Script to install required dependencies for Hatsune Miku Bot
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip."""
    try:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error installing {package}: {e}")
        return False

def check_package(package):
    """Check if a package is already installed."""
    try:
        __import__(package)
        print(f"✅ {package} is already installed")
        return True
    except ImportError:
        print(f"❌ {package} is not installed")
        return False

def main():
    """Main function to install all required packages."""
    print("🤖 Hatsune Miku Bot - Dependency Installer")
    print("=" * 50)
    
    # List of required packages
    required_packages = [
        "disnake",
        "aiohttp",
        "asyncio",
        "datetime",
        "typing",
        "dotenv",
        "aiosqlite",
        "psutil",
        "PyNaCl",
        "re"
    ]
    
    # Packages that need to be installed via pip
    pip_packages = [
        "disnake",
        "aiohttp"
    ]
    
    print("Checking installed packages...")
    print("-" * 30)
    
    # Check which packages are missing
    missing_packages = []
    for package in required_packages:
        if not check_package(package):
            if package in pip_packages:
                missing_packages.append(package)
    
    if not missing_packages:
        print("\n🎉 All required packages are already installed!")
        return True
    
    print(f"\n📦 Installing {len(missing_packages)} missing packages...")
    print("-" * 30)
    
    # Install missing packages
    success_count = 0
    for package in missing_packages:
        if install_package(package):
            success_count += 1
        print()
    
    print("=" * 50)
    if success_count == len(missing_packages):
        print("🎉 All packages installed successfully!")
        print("✅ Bot should now run without import errors")
    else:
        print(f"⚠️  {success_count}/{len(missing_packages)} packages installed")
        print("❌ Some packages failed to install")
    
    return success_count == len(missing_packages)

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🚀 You can now run the bot!")
        else:
            print("\n❌ Please check the errors above and try again")
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
