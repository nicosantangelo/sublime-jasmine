# Jasmine

Sublime Text package that includes syntax highlighting, snippets and commands for [Jasmine](http://jasmine.github.io) the Javascript BDD framework.

This package is a merge between [Jasmine BDD](https://github.com/caiogondim/jasmine-sublime-snippets) from [@caiogondim](https://github.com/caiogondim) and [Jasmine](https://github.com/gja/sublime-text-2-jasmine) from [@gja](https://github.com/gja).

## Snippets

Below is a list of all snippets currently supported on this package and the triggers of each one. The **⇥** means the `TAB` key.

### Specs
- `describe`: desc⇥
- `xdescribe`: xdesc⇥
- `it`: it⇥
- `xit`: xit⇥
- `afterEach`: ae⇥
- `beforeEach`: be⇥

### Expectations
- `expect`: exp⇥
- `expect().toBe`: tb⇥
- `expect().toBeCloseTo`: tbct⇥
- `expect().toBeDefined`: tbd⇥
- `expect().toBeFalsy`: tbf⇥
- `expect().toBeGreaterThan`: tbgt⇥
- `expect().toBeLessThan`: tblt⇥
- `expect().toBeNull`: tbn⇥
- `expect().toBeTruthy`: tbt⇥
- `expect().toBeUndefined`: tbu⇥
- `expect().toContain`: tc⇥
- `expect().toEqual`: te⇥
- `expect().toHaveBeenCalled`: thbc⇥
- `expect().toHaveBeenCalledWith`: thbcw⇥
- `expect().toMatch`: tm⇥
- `expect().toThrow`: tt⇥
- `expect().not.toBe`: nb⇥
- `expect().not.toBeCloseTo`: nct⇥
- `expect().not.toBeDefined`: nd⇥
- `expect().not.toBeFalsy`: nf⇥
- `expect().not.toBeGreaterThan`: ngt⇥
- `expect().not.toBeLessThan`: nlt⇥
- `expect().not.toBeNull`: nn⇥
- `expect().not.toBeTruthy`: nt⇥
- `expect().not.toBeUndefined`: nu⇥
- `expect().not.toContain`: nc⇥
- `expect().not.toEqual`: ne⇥
- `expect().not.toMatch`: nm⇥
- `expect().not.toThrow`: nt⇥
- `jasmine.any`: a⇥
- `jasmine.objectContaining`: oc⇥

### Spies
- `spyOn`: s⇥
- `spyOn.and.callThrough`: sct⇥
- `spyOn.and.returnValue`: srv⇥
- `spyOn.and.stub`: ss⇥
- `spyOn.and.throwError`: se⇥
- `spy.calls.all`: ca⇥
- `spy.calls.allArgs`: caa⇥
- `spy.calls.any`: ca⇥
- `spy.calls.argsFor`: caf⇥
- `spy.calls.count`: cc⇥
- `spy.calls.first`: cf⇥
- `spy.calls.mostRecent`: cmr⇥
- `spy.calls.reset`: cr⇥
- `createSpy`: cs⇥
- `createSpyObj`: cso⇥


## Commands

### Switch between code and spec

This command will open the spec or source file that has the same path of the active view file.
If you're looking at a source file and the package can't find any specs, it'll display a list of possible directories to create a new one.

To run this command, you can use `ctrl+.`/`super+.` or `ctrl+shift+.`/`super+shift+.`, this last one will open a split view. Also you can select `Jasmine: Switch between code and spec` from the command palette.

### Create spec file

This command is exactly the same as running `Jasmine: Switch between code and spec` and not finding specs.

It doesn't have a key binding, but you can use `jasmine_create_spec` as a command name, like this:

`{ "keys": ["KEYS"], "command": "jasmine_create_spec", "args": { "split_view": false } }`

### (legacy) Switch between code and spec

Runs the command from [@gja](https://github.com/gja) package, found in [run_jasmine.py](https://github.com/gja/sublime-text-2-jasmine/blob/master/run_jasmine.py).

If you want to setup a keybinding for it, you can use:

`{ "keys": ["KEYS"], "command": "legacy_jasmine_switch" }`

### Toggle quotes

This command will change the snippets from the current active quotes to it's counterpart.

For example, it will transform this:

````
describe("Name of the group", function() {
    
});
````

to this

````
describe('Name of the group', function() {
    
});
````

If you want to setup a keybinding for it, you can use:

`{ "keys": ["KEYS"], "command": "jasmine_toggle_quotes" }`

**Important!**

After each toggle you may need to restart Sublime to the changes to take effect.

### Command Settings

There are two possible settings:
```javascript
{
    // Ignore directories when searching for files (source and specs)
    "ignored_directories": [".git", "vendor", "tmp", "node_modules"],

    // The parent folder name for the spec files
    "jasmine_path": "spec",

    // Extension used when creating a new spec file. 
    "spec_file_extension": ".spec.js"
}
```

**Remember** that this settings only apply to the new command (they won't affect `(legacy) Switch between code and spec`).

## Syntax

With this package, the editor will recognize `.spec.js` files as having Jasmine syntax. It will highlight `(x)describe` and `(x)it`.

Take into account that any other packages that are using `javascript` as a syntax may not work with `jasmine`, you can always turn it back off by opening a `.spec.js` file and selecting "View > Syntax > Open all with current extension as... > Javascript".

## Installation

### PackageControl

If you have [PackageControl](http://wbond.net/sublime_packages/package_control) installed, you can use it to install the package.

Just type `cmd-shift-p`/`ctrl-shift-p` to bring up the command pallete and pick `Package Control: Install Package` from the dropdown, search and select the package there and you're all set.

### Manual

You can clone the repo in your `/Packages` (*Preferences -> Browse Packages...*) folder and start using/hacking it.
    
    cd ~/path/to/Packages
    git clone https://github.com/NicoSantangelo/sublime-jasmine.git Jasmine
