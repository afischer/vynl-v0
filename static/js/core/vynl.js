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
 * @version 1.0
 */

// / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / 
// Namespace

 (function() { vynl = { version: "1.0" }; })();

 // / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
 // Core
  
  

/*
 * Debug mode configuration object.
 */


/*
 * Logging
 */
 vynl.logger = function() {
    console.warn("LOGGER");
    var printMsg = function(logger, prefix, messages) {
         logger.apply(console, args);
     };
    
     return {
       "generate" : function(level, args) {
          printMsg(logger, forLevel.toUpperCase(), arguments);
       }
    }
 }();