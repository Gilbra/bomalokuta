$(function () {
  const chatContainer = $('#chat-container');
  let lastUserText = '';

  function ajouterMessage(content, type) {
    const messageDiv = $('<div></div>')
      .addClass('d-flex mb-3 align-items-start fade-in')
      .addClass(type === 'user' ? 'justify-content-end' : 'justify-content-start');

    const avatar = $('<div></div>').addClass('me-2')
      .html(type === 'user'
        ? '<i class="fas fa-user-circle fa-2x text-primary"></i>'
        : '<i class="fas fa-robot fa-2x text-success"></i>');

    const bubble = $('<div></div>')
      .addClass('p-3 rounded shadow-sm')
      .addClass(type === 'user' ? 'bg-primary text-white' : 'bg-light text-dark')
      .css({
        'max-width': '75%',
        'white-space': 'pre-wrap',
        'animation': 'pop 0.3s ease-out'
      })
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
    if ($('#typing').length > 0) return;

    const typingDiv = $('<div></div>')
      .attr('id', 'typing')
      .addClass('d-flex mb-3 align-items-start justify-content-start');

    const avatar = $('<div></div>').addClass('me-2')
      .html('<i class="fas fa-robot fa-2x text-success"></i>');

    const bubble = $('<div></div>')
      .addClass('p-3 rounded shadow-sm bg-light text-muted')
      .html('<span class="dotting"></span>');

    typingDiv.append(avatar).append(bubble);
    chatContainer.append(typingDiv);
    chatContainer.scrollTop(chatContainer[0].scrollHeight);
  }

  function supprimerAnimationFrappe() {
    $('#typing').remove();
  }

  function formaterResultat(result) {
    if (typeof result === 'string') return result; // fallback texte brut

    const verdict = `<strong>🕵️ Verdict :</strong> ${result.verdict || 'Inconnu'}`;
    const score = `<strong>🔍 Confiance :</strong> ${result.score ?? 'N/A'}%`;
    const explication = `<strong>💬 Explication :</strong> ${result.explication || '...'}`;
    const sources = result.sources && result.sources.length
      ? `<strong>📚 Sources :</strong><br><ul>${result.sources.map(s => `<li><a href="${s}" target="_blank">${s}</a></li>`).join('')}</ul>`
      : `<strong>📚 Sources :</strong> Aucune`;

    return `${verdict}<br>${score}<br>${explication}<br>${sources}`;
  }

  $('#analyseForm').on('submit', function (e) {
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
      success: function (data) {
        const afficher = (res) => {
          supprimerAnimationFrappe();
          ajouterMessage(formaterResultat(res), 'bot');
          $('#texteAAnalyser').prop('disabled', false).val('');
          $('button[type=submit]').prop('disabled', false);
        };

        if (data.status === 'done') {
          return afficher(data.result);
        }

        const taskId = data.task_id;
        let attempts = 0, maxAttempts = 15;

        const interval = setInterval(() => {
          if (++attempts >= maxAttempts) {
            clearInterval(interval);
            supprimerAnimationFrappe();
            ajouterMessage("⚠️ L'IA est temporairement indisponible. Veuillez réessayer plus tard.", 'bot');
            $('#texteAAnalyser').prop('disabled', false).val(lastUserText);
            $('button[type=submit]').prop('disabled', false);
            return;
          }

          $.get(`/bomalokuta/api/analyze/${taskId}/`, function (res) {
            if (res.status === 'done') {
              clearInterval(interval);
              afficher(res.result);
            } else if (res.status === 'error') {
              clearInterval(interval);
              supprimerAnimationFrappe();
              ajouterMessage("⚠️ Une erreur est survenue : " + (res.result?.error || "Analyse échouée."), 'bot');
              $('#texteAAnalyser').prop('disabled', false).val(lastUserText);
              $('button[type=submit]').prop('disabled', false);
            }
          }).fail(function () {
            console.warn("Erreur de polling...");
          });
        }, 2000);
      },
      error: function (xhr) {
        supprimerAnimationFrappe();
        const errMsg = xhr.responseJSON?.message || "Erreur lors de la requête.";
        ajouterMessage(`<strong>Erreur :</strong> ${errMsg}`, 'bot');
        $('#texteAAnalyser').prop('disabled', false).val(lastUserText);
        $('button[type=submit]').prop('disabled', false);
      }
    });
  });
});
