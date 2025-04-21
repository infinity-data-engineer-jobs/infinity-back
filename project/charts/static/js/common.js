ajax_get = function(url,func){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.setRequestHeader('Content-type', 'application/json');
    xhr.onload = function(){
        if (this.status == 200) {
            var data = JSON.parse(this.responseText);
            func(data);
        } else {
            console.error("Error fetching data: " + this.statusText);
        }
    }
    xhr.send();
}