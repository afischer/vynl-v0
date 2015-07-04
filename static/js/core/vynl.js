/**
 * Vynl Javascript
 * @version 0.1
 */

/**
 * SumAll Javascript
 *
 * This module contains globally required Vynl functionality.
 *
 * @author AndrewFischer
 *
 * @version 1.0
 */

// / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / 
// Namespace

 (function() { Vynl = { version: "1.0" }; })();

 // / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
 // Core
  
  
/*
 * Logging
 */
Vynl.log   = console.log();
Vynl.info  = console.info();
Vynl.warn  = console.warn();
Vynl.error = "";


/*
 * Debug mode configuration object.
 */
Vynl.debug = function() {
    return {
        "on"   : function(ft) {
        },
        "off"   : function(ft) {
        },
        "isOn"  : function(ft) {
        }
    };
}();
