# RequireJS-Module-Manager
Sublime Text plugin for adding, removing, and organizing AMD requirements in a JavaScript file using RequireJS and Escope.

This plugin removes the hassle from developing AMD modules with long and changing dependency lists.
It knows where to find your project's existing modules and allows you to add, modify or remove them as dependencies from a module easily.
It also keeps your modules' dependencies organized and formatted according to your own preferences.

**Warning! Not ready for primetime yet.**

## Settings

For all settings that can be set either at the plugin level or the individual project level, please consult the sublime-settings file.
All settings are optional, but the most important are listed here with additional information.

- `node_command`

  The executable the plugin will use to issue commands to Node.JS. If node is seen by Sublime Text's PATH, the plugin will use it. If not, specify your own location to use.

- `requirejs_config`

  You will typically always want to specify this setting in an individual project's settings file.
  Can be either a RequireJS config object in JSON format that includes at minimum `"baseUrl"`, or a path to a js file relative to the first folder in the project, containing a `requirejs.config`.

- `dependency_template`

  When altering dependencies in your file, the plugin will infer your formatting preferences from existing code.
  If, however, no module definition or require call are available to infer formatting from, the plugin will wrap the existing file contents in a module definition.
  Use this setting to specify your own formatting preferences (whitespace, newlines, tabs, etc.) for the newly-created dependency module id array and module function.

## Commands

**The plugin's commands must be run in a JS file inside a Sublime Text project with an existing top-level folder.**

When a command is invoked, the plugin finds the current dependencies of the nearest-most `require` or `define` function scope.

Take this module definition for example:

```javascript
define(['foo', './bar'], function(foo) {
  // outer dependencies function scope
  
  require(['/baz'], function(baz) {
    // inner dependencies function scope
  });
  
});
```

If a command is invoked while the cursor is inside the outer function scope or the parameters of the `define` call, the command will operate on the dependency list including `'foo'` and `'./bar'`.
If inside the inner function scope or the parameters of the `require` call, the command will operate on the dependency list including `'/baz'`.

### Add or Modify Dependency

When invoked without a selection, the command will parse your project's RequireJS config and present a list of modules on your filesystem following the config's `baseUrl` and `paths` properties.
Additionally, you can manually input a module ID or path.

If the selection or input matches a module ID or path string in the module dependencies array, the command will modify the function parameter name mapped to that module.

If the selection or input doesn't match any existing module ID or path, you will be prompted to input a name to be mapped to the module ID or path as a parameter in the define/require function definition and the new dependency will be added.

In the example from above:
```javascript
define(['foo', './bar'], function(foo) {
  ...
```

Running the command and then selecting or inputting the `'foo'` mudule ID, or running the command with `'foo'` (the module ID) selected will prompt you to modify the function parameter named `foo`.
It is perfectly okay to modify the parameter to be an empty string. This will alter the dependency to be unnamed in the function block just like `'./bar'` is in the example.

Running the command with `foo` (the function parameter) selected will prompt you to modify the module ID or path set to `'foo'` via the list of all your project's modules, or manual input.

### Remove Dependency

When invoked without a selection, the command will parse the dependencies of the nearest-most `require` or `define` function scope and present their module IDs or paths to you in a list.
Selecting a module from that list will remove the module—both the ID or path from the dependency array, and its matched function parameter from the define/require function definition.

Running the command with a module ID or path in a dependency array selected will automatically remove that dependency along with its matched function parameter from the define/require function definition.

Running the command with a parameter from the define/require function definition selected will automatically remove that parameter along with its matched module ID or path from the dependency array.
