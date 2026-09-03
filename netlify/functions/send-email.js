// Netlify Function: send-email
//
// This runs on Netlify's server, never in the browser. It holds the
// Brevo API key as an environment variable (set in the Netlify site
// dashboard, NOT in this file and NOT in the repo), and forwards the
// PDF attachment + recipient details to Brevo's transactional email API.
//
// The front-end (index.html) calls this function at:
//   /.netlify/functions/send-email
// instead of calling Brevo directly, so the API key is never exposed
// in page source.

exports.handler = async function (event) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const BREVO_API_KEY = process.env.BREVO_API_KEY;
  const RECIPIENT_EMAIL = 'neromaria.pinoyhomesadelaide@gmail.com';
  const SENDER_EMAIL = 'neromaria.pinoyhomesadelaide@gmail.com';
  const SENDER_NAME = 'pinoyhomes';

  if (!BREVO_API_KEY) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'BREVO_API_KEY is not configured on the server.' })
    };
  }

  let data;
  try {
    data = JSON.parse(event.body || '{}');
  } catch (e) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Invalid JSON body.' }) };
  }

  const { filename, pdfBase64, applicantName } = data;

  if (!filename || !pdfBase64) {
    return { statusCode: 400, body: JSON.stringify({ error: 'filename and pdfBase64 are required.' }) };
  }

  const payload = {
    sender: { name: SENDER_NAME, email: SENDER_EMAIL },
    to: [{ email: RECIPIENT_EMAIL }],
    subject: 'Needs Analysis Submission — ' + (applicantName || 'Needs Analysis Submission'),
    htmlContent: '<p>Please find the completed Needs Analysis for <strong>' +
      (applicantName || 'the applicant') + '</strong> attached.</p>',
    attachment: [{ name: filename, content: pdfBase64 }]
  };

  try {
    const response = await fetch('https://api.brevo.com/v3/smtp/email', {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'content-type': 'application/json',
        'api-key': BREVO_API_KEY
      },
      body: JSON.stringify(payload)
    });

    const resultText = await response.text();

    if (!response.ok) {
      return { statusCode: response.status, body: resultText };
    }

    return { statusCode: 200, body: resultText };
  } catch (error) {
    return { statusCode: 500, body: JSON.stringify({ error: String(error) }) };
  }
};
