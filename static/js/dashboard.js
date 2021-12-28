
var dashboard = function(){
  this.ejecutar = function(){
    var consulta = $('#console').html();
    $.ajax({
      method: "POST",
      url: "/consulta",
      data: { sql: consulta }
    })
    .done(function( response ) {
      $('#respuesta').html(response)
    });
  }
}

var odashboard = new dashboard();
