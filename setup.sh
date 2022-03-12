#!/usr/bin/env bash

# font color
green=$(tput setaf 2)
white=$(tput sgr0)

# functions
setup_virtualenv() {
    echo "🛠 $white Removing existing venv-auto-discord"
    rm -rf venv-auto-discord
    virtualenv venv-auto-discord
    echo "🔧 $white Activating virtual environment"
    source venv-auto-discord/bin/activate
}

pip_install() {
    echo "🐍 $white Installing Python dependencies with pip"
    pip3 install -r requirements.txt
    ln -s /usr/lib/python3/dist-packages/gi venv-auto-discord/lib/python3.8/site-packages/
    echo "$green✔$white Completed pip install"
}

echo_finish() {
    echo "$green✔$white$1 Finished setup"
}

main() {
    setup_virtualenv
    pip_install
    echo_finish
}

main
