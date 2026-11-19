# Plan de pruebas funcionales

Las pruebas se hacen sobre la aplicación en ejecución (`python app.py`) con los datos
de `database/backup.sql`. Las capturas de pantalla de cada caso se guardan en
`docs/evidencias/` con el nombre del caso (por ejemplo `CP-01.png`).

Para los casos CP-01 a CP-18 y CP-22 se inicia sesión primero como administrador.

Además, los mismos casos están automatizados en `tests/test_crud.py` (48 pruebas con pytest):

```bash
python -m pytest -v
```

| ID | Tabla | Operación | Datos de entrada | Resultado esperado | Resultado obtenido | Evidencia |
|---|---|---|---|---|---|---|
| CP-01 | marcas | Crear | Marca «Suzuki», país «Japón» | Se guarda y aparece en el listado | Cumple ✓ | ![CP-01](evidencias/CP-01.png) |
| CP-02 | marcas | Crear (duplicado) | Marca «Mazda» (ya existe) | Mensaje: «Ya existe un registro con ese valor» | Cumple ✓ | ![CP-02](evidencias/CP-02.png) |
| CP-03 | marcas | Eliminar relacionado | Eliminar «Chevrolet» (tiene vehículos) | Mensaje: no se puede eliminar porque está relacionado | Cumple ✓ | ![CP-03](evidencias/CP-03.png) |
| CP-04 | vehiculos | Crear | Mazda CX-30 2023, placa «abc901», SUV, 5.000 km, $115.000.000 | Se guarda con la placa en mayúsculas (ABC901) y aparece la marca en el listado | Cumple ✓ | ![CP-04](evidencias/CP-04.png) |
| CP-05 | vehiculos | Editar | Cambiar estado del vehículo JKL482 a «Reservado» | El formulario carga precargado; se actualiza el estado | Cumple ✓ | ![CP-05](evidencias/CP-05.png) |
| CP-06 | vehiculos | Datos inválidos | Año 1950, placa «12-ABC», kilometraje -1, precio 0 | Mensajes de validación por cada campo; no se guarda | Cumple ✓ | ![CP-06](evidencias/CP-06.png) |
| CP-07 | vehiculos | Crear (duplicado) | Placa «JKL482» (ya existe) | Mensaje: «Ya existe un registro con ese valor» | Cumple ✓ | ![CP-07](evidencias/CP-07.png) |
| CP-08 | clientes | Crear | Documento 1075000111, nombre, teléfono, email y ciudad válidos | Se guarda y aparece en el listado | Cumple ✓ | ![CP-08](evidencias/CP-08.png) |
| CP-09 | clientes | Datos inválidos | Documento «12ab», teléfono «abc», email «malo» | Mensajes: solo números / formato de email no válido | Cumple ✓ | ![CP-09](evidencias/CP-09.png) |
| CP-10 | clientes | Eliminar relacionado | Eliminar a «Daniela Castro Ibarra» (tiene operaciones) | Mensaje: no se puede eliminar porque está relacionado | Cumple ✓ | ![CP-10](evidencias/CP-10.png) |
| CP-11 | asesores | Crear | Nombre, teléfono, email nuevo, comisión 1.5 | Se guarda y aparece en el listado | Cumple ✓ | ![CP-11](evidencias/CP-11.png) |
| CP-12 | asesores | Datos inválidos | Comisión 15 % | Mensaje: «Comisión (%)» debe ser menor o igual a 10 | Cumple ✓ | ![CP-12](evidencias/CP-12.png) |
| CP-13 | asesores | Eliminar | Eliminar el asesor creado en CP-11 (sin operaciones) | Pide confirmación, se elimina y desaparece del listado | Cumple ✓ | ![CP-13](evidencias/CP-13.png) |
| CP-14 | operaciones | Crear | Venta del Onix JKL482 a Juan Camilo Rojas, asesora Natalia Quintero, $57.000.000, Crédito | Se guarda; el listado muestra marca, línea, placa, cliente y asesor (no los ID) | Cumple ✓ | ![CP-14](evidencias/CP-14.png) |
| CP-15 | operaciones | Editar | Cambiar la operación de CP-14 a «Compra» y valor $50.000.000 | El formulario carga precargado; se actualizan los datos | Cumple ✓ | ![CP-15](evidencias/CP-15.png) |
| CP-16 | operaciones | Datos inválidos | Fecha vacía, sin cliente, valor -10 | Mensajes de validación; no se guarda | Cumple ✓ | ![CP-16](evidencias/CP-16.png) |
| CP-17 | operaciones | Eliminar | Eliminar la operación de CP-14 | Pide confirmación, se elimina y desaparece del listado | Cumple ✓ | ![CP-17](evidencias/CP-17.png) |
| CP-18 | marcas | Listar | Abrir el menú «Marcas» | Se ven las 10 marcas con el número de vehículos de cada una | Cumple ✓ | ![CP-18](evidencias/CP-18.png) |
| CP-19 | (sesión) | Iniciar sesión | Usuario «admin» con contraseña incorrecta | Mensaje «Usuario o contraseña incorrectos»; no entra | Cumple ✓ | ![CP-19](evidencias/CP-19.png) |
| CP-20 | (sesión) | Acceso sin sesión | Un visitante abre `/marcas/` directamente | Redirige al inicio de sesión con el aviso «Inicia sesión para administrar los datos» | Cumple ✓ | ![CP-20](evidencias/CP-20.png) |
| CP-21 | vehiculos | Catálogo público | Abrir la página principal sin iniciar sesión | Solo aparecen vehículos disponibles o reservados, con foto y sin botones de editar o eliminar | Cumple ✓ | ![CP-21](evidencias/CP-21.png) |
| CP-22 | vehiculos | Editar con foto | Abrir el Mazda 3 (MZD903) para editar | El formulario muestra la foto actual con las opciones de cambiarla o quitarla | Cumple ✓ | ![CP-22](evidencias/CP-22.png) |
