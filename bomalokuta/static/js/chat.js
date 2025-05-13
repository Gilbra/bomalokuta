// static/js/chat.js

$(function() {
  const chatContainer = $('#chat-container');
  let lastUserText = '';

  function ajouterMessage(content, type) {
    const messageDiv = $('<div></div>')
      .addClass('d-flex mb-3 align-items-start')
      .addClass(type === 'user' ? 'justify-content-end' : 'justify-content-start');
    const avatar = $('<div></div>').addClass('me-2').html(
      type === 'user'
        ? '<i class="fas fa-user-circle fa-2x text-primary"></i>'
        : '<i class="fas fa-robot fa-2x text-success"></i>'
    );
    const bubble = $('<div></div>')
      .addClass('p-3 rounded shadow-sm')
      .addClass(type === 'user' ? 'bg-primary text-white' : 'bg-white text-dark')
      .css({ 'max-width': '75%', 'white-space': 'pre-wrap' })
      .html(content);

    if (type === 'user') {
      messageDiv.append(bubble).append(avatar);
    } else {
      messageDiv.append(avatar).append(bubble);
    }

    chatContainer.append(messageDiv);
    chatContainer.scrollTop(chatContainer[0].scrollHeight);
  }

  function afficherAnimationFrappe() {
    const typingDiv = $('<div></div>')
      .addClass('d-flex mb-3 align-items-start justify-content-start')
      .attr('id', 'typing');
    typingDiv.append(
      $('<div></div>')
        .addClass('me-2')
        .html('<i class="fas fa-robot fa-2x text-success"></i>'),
      $('<div></div>')
        .addClass('p-3 rounded shadow-sm bg-white text-muted')
        .html('<i class="fas fa-ellipsis-h fa-fade"></i>')
    );
    chatContainer.append(typingDiv);
    chatContainer.scrollTop(chatContainer[0].scrollHeight);
  }

  function supprimerAnimationFrappe() {
    $('#typing').remove();
  }

  $('#analyseForm').on('submit', function(e) {
    e.preventDefault();
    const texte = $('#texteAAnalyser').val().trim();
    if (!texte) return;

    lastUserText = texte;                // conserve en cas de timeout
    ajouterMessage(texte, 'user');
    $('#texteAAnalyser').val('').prop('disabled', true);
    $('button[type=submit]').prop('disabled', true);
    afficherAnimationFrappe();

    // envoi initial
    $.ajax({
      url: "/bomalokuta/api/analyze/",
      method: "POST",
      contentType: "application/json",
      headers: { "X-CSRFToken": "{{ csrf_token }}" },
      data: JSON.stringify({ text: texte }),
      success: function(data) {
        const taskId = data.task_id;
        console.log("taskId reçu:", taskId);

        let attempts = 0,
            maxAttempts = 15; // essais max (≈30 s)
        const interval = setInterval(function() {
          attempts++;
          if (attempts >= maxAttempts) {
            clearInterval(interval);
            supprimerAnimationFrappe();
            ajouterMessage("Le serveur ne répond pas, réessaie plus tard.", 'bot');
            // réactive le champ avec le texte initial
            $('#texteAAnalyser').prop('disabled', false).val(lastUserText);
            $('button[type=submit]').prop('disabled', false);
            return;
          }

          console.log("Polling status pour", taskId);
          $.get(`/bomalokuta/api/analyze/${taskId}/`, function(res) {
            console.log("Réponse polling:", res);
            if (res.status === 'done') {
              clearInterval(interval);
              supprimerAnimationFrappe();
              ajouterMessage(res.result, 'bot');
              $('#texteAAnalyser').prop('disabled', false);
              $('button[type=submit]').prop('disabled', false);
            }
          }).fail(function() {
            // en cas d’erreur temporaire, on retente jusqu’au timeout
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
