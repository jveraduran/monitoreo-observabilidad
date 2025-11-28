// Importa el framework Express
const express = require('express');
// Crea una instancia de la aplicación Express
const app = express();
// Define el puerto en el que se ejecutará el servidor
const port = 3000;

// Define un manejador de ruta para la página de inicio (/)
app.get('/', (req, res) => {
  // Envía una respuesta de texto al cliente
  res.send('¡Hola Mundo desde Express en el puerto ' + port + '!');
});

// Nueva ruta para simular un Error 500 (Internal Server Error)
app.get('/error-500', (req, res, next) => {
  console.error('Simulando un error 500 intencionalmente...');
  // Simular un error lanzando una excepción. 
  // Express captura esto y envía un estado 500 por defecto.
  throw new Error('¡Algo salió muy mal en el servidor! (Error 500 simulado)');
  
  // Nota: Si usaras lógica asíncrona (como promesas o async/await), 
  // necesitarías usar next(error) para pasar el error al manejador de errores de Express.
  // Ejemplo asíncrono: Promise.reject(new Error('...')).catch(next);
});

// Se puede añadir un middleware de manejo de errores explícito (opcional)
// que debe tener exactamente cuatro argumentos (err, req, res, next)
app.use((err, req, res, next) => {
  console.error('Manejador de errores atrapó:', err.stack);
  // Se asegura de que la respuesta sea 500 si no se ha enviado otra respuesta antes
  res.status(500).send({
    message: 'Error Interno del Servidor (500)',
    error: process.env.NODE_ENV === 'production' ? {} : err.message // Oculta detalles del error en producción
  });
});


// Inicia el servidor y escucha en el puerto especificado
app.listen(port, () => {
  // Mensaje que se muestra en la consola al iniciar el servidor
  console.log(`La aplicación está corriendo en http://localhost:${port}`);
  console.log('Ruta de prueba para simular error 500: http://localhost:${port}/error-500');
  console.log('Presiona Ctrl+C para detener el servidor.');
});