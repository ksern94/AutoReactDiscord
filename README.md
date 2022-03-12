# AutoDiscord
### Software :computer:

- Python 3.6+
- [pip](https://pip.pypa.io/en/stable/) package installer
- Python [virtual environment](https://virtualenv.pypa.io/en/latest/)
- [chromedriver](https://chromedriver.chromium.org/downloads) based off your OS & Chrome version

### File configuration 

- Rename `config.json.example` to `config.json` and add/update the information accordingly.

## Setup & Run 

This project is tested and developed on Window. You can probably get this up and running on Linux or Mac with some minor tweaks.

1. Change the `chromedriver-binary==99.0.4844.51.0` version in `requirements.txt` according to your chrome version
	- Chrome top right three dot > Help > About Google Chrome, you will find your chrome version there.

2. Run `./setup.sh` 

3. Run `python3 main.py`