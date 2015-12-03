var page = require('webpage').create();
var system = require('system');
var fs = require('fs');// File System Module

page.settings.userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36';
page.settings.javascriptEnabled = 'true';

var args = system.args;
console.log(args);
url=args[1];
index = args[2];
token = args[3];

console.log(token);
var output = '../comments/' + token + '/'+ index + '-y.txt'; // path for saving the local file 

function waitFor(testFx, onReady, timeOutMillis) {
    var maxtimeOutMillis = timeOutMillis ? timeOutMillis : 3000, //< Default Max Timout is 3s
        start = new Date().getTime(),
        condition = false,
        interval = setInterval(function() {
            if ( (new Date().getTime() - start < maxtimeOutMillis) && !condition ) {
                // If not time-out yet and condition not yet fulfilled
                condition = (typeof(testFx) === "string" ? eval(testFx) : testFx()); //< defensive code
            } else {
                if(!condition) {
                    // If condition still not fulfilled (timeout but condition is 'false')
                    console.log("'waitFor()' timeout");
                    phantom.exit(1);
                } else {
                    // Condition fulfilled (timeout and/or condition is 'true')
                    // console.log("'waitFor()' finished in " + (new Date().getTime() - start) + "ms.");
                    typeof(onReady) === "string" ? eval(onReady) : onReady(); //< Do what it's supposed to do once the condition is fulfilled
                    clearInterval(interval); //< Stop this interval
                }
            }
        }, 250); //< repeat check every 250ms
};

page.open(url, function(s) { // open the file 
    cnt = 0;

    waitFor(function() {
        if (cnt > 15) {
            return true;
        } else {
            cnt += 1;
            // console.log("CNT=" + cnt);
        }
    }, function() {
        var data = page.evaluate(function() {
            CLASS_TEXT = "GCARQJCDEXD";
            CLASS_NAME = "GCARQJCDNHD";
            return { 
                "name" : document.getElementsByClassName(CLASS_NAME)[0].innerText,
                "comment" : document.getElementsByClassName(CLASS_TEXT)[0].innerText
            }
        });
        try {
        	//console.log(data["name"].replace("Comment Submitted by ", ""));
        	fs.write(output, data["name"].replace("Comment Submitted by ", "") + ' ' + data["comment"], 'w');    
		//console.log(data["comment"]);
        } catch (e) {
            //pass
        }
        phantom.exit();
    }, 5000);
});
