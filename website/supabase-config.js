// Supabase publishable keys are safe for browser use. Row Level Security
// protects private Eden data; never place a Supabase service-role key here.
window.EDEN_SUPABASE_URL = 'https://ppzdymxnpjuwhdzchafn.supabase.co';
window.EDEN_SUPABASE_PUBLISHABLE_KEY = 'sb_publishable_QHZKh4wrSIvTcSPhWm_0LQ_KGh0Lh6v';

// Billing sessions are created server-side by Supabase Edge Functions. Never
// place a Stripe secret key in this browser file.
window.EDEN_BILLING_FUNCTION_BASE =
  `${window.EDEN_SUPABASE_URL}/functions/v1`;

// This is the deployed Eden application, not a local-development address.
window.EDEN_APP_URL = 'https://znrmfh8pgum4zdufs6hexz.streamlit.app/';

// Always enter through Eden's account-switching login page. This prevents a
// website user from being dropped into a different Eden account whose app
// session was already saved on the Streamlit domain.
window.EDEN_APP_LOGIN_URL = `${window.EDEN_APP_URL}Login`;
