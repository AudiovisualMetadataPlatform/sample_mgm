# Sample MGM
This is a sample MGM repository that can be used as the
basis for your own MGM development

The repo consists of a few files:
* amp_build.py -- used to build the software and install it or create a package
* sample_mgm.py -- this is the MGM code itself
* sample_mgm.xml -- this is the interface between the MGM and Galaxy
* sample_mgm.amp -- this provides additional metadata to AMP.  It's a YAML file, despite the extension
* sample_mgm.default -- this is the default configuration values
* pre_script.py -- this script will be run prior to installing
* post_script.py -- this script will be run after installing
* config_script.py -- this script will be run during configuration

## Hook scripts
The *_script.py files are used as hooks during the installation and configuration phases.

They're not required but do provide an opportunity for the package to do interesting
things during those phases.
