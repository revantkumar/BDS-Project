SomApi.account = "SOM564ba5be4012c";  //your API Key here
SomApi.domainName = "guptamayank.com:5000";     //your domain or sub-domain here
SomApi.onTestCompleted = onTestCompleted;
SomApi.onError = onError;
SomApi.onProgress = onProgress;

var msgDiv = document.getElementById("msg");
var prgsDiv = document.getElementById("prgs");
var speedTest = document.getElementsByClassName('speedtest')[0];
var download = document.getElementById('download-speed');
var upload = document.getElementById('upload-speed');
var jitter = document.getElementById('jitter');
var latency = document.getElementById('latency');

function btnStartClick() {
    //set config values
SomApi.config.sustainTime = 8;
    SomApi.config.testServerEnabled = true;
    SomApi.config.userInfoEnabled = true;
    SomApi.config.latencyTestEnabled = true;
    SomApi.config.uploadTestEnabled = true;
    SomApi.config.progress.enabled = true;
    SomApi.config.progress.verbose = true;

    // msgDiv.innerHTML = "<h3>--------------- Test Result ---------------</h3><h4>" +
    //     "Speed test in progress. Please wait...</h4>";
    speedTest.innerHTML = '<i class="fa fa-dashboard"></i> Testing download...';
    download.innerHTML = 'Download: ...';
    upload.innerHTML = 'Upload: ...';
    jitter.innerHTML = 'Jitter: ...';
    latency.innerHTML = 'Latency: ...';
    SomApi.startTest();
}

function onTestCompleted(testResult) {
    gauge.set(testResult.download); // set actual value
    gauge.setTextField(document.getElementById("gauge-text"));
    speedTest.innerHTML = '<i class="fa fa-dashboard"></i> Test again';
    download.innerHTML = 'Download: ' + testResult.download + " Mbps";
    upload.innerHTML = 'Upload: ' + testResult.upload + " Mbps";
    jitter.innerHTML = 'Jitter: ' + testResult.jitter + " ms";
    latency.innerHTML = 'Latency: ' + testResult.latency + " ms";
    // msgDiv.innerHTML = "<h3>--------------- Test Result ---------------</h3><h4>" +
    //     "Download: " + testResult.download + " Mbps <br/>" +
    //     "Upload: " + testResult.upload + " Mbps <br/>" +
    //     "Latency: " + testResult.latency + " ms <br/>" +
    //     "Jitter: " + testResult.jitter + " ms <br/>" +
    //     "Test Server: " + testResult.testServer + "<br/>" +
    //     "IP: " + testResult.ip_address + "<br/>" +
    //     "Hostname: " + testResult.hostname + "<br/>" +
    // "</h4>";
}

// var target = document.getElementById('foo'); // your canvas element
// var gauge = new Gauge(target).setOptions(opts); // create sexy gauge!

function onError(error) {
    msgDiv.innerHTML = "Error " + error.code + ": " + error.message;
}

function onProgress(progress) {
    // prgsDiv.innerHTML =
    // "<h3>--------------- Progress ---------------</h3><h4>" +
    //     "Progress Type: " + progress.type + "<br/>" +
    //     "Pass: " + progress.pass + "<br/>" +
    //     "Percent Done: " + progress.percentDone + "% <br/>" +
    //     "Current Speed: " + progress.currentSpeed + " Mbps <br/>" +
    // "</h4>";
    speedTest.innerHTML = '<i class="fa fa-dashboard"></i> Testing '+ progress.type +'...';
    if (progress.type == 'download') {
        download.innerHTML = 'Download: ' + progress.currentSpeed + " Mbps";
    }
    if (progress.type == 'upload') {
        upload.innerHTML = 'Upload: ' + progress.currentSpeed + " Mbps";
    }
    gauge.maxValue = 100; // set max gauge value
    gauge.animationSpeed = 32; // set animation speed (32 is default value)
    // if (progress.type == 'download') {
      gauge.set(progress.currentSpeed); // set actual value
      gauge.setTextField(document.getElementById("gauge-text"));
    // }

}
