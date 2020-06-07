#!/bin/bash

if (( $EUID != 0 )); then
    echo "Please run as root"
    exit
fi

echo "Installing dependencies..."
pip3 install -r requirements.txt

# Remove old marker files
echo "Removing old files"
rm -rf /usr/local/marker
rm -rf /usr/local/bin/automark
rm -rf /usr/local/bin/prepare
rm -rf /usr/local/bin/lms-download
rm -rf /usr/local/bin/lms-upload-marks
rm -rf /usr/local/bin/lms-upload-reports
rm -rf /usr/local/bin/lms-set-status

# Copy over all the files
echo "Copying over new files to /usr/local/marker"
mkdir /usr/local/marker
chmod -R +x *
cp -r * /usr/local/marker/

# Link the core files to /usr/local/bin
echo "Adding executables to /usr/local/bin"
ln -s /usr/local/marker/automark /usr/local/bin/automark
ln -s /usr/local/marker/prepare /usr/local/bin/prepare
ln -s /usr/local/marker/lms-download /usr/local/bin/lms-download
ln -s /usr/local/marker/lms-upload-marks /usr/local/bin/lms-upload-marks
ln -s /usr/local/marker/lms-upload-reports /usr/local/bin/lms-upload-reports
ln -s /usr/local/marker/lms-set-status /usr/local/bin/lms-set-status

echo "Done."