function update(rowId) {
  var row = $("#row" + rowId);
  var subject = row.find('#subject').text();
  var injectCount = row.find('#inject_count').val();
  var engageCount = row.find('#engage_count').val();
  var engageRate = row.find('#engage_percent').val();
  var request = $.ajax('/dev/subjects/' + encodeURIComponent(subject),
    {
      data: JSON.stringify({ inject_count: injectCount, engage_count: engageCount, engage_percent: engageRate }),
      contentType: 'application/json',
      method: 'put'
    });
  request.done(function() {
    location.reload();
  });
  request.fail(function() {
    alert('something went wrong');
  });
}

function deleteRow(rowId) {
  var row = $("#row" + rowId);
  var subject = row.find('#subject').text();
  var request = $.ajax('/dev/subjects/' + encodeURIComponent(subject),
    {
      method: 'delete'
    });
  request.done(function() {
    location.reload();
  });
  request.fail(function() {
    alert('something went wrong');
  });
}
