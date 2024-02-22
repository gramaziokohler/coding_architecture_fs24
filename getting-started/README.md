# Getting Started

## Software requirements

Before you begin the installation of the tools required for this course, make sure you have the following pre-requisites installed on your system:

* Rhino 7: https://www.rhino3d.com/download
* VS Code (free): https://code.visualstudio.com/
* GIT (free): https://git-scm.com/

> NOTE: On Mac, GIT is usually pre-installed, you do not need to install again. To check if it is installed, open a terminal window and type `git`, if the result does not indicate any error, it means you already have it in your system.

Once that is done, follow the step-by-step instructions below.

## Installation guide

**Windows Users**

* Download the installer: https://dfab.link/ca-fs24/installer.zip
* Extract it! (**DO NOT RUN THE NEXT STEP FROM WITHIN THE ZIP FILE**)
* Run the installer by double-clicking the file `win_install.cmd`

**Mac Users**

On Mac, it's not necessary to download the installer. Instead, open the **Terminal** application of your mac, copy & paste the following command, and press Enter:
```bash
  curl -s https://dfab.link/ca-fs24/mac_install.bash | bash
```

**Troubleshooting**

If the installer fails:

* Some antivirus software might interfere with the download process. In case of errors during instal, try to disable your antivirus momentarily, and run the installer again.
* For a clean retry, delete the folder `Miniconda` (or `Miniconda3`) from your user profile, and try again.
* On Windows, make sure you extract/unzip the installer first, and then run it. If you run the installer directly from within the zip file, it will fail. 
