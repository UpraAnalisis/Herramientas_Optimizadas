# Herramientas Optimizadas

Las herramientas optimizadas de geoprocesamiento desarrollados por la UPRA incorporan una interfaz gráfica que facilita al usuario la interacción con la información Geográfica mediante el uso de los programas ArcMap y ArcCatalog, permitiendo su fácil incorporación en modelos de geoprocesamiento creados con Model Builder. La característica principal de los scripts desarrollados por la UPRA consiste en hacer uso de **Cursores, Procesamiento en Paralelo y Procesamiento en Segundo Plano a 64 Bits**.
Su objetivo principal es agilizar los procesos de análisis realizados por la entidad.


## Limitantes y Recomendaciones

+ Estas herramientas están diseñadas para funcionar con **ArcGis Desktop 10.5**  y/o versiones superiores.

+ Estas herramientas están desarrolladas para funcionar con el sistema de coordenadas Magna Colombia Bogota [EPSG: 3116]([http://spatialreference.org/ref/epsg/magna-sirgas-colombia-bogota-zone/), por ello, si se desea emplear un nuevo sistema de coordenadas se recomienda cambiar en los scripts las líneas que contengan el siguiente código:

``` py
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
```
Por el Sistema de coordenadas con el que se desee trabajar.
+ La mayoría de estas herramientas hacen uso del complemento [ArcGIS for Desktop Background Geoprocessing (64 bits)](http://desktop.arcgis.com/es/arcmap/10.3/analyze/executing-tools/64bit-background.htm) versión 10.5. Por ello para su correcta ejecución se hace necesario la  instalación de dicho complemento.

+ Estas herramientas no trabajan con las selecciones activas; aunque reciben como parámetros feature layers, estas trabajan directamente con los feature class asociados a estos.

## Instrucciones de Uso

Para hacer uso de las herramientas optimizadas lo primero que se debe hacer es descargar el repositorio y almacenar la carpeta **SCRIPTS_ANALISIS** en el disco C del pc. Para hacerlo, se debe hacer clic en la siguiente en el ícono de Download, tal y como se muestra en la siguiente imagen.

![descarga](/Images/descarga.png)

Luego, una vez descargado, se debe descomprimir y se debe copiar la carpeta SCRIPTS_ANALISIS preferiblemente el disco C del equipo. En caso de que no se pueda, se debe copiar en el disco D o  E o en la raíz de cualquier unidad disponible. La razón por la que se deben copiar estas herramientas en tal directorio, se debe a que las herramientas optimizadas tienen rutas relativas y automáticamente se redireccionan a la capeta **SCRIPTS_ANALISIS** localizada en la raíz de cualquier unidad de disco disponible. Esto es necesario si se van a emplear los modelos de geoprocesamiento suministrados en el repositorio de [modelos de geoprocesamiento](https://github.com/UpraAnalisis/Modelos-de-Geoprocesamiento).

Una vez se hayan descargado las herramientas y en caso de inconvenientes, se hayan 

## Solución de problemas

Si no se tiene en cuenta el procedimiento de almacenar los scripts en la carpeta **SCRIPTS_ANALISIS** en el directorio raíz de una de las unidades de disco disponible, es probable que las herramientas no encuentren la ruta del script. ¿Cómo identificar este problema? El problema se presenta cuando al ejecutar la herramienta aparece el siguiente mensaje.

![desconexión](/Images/desconexion.png)

Otra forma de ver el inconveniente, es cuando se hace clic sobre la herramienta dentro de un modelo o dentro de un toolbox y la opción de editar desaparece.

![sin edición](/Images/desconexion2.png)

Para redireccionar la herramienta haga clic derecho sobre el script con problema de direccionamiento e ingrese en la opción propiedades.

![propiedades](/Images/desconexion3.png)

 Una vez allí, seleccione la pestaña Source en donde debe seleccionar el archivo de Python que lleva el nombre de la herramienta o la palabra **principal** dentro del nombre.

![ruta vacía](/Images/desconexion4.png)

![nombre del script](/Images/desconexion5.png)

 Contrario a esto, No se debe seleccionar el archivo de Python que tienen en su nombre las palabras Aux o Auxiliar.

 Una vez terminado, se debe hacer clic en aceptar.

![ruta vacía](/Images/desconexion6.png)

Ahora si se hace clic derecho sobre la herramienta, es posible editar el script.

![ruta vacía](/Images/desconexion7.png)

Si los problemas persisten, por favor escribanos un correo a atencionalusuario@upra.gov.co
