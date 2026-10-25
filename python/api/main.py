"""Compatibility entry point for the supported local CPU workbench."""
from neurosim.workbench.api import app, serve

if __name__ == "__main__":
    serve()
