// === Gestion des notifications (son, vibration, visuel) ===

// 🔊 Lecture d’un son quand un message bot est ajouté
function jouerSonNotification() {
    const audio = new Audio('/static/sounds/notification.mp3');
    audio.play().catch(e => console.warn("Erreur audio:", e));
}

// 📳 Vibration sur mobile
function vibrerSiSupporté() {
    if (navigator.vibrate) {
        navigator.vibrate(200); // Vibre 200ms
    }
}

// 🔔 Notification flottante si onglet n’est pas actif
function notifierVisuellement(message = "Nouvelle réponse du bot") {
    if (!document.hasFocus()) {
        const notif = $('<div></div>')
            .addClass('notification-toast')
            .text(message)
            .hide()
            .fadeIn(300)
            .delay(2500)
            .fadeOut(300, function () { $(this).remove(); });

        $('body').append(notif);
    }
}

// 🔔 CSS de la notification toast
$("<style>")
    .prop("type", "text/css")
    .html(`
    .notification-toast {
        position: fixed;
        bottom: 100px;
        right: 20px;
        background-color: #28a745;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        z-index: 9999;
        font-weight: bold;
    }
`)
.appendTo("head");

// === À appeler dans chat.js quand un message bot est affiché ===
function declencherNotificationGlobale() {
    jouerSonNotification();
    vibrerSiSupporté();
    notifierVisuellement();
}
