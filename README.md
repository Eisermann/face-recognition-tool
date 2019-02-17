#Virtual Assistant 1.0

##Install
###1. Install OS dependencies (Mac OS)
```bash
brew cask install xquartz
brew install gtk+3 boost
brew install boost-python --with-python3
brew install cmake
brew install opencv@4 --with-contrib
```

###2. Create virtualenv for Python 3.7.0
```bash
pyenv virtualenv 3.7.0 computer-vision
```

###3. Install project
```bash
make install
```

##Run
```bash
make run
```
