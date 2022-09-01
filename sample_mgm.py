#!/bin/env amp_python.sif
# amp_python.sif is a python 3.10 runtime that has a ton of useful packages 
# as well as several system packages which are useful:  ffmpeg, sox, 
# ImageMagick, gnuplot, etc.
#
# Most MGMs can use amp_python.sif as the runtime, but if further dependencies
# are required, then the MGM should be packaged as a SIF container.  
#
# The AMP environment (either when run under Galaxy or in the amp_devel.py 
# shell) provides additional utilities:
# * the amp.* modules are in the PYTHONPATH, providing functionality for config
#   and logging
# * AMP_ROOT and AMP_DATA_ROOT are available in the event that other locations
#   within the installation need to be accessed (although you shouldn't need 
#   to) so when setting up logging it can find the right place to put the log.
#
# This MGM is fairly simple:  take an input audio file and convert it to a
# waveform image with the given parameters.
import os
import argparse
import logging
import subprocess
from pathlib import Path
from amp.logging import setup_logging
from amp.config import load_amp_config, get_config_value
import tempfile
import shutil

def main():
    # Set up the script arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", default=False, action="store_true", help="Turn on debugging")
    parser.add_argument("audio_in", help="Input audio file")
    parser.add_argument("image_out", help="Output image file")
    parser.add_argument('--color', type=str, default='#ff0000', help="Color of the waveform data")
    args = parser.parse_args()

    # Set up logging, and do a quick test
    setup_logging("sample_mgm", args.debug)
    logging.debug("A debugging message")
    logging.info("An info message")

    # Verify that the program arguments make sense.    
    # Under galaxy all of the filenames that get passed will have a .dat
    # extension, which confuses most tools.  
    # so let's make sure that audio_in looks like a wav file so we can
    # explictly tell sox that it's a wav file.
    p = subprocess.run(['file', args.audio_in], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", check=True)
    if 'layer III' in p.stdout:
        fmt = 'mp3'
    elif 'WAVE' in p.stdout:
        fmt = 'wav'
    else:
        logging.error(f"Cannot process unknown audio type: {p.stdout}")
        exit(1)

    # color should look like '#xxxxxx'.  We'll just do a little verification here.
    if len(args.color) != 7 or not args.color.startswith('#'):
        logging.error(f"Color should be in the #xxxxxx format: {args.color}")
        exit(1)

    # Load the AMP configuration data
    config = load_amp_config()
    
    # arguments look good, so actually do the work
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            # convert the sound file into raw text data
            rfile = Path(tmpdir, "raw_data.dat")
            logging.info(f"Converting {args.audio_in} as {fmt} to data")
            subprocess.run(['sox', '-t', fmt, args.audio_in, str(rfile)], check=True)
            ffile = Path(tmpdir, "fixed_data.dat")
            with open(rfile) as i:
                # remove the first two lines which are comments
                i.readline()                
                i.readline()
                with open(ffile, "w") as o:
                    for l in i.readlines():
                        o.write(l)

            # create a gnuplot script
            logging.info("Generating gnuplot script")
            # get the watermark label from the amp config.
            label = get_config_value(config, ['mgms', 'sample_mgm', 'watermark'], 'no default set')
            sfile = Path(tmpdir, "gnuplot.script")
            pfile = Path(tmpdir, "audio.png")
            with open(sfile, "w") as s:
                s.write("set term png size 1024,768\n")
                s.write(f'set output "{pfile!s}"\n')
                s.write(f"set style line 1 linecolor rgb '{args.color}'\n")
                s.write(f'set label "{label}" at 0,-1\n')
                s.write(f'plot "{ffile!s}" with lines ls 1 notitle\n')

            # run the gnuplot script to create the image
            logging.info("Plotting data")
            subprocess.run(['gnuplot', str(sfile)], check=True)

            # copy the newly created file to the destination
            logging.info(f"Copying {pfile!s} to {args.image_out}")
            shutil.copyfile(pfile, args.image_out)

    except Exception as e:
        logging.exception(f"Failed to create image: {e}")
        exit(1)

if __name__ == "__main__":
    main()