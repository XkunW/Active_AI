#!/usr/bin/env bash
if (whoami != root)
  then echo "Please run as root"
  exit -1 
fi

apt-get install python3
apt-get install python3-distutils
apt install python3-pip
pip install --upgrade pip
pip install --upgrade setuptools
python3 setup.py install

python3 -m spacy download en_core_web_sm
python3 -c "import nltk; nltk.download('punkt')" 

