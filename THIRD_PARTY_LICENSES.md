# Puppy Timer — Third-Party Licenses

This file records third-party software and assets used by Puppy Timer.

The Puppy Timer source code itself is governed by the custom license in `LICENSE`.
Third-party components listed below are **not** relicensed under the Puppy Timer
license. Their respective copyright and license terms continue to apply.

> License information below was checked against the package/project metadata
> available at the time this file was prepared. When redistributing a package
> itself, retain the original package's license and copyright notices.

## Directly Used Components

### PySide6 / Qt for Python — 6.11.2
- License: LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
- Includes/related packages used by Puppy Timer:
  - PySide6
  - PySide6_Addons
  - PySide6_Essentials
  - shiboken6
- Source: https://pypi.org/project/PySide6/6.11.2/
- Important: PySide6 is copyleft-licensed. If you distribute Puppy Timer as an
  application containing PySide6, review the applicable LGPL/GPL terms and
  Qt deployment requirements for the exact way you distribute it.

### Vosk — 0.3.45
- License: Apache-2.0
- Source: https://pypi.org/project/vosk/0.3.45/
- Copyright/ownership remains with the Vosk/Alpha Cephei project and its
  respective contributors.

### NumPy — 2.5.2
- License expression: BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0
- Source: https://pypi.org/project/numpy/2.5.2/

### sounddevice — 0.5.6
- License: MIT
- Source: https://pypi.org/project/sounddevice/0.5.6/

### Bootstrap Icons
- License: MIT
- Copyright: The Bootstrap Authors
- Source: https://github.com/twbs/icons
- License text: https://github.com/twbs/icons/blob/main/LICENSE

## Packages Present in requirements.txt

The following packages are also pinned in Puppy Timer's `requirements.txt`.
Some are direct dependencies and some may be transitive/runtime
dependencies. They remain under their own licenses.

| Package | Version | License |
|---|---:|---|
| certifi | 2026.7.22 | MPL-2.0 |
| cffi | 2.1.1 | MIT-0 |
| charset-normalizer | 3.5.1 | MIT |
| colorama | 0.4.6 | BSD-3-Clause |
| idna | 3.19 | BSD-3-Clause |
| numpy | 2.5.2 | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 |
| pycparser | 3.0 | BSD-3-Clause |
| PySide6 | 6.11.2 | LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only |
| PySide6_Addons | 6.11.2 | LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only |
| PySide6_Essentials | 6.11.2 | LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only |
| requests | 2.34.2 | Apache-2.0 |
| srt | 3.5.3 | MIT |
| tqdm | 4.70.0 | MPL-2.0 AND MIT |
| urllib3 | 2.7.0 | MIT |
| vosk | 0.3.45 | Apache-2.0 |
| websockets | 17.0.1 | BSD-3-Clause |
| shiboken6 | 6.11.2 | LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only |

## Notes on Dependency Packages

`requirements.txt` contains packages that may have been installed as
dependencies of other packages. Listing them here does not mean that all
of them are directly imported by Puppy Timer.

For packages such as Requests and its dependencies, their own licenses
continue to apply independently.

## Vosk Models

Puppy Timer may also include or reference a Vosk speech-recognition model.
A Vosk model is separate from the `vosk` Python package and may have its
own license and attribution requirements.

Before committing a Vosk model to the repository, check the exact model
directory/archive you are using and preserve the license/README files
distributed with that model.

## Audio / Other Assets

Any sound effects, images, fonts, icons, or other files obtained from
third-party websites are separate copyrighted works. Their individual
licenses must be respected.

For each asset actually included in the repository, keep its source and
license information where practical. Do not assume that an asset has the
same license as the Python packages listed above.

## Important Scope

This document is an attribution and license-information record. It does
not replace the original licenses of third-party software. If the original
package includes a LICENSE, NOTICE, copyright file, or other required
attribution, those materials should be retained when required by that
package's license.
