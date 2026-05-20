from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "hd5wk30ldhw9h44kjh"

DB_NAME = "helpdesk_db"

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "escola"
}


def conectar(usar_banco=True):
    config = db_config.copy()

    if usar_banco:
        config["database"] = DB_NAME

    return mysql.connector.connect(**config)


def inicializar_banco():
    try:
        conexao = conectar(usar_banco=False)
        cursor = conexao.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME} "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )

        cursor.execute(f"USE {DB_NAME}")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tecnicos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(120) NOT NULL UNIQUE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chamados (
                id INT AUTO_INCREMENT PRIMARY KEY,
                equipamento VARCHAR(150) NOT NULL,
                problema TEXT NOT NULL,
                nivel ENUM('Alto', 'Médio', 'Baixo') NOT NULL,
                tecnico_id INT NOT NULL,
                status ENUM('aberto', 'finalizado') NOT NULL DEFAULT 'aberto',
                criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                finalizado_em DATETIME NULL,

                FOREIGN KEY (tecnico_id) REFERENCES tecnicos(id)
            )
        """)

        tecnicos_iniciais = ["João", "Maria", "Carlos"]

        for tecnico in tecnicos_iniciais:
            cursor.execute(
                "INSERT IGNORE INTO tecnicos (nome) VALUES (%s)",
                (tecnico,)
            )

        conexao.commit()

    except Error as erro:
        print(f"Erro ao inicializar banco: {erro}")

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()


@app.route("/")
def index():
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("SELECT * FROM tecnicos ORDER BY nome")
        tecnicos = cursor.fetchall()

        cursor.execute("""
            SELECT
                c.id,
                c.equipamento,
                c.problema,
                c.nivel,
                c.status,
                c.criado_em,
                c.finalizado_em,
                t.nome AS tecnico_nome
            FROM chamados c
            INNER JOIN tecnicos t ON t.id = c.tecnico_id
            ORDER BY
                CASE WHEN c.status = 'aberto' THEN 0 ELSE 1 END,
                c.id DESC
        """)
        chamados = cursor.fetchall()

        cursor.execute("""
            SELECT
                t.nome,
                COUNT(c.id) AS total_chamados,
                COALESCE(SUM(CASE WHEN c.status = 'finalizado' THEN 1 ELSE 0 END), 0) AS chamados_finalizados
            FROM tecnicos t
            LEFT JOIN chamados c ON c.tecnico_id = t.id
            GROUP BY t.id, t.nome
            ORDER BY chamados_finalizados DESC, total_chamados DESC, t.nome ASC
        """)
        ranking = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) AS total FROM chamados")
        total_chamados = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM chamados WHERE status = 'aberto'")
        chamados_abertos = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM chamados WHERE status = 'finalizado'")
        chamados_finalizados = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM chamados WHERE nivel = 'Alto'")
        chamados_altos = cursor.fetchone()["total"]

        dados_dashboard = {
            "total_chamados": total_chamados,
            "chamados_abertos": chamados_abertos,
            "chamados_finalizados": chamados_finalizados,
            "chamados_altos": chamados_altos
        }

        return render_template(
            "index.html",
            tecnicos=tecnicos,
            chamados=chamados,
            ranking=ranking,
            dados_dashboard=dados_dashboard
        )

    except Error as erro:
        return f"Erro no banco de dados: {erro}"

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()


@app.route("/cadastrar-tecnico", methods=["POST"])
def cadastrar_tecnico():
    nome = request.form.get("nome", "").strip()

    if not nome:
        flash("Informe o nome do técnico.")
        return redirect(url_for("index"))

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "INSERT INTO tecnicos (nome) VALUES (%s)",
            (nome,)
        )

        conexao.commit()
        flash("Técnico cadastrado com sucesso.")

    except Error as erro:
        flash(f"Erro ao cadastrar técnico: {erro}")

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()

    return redirect(url_for("index"))


@app.route("/criar-chamado", methods=["POST"])
def criar_chamado():
    equipamento = request.form.get("equipamento", "").strip()
    problema = request.form.get("problema", "").strip()
    nivel = request.form.get("nivel", "").strip()
    tecnico_id = request.form.get("tecnico_id", "").strip()

    if not equipamento or not problema or not nivel or not tecnico_id:
        flash("Preencha todos os campos do chamado.")
        return redirect(url_for("index"))

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO chamados
            (equipamento, problema, nivel, tecnico_id)
            VALUES (%s, %s, %s, %s)
        """, (equipamento, problema, nivel, tecnico_id))

        conexao.commit()
        flash("Chamado criado com sucesso.")

    except Error as erro:
        flash(f"Erro ao criar chamado: {erro}")

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()

    return redirect(url_for("index"))


@app.route("/finalizar-chamado/<int:id_chamado>", methods=["POST"])
def finalizar_chamado(id_chamado):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE chamados
            SET status = 'finalizado',
                finalizado_em = NOW()
            WHERE id = %s
              AND status = 'aberto'
        """, (id_chamado,))

        conexao.commit()

        if cursor.rowcount > 0:
            flash("Chamado finalizado com sucesso.")
        else:
            flash("Chamado não encontrado ou já finalizado.")

    except Error as erro:
        flash(f"Erro ao finalizar chamado: {erro}")

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    inicializar_banco()
    app.run(debug=True)