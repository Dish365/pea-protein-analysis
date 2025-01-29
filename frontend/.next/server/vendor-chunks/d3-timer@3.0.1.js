"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
exports.id = "vendor-chunks/d3-timer@3.0.1";
exports.ids = ["vendor-chunks/d3-timer@3.0.1"];
exports.modules = {

/***/ "(ssr)/../node_modules/.pnpm/d3-timer@3.0.1/node_modules/d3-timer/src/timer.js":
/*!*******************************************************************************!*\
  !*** ../node_modules/.pnpm/d3-timer@3.0.1/node_modules/d3-timer/src/timer.js ***!
  \*******************************************************************************/
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   Timer: () => (/* binding */ Timer),\n/* harmony export */   now: () => (/* binding */ now),\n/* harmony export */   timer: () => (/* binding */ timer),\n/* harmony export */   timerFlush: () => (/* binding */ timerFlush)\n/* harmony export */ });\nvar frame = 0, timeout = 0, interval = 0, pokeDelay = 1000, taskHead, taskTail, clockLast = 0, clockNow = 0, clockSkew = 0, clock = typeof performance === \"object\" && performance.now ? performance : Date, setFrame =  false ? 0 : function(f) {\n    setTimeout(f, 17);\n};\nfunction now() {\n    return clockNow || (setFrame(clearNow), clockNow = clock.now() + clockSkew);\n}\nfunction clearNow() {\n    clockNow = 0;\n}\nfunction Timer() {\n    this._call = this._time = this._next = null;\n}\nTimer.prototype = timer.prototype = {\n    constructor: Timer,\n    restart: function(callback, delay, time) {\n        if (typeof callback !== \"function\") throw new TypeError(\"callback is not a function\");\n        time = (time == null ? now() : +time) + (delay == null ? 0 : +delay);\n        if (!this._next && taskTail !== this) {\n            if (taskTail) taskTail._next = this;\n            else taskHead = this;\n            taskTail = this;\n        }\n        this._call = callback;\n        this._time = time;\n        sleep();\n    },\n    stop: function() {\n        if (this._call) {\n            this._call = null;\n            this._time = Infinity;\n            sleep();\n        }\n    }\n};\nfunction timer(callback, delay, time) {\n    var t = new Timer;\n    t.restart(callback, delay, time);\n    return t;\n}\nfunction timerFlush() {\n    now(); // Get the current time, if not already set.\n    ++frame; // Pretend we’ve set an alarm, if we haven’t already.\n    var t = taskHead, e;\n    while(t){\n        if ((e = clockNow - t._time) >= 0) t._call.call(undefined, e);\n        t = t._next;\n    }\n    --frame;\n}\nfunction wake() {\n    clockNow = (clockLast = clock.now()) + clockSkew;\n    frame = timeout = 0;\n    try {\n        timerFlush();\n    } finally{\n        frame = 0;\n        nap();\n        clockNow = 0;\n    }\n}\nfunction poke() {\n    var now = clock.now(), delay = now - clockLast;\n    if (delay > pokeDelay) clockSkew -= delay, clockLast = now;\n}\nfunction nap() {\n    var t0, t1 = taskHead, t2, time = Infinity;\n    while(t1){\n        if (t1._call) {\n            if (time > t1._time) time = t1._time;\n            t0 = t1, t1 = t1._next;\n        } else {\n            t2 = t1._next, t1._next = null;\n            t1 = t0 ? t0._next = t2 : taskHead = t2;\n        }\n    }\n    taskTail = t0;\n    sleep(time);\n}\nfunction sleep(time) {\n    if (frame) return; // Soonest alarm already set, or will be.\n    if (timeout) timeout = clearTimeout(timeout);\n    var delay = time - clockNow; // Strictly less than if we recomputed clockNow.\n    if (delay > 24) {\n        if (time < Infinity) timeout = setTimeout(wake, time - clock.now() - clockSkew);\n        if (interval) interval = clearInterval(interval);\n    } else {\n        if (!interval) clockLast = clock.now(), interval = setInterval(poke, pokeDelay);\n        frame = 1, setFrame(wake);\n    }\n}\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHNzcikvLi4vbm9kZV9tb2R1bGVzLy5wbnBtL2QzLXRpbWVyQDMuMC4xL25vZGVfbW9kdWxlcy9kMy10aW1lci9zcmMvdGltZXIuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7OztBQUFBLElBQUlBLFFBQVEsR0FDUkMsVUFBVSxHQUNWQyxXQUFXLEdBQ1hDLFlBQVksTUFDWkMsVUFDQUMsVUFDQUMsWUFBWSxHQUNaQyxXQUFXLEdBQ1hDLFlBQVksR0FDWkMsUUFBUSxPQUFPQyxnQkFBZ0IsWUFBWUEsWUFBWUMsR0FBRyxHQUFHRCxjQUFjRSxNQUMzRUMsV0FBVyxNQUEwRCxHQUFHQyxDQUF5Q0EsR0FBRyxTQUFTRyxDQUFDO0lBQUlDLFdBQVdELEdBQUc7QUFBSztBQUVsSixTQUFTTjtJQUNkLE9BQU9KLFlBQWFNLENBQUFBLFNBQVNNLFdBQVdaLFdBQVdFLE1BQU1FLEdBQUcsS0FBS0gsU0FBUTtBQUMzRTtBQUVBLFNBQVNXO0lBQ1BaLFdBQVc7QUFDYjtBQUVPLFNBQVNhO0lBQ2QsSUFBSSxDQUFDQyxLQUFLLEdBQ1YsSUFBSSxDQUFDQyxLQUFLLEdBQ1YsSUFBSSxDQUFDQyxLQUFLLEdBQUc7QUFDZjtBQUVBSCxNQUFNSSxTQUFTLEdBQUdDLE1BQU1ELFNBQVMsR0FBRztJQUNsQ0UsYUFBYU47SUFDYk8sU0FBUyxTQUFTQyxRQUFRLEVBQUVDLEtBQUssRUFBRUMsSUFBSTtRQUNyQyxJQUFJLE9BQU9GLGFBQWEsWUFBWSxNQUFNLElBQUlHLFVBQVU7UUFDeERELE9BQU8sQ0FBQ0EsUUFBUSxPQUFPbkIsUUFBUSxDQUFDbUIsSUFBRyxJQUFNRCxDQUFBQSxTQUFTLE9BQU8sSUFBSSxDQUFDQSxLQUFJO1FBQ2xFLElBQUksQ0FBQyxJQUFJLENBQUNOLEtBQUssSUFBSWxCLGFBQWEsSUFBSSxFQUFFO1lBQ3BDLElBQUlBLFVBQVVBLFNBQVNrQixLQUFLLEdBQUcsSUFBSTtpQkFDOUJuQixXQUFXLElBQUk7WUFDcEJDLFdBQVcsSUFBSTtRQUNqQjtRQUNBLElBQUksQ0FBQ2dCLEtBQUssR0FBR087UUFDYixJQUFJLENBQUNOLEtBQUssR0FBR1E7UUFDYkU7SUFDRjtJQUNBQyxNQUFNO1FBQ0osSUFBSSxJQUFJLENBQUNaLEtBQUssRUFBRTtZQUNkLElBQUksQ0FBQ0EsS0FBSyxHQUFHO1lBQ2IsSUFBSSxDQUFDQyxLQUFLLEdBQUdZO1lBQ2JGO1FBQ0Y7SUFDRjtBQUNGO0FBRU8sU0FBU1AsTUFBTUcsUUFBUSxFQUFFQyxLQUFLLEVBQUVDLElBQUk7SUFDekMsSUFBSUssSUFBSSxJQUFJZjtJQUNaZSxFQUFFUixPQUFPLENBQUNDLFVBQVVDLE9BQU9DO0lBQzNCLE9BQU9LO0FBQ1Q7QUFFTyxTQUFTQztJQUNkekIsT0FBTyw0Q0FBNEM7SUFDbkQsRUFBRVgsT0FBTyxxREFBcUQ7SUFDOUQsSUFBSW1DLElBQUkvQixVQUFVaUM7SUFDbEIsTUFBT0YsRUFBRztRQUNSLElBQUksQ0FBQ0UsSUFBSTlCLFdBQVc0QixFQUFFYixLQUFLLEtBQUssR0FBR2EsRUFBRWQsS0FBSyxDQUFDaUIsSUFBSSxDQUFDQyxXQUFXRjtRQUMzREYsSUFBSUEsRUFBRVosS0FBSztJQUNiO0lBQ0EsRUFBRXZCO0FBQ0o7QUFFQSxTQUFTd0M7SUFDUGpDLFdBQVcsQ0FBQ0QsWUFBWUcsTUFBTUUsR0FBRyxFQUFDLElBQUtIO0lBQ3ZDUixRQUFRQyxVQUFVO0lBQ2xCLElBQUk7UUFDRm1DO0lBQ0YsU0FBVTtRQUNScEMsUUFBUTtRQUNSeUM7UUFDQWxDLFdBQVc7SUFDYjtBQUNGO0FBRUEsU0FBU21DO0lBQ1AsSUFBSS9CLE1BQU1GLE1BQU1FLEdBQUcsSUFBSWtCLFFBQVFsQixNQUFNTDtJQUNyQyxJQUFJdUIsUUFBUTFCLFdBQVdLLGFBQWFxQixPQUFPdkIsWUFBWUs7QUFDekQ7QUFFQSxTQUFTOEI7SUFDUCxJQUFJRSxJQUFJQyxLQUFLeEMsVUFBVXlDLElBQUlmLE9BQU9JO0lBQ2xDLE1BQU9VLEdBQUk7UUFDVCxJQUFJQSxHQUFHdkIsS0FBSyxFQUFFO1lBQ1osSUFBSVMsT0FBT2MsR0FBR3RCLEtBQUssRUFBRVEsT0FBT2MsR0FBR3RCLEtBQUs7WUFDcENxQixLQUFLQyxJQUFJQSxLQUFLQSxHQUFHckIsS0FBSztRQUN4QixPQUFPO1lBQ0xzQixLQUFLRCxHQUFHckIsS0FBSyxFQUFFcUIsR0FBR3JCLEtBQUssR0FBRztZQUMxQnFCLEtBQUtELEtBQUtBLEdBQUdwQixLQUFLLEdBQUdzQixLQUFLekMsV0FBV3lDO1FBQ3ZDO0lBQ0Y7SUFDQXhDLFdBQVdzQztJQUNYWCxNQUFNRjtBQUNSO0FBRUEsU0FBU0UsTUFBTUYsSUFBSTtJQUNqQixJQUFJOUIsT0FBTyxRQUFRLHlDQUF5QztJQUM1RCxJQUFJQyxTQUFTQSxVQUFVNkMsYUFBYTdDO0lBQ3BDLElBQUk0QixRQUFRQyxPQUFPdkIsVUFBVSxnREFBZ0Q7SUFDN0UsSUFBSXNCLFFBQVEsSUFBSTtRQUNkLElBQUlDLE9BQU9JLFVBQVVqQyxVQUFVaUIsV0FBV3NCLE1BQU1WLE9BQU9yQixNQUFNRSxHQUFHLEtBQUtIO1FBQ3JFLElBQUlOLFVBQVVBLFdBQVc2QyxjQUFjN0M7SUFDekMsT0FBTztRQUNMLElBQUksQ0FBQ0EsVUFBVUksWUFBWUcsTUFBTUUsR0FBRyxJQUFJVCxXQUFXOEMsWUFBWU4sTUFBTXZDO1FBQ3JFSCxRQUFRLEdBQUdhLFNBQVMyQjtJQUN0QjtBQUNGIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vcHJvY2Vzcy1hbmFseXNpcy1mcm9udGVuZC8uLi9ub2RlX21vZHVsZXMvLnBucG0vZDMtdGltZXJAMy4wLjEvbm9kZV9tb2R1bGVzL2QzLXRpbWVyL3NyYy90aW1lci5qcz9iYzM3Il0sInNvdXJjZXNDb250ZW50IjpbInZhciBmcmFtZSA9IDAsIC8vIGlzIGFuIGFuaW1hdGlvbiBmcmFtZSBwZW5kaW5nP1xuICAgIHRpbWVvdXQgPSAwLCAvLyBpcyBhIHRpbWVvdXQgcGVuZGluZz9cbiAgICBpbnRlcnZhbCA9IDAsIC8vIGFyZSBhbnkgdGltZXJzIGFjdGl2ZT9cbiAgICBwb2tlRGVsYXkgPSAxMDAwLCAvLyBob3cgZnJlcXVlbnRseSB3ZSBjaGVjayBmb3IgY2xvY2sgc2tld1xuICAgIHRhc2tIZWFkLFxuICAgIHRhc2tUYWlsLFxuICAgIGNsb2NrTGFzdCA9IDAsXG4gICAgY2xvY2tOb3cgPSAwLFxuICAgIGNsb2NrU2tldyA9IDAsXG4gICAgY2xvY2sgPSB0eXBlb2YgcGVyZm9ybWFuY2UgPT09IFwib2JqZWN0XCIgJiYgcGVyZm9ybWFuY2Uubm93ID8gcGVyZm9ybWFuY2UgOiBEYXRlLFxuICAgIHNldEZyYW1lID0gdHlwZW9mIHdpbmRvdyA9PT0gXCJvYmplY3RcIiAmJiB3aW5kb3cucmVxdWVzdEFuaW1hdGlvbkZyYW1lID8gd2luZG93LnJlcXVlc3RBbmltYXRpb25GcmFtZS5iaW5kKHdpbmRvdykgOiBmdW5jdGlvbihmKSB7IHNldFRpbWVvdXQoZiwgMTcpOyB9O1xuXG5leHBvcnQgZnVuY3Rpb24gbm93KCkge1xuICByZXR1cm4gY2xvY2tOb3cgfHwgKHNldEZyYW1lKGNsZWFyTm93KSwgY2xvY2tOb3cgPSBjbG9jay5ub3coKSArIGNsb2NrU2tldyk7XG59XG5cbmZ1bmN0aW9uIGNsZWFyTm93KCkge1xuICBjbG9ja05vdyA9IDA7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBUaW1lcigpIHtcbiAgdGhpcy5fY2FsbCA9XG4gIHRoaXMuX3RpbWUgPVxuICB0aGlzLl9uZXh0ID0gbnVsbDtcbn1cblxuVGltZXIucHJvdG90eXBlID0gdGltZXIucHJvdG90eXBlID0ge1xuICBjb25zdHJ1Y3RvcjogVGltZXIsXG4gIHJlc3RhcnQ6IGZ1bmN0aW9uKGNhbGxiYWNrLCBkZWxheSwgdGltZSkge1xuICAgIGlmICh0eXBlb2YgY2FsbGJhY2sgIT09IFwiZnVuY3Rpb25cIikgdGhyb3cgbmV3IFR5cGVFcnJvcihcImNhbGxiYWNrIGlzIG5vdCBhIGZ1bmN0aW9uXCIpO1xuICAgIHRpbWUgPSAodGltZSA9PSBudWxsID8gbm93KCkgOiArdGltZSkgKyAoZGVsYXkgPT0gbnVsbCA/IDAgOiArZGVsYXkpO1xuICAgIGlmICghdGhpcy5fbmV4dCAmJiB0YXNrVGFpbCAhPT0gdGhpcykge1xuICAgICAgaWYgKHRhc2tUYWlsKSB0YXNrVGFpbC5fbmV4dCA9IHRoaXM7XG4gICAgICBlbHNlIHRhc2tIZWFkID0gdGhpcztcbiAgICAgIHRhc2tUYWlsID0gdGhpcztcbiAgICB9XG4gICAgdGhpcy5fY2FsbCA9IGNhbGxiYWNrO1xuICAgIHRoaXMuX3RpbWUgPSB0aW1lO1xuICAgIHNsZWVwKCk7XG4gIH0sXG4gIHN0b3A6IGZ1bmN0aW9uKCkge1xuICAgIGlmICh0aGlzLl9jYWxsKSB7XG4gICAgICB0aGlzLl9jYWxsID0gbnVsbDtcbiAgICAgIHRoaXMuX3RpbWUgPSBJbmZpbml0eTtcbiAgICAgIHNsZWVwKCk7XG4gICAgfVxuICB9XG59O1xuXG5leHBvcnQgZnVuY3Rpb24gdGltZXIoY2FsbGJhY2ssIGRlbGF5LCB0aW1lKSB7XG4gIHZhciB0ID0gbmV3IFRpbWVyO1xuICB0LnJlc3RhcnQoY2FsbGJhY2ssIGRlbGF5LCB0aW1lKTtcbiAgcmV0dXJuIHQ7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiB0aW1lckZsdXNoKCkge1xuICBub3coKTsgLy8gR2V0IHRoZSBjdXJyZW50IHRpbWUsIGlmIG5vdCBhbHJlYWR5IHNldC5cbiAgKytmcmFtZTsgLy8gUHJldGVuZCB3ZeKAmXZlIHNldCBhbiBhbGFybSwgaWYgd2UgaGF2ZW7igJl0IGFscmVhZHkuXG4gIHZhciB0ID0gdGFza0hlYWQsIGU7XG4gIHdoaWxlICh0KSB7XG4gICAgaWYgKChlID0gY2xvY2tOb3cgLSB0Ll90aW1lKSA+PSAwKSB0Ll9jYWxsLmNhbGwodW5kZWZpbmVkLCBlKTtcbiAgICB0ID0gdC5fbmV4dDtcbiAgfVxuICAtLWZyYW1lO1xufVxuXG5mdW5jdGlvbiB3YWtlKCkge1xuICBjbG9ja05vdyA9IChjbG9ja0xhc3QgPSBjbG9jay5ub3coKSkgKyBjbG9ja1NrZXc7XG4gIGZyYW1lID0gdGltZW91dCA9IDA7XG4gIHRyeSB7XG4gICAgdGltZXJGbHVzaCgpO1xuICB9IGZpbmFsbHkge1xuICAgIGZyYW1lID0gMDtcbiAgICBuYXAoKTtcbiAgICBjbG9ja05vdyA9IDA7XG4gIH1cbn1cblxuZnVuY3Rpb24gcG9rZSgpIHtcbiAgdmFyIG5vdyA9IGNsb2NrLm5vdygpLCBkZWxheSA9IG5vdyAtIGNsb2NrTGFzdDtcbiAgaWYgKGRlbGF5ID4gcG9rZURlbGF5KSBjbG9ja1NrZXcgLT0gZGVsYXksIGNsb2NrTGFzdCA9IG5vdztcbn1cblxuZnVuY3Rpb24gbmFwKCkge1xuICB2YXIgdDAsIHQxID0gdGFza0hlYWQsIHQyLCB0aW1lID0gSW5maW5pdHk7XG4gIHdoaWxlICh0MSkge1xuICAgIGlmICh0MS5fY2FsbCkge1xuICAgICAgaWYgKHRpbWUgPiB0MS5fdGltZSkgdGltZSA9IHQxLl90aW1lO1xuICAgICAgdDAgPSB0MSwgdDEgPSB0MS5fbmV4dDtcbiAgICB9IGVsc2Uge1xuICAgICAgdDIgPSB0MS5fbmV4dCwgdDEuX25leHQgPSBudWxsO1xuICAgICAgdDEgPSB0MCA/IHQwLl9uZXh0ID0gdDIgOiB0YXNrSGVhZCA9IHQyO1xuICAgIH1cbiAgfVxuICB0YXNrVGFpbCA9IHQwO1xuICBzbGVlcCh0aW1lKTtcbn1cblxuZnVuY3Rpb24gc2xlZXAodGltZSkge1xuICBpZiAoZnJhbWUpIHJldHVybjsgLy8gU29vbmVzdCBhbGFybSBhbHJlYWR5IHNldCwgb3Igd2lsbCBiZS5cbiAgaWYgKHRpbWVvdXQpIHRpbWVvdXQgPSBjbGVhclRpbWVvdXQodGltZW91dCk7XG4gIHZhciBkZWxheSA9IHRpbWUgLSBjbG9ja05vdzsgLy8gU3RyaWN0bHkgbGVzcyB0aGFuIGlmIHdlIHJlY29tcHV0ZWQgY2xvY2tOb3cuXG4gIGlmIChkZWxheSA+IDI0KSB7XG4gICAgaWYgKHRpbWUgPCBJbmZpbml0eSkgdGltZW91dCA9IHNldFRpbWVvdXQod2FrZSwgdGltZSAtIGNsb2NrLm5vdygpIC0gY2xvY2tTa2V3KTtcbiAgICBpZiAoaW50ZXJ2YWwpIGludGVydmFsID0gY2xlYXJJbnRlcnZhbChpbnRlcnZhbCk7XG4gIH0gZWxzZSB7XG4gICAgaWYgKCFpbnRlcnZhbCkgY2xvY2tMYXN0ID0gY2xvY2subm93KCksIGludGVydmFsID0gc2V0SW50ZXJ2YWwocG9rZSwgcG9rZURlbGF5KTtcbiAgICBmcmFtZSA9IDEsIHNldEZyYW1lKHdha2UpO1xuICB9XG59XG4iXSwibmFtZXMiOlsiZnJhbWUiLCJ0aW1lb3V0IiwiaW50ZXJ2YWwiLCJwb2tlRGVsYXkiLCJ0YXNrSGVhZCIsInRhc2tUYWlsIiwiY2xvY2tMYXN0IiwiY2xvY2tOb3ciLCJjbG9ja1NrZXciLCJjbG9jayIsInBlcmZvcm1hbmNlIiwibm93IiwiRGF0ZSIsInNldEZyYW1lIiwid2luZG93IiwicmVxdWVzdEFuaW1hdGlvbkZyYW1lIiwiYmluZCIsImYiLCJzZXRUaW1lb3V0IiwiY2xlYXJOb3ciLCJUaW1lciIsIl9jYWxsIiwiX3RpbWUiLCJfbmV4dCIsInByb3RvdHlwZSIsInRpbWVyIiwiY29uc3RydWN0b3IiLCJyZXN0YXJ0IiwiY2FsbGJhY2siLCJkZWxheSIsInRpbWUiLCJUeXBlRXJyb3IiLCJzbGVlcCIsInN0b3AiLCJJbmZpbml0eSIsInQiLCJ0aW1lckZsdXNoIiwiZSIsImNhbGwiLCJ1bmRlZmluZWQiLCJ3YWtlIiwibmFwIiwicG9rZSIsInQwIiwidDEiLCJ0MiIsImNsZWFyVGltZW91dCIsImNsZWFySW50ZXJ2YWwiLCJzZXRJbnRlcnZhbCJdLCJzb3VyY2VSb290IjoiIn0=\n//# sourceURL=webpack-internal:///(ssr)/../node_modules/.pnpm/d3-timer@3.0.1/node_modules/d3-timer/src/timer.js\n");

/***/ })

};
;