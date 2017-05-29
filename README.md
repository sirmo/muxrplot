# muxrplot
Logging and plotting the voltnut way

![Example Capture](http://i.imgur.com/4WDruSV.png)

This is the example output of `mplot`. Data was captured with `mplotlogger`. Both scripts are part of this project. The device polled was Keithley 2015 via USB Serial rs232. But you should be able to make it work with any device with minor tweaks.

# Clone the repo
```bash
git clone git@github.com:sirmo/muxrplot.git
cd muxrplot
```
# Setup a virtualenv (optional)
Virtualenv lets you install all the prerequisites for this program in the repo directory itself. This way you don't have to modify anything on your system. To initialize `virtualenv`, do the following:

```bash
virtualenv env
source env/bin/activate
```
By the way you will have to run the activate command every time you want to run `mplot` with a new session. Once activated you will usually see a `(env)` in your prompt.

# Install

To install `mplot` on your system:

```bash
make install
```

Once installed you can run.
```bash
> mplotlogger -h
usage: mplotlogger [-h] [-d DEVICE] [-i INTERVAL] [outfile]

positional arguments:
  outfile

optional arguments:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE
                        Path to the serial device
  -i INTERVAL, --interval INTERVAL
                        Polling interval
```

and:

```bash
> mplot -h
mplot
usage: mplot [-h] [-t TITLE] [-y YDIGITS] [infile] [outfile]

positional arguments:
  infile
  outfile

optional arguments:
  -h, --help            show this help message and exit
  -t TITLE, --title TITLE
                        title to be used in the chart
```

# Example Usage

Suppose you have a Keithley 2000, 2001 or similar connected to /dev/cu.usbserial

```bash
> mplotlogger -d /dev/cu.usbserial target/my_first_capture
logging to: target/my_first_capture
|
```
If you check directory `target` (provided you've made one) and file `my_first_capture` you should see a comma delimited file which contains the captured data.

```csv
> head target/my_first_capture
timestamp;value
1496033039.2;9.9999562
1496033040.2;9.99995613
1496033041.2;9.99997087
1496033042.21;9.99996245
1496033043.21;9.9999628
1496033044.21;9.99996742
1496033045.21;9.99997018
1496033046.22;9.99995482
1496033047.22;9.99996508
```

To plot this data you invoke the `mplot`:

```bash
> mplot target/my_first_capture
mplot
target/my_first_capture (29-May-2017)
max: 9.99997749
min: 9.99994525
p-p: 0.00003224
o: 6.782e-06
samples: 137
duration: 0d 00:02.16
mean: 9.99995736
```
The end result, will be a `.png` file `target/my_first_capture.png`:
![Example Capture](http://i.imgur.com/lLkGS6A.png)

## Install issues
If you run into install issues during `make install` try using pip separately, and make sure `numpy` and `scipy` are installed properly. For some reason these two seem to give me most problems.

```bash
pip install scipy
pip install numpy
```
