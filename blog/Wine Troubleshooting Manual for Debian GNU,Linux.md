# Wine Troubleshooting Manual for Debian GNU/Linux

## Front Matter

**Document Title:** Wine Troubleshooting Manual for Debian GNU/Linux  
**Document Version:** 1.0  
**Date:** December 6, 2025  
**Author:** AI Documentation Specialist  
**Organization:** Software Engineering Team  
**Purpose:** This manual provides step-by-step guidance for resolving common Wine configuration issues on Debian GNU/Linux systems, enabling successful execution of Windows applications in a Linux environment.  
**Target Audience:** System administrators, developers, and users running Windows applications on headless Debian servers.  
**Prerequisites:** Basic Linux command-line knowledge, root or sudo access.  
**Related Documents:** WineHQ Documentation, Debian Package Management Guide.  
**Conformance:** This document adheres to ISO/IEC/IEEE 26514:2008 standards for system and software user documentation, ensuring clarity, completeness, and accessibility.

## Table of Contents

1. [Introduction](#introduction)
2. [Concept of Operations](#concept-of-operations)
3. [Procedures](#procedures)
   1. [Diagnosing Wine Issues](#diagnosing-wine-issues)
   2. [Installing Wine and Dependencies](#installing-wine-and-dependencies)
   3. [Setting Up Headless Operation](#setting-up-headless-operation)
   4. [Installing Git Inside Wine](#installing-git-inside-wine)
   5. [Configuring Environment Variables](#configuring-environment-variables)
   6. [Running Applications](#running-applications)
4. [Troubleshooting](#troubleshooting)
5. [Information for Uninstallation](#information-for-uninstallation)
6. [Glossary](#glossary)
7. [Index](#index)

## Introduction

### Purpose and Scope

This manual guides users through diagnosing and resolving Wine configuration issues on Debian GNU/Linux systems. Wine allows running Windows applications on Linux, but common problems include missing components, display server conflicts, and dependency issues. The scope covers headless server environments where GUI access is unavailable.

### Audience

- **Primary:** System administrators maintaining Linux servers
- **Secondary:** Developers deploying Windows applications in Linux environments
- **Assumed Knowledge:** Basic Linux commands, package management with apt

### Conventions Used

- **Commands:** `wine --version`
- **File Paths:** `/home/user/application.exe`
- **Warnings:** ⚠️ Indicates potential security or stability concerns
- **Notes:** ℹ️ Provides additional context or alternatives

### Related Documents

- WineHQ Official Documentation: https://wiki.winehq.org/
- Debian Wine Packages: https://packages.debian.org/wine

## Concept of Operations

### Overview

Wine translates Windows API calls to POSIX calls, enabling Windows applications to run on Linux. In headless environments, applications requiring GUI components need virtual displays. This manual addresses three primary issues:

1. **Missing Wine Components:** Incomplete 32-bit or 64-bit Wine installations
2. **Display Server Requirements:** Lack of X server in headless setups
3. **Application Dependencies:** Missing Windows components like Git for Python applications

### Operational Context

- **Environment:** Debian GNU/Linux (sid/unstable) on headless servers
- **Use Cases:** Running analysis tools, legacy Windows applications
- **Constraints:** No GUI access, root user considerations
- **Dependencies:** Internet access for package downloads, adequate disk space

### User Characteristics

- **Experience Level:** Intermediate to advanced Linux users
- **Tasks Performed:** System configuration, application deployment
- **Goals:** Successful application execution, minimal downtime

## Procedures

### Diagnosing Wine Issues

**Purpose:** Identify specific Wine configuration problems before applying fixes.

1. Check Wine version and status:
   ```
   wine --version
   ```
   Expected output: Wine version number or error messages.

2. Attempt to run a test application:
   ```
   wine notepad.exe
   ```
   Common errors:
   - "wine32 is missing" - Indicates incomplete installation
   - "nodrv_CreateWindow" - Display server issues
   - "Bad git executable" - Missing Git in Wine environment

3. Verify system architecture:
   ```
   dpkg --print-architecture
   uname -m
   ```
   Ensure 32-bit architecture is enabled if needed.

### Installing Wine and Dependencies

**Purpose:** Install Wine with proper architecture support for Debian systems.

⚠️ **Warning:** Running Wine as root is not recommended for security reasons. Consider creating a dedicated user account.

1. Enable 32-bit architecture:
   ```
   dpkg --add-architecture i386
   apt update
   ```

2. Install Wine packages:
   ```
   apt install -y wine64
   ```
   Note: wine32 may have dependency conflicts in Debian sid; wine64 suffices for most applications.

3. Verify installation:
   ```
   wine --version
   ```
   Expected: Version output without errors.

### Setting Up Headless Operation

**Purpose:** Configure virtual display for GUI applications in headless environments.

1. Install Xvfb (X Virtual Framebuffer):
   ```
   apt install -y xvfb
   ```

2. Test virtual display:
   ```
   xvfb-run -a xterm -e "echo 'Display test successful'"
   ```

3. Use xvfb-run for Wine applications:
   ```
   xvfb-run -a wine application.exe
   ```

### Installing Git Inside Wine

**Purpose:** Provide Git executable for applications using GitPython or similar libraries.

1. Download portable Git for Windows:
   ```
   wget https://github.com/git-for-windows/git/releases/download/v2.45.2.windows.1/PortableGit-2.45.2-64-bit.7z.exe -O git-portable.exe
   ```

2. Extract the archive:
   ```
   7z x git-portable.exe -o/tmp/git-extract
   ```

3. Install to Wine prefix:
   ```
   mkdir -p ~/.wine/drive_c/Program\ Files/Git
   cp -r /tmp/git-extract/* ~/.wine/drive_c/Program\ Files/Git/
   ```

4. Test Git installation:
   ```
   xvfb-run -a wine "C:\Program Files\Git\cmd\git.exe" --version
   ```
   Expected: Git version output.

5. Clean up temporary files:
   ```
   rm git-portable.exe
   rm -rf /tmp/git-extract
   ```

### Configuring Environment Variables

**Purpose:** Set environment variables for applications requiring specific paths.

1. Set Git executable path:
   ```
   export GIT_PYTHON_GIT_EXECUTABLE="C:\\Program Files\\Git\\cmd\\git.exe"
   ```

2. Make persistent (add to ~/.bashrc):
   ```
   echo 'export GIT_PYTHON_GIT_EXECUTABLE="C:\\Program Files\\Git\\cmd\\git.exe"' >> ~/.bashrc
   ```

3. Verify environment:
   ```
   echo $GIT_PYTHON_GIT_EXECUTABLE
   ```

### Running Applications

**Purpose:** Execute Windows applications successfully in the configured environment.

1. Navigate to application directory:
   ```
   cd /path/to/application
   ```

2. Run with proper environment:
   ```
   export GIT_PYTHON_GIT_EXECUTABLE="C:\\Program Files\\Git\\cmd\\git.exe"
   xvfb-run -a wine application.exe [arguments]
   ```

3. Example for analysis tool:
   ```
   cd /home/example
   export GIT_PYTHON_GIT_EXECUTABLE="C:\\Program Files\\Git\\cmd\\git.exe"
   xvfb-run -a wine /home/example/ExampleApp.exe analyze --help
   ```

4. Monitor execution:
   - Check for error messages
   - Verify output files
   - Confirm successful completion

## Troubleshooting

### Common Issues and Solutions

| Issue | Symptom | Solution |
|-------|---------|----------|
| Wine32 missing | "it looks like wine32 is missing" | Use wine64; install manually if needed |
| Display errors | "nodrv_CreateWindow" | Use xvfb-run for headless operation |
| Git not found | "Bad git executable" | Install Git inside Wine prefix |
| Permission errors | Access denied | Run as appropriate user or adjust permissions |
| Package conflicts | Dependency resolution failed | Use --fix-broken or manual installation |

### Advanced Diagnostics

1. Check Wine configuration:
   ```
   winecfg
   ```
   (Requires display or xvfb)

2. Examine Wine logs:
   ```
   WINEDEBUG=+all xvfb-run -a wine application.exe 2>&1 | head -50
   ```

3. Verify Wine prefix integrity:
   ```
   ls -la ~/.wine/drive_c/
   ```

### Getting Help

- WineHQ Forums: https://forum.winehq.org/
- Debian Wine Bugs: https://bugs.debian.org/wine
- Community Support: IRC #winehq on libera.chat

## Information for Uninstallation

### Removing Wine Components

**Purpose:** Completely remove Wine and associated components when no longer needed.

⚠️ **Warning:** This will remove all Wine applications and configurations.

1. Remove Wine packages:
   ```
   apt remove --purge wine wine64 wine32
   ```

2. Remove Wine prefix:
   ```
   rm -rf ~/.wine
   ```

3. Remove associated packages:
   ```
   apt autoremove
   apt autoclean
   ```

4. Remove 32-bit architecture (if no longer needed):
   ```
   dpkg --remove-architecture i386
   apt update
   ```

### Data Preservation

- Backup Wine prefix before removal: `cp -r ~/.wine ~/.wine-backup`
- Export registry settings if needed: `wine regedit /E wine_settings.reg`

## Glossary

- **Headless:** System without graphical display
- **Wine Prefix:** Isolated Windows environment within Wine
- **Xvfb:** X Virtual Framebuffer for headless GUI applications
- **Portable Application:** Self-contained software not requiring installation
- **GitPython:** Python library for Git operations

## Index

A
- Applications, running: 6.1
- Architecture, enabling: 4.2

D
- Dependencies, installing: 4
- Diagnostics, advanced: 7.2
- Display server: 5

E
- Environment variables: 6
- Errors, common: 7.1

G
- Git installation: 5.4
- GUI applications, headless: 5

H
- Headless operation: 5

I
- Installation, Wine: 4

P
- Portable Git: 5.4
- Procedures: 4-6

R
- Running applications: 6.1

T
- Troubleshooting: 7

U
- Uninstallation: 8

V
- Virtual display: 5

W
- Wine configuration: 7.2
- Wine prefix: 5.4
