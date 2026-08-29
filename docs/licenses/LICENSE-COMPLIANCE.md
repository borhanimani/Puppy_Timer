# License Compliance Notes

This document explains how Puppy Timer uses third-party software,
models, and external assets.

The purpose of this document is to help maintain proper license
compliance during development and distribution.


---

# Project License

The original source code written specifically for Puppy Timer is licensed
under the project license located in the repository root:

LICENSE


This license applies only to original Puppy Timer code.

It does not replace or override third-party licenses.


---

# Third-Party Dependencies

Puppy Timer uses several external dependencies.

Examples:

- PySide6
- Shiboken6
- Vosk
- SoundDevice
- NumPy
- Requests
- PyInstaller


Each dependency remains under its original license.

A complete list is available in:

docs/licenses/THIRD-PARTY-LICENSES.md


---

# External Assets

Puppy Timer may include external assets such as:

- Audio files
- Icons
- Images
- Other creative resources


These assets remain under their original licenses.

A complete list is available in:

docs/licenses/ASSET-LICENSES.md


---

# Source Repository

Some files are intentionally excluded from the public repository.

Examples may include:

- Large speech recognition models
- Optional audio resources
- Local development files


These files can be replaced by users with their own compatible files.

Users are responsible for ensuring that replacement resources comply
with their own licenses.


---

# Vosk Models

Puppy Timer uses Vosk for offline speech recognition.

The speech recognition model is a separate resource from the Vosk
software package.

Models may have their own licensing terms.

Users should verify the license of any model they choose to use.


---

# Application Builds

When creating executable builds:

- Third-party license requirements must still be respected.
- Required notices should remain available.
- External components should not be presented as original Puppy Timer code.


---

# Modification Policy

The Puppy Timer source license controls the use of original project code.

Third-party components may have different permissions and restrictions.

Always check the original license of each component before reuse.


---

# Summary

Puppy Timer combines:

- Original project code
- Open-source libraries
- External assets
- Optional external models


Each part keeps its own ownership and licensing rules.

For detailed information, see:

- LICENSE
- THIRD-PARTY-LICENSES.md
- ASSET-LICENSES.md
