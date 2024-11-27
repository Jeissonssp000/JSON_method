# Guía para Construir una Aplicación Python con PyInstaller

Este documento describe cómo crear un ejecutable de una aplicación Python utilizando **PyInstaller** en sistemas operativos **Windows**, **Linux**, y **macOS**.

## Tecnologías Utilizadas

### PyInstaller
**PyInstaller** es una herramienta que permite empaquetar programas escritos en Python en un solo ejecutable, lo que facilita la distribución a otros usuarios sin necesidad de instalar Python ni otras dependencias adicionales. PyInstaller funciona en múltiples plataformas, incluyendo Windows, Linux y macOS, creando ejecutables específicos para cada sistema operativo.

### Entornos Soportados
- **Windows**: Genera archivos `.exe` que pueden ejecutarse directamente en sistemas Windows.
- **Linux**: Genera archivos ejecutables nativos de Linux sin extensión.
- **macOS**: Genera aplicaciones `.app` que pueden ejecutarse en sistemas macOS.

## Requisitos Previos para el Repo
- **Python 3.12.7** debe estar instalado en el sistema. (opt: pyenv ;D)
- **Paquetes** instalar con:
   ```bash
   pip install PyQt5 pyinstaller pygame pandas
   ```

## Instrucciones para Generar un Ejecutable

### Ejecutable
**Crear el Ejecutable**:   
   ```bash
   pyinstaller --onefile app.py
   ```

**Ubicar el Ejecutable**:
   - Buscar el archivo generado en la carpeta `dist/`.

**Opcional windows, Sin Consola**:
   Si no desea que se muestre la consola de Windows al ejecutar la aplicación, agregar el flag `--noconsole`:
   
   ```bash
   pyinstaller --onefile --noconsole app.py
   ```

**Opcional macOS**:
   - En macOS, también se puede convertir en un paquete `.app` si se necesita una experiencia más nativa.

## Resumen
- **Windows**: Utilizar `pyinstaller --onefile app.py` para generar un `.exe`.
- **Linux y macOS**: Utilizar `pyinstaller --onefile app.py` para generar un ejecutable nativo.
- **Distribución**: Los archivos generados en la carpeta `dist/` son independientes y pueden ser distribuidos a los usuarios sin tener que instalar nada.
