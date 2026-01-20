from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "clave_secreta"



def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="agenda_web",
        connection_timeout=3,
        use_pure=True
    )

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            con = conectar()
            cur = con.cursor(dictionary=True)
            cur.execute("SELECT * FROM usuario WHERE email = %s", (email,))
            usuario = cur.fetchone()  # Devuelve un dict con columnas

            if usuario:
                # Verificar la contraseña hasheada
                if check_password_hash(usuario["password"], password):
                    # Guardar datos en sesión
                    session["user_id"] = usuario["id"]
                    session["user_nombre"] = usuario["nombre"]
                    return redirect("/dashboard")
                else:
                    error = "❌ Contraseña incorrecta"
            else:
                error = "❌ Usuario no encontrado"

        except Exception as e:
            error = f"❌ Error inesperado: {e}"

        finally:
            if 'cur' in locals():
                cur.close()
            if 'con' in locals():
                con.close()

    return render_template("login.html", error=error)
# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        password = request.form.get("password")

        # 🔒 Hashear contraseña antes de guardar
        hash_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)

        try:
            con = conectar()
            cur = con.cursor()
            cur.execute(
                "INSERT INTO usuario (nombre, email, password) VALUES (%s, %s, %s)",
                (nombre, email, hash_password)
            )
            con.commit()
            return redirect("/login")  # Redirige al login después de registrarse
        except mysql.connector.Error as e:
            error = f"❌ Error al registrar: {e}"
        finally:
            if 'cur' in locals():
                cur.close()
            if 'con' in locals():
                con.close()

    return render_template("register.html", error=error)


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    con = conectar()
    cur = con.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM contacto WHERE usuario_id=%s",
        (session["user_id"],)
    )
    contactos = cur.fetchall()
    con.close()

    return render_template("dashboard.html", contactos=contactos)

# ---------------- NUEVO CONTACTO ----------------
@app.route("/contacto/nuevo", methods=["GET", "POST"])
def nuevo_contacto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        email = request.form["email"]

        con = conectar()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO contacto (nombre, telefono, email, usuario_id) VALUES (%s,%s,%s,%s)",
            (nombre, telefono, email, session["user_id"])
        )
        con.commit()
        con.close()
        return redirect("/dashboard")

    return render_template("contacto_form.html")

# ---------------- EDITAR CONTACTO ----------------
@app.route("/contacto/editar/<int:id>", methods=["GET", "POST"])
def editar_contacto(id):
    con = conectar()
    cur = con.cursor(dictionary=True)

    if request.method == "POST":
        cur.execute(
            "UPDATE contacto SET nombre=%s, telefono=%s, email=%s WHERE id=%s",
            (request.form["nombre"], request.form["telefono"], request.form["email"], id)
        )
        con.commit()
        con.close()
        return redirect("/dashboard")

    cur.execute("SELECT * FROM contacto WHERE id=%s", (id,))
    contacto = cur.fetchone()
    con.close()
    return render_template("contacto_form.html", contacto=contacto)

# ---------------- ELIMINAR ----------------
@app.route("/contacto/eliminar/<int:id>")
def eliminar_contacto(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM contacto WHERE id=%s", (id,))
    con.commit()
    con.close()
    return redirect("/dashboard")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
