// Netlify Function: send-email
// Handles (1) signed Supabase upload tokens and (2) Brevo PDF notification email.
// Secrets must be configured in Netlify Environment Variables, never in browser code.

const { createClient } = require('@supabase/supabase-js');

const DEFAULT_ALLOWED_ORIGINS = [
  'https://neromariapinoyhomesadelaide.github.io',
  'https://dreamy-taiyaki-dded84.netlify.app'
];
const STORAGE_BUCKET = process.env.SUPABASE_BUCKET || 'needs-analysis-documents';
const MAX_FILE_BYTES = 10 * 1024 * 1024;
const ALLOWED_EXTENSIONS = new Set(['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx']);

function getAllowedOrigins() {
  const configured = (process.env.ALLOWED_ORIGINS || '')
    .split(',').map(x => x.trim()).filter(Boolean);
  return [...new Set([...DEFAULT_ALLOWED_ORIGINS, ...configured])];
}

function corsHeaders(event) {
  const origin = event.headers?.origin || event.headers?.Origin || '';
  const allowed = getAllowedOrigins();
  return {
    'Access-Control-Allow-Origin': allowed.includes(origin) ? origin : allowed[0],
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Vary': 'Origin',
    'Content-Type': 'application/json'
  };
}

function json(statusCode, body, headers) {
  return { statusCode, headers, body: JSON.stringify(body) };
}

function cleanName(name = 'file') {
  return String(name)
    .normalize('NFKD')
    .replace(/[^a-zA-Z0-9._-]/g, '_')
    .replace(/_+/g, '_')
    .slice(0, 140) || 'file';
}

function cleanId(id = '') {
  return String(id).replace(/[^a-zA-Z0-9_-]/g, '').slice(0, 80);
}

function escapeHtml(value = '') {
  return String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
}

exports.handler = async function (event) {
  const headers = corsHeaders(event);
  if (event.httpMethod === 'OPTIONS') return { statusCode: 200, headers, body: '' };
  if (event.httpMethod !== 'POST') return json(405, { error: 'Method Not Allowed' }, headers);

  const origin = event.headers?.origin || event.headers?.Origin || '';
  if (origin && !getAllowedOrigins().includes(origin)) {
    return json(403, { error: 'Origin not allowed.' }, headers);
  }

  let data;
  try { data = JSON.parse(event.body || '{}'); }
  catch { return json(400, { error: 'Invalid JSON body.' }, headers); }

  const SUPABASE_URL = process.env.SUPABASE_URL;
  const SUPABASE_SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
  const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY;
  if (!SUPABASE_URL || !SUPABASE_SERVICE_ROLE_KEY || !SUPABASE_ANON_KEY) {
    return json(500, { error: 'Supabase environment variables are incomplete.' }, headers);
  }
  const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, {
    auth: { persistSession: false, autoRefreshToken: false }
  });

  if (data.action === 'create-upload') {
    const submissionId = cleanId(data.submissionId);
    const fileName = cleanName(data.fileName);
    const fileSize = Number(data.fileSize || 0);
    const ext = (fileName.split('.').pop() || '').toLowerCase();
    if (!submissionId || !fileName) return json(400, { error: 'submissionId and fileName are required.' }, headers);
    if (!ALLOWED_EXTENSIONS.has(ext)) return json(400, { error: 'Unsupported file type.' }, headers);
    if (!Number.isFinite(fileSize) || fileSize <= 0 || fileSize > MAX_FILE_BYTES) {
      return json(400, { error: 'Each file must be between 1 byte and 10 MB.' }, headers);
    }

    const unique = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}-${fileName}`;
    const path = `submissions/${submissionId}/${unique}`;
    const { data: signed, error } = await supabase.storage.from(STORAGE_BUCKET).createSignedUploadUrl(path);
    if (error) return json(500, { error: 'Could not create upload link: ' + error.message }, headers);

    return json(200, {
      bucket: STORAGE_BUCKET,
      path,
      token: signed.token,
      supabaseUrl: SUPABASE_URL,
      supabaseAnonKey: SUPABASE_ANON_KEY
    }, headers);
  }

  if (data.action === 'send-email' || !data.action) {
    const BREVO_API_KEY = process.env.BREVO_API_KEY;
    const RECIPIENT_EMAIL = process.env.RECIPIENT_EMAIL || 'neromaria.pinoyhomesadelaide@gmail.com';
    const SENDER_EMAIL = process.env.SENDER_EMAIL || 'neromaria.pinoyhomesadelaide@gmail.com';
    const SENDER_NAME = process.env.SENDER_NAME || 'Pinoy Homes Adelaide';
    if (!BREVO_API_KEY) return json(500, { error: 'BREVO_API_KEY is not configured.' }, headers);

    const { filename, pdfBase64, applicantName, submissionId } = data;
    const uploadedFiles = Array.isArray(data.uploadedFiles) ? data.uploadedFiles.slice(0, 10) : [];
    if (!filename || !pdfBase64) return json(400, { error: 'filename and pdfBase64 are required.' }, headers);

    const links = [];
    for (const file of uploadedFiles) {
      if (!file?.path || !file?.name) continue;
      const { data: signed, error } = await supabase.storage.from(STORAGE_BUCKET).createSignedUrl(file.path, 60 * 60 * 24 * 7, { download: file.name });
      if (!error && signed?.signedUrl) links.push({ name: file.name, url: signed.signedUrl });
    }

    const safeApplicant = escapeHtml(applicantName || 'the applicant');
    const documentsHtml = links.length
      ? '<p><strong>Supporting documents (secure links, expire in 7 days):</strong></p><ul>' +
        links.map(f => `<li><a href="${escapeHtml(f.url)}">${escapeHtml(f.name)}</a></li>`).join('') + '</ul>'
      : (uploadedFiles.length ? '<p>Supporting documents were uploaded, but secure links could not be generated. Check Supabase Storage.</p>' : '<p>No supporting documents were uploaded.</p>');

    const payload = {
      sender: { name: SENDER_NAME, email: SENDER_EMAIL },
      to: [{ email: RECIPIENT_EMAIL }],
      subject: 'Needs Analysis Submission — ' + (applicantName || 'Needs Analysis Submission'),
      htmlContent:
        `<p>Please find the completed Needs Analysis for <strong>${safeApplicant}</strong> attached.</p>` +
        (submissionId ? `<p><strong>Submission ID:</strong> ${escapeHtml(submissionId)}</p>` : '') +
        documentsHtml,
      attachment: [{ name: cleanName(filename), content: pdfBase64 }]
    };

    try {
      const response = await fetch('https://api.brevo.com/v3/smtp/email', {
        method: 'POST',
        headers: {
          accept: 'application/json',
          'content-type': 'application/json',
          'api-key': BREVO_API_KEY
        },
        body: JSON.stringify(payload)
      });
      const resultText = await response.text();
      if (!response.ok) return { statusCode: response.status, headers, body: resultText };
      let result = {};
      try { result = JSON.parse(resultText); } catch { result = { result: resultText }; }
      return json(200, { ...result, uploadedDocumentCount: uploadedFiles.length }, headers);
    } catch (error) {
      return json(500, { error: String(error) }, headers);
    }
  }

  return json(400, { error: 'Unknown action.' }, headers);
};
