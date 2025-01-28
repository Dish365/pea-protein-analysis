"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
exports.id = "vendor-chunks/simple-swizzle@0.2.2";
exports.ids = ["vendor-chunks/simple-swizzle@0.2.2"];
exports.modules = {

/***/ "(ssr)/../node_modules/.pnpm/simple-swizzle@0.2.2/node_modules/simple-swizzle/index.js":
/*!***************************************************************************************!*\
  !*** ../node_modules/.pnpm/simple-swizzle@0.2.2/node_modules/simple-swizzle/index.js ***!
  \***************************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

eval("\nvar isArrayish = __webpack_require__(/*! is-arrayish */ \"(ssr)/../node_modules/.pnpm/is-arrayish@0.3.2/node_modules/is-arrayish/index.js\");\nvar concat = Array.prototype.concat;\nvar slice = Array.prototype.slice;\nvar swizzle = module.exports = function swizzle(args) {\n    var results = [];\n    for(var i = 0, len = args.length; i < len; i++){\n        var arg = args[i];\n        if (isArrayish(arg)) {\n            // http://jsperf.com/javascript-array-concat-vs-push/98\n            results = concat.call(results, slice.call(arg));\n        } else {\n            results.push(arg);\n        }\n    }\n    return results;\n};\nswizzle.wrap = function(fn) {\n    return function() {\n        return fn(swizzle(arguments));\n    };\n};\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHNzcikvLi4vbm9kZV9tb2R1bGVzLy5wbnBtL3NpbXBsZS1zd2l6emxlQDAuMi4yL25vZGVfbW9kdWxlcy9zaW1wbGUtc3dpenpsZS9pbmRleC5qcyIsIm1hcHBpbmdzIjoiQUFBQTtBQUVBLElBQUlBLGFBQWFDLG1CQUFPQSxDQUFDO0FBRXpCLElBQUlDLFNBQVNDLE1BQU1DLFNBQVMsQ0FBQ0YsTUFBTTtBQUNuQyxJQUFJRyxRQUFRRixNQUFNQyxTQUFTLENBQUNDLEtBQUs7QUFFakMsSUFBSUMsVUFBVUMsT0FBT0MsT0FBTyxHQUFHLFNBQVNGLFFBQVFHLElBQUk7SUFDbkQsSUFBSUMsVUFBVSxFQUFFO0lBRWhCLElBQUssSUFBSUMsSUFBSSxHQUFHQyxNQUFNSCxLQUFLSSxNQUFNLEVBQUVGLElBQUlDLEtBQUtELElBQUs7UUFDaEQsSUFBSUcsTUFBTUwsSUFBSSxDQUFDRSxFQUFFO1FBRWpCLElBQUlYLFdBQVdjLE1BQU07WUFDcEIsdURBQXVEO1lBQ3ZESixVQUFVUixPQUFPYSxJQUFJLENBQUNMLFNBQVNMLE1BQU1VLElBQUksQ0FBQ0Q7UUFDM0MsT0FBTztZQUNOSixRQUFRTSxJQUFJLENBQUNGO1FBQ2Q7SUFDRDtJQUVBLE9BQU9KO0FBQ1I7QUFFQUosUUFBUVcsSUFBSSxHQUFHLFNBQVVDLEVBQUU7SUFDMUIsT0FBTztRQUNOLE9BQU9BLEdBQUdaLFFBQVFhO0lBQ25CO0FBQ0QiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9wcm9jZXNzLWFuYWx5c2lzLWZyb250ZW5kLy4uL25vZGVfbW9kdWxlcy8ucG5wbS9zaW1wbGUtc3dpenpsZUAwLjIuMi9ub2RlX21vZHVsZXMvc2ltcGxlLXN3aXp6bGUvaW5kZXguanM/OTI2MCJdLCJzb3VyY2VzQ29udGVudCI6WyIndXNlIHN0cmljdCc7XG5cbnZhciBpc0FycmF5aXNoID0gcmVxdWlyZSgnaXMtYXJyYXlpc2gnKTtcblxudmFyIGNvbmNhdCA9IEFycmF5LnByb3RvdHlwZS5jb25jYXQ7XG52YXIgc2xpY2UgPSBBcnJheS5wcm90b3R5cGUuc2xpY2U7XG5cbnZhciBzd2l6emxlID0gbW9kdWxlLmV4cG9ydHMgPSBmdW5jdGlvbiBzd2l6emxlKGFyZ3MpIHtcblx0dmFyIHJlc3VsdHMgPSBbXTtcblxuXHRmb3IgKHZhciBpID0gMCwgbGVuID0gYXJncy5sZW5ndGg7IGkgPCBsZW47IGkrKykge1xuXHRcdHZhciBhcmcgPSBhcmdzW2ldO1xuXG5cdFx0aWYgKGlzQXJyYXlpc2goYXJnKSkge1xuXHRcdFx0Ly8gaHR0cDovL2pzcGVyZi5jb20vamF2YXNjcmlwdC1hcnJheS1jb25jYXQtdnMtcHVzaC85OFxuXHRcdFx0cmVzdWx0cyA9IGNvbmNhdC5jYWxsKHJlc3VsdHMsIHNsaWNlLmNhbGwoYXJnKSk7XG5cdFx0fSBlbHNlIHtcblx0XHRcdHJlc3VsdHMucHVzaChhcmcpO1xuXHRcdH1cblx0fVxuXG5cdHJldHVybiByZXN1bHRzO1xufTtcblxuc3dpenpsZS53cmFwID0gZnVuY3Rpb24gKGZuKSB7XG5cdHJldHVybiBmdW5jdGlvbiAoKSB7XG5cdFx0cmV0dXJuIGZuKHN3aXp6bGUoYXJndW1lbnRzKSk7XG5cdH07XG59O1xuIl0sIm5hbWVzIjpbImlzQXJyYXlpc2giLCJyZXF1aXJlIiwiY29uY2F0IiwiQXJyYXkiLCJwcm90b3R5cGUiLCJzbGljZSIsInN3aXp6bGUiLCJtb2R1bGUiLCJleHBvcnRzIiwiYXJncyIsInJlc3VsdHMiLCJpIiwibGVuIiwibGVuZ3RoIiwiYXJnIiwiY2FsbCIsInB1c2giLCJ3cmFwIiwiZm4iLCJhcmd1bWVudHMiXSwic291cmNlUm9vdCI6IiJ9\n//# sourceURL=webpack-internal:///(ssr)/../node_modules/.pnpm/simple-swizzle@0.2.2/node_modules/simple-swizzle/index.js\n");

/***/ })

};
;