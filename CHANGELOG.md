  * 0.0.1 (2020-05-01): A basic tray application using App Indicator  
  Basic application that reads the grub config and displays items in the menu.  
  Added ability to reboot into a specific OS, but top level only.  
  
  * 0.0.2 (2020-05-23): Ability to reboot into sub menu items  
  Ability to reboot into the submenus of OSes. For example different kernels.

  * 0.0.6 (2020-06-06): Shutdown option
  Added menu item for shutdown, as a convenience function.

  * 0.0.7 (2022-08-22): Build for Ubuntu 22.04
  Rebuilt package for Ubuntu 22.04 Jammy Jellyfish

  * 0.0.8 (2023-07-22): Build for Ubuntu 23.04
  Rebuilt package for Ubuntu 23.04 Lunar Lobster

  * 0.0.9 (2024-08-03): Parsing and menu hover bugfix
  Bugfix, some menu items weren't parsed correctly.
  Bugfix, menu items weren't nesting correctly.
  Bugfix, menu items were being activated on hover.
  Rebuilt package for Ubuntu 24.04 Noble Numbat.

  * 0.0.10 (2025-08-02): Support for molly-guard
  Support for molly-guard by timur-tabi.
  Will use the .no-molly-guard version of reboot command if exists.