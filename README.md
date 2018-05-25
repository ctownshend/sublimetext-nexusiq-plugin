# sublimetext-nexusiq-plugin
Sublimetext-nexusiq-plugin will evaluate a package.json npm file in Sublime text against the Nexus IQ server



## Install
Deploy the entire folder to ~/"Library/Application Support/Sublime Text 3/Packages"
i.e. /Users/[username]/Library/Application Support/Sublime Text 3/Packages/sublimetext-nexusiq-plugin

This will enable the package in Sublime. 

## Usage
1) Make sure that you have a package.json file active
2) Right click on the package.Json file
3) A menu will Appear - "Nexus IQ Evaluation"
4) Select this menu item and wait for the magic to happen


## code
NexusIQEvaluation.py -> python code that runs the app

## Settings
Base File.sublime-settings -> set the url to your Nexus IQ server as well as the user name and password
Context.sublime-menu -> Enabled the context menu
Default (OSX).sublime-keymap -> short cut key
Main.sublime-menu -> targets the menu system
Side Bar.sublime-menu -> left menu settings
Package Control.sublime-settings -> Sublime text use
