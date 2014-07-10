# Jasmine

Sublime package that includes syntax highlighting, snippets and commands for [Jasmine](http://jasmine.github.io) the Javascript BDD framework.

This package is a merge between [Jasmine BDD](https://github.com/caiogondim/jasmine-sublime-snippets) from [@caiogondim](https://github.com/caiogondim) and [Jasmine](https://github.com/gja/sublime-text-2-jasmine) from [@gja](https://github.com/gja).

## Syntax

This is a simple syntax highlighter, it recognizes `(x)describe` and `(x)it`. Take into account that any other packages that are using `javascript` as a syntax may not work with `jasmine`, you can always turn it back off by opening a `.spec.js` file and selecting "View > Syntax > Open all with current extension as... > Javascript".

With this package, the editor will recognize `.spec.js` files as having Jasmine syntax.

## Installation

### Manual

You can clone the repo in your `/Packages` (*Preferences -> Browse Packages...*) folder and start using/hacking it.
    
    cd ~/path/to/Packages
    git clone https://github.com/NicoSantangelo/jasmine-syntax.git JasmineSyntax


After installing the plugin, you will be able to use it by going to View -> Syntax -> Jasmine.
Once selected, you will see the Jasmine label on the bottom right corner.