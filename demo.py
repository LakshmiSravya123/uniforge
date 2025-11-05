#!/usr/bin/env python3
"""
Demo script to showcase CodeForge capabilities
Generates 5 example apps to demonstrate variety
"""

import subprocess
import sys

EXAMPLES = [
    "A simple todo list with categories and due dates",
    "URL shortener with click analytics and QR codes",
    "Recipe manager with ingredients search and ratings",
    "Daily habit tracker with streak counting",
    "Markdown note taking app with folders and tags",
]

def main():
    print("🔥 CodeForge Demo - Generating 5 Example Apps\n")
    print("=" * 70)
    
    for i, idea in enumerate(EXAMPLES, 1):
        print(f"\n📦 Example {i}/5: {idea}")
        print("-" * 70)
        
        try:
            subprocess.run(
                [sys.executable, "codeforge.py", idea],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"❌ Error generating app: {e}")
            continue
        
        print("✅ Generated successfully!")
    
    print("\n" + "=" * 70)
    print("🎉 Demo Complete!")
    print("\n📁 Check generated/ directory for all apps")
    print("\n🚀 To run any app:")
    print("   cd generated/APP_NAME")
    print("   bash ../quickstart.sh")


if __name__ == '__main__':
    main()
