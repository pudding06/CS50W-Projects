document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Submit handler
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function viewEmail(id){
  console.log(id);
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(email);

    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
    
    document.querySelector('#email-view').innerHTML = `
      <ul class="list-group">
        <li class="list-group-item">From: ${email.sender}</li>
        <li class="list-group-item">To: ${email.recipients}</li>
        <li class="list-group-item">Subject: ${email.subject}</li>
        <li class="list-group-item">Time: ${email.timestamp}</li>
        <li class="list-group-item">${email.body}</li>
      </ul>
    `;

    fetch(`/emails/${email.id}}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })

    const button_archived = document.createElement('button');
    button_archived.innerHTML = email.archived ? "Unarchived" : "Archived";
    button_archived.className = email.archived ? "btn btn-success" : "btn btn-danger";
    button_archived.addEventListener('click', function() {
      fetch(`/emails/${email.id}}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !email.archived
        })
      })
      .then(() => {
        load_mailbox('archive')
      })
      });
    document.querySelector('#email-view').append(button_archived);
    });

    // Reply logic
    const button_reply = document.createElement('button');
    button_reply.innerHTML = "Reply";
    button_reply.className = "btn btn-info";
    button_reply.addEventListener('click', function() {
      console.log("reply sent")
    });
    document.querySelector('#email-view').append(button_reply);

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      emails.forEach(email => {
        const newemail = document.createElement('div');
        newemail.className = "list-group-item";
        newemail.innerHTML = `
          <h6>Sender: ${email.sender}</h6>
          <p>Subject: ${email.subject}</p>
          <p>${email.timestamp}</p>
        `;

        newemail.className = email.read ? 'read' : 'unread';

        newemail.addEventListener('click',() => {viewEmail(email.id)});
        document.querySelector('#emails-view').append(newemail);
      })
  });
}

function send_email(){
  recipients = document.querySelector("#compose-recipients").value;
  subject = document.querySelector("#compose-subject").value;
  body = document.querySelector('#compose-body').value;
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  })
}
