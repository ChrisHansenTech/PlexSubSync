import os, sys
# Prepend src directory to sys.path for imports in tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))