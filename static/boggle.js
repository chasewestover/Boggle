"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  let response = await axios.get("/api/new-game");
  gameId = response.data.gameId;
  console.log(response.data);
  let board = response.data.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();
  const body = $('<tbody>');
  for (let i = 0; i < board.length; i++) {
    const row = $('<tr>');
    for (let j = 0; j < board.length; j++) {
      row.append( $('<td>').text(board[i][j]) );
    }
    body.append(row)
  }
  $table.append(body)
}

function displayResult(word, wordResult) {
  $wordInput.val('')
  if (wordResult.result === "ok") {
    $playedWords.append(`<li>${word}</li>`);
    $message.text("");
  } else {
    $message.text(`This is ${wordResult.result}`);
  }
}

start();
$form.on("submit", async function (e) {
  e.preventDefault();
  let word = $wordInput.val();
  let wordResult = await axios({
    method: "post",
    url: "/api/score-word",
    data: { gameId, word }
  });
  displayResult(word, wordResult.data);
});


