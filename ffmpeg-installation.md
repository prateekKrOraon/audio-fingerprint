# FFMPEG Installation

The following instructions are for installing ffmpeg on Amazon Linux based AMI which is probably based on some version of CentOS.

For Debian and Ubuntu distributions, ffmpeg is available as a apt-get package but for other distributions you have to manually compile it.

For CentOS visit [here](https://trac.ffmpeg.org/wiki/CompilationGuide/Centos)

__Step 1:__ Connect to your EC2 instance via SSH or web client and become root

    sudo su -

__Step 2:__ Go to the directory `usr/local/bin`

    cd usr/local/bin

__Step 3:__ Create a directory named `ffmpeg` inside `usr/local/bin` and go inside it.

    mkdir ffmpeg
    cd ffmpeg

__Step 4:__ Download a static release build of ffmpeg from [here](https://johnvansickle.com/ffmpeg/)

    wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz

To check if your system is 32-bit or 64-bit you can execute the following command:

    uname -a

Output will be something like this:

    Linux ip-xxx-xx-xx-xx.ap-south-1.compute.internal 4.14.192-147.314.amzn2.x86_64 #1 SMP Mon Aug 17 06:07:07 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux

__Note:__ The last `i386` indicates that it’s 32-bit and `x86_64` indicates 64-bit.

Also, by hit and trial, I found out that the processor is AMD and not ARM.

__Step 5:__ Unzip the downloaded file

    tar -xf ffmpeg-release-amd64-static.tar.xz

This will create a folder named `ffmpeg-4.3.1-amd64-static`.

Go inside this folder and check if it is installed successfully or not.

    cd ffmpeg-4.3.1-amd64-static
    ./ffmpeg -version

Output will be something like this

    ffmpeg version 4.3.1-static https://johnvansickle.com/ffmpeg/  .
    .
    .
    .
    Hyper fast Audio and Video encoder

__Step 6:__ Copy all the files to the outer directory.

    cp -a /usr/local/bin/ffmpeg/ffmpeg-4.3.1-amd64-static/ . /usr/local/bin/ffmpeg/

__Step 7:__ Create a symlink to use `ffmpeg` and `ffprobe` from any location.

    ln -s /usr/local/bin/ffmpeg/ffmpeg /usr/bin/ffmpeg

    ln -s /usr/local/bin/ffmpeg/ffprobe /usr/bin/ffprobe

__Step 8:__ Finally check if the symlink is created successfully or not. Go to root directory and run following command

    ffmpeg -verion
    ffprobe -version


I found this solution on AWS forums [here](https://forums.aws.amazon.com/thread.jspa?messageID=332091)