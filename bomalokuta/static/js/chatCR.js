// static/js/chat.js

$(function() {
  const chatContainer = $('#chat-container');
  let lastUserText = '';

  function ajouterMessage(content, type) { /* … */ }
  function afficherAnimationFrappe()    { /* … */ }
  function supprimerAnimationFrappe()   { /* … */ }

  $('#analyseForm').on('submit', function(e) {
    e.preventDefault();
    const texte = $('#texteAAnalyser').val().trim();
    if (!texte) return;

    lastUserText = texte;
    ajouterMessage(texte, 'user');
    $('#texteAAnalyser').val('').prop('disabled', true);
    $('button[type=submit]').prop('disabled', true);
    afficherAnimationFrappe();

    $.ajax({
      url: "/bomalokuta/api/analyze/",
      method: "POST",
      contentType: "application/json",
      headers: { "X-CSRFToken": "{{ csrf_token }}" },
      data: JSON.stringify({ text: texte }),
      success: function(data) {
        if (data.status === 'done') {
          // réponse immédiate
          supprimerAnimationFrappe();
          ajouterMessage(data.result, 'bot');
          $('#texteAAnalyser').prop('disabled', false).val('');
          $('button[type=submit]').prop('disabled', false);
          return;
        }
        // sinon on poll
        const taskId = data.task_id;
        let attempts = 0, maxAttempts = 15;
        const interval = setInterval(function() {
          if (++attempts >= maxAttempts) {
            clearInterval(interval);
            supprimerAnimationFrappe();
            ajouterMessage("Le serveur ne répond pas, réessaie plus tard.", 'bot');
            $('#texteAAnalyser').prop('disabled', false).val(lastUserText);
            $('button[type=submit]').prop('disabled', false);
            return;
          }
          $.get(`/bomalokuta/api/analyze/${taskId}/`, function(res) {
            if (res.status === 'done') {
              clearInterval(interval);
              supprimerAnimationFrappe();
              ajouterMessage(res.result, 'bot');
              $('#texteAAnalyser').prop('disabled', false).val('');
              $('button[type=submit]').prop('disabled', false);
            }
          }).fail(function() {
            console.warn("Erreur polling, re-tentative...");
          });
        }, 2000);
      },
      error: function(xhr) {
        supprimerAnimationFrappe();
        let errMsg = xhr.responseJSON?.message || "Erreur lors de la requête.";
        ajouterMessage(`<strong>Erreur :</strong> ${errMsg}`, 'bot');
        $('#texteAAnalyser').prop('disabled', false).val(lastUserText);
        $('button[type=submit]').prop('disabled', false);
      }
    });
  });
});

