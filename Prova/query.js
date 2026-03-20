const db = require("./db");

// LISTAR
function listar() {
  db.query("SELECT * FROM Disciplinas", (err, result) => {
    if (err) throw err;
    console.log(result);
  });
}

// INSERIR (atividade 02)
function inserir() {
  const sql = `
    INSERT INTO Disciplinas (descricao, cargaHoraria, nomeProfessor)
    VALUES ("Linguagem de Programação back-end", "120", "Pedro Vieira")
  `;

  db.query(sql, (err) => {
    if (err) throw err;
    console.log("Inserido com sucesso!");
  });
}

// ATUALIZAR
function atualizar() {
  db.query(
    'UPDATE Disciplinas SET nomeProfessor="João" WHERE codDisciplina=1',
    (err) => {
      if (err) throw err;
      console.log("Atualizado!");
    }
  );
}

// DELETAR
function deletar() {
  db.query(
    "DELETE FROM Disciplinas WHERE codDisciplina=4",
    (err) => {
      if (err) throw err;
      console.log("Deletado!");
    }
  );
}

module.exports = { listar, inserir, atualizar, deletar };
