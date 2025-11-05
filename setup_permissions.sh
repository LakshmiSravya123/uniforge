#!/bin/bash
# setup_permissions.sh - Guide for macOS Accessibility Setup

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║        UniForge - macOS Accessibility Permissions Setup      ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "To enable keyboard recording/replay, you need to:"
echo ""
echo "1. Open System Settings"
echo "2. Go to Privacy & Security → Accessibility"
echo "3. Click the '+' button"
echo "4. Add one of these applications:"
echo "   - Terminal.app (if running from Terminal)"
echo "   - iTerm.app (if running from iTerm)"
echo "   - VS Code.app (if running from VS Code terminal)"
echo "   - Or add Python directly: $(which python3)"
echo ""
echo "5. After adding, toggle it ON"
echo "6. Restart the UniForge application"
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                        Quick Test                             ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "Testing keyboard library..."
echo ""

# Try to import keyboard and check permissions
python3 << 'PYEOF'
try:
    import keyboard
    print("✅ Keyboard library installed")
    try:
        # This will fail without permissions
        keyboard.hook(lambda e: None)
        keyboard.unhook_all()
        print("✅ Accessibility permissions GRANTED - keyboard recording will work!")
    except OSError as e:
        if "administrator" in str(e).lower() or "permission" in str(e).lower():
            print("❌ Accessibility permissions NOT granted")
            print("   Please follow the steps above to grant permissions.")
        else:
            raise
except ImportError:
    print("❌ Keyboard library not installed")
    print("   Run: pip install keyboard")
except Exception as e:
    print(f"❌ Error: {e}")
PYEOF

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    Alternative: Run with sudo                ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "If you can't grant permissions, run with sudo:"
echo "  sudo $(pwd)/.venv/bin/python run.py"
echo ""
echo "⚠️  Note: The app works WITHOUT keyboard permissions, but"
echo "   recording/replay features will be disabled."
echo ""
