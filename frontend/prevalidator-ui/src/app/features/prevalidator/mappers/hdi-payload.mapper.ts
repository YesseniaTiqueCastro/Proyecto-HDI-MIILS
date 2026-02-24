export function buildHdiPayload(form: any, idInspeccion: number) {

  return {
    inspeccion: {
      id_inspeccion: idInspeccion,

      usuarioCreador: "COLSERAUTO",

      fechaHoraInspeccion: form.fechaHoraInspeccion,
      fechaHoraSalidaInspeccion: form.fechaHoraSalidaInspeccion,

      tipo: form.tipo,
      codigoFasecolda: form.codigoFasecolda,
      servicio: form.servicio,

      chasis: form.chasis,
      serial: form.serial,
      motor: form.motor,
      modelo: form.modelo,

      color: form.color,
      tipoCarroceria: form.tipoCarroceria,
      tipoVehiculo: form.tipoVehiculo,

      vehiculo: {
        color_id: Number(form.color),
        tipo_vehiculo_id: Number(form.tipoVehiculo),
        tipo_caja_id: Number(form.caja),
        tipo_pintura_id: Number(form.tipoPintura),
        carroceria_id: Number(form.tipoCarroceria),
        servicio_id: Number(form.servicio)
      }
    },

    aprobacion: {
      identificacion: {
        tipoDocumento: "CC",
        numeroDocumento: "12345678"
      },
      operario: {
        usuario: "COLSERAUTO"
      }
    },

    calificaciones: [],
    accesorios: [],
    comentarios: []
  };
}