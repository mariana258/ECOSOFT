-- Base de datos ecosoft

CREATE DATABASE IF NOT EXISTS ecosoft;
USE ecosoft;

-- Tabla Roles
CREATE TABLE roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

INSERT INTO roles(nombre, descripcion) VALUES
('cliente', 'Usuario que puede retirar materiales'),
('vendedor', 'Intermediario que gestiona pedidos'),
('proveedor', 'Usuario que puede agregar stock'),
('administrador', 'Usuario con todos los permisos, exclusivo');

-- Tabla Usuarios
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    contraseña VARCHAR(255) NOT NULL,
    estado VARCHAR(20) DEFAULT 'activo',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    solicitud_rol ENUM('ninguna','pendiente','aprobada','rechazada') DEFAULT 'ninguna',
    rol_solicitado INT NULL,
    FOREIGN KEY (rol_solicitado) REFERENCES roles(id_rol)
);

-- Usuario_Roles
CREATE TABLE usuario_roles (
    usuario_id INT NOT NULL,
    rol_id INT NOT NULL,
    PRIMARY KEY(usuario_id, rol_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (rol_id) REFERENCES roles(id_rol) ON DELETE CASCADE
);

-- Materiales
CREATE TABLE materiales (
    id_material INT AUTO_INCREMENT PRIMARY KEY,
    id_proveedor INT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    unidad_medida VARCHAR(20) NOT NULL,
    precio_compra DECIMAL(10,2) NOT NULL,
    precio_venta DECIMAL(10,2) NOT NULL,
    tipo ENUM('entrada','salida') NOT NULL,
    FOREIGN KEY (id_proveedor) REFERENCES usuarios(id_usuario)
);

-- Inventario
CREATE TABLE inventario (
    id_inventario INT AUTO_INCREMENT PRIMARY KEY,
    id_material INT NOT NULL UNIQUE,
    cantidad DECIMAL(10,2) DEFAULT 0,
    stock_minimo DECIMAL(10,2) DEFAULT 0,
    ultima_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_material) REFERENCES materiales(id_material)
);

-- Historial Inventario
CREATE TABLE historial_inventario (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_material INT NOT NULL,
    id_usuario_operacion INT NOT NULL,
    rol_usuario ENUM('cliente','proveedor') NOT NULL,
    id_vendedor INT NOT NULL,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    cantidad_antes DECIMAL(10,2) NOT NULL,
    cantidad_despues DECIMAL(10,2) NOT NULL,
    precio_compra DECIMAL(10,2) NOT NULL,
    precio_venta DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_material) REFERENCES materiales(id_material),
    FOREIGN KEY (id_usuario_operacion) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_vendedor) REFERENCES usuarios(id_usuario)
);

-- Pedidos
CREATE TABLE pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_vendedor INT NULL,
    fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_programada DATETIME NULL,
    estado ENUM('pendiente','en proceso','completado','cancelado') DEFAULT 'pendiente',
    total DECIMAL(10,2) DEFAULT 0,
    observaciones TEXT,
    FOREIGN KEY (id_cliente) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_vendedor) REFERENCES usuarios(id_usuario)
);

-- Detalle Pedido
CREATE TABLE detalle_pedido (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_material INT NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_material) REFERENCES materiales(id_material)
);

-- Facturas
CREATE TABLE facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL UNIQUE,
    fecha_emision DATETIME DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    metodo_pago ENUM('efectivo','transferencia','tarjeta') NOT NULL,
    estado ENUM('pagada','pendiente','anulada') DEFAULT 'pendiente',
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido)
);

-- Pagos
CREATE TABLE pagos (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_factura INT NOT NULL,
    fecha_pago DATETIME DEFAULT CURRENT_TIMESTAMP,
    monto DECIMAL(10,2) NOT NULL,
    comprobante VARCHAR(255) NULL,
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura) ON DELETE CASCADE
);

-- Trigger admin
DELIMITER //
CREATE TRIGGER check_admin_roles
BEFORE INSERT ON usuario_roles
FOR EACH ROW
BEGIN
    DECLARE rol_admin INT;
    SELECT id_rol INTO rol_admin FROM roles WHERE nombre = 'administrador';
    IF NEW.rol_id = rol_admin THEN
        DECLARE count_admin INT;
        SELECT COUNT(*) INTO count_admin FROM usuario_roles WHERE usuario_id = NEW.usuario_id;
        IF count_admin > 0 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Un administrador no puede tener otros roles.';
        END IF;
    END IF;
END;
//
DELIMITER ;

-- Trigger historial inventario
DELIMITER //
CREATE TRIGGER log_movimiento_inventario
AFTER UPDATE ON inventario
FOR EACH ROW
BEGIN
    INSERT INTO historial_inventario(
        id_material, id_usuario_operacion, rol_usuario, id_vendedor,
        cantidad_antes, cantidad_despues, precio_compra, precio_venta
    ) VALUES (
        NEW.id_material,
        @usuario_operacion,
        @rol_usuario,
        @id_vendedor,
        OLD.cantidad,
        NEW.cantidad,
        (SELECT precio_compra FROM materiales WHERE id_material = NEW.id_material),
        (SELECT precio_venta FROM materiales WHERE id_material = NEW.id_material)
    );
END;
//
DELIMITER ;