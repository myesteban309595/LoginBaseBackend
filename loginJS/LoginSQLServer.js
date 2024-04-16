
//* npm install mssql

// Importar las dependencias utilizando la sintaxis de módulos de ES
import express from 'express';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';
import sql from 'mssql';

const app = express();
app.use(express.json());

// Configuración para la conexión a la base de datos SQL Server
const config = {
  user: 'tu_usuario',
  password: 'tu_contraseña',
  server: 'localhost', // Puedes cambiarlo si tu SQL Server está en otro servidor
  database: 'nombre_de_tu_base_de_datos',
  options: {
    encrypt: true, // Para habilitar la encriptación de los datos
    trustServerCertificate: true // Para confiar en el certificado del servidor
  }
};

// Ruta para el registro de usuarios
app.post('/register', async (req, res) => {
  try {
    await sql.connect(config);
    const { username, password } = req.body;
    // Hashear la contraseña antes de guardarla
    const hashedPassword = await bcrypt.hash(password, 10);
    // Insertar el nuevo usuario en la base de datos
    const result = await sql.query`INSERT INTO Users (username, password) VALUES (${username}, ${hashedPassword})`;
    res.status(201).send('Usuario registrado exitosamente');
  } catch (error) {
    res.status(500).send('Error al registrar al usuario');
  } finally {
    sql.close();
  }
});

// Ruta para el inicio de sesión
app.post('/login', async (req, res) => {
  try {
    await sql.connect(config);
    const { username, password } = req.body;
    // Buscar al usuario en la base de datos
    const result = await sql.query`SELECT * FROM Users WHERE username = ${username}`;
    const user = result.recordset[0];
    if (!user) {
      return res.status(401).send('Credenciales incorrectas');
    }
    // Verificar la contraseña
    const passwordValid = await bcrypt.compare(password, user.password);
    if (!passwordValid) {
      return res.status(401).send('Credenciales incorrectas');
    }
    // Generar y enviar el token JWT
    const token = jwt.sign({ username: user.username }, 'secretKey');
    res.send({ token });
  } catch (error) {
    res.status(500).send('Error al iniciar sesión');
  } finally {
    sql.close();
  }
});

// Middleware para verificar el token JWT en las rutas protegidas
function authenticateToken(req, res, next) {
  // Implementa la verificación del token JWT aquí
}

// Ruta protegida
app.get('/protected', authenticateToken, (req, res) => {
  res.send('Esta es una ruta protegida');
});

// Iniciar el servidor
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor iniciado en el puerto ${PORT}`);
});
