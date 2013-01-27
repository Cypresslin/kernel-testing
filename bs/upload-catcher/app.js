var express = require('express');
var fs = require('fs');  // we will need it for file uploads
var http = require('http');

var app = express();

app.configure(function(){
    app.set('port', process.env.PORT || 3000);
    app.use(express.bodyParser());
    app.use(express.methodOverride());
    app.use(app.router);
    app.use(express.static(__dirname + '/public'));
});

app.configure('development', function(){
    app.use(express.errorHandler({ dumpExceptions: true, showStack: true }));
});

app.configure('production', function(){
    app.use(express.errorHandler());
});

app.get('/', function(req, res) {
    res.send('<form method="post" enctype="multipart/form-data">'
      + '<p>Image: <input type="file" name="uploadfile" /></p>'
      + '<p><input type="submit" value="Upload" /></p>'
      + '</form>');

});

app.post('/upload', function(req, res){
    var temp_path = req.files.uploadfile.path;
    var save_path = './raw-results/';
    var path_bits = req.files.uploadfile.name.split('/');

    if (path_bits.length > 1) {
    	save_path += path_bits[path_bits.length - 1];
    }
    else {
    	save_path += path_bits;
    }

    fs.rename(temp_path, save_path, function(error){
     	if(error) throw error;

     	fs.unlink(temp_path, function(){
     		if(error) throw error;
     		res.send("File uploaded to: " + save_path);
     	});

     });
});

http.createServer(app).listen(app.get('port'), function(){
    console.log("Express server listening on port " + app.get('port'));
});


