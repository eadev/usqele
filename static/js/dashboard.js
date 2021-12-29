
var dashboard = function(){
  this.ejecutar = function(){
    var consulta = $('#console').val();
    $('#loading').show()
    $.ajax({
      method: "POST",
      url: "/consulta",
      data: { sql: consulta }
    })
    .done(function( response ) {
      $('#respuesta').html(response)
      $('#loading').hide()
    });
  }
  /**
   * Nos permite seleccionar y cargar una tabla determinada.
   */
  this.seleccionar = function(recurso){
    $('#console').val("SELECT * FROM "+recurso+" LIMIT 1000;");
    this.ejecutar();
  }
  /**
   *
   * @param recurso
   */
  this.guardar = function(){
    var sentencia = $('#console').val();
    var clases = "list-group-item d-flex justify-content-between align-items-center bg-warning mt-1";
    var item = '<li class="'+clases+'" >'+sentencia+
      '<span class="btn btn-dark badge badge-dark badge-pill p-1" style="cursor:pointer;" onclick="odashboard.ejecutar_sentencia(\''+sentencia+'\');">Ejecutar</span></li>'
    $('#marcadores').append(item);
  }
  /**
   * Permite seleccionar un marcador.
   */
  this.ejecutar_sentencia = function(sentencia){
    $('#console').html(sentencia);
    this.ejecutar();
  }
}

var odashboard = new dashboard();
