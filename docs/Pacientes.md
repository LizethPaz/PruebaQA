## 1. Acceso al módulo

Para ingresar al módulo **Pacientes**, siga estos pasos:

1. Ubíquese en la **barra lateral izquierda** del sistema.
2. Haga clic en la opción **“Pacientes”**.

Al ingresar, el sistema mostrará la pantalla principal con el listado de pacientes registrados.

---

## 2. Descripción de la pantalla

En la pantalla principal se visualiza:

* Título **“Pacientes”** en la parte superior.
* Campo **Buscar Paciente** para realizar búsquedas rápidas.
* Tarjetas individuales por cada paciente registrado.
* Estado del paciente (**Activo** o **Inactivo**).
* **Nombre completo**.
* **Número de identificación**.
* **Administradora (EPS o entidad)**.
* **Sede**.

En cada tarjeta se encuentra un botón con ícono de **ojo 👁**, que permite ingresar al detalle del paciente.

En la parte superior derecha se encuentran los siguientes botones:

* ![Captura de pantalla 2026-02-27 a la(s) 11.41.50 a.m..png](img/Captura de pantalla 2026-02-27 a la(s) 11.41.50 a.m..png){ width=37 } **Botón azul**
* ![Captura de pantalla 2026-02-27 a la(s) 11.42.30 a.m..png](img/Captura de pantalla 2026-02-27 a la(s) 11.42.30 a.m..png){ width=35 } **Botón verde**
* ![Captura de pantalla 2026-02-27 a la(s) 11.54.51 a.m..png](img/Captura de pantalla 2026-02-27 a la(s) 11.54.51 a.m..png){ width=39 } **Botón para crear paciente**

---

## 3. ¿Qué se puede hacer en este módulo?

Desde el módulo **Pacientes**, el usuario puede:

1. **Consultar** el listado de pacientes registrados.
2. **Buscar** pacientes por nombre o identificación.
3. **Crear** nuevos pacientes.
4. **Consultar** pacientes mediante interoperabilidad.
5. **Trasladar** pacientes cuando existan registros duplicados.
6. **Exportar** la información de pacientes.
7. **Ingresar** al detalle completo de cada paciente.

---

## 4. Procedimientos principales

### 4.1 Crear un nuevo paciente

1. Haga clic en el botón ![Captura de pantalla 2026-02-27 a la(s) 11.54.51 a.m..png](img/Captura de pantalla 2026-02-27 a la(s) 11.54.51 a.m..png){ width=39 } **(Crear)** ubicado en la parte superior derecha.
2. Se abrirá la ventana **Crear Paciente**.
3. Complete la información solicitada en las secciones:

   * **Información Paciente**
   * **Información Administrativa**
   * **Ubicación**
   * **Responsable / Acompañante**
   * **Otros**
4. Haga clic en **Crear** para guardar el registro.

---

### 4.2 Consultar pacientes por interoperabilidad (Ecopetrol)

1. Haga clic en el botón ![Captura de pantalla 2026-02-27 a la(s) 11.42.30 a.m..png](img/Captura de pantalla 2026-02-27 a la(s) 11.42.30 a.m..png){ width=35 }.
2. El sistema abrirá la pantalla **FHIR – Historial Paciente**.
3. Complete los filtros solicitados, como:

   * **Identificación**
   * **Tipo de Identificación**
   * **Género**
   * **Nombre(s)**
   * **Apellidos**
   * **Fecha de Nacimiento (opcional)**
4. Haga clic en el botón de búsqueda 🔍.

Esta opción permite consultar información del paciente mediante **interoperabilidad** con **Ecopetrol**. Ecopetrol

---

### 4.3 Trasladar un paciente (cuando existen duplicados)

1. Haga clic en el botón ![Captura de pantalla 2026-02-27 a la(s) 11.41.50 a.m..png](img/Captura de pantalla 2026-02-27 a la(s) 11.41.50 a.m..png){ width=37 }.
2. Seleccione la opción **Traslado**.
3. En la ventana **Gestión Traslado**:

   1. Seleccione el **Paciente Origen**.
   2. Seleccione el **Paciente Destino**.
   3. Si es necesario, marque la opción **Anular paciente origen**.
4. Haga clic en **Guardar**.



!!! warning "Nota"
    **Este procedimiento se utiliza cuando existen pacientes duplicados y se requiere unificar la información.**



---

### 4.4 Exportar listado de pacientes

Desde el botón ![Captura de pantalla 2026-02-27 a la(s) 11.41.50 a.m..png](img/Captura de pantalla 2026-02-27 a la(s) 11.41.50 a.m..png){ width=37 }, también se encuentra la opción de **Exportar**.

Permite descargar el listado completo de pacientes en los siguientes formatos:

* **PDF**
* **Excel**
* **CSV**
* **TXT**

---

### 4.5 Ver detalle del paciente

1. Ubique el paciente en el listado.
2. Haga clic en el botón con ícono ![Captura de pantalla 2026-02-27 a la(s) 2.25.44 p.m..png](img/Captura de pantalla 2026-02-27 a la(s) 2.25.44 p.m..png){ width=32 }.
3. El sistema abrirá la pantalla de detalle del paciente.



!!! info video-tutorial "▶️ Video tutorial"

![Cap 2026-03-02 at 09.33.26.gif](img/Cap 2026-03-02 at 09.33.26.gif){ width=756 }

---

## 5. Secciones dentro del detalle del paciente

Al ingresar al detalle, se visualizan las siguientes pestañas:

### 5.1 Información

Contiene:

* **Tipo y número de documento**
* **Nombres y apellidos**
* **Género**
* **Estado**
* **Administradora**
* **Régimen**
* **Sede**
* **Responsable / acompañante**
* **Datos de ubicación y contacto**
* **Información adicional**

---

### 5.2 Contactos

Permite visualizar y agregar:

* **Contactos asociados al paciente.**
* **Parentesco del contacto con el paciente.**
* **Información de contacto registrada.**

---

### 5.3 Beneficiarios

Muestra los beneficiarios asociados al paciente, cuando aplique.

---

### 5.4 Citas 📅

En esta pestaña se visualizan:

* **Fecha inicial**
* **Fecha final**
* **Profesional**
* **Descripción del servicio**
* **Ubicación**
* **Tipo**
* **Acciones disponibles**

Aquí se pueden consultar todas las citas programadas o atendidas del paciente.

---

### 5.5 Archivo

Permite visualizar los archivos adjuntos relacionados con el paciente.

Estos pueden ser documentos cargados por razones administrativas o clínicas.

---

### 5.6 RDA – Resumen Digital

Permite visualizar el resumen digital de atenciones, donde se muestran:

* **Información general de la consulta**
* **Diagnóstico**
* **Médico tratante**
* **Evoluciones registradas**

---

## 6. Acciones disponibles

Dentro del detalle del paciente, el usuario puede:

* **Editar** información (ícono de lápiz ✏️).
* **Gestionar** fotografía del paciente.
* **Adjuntar** documentos.
* **Consultar** citas.
* **Visualizar** historial digital.

---



!!! success "Buenas prácticas ✅"
    * **Verifique** si el paciente ya existe antes de crearlo, utilizando el campo de búsqueda.
    * **Utilice** la opción **Traslado** únicamente cuando esté seguro de que se trata de registros duplicados.
    * **Revise** cuidadosamente la identificación antes de guardar un nuevo paciente.
    * **Mantenga** actualizada la información de contacto.
    * **Adjunte** únicamente documentos relevantes y necesarios.



!!! info video-tutorial "▶️ Video tutorial"

![Detalles Paciente.gif](img/Detalles Paciente.gif){ width=760 }
