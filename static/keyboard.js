document.addEventListener('keydown', function(event) {
    var key = event.key;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/keypress');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({key: key}));
  });
