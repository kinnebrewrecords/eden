const edenSupabase = window.supabase.createClient(
  window.EDEN_SUPABASE_URL,
  window.EDEN_SUPABASE_PUBLISHABLE_KEY
);

const authPanel = document.querySelector('#auth-panel');
const signedInPanel = document.querySelector('#signed-in-panel');
const accountEmail = document.querySelector('#account-email');
const authMessage = document.querySelector('#auth-message');
const authForms = document.querySelectorAll('.auth-form');
const billingMessage = document.querySelector('#billing-message');
const accessTitle = document.querySelector('#access-title');
const accessDetail = document.querySelector('#access-detail');
const workspaceButton = document.querySelector('#open-workspace-button');
let recoveryMode = false;

async function callBillingFunction(name) {
  const { data: { session } } = await edenSupabase.auth.getSession();
  if (!session) throw new Error('Sign in before managing your subscription.');

  const response = await fetch(`${window.EDEN_BILLING_FUNCTION_BASE}/${name}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${session.access_token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ return_url: window.location.href.split('?')[0] })
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok || !payload.url) {
    throw new Error(payload.error || 'Billing is temporarily unavailable.');
  }
  window.location.assign(payload.url);
}

function showMessage(message, type = 'info') {
  authMessage.hidden = false;
  authMessage.className = `auth-message ${type}`;
  authMessage.textContent = message;
}

function showBillingMessage(message, type = 'info') {
  billingMessage.hidden = false;
  billingMessage.className = `auth-message ${type}`;
  billingMessage.textContent = message;
}

function setSignedInView(user) {
  const isSignedIn = Boolean(user);
  authPanel.hidden = recoveryMode ? false : isSignedIn;
  signedInPanel.hidden = recoveryMode ? true : !isSignedIn;
  if (isSignedIn) {
    accountEmail.textContent = user.email;
    refreshAccess();
  }
}

function setAccessView(access) {
  const hasAccess = Boolean(access?.has_access);
  workspaceButton.disabled = !hasAccess;
  workspaceButton.classList.toggle('text-action-disabled', !hasAccess);

  if (hasAccess) {
    const type = access.access_type === 'beta' ? 'Beta access active' : 'Subscription active';
    accessTitle.textContent = type;
    accessDetail.textContent = 'Your Eden access is active. Continue to your workspace. If this browser is not already signed in to Eden, use this same email there.';
    workspaceButton.textContent = 'Continue to my workspace';
  } else {
    accessTitle.textContent = 'No active access yet';
    accessDetail.textContent = 'Start a trial or redeem a private beta code to unlock Eden.';
    workspaceButton.textContent = 'Available with access';
  }
}

async function refreshAccess() {
  const { data, error } = await edenSupabase.rpc('get_eden_access');
  if (error) {
    setAccessView(null);
    return;
  }
  setAccessView(data);
}

function showAuthForm(formId) {
  authForms.forEach((form) => {
    form.hidden = form.id !== formId;
  });
}

function isStrongPassword(password) {
  return password.length >= 8;
}

function setActiveTab(tabName) {
  document.querySelectorAll('[data-auth-tab]').forEach((button) => {
    button.classList.toggle('active', button.dataset.authTab === tabName);
  });
  showAuthForm(tabName === 'signup' ? 'sign-up-form' : 'sign-in-form');
  authMessage.hidden = true;
}

document.querySelectorAll('[data-auth-tab]').forEach((button) => {
  button.addEventListener('click', () => setActiveTab(button.dataset.authTab));
});

document.querySelector('#forgot-password-button').addEventListener('click', () => {
  recoveryMode = false;
  authPanel.hidden = false;
  showAuthForm('reset-request-form');
  authMessage.hidden = true;
});

document.querySelector('#back-to-sign-in-button').addEventListener('click', () => {
  setActiveTab('signin');
});

document.querySelector('#sign-in-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const email = document.querySelector('#sign-in-email').value.trim();
  const password = document.querySelector('#sign-in-password').value;
  const { data, error } = await edenSupabase.auth.signInWithPassword({ email, password });
  if (error) return showMessage('We could not sign you in. Check your email and password.', 'error');
  setSignedInView(data.user);
});

document.querySelector('#sign-up-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const email = document.querySelector('#sign-up-email').value.trim();
  const password = document.querySelector('#sign-up-password').value;
  const confirmation = document.querySelector('#sign-up-password-confirm').value;

  if (!isStrongPassword(password)) {
    return showMessage(
      'Use at least 8 characters for your password.',
      'error'
    );
  }

  if (password !== confirmation) {
    return showMessage('The passwords do not match. Please re-enter them.', 'error');
  }
  const options = {};
  if (window.location.protocol.startsWith('http')) {
    options.emailRedirectTo = `${window.location.origin}${window.location.pathname}`;
  }
  const { data, error } = await edenSupabase.auth.signUp({ email, password, options });
  if (error) return showMessage(error.message, 'error');
  if (data.session) return setSignedInView(data.user);
  setActiveTab('signin');
  showMessage('Check your email to confirm your account, then return here to sign in.', 'success');
});

document.querySelector('#reset-request-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const email = document.querySelector('#reset-email').value.trim();
  const redirectTo = `${window.location.origin}${window.location.pathname}`;
  const { error } = await edenSupabase.auth.resetPasswordForEmail(email, { redirectTo });

  if (error) return showMessage('We could not send the reset email. Please try again.', 'error');

  setActiveTab('signin');
  showMessage('If an Eden account uses that email, a password-reset link is on its way.', 'success');
});

document.querySelector('#update-password-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const password = document.querySelector('#new-password').value;
  const confirmation = document.querySelector('#confirm-password').value;

  if (password.length < 8) return showMessage('Use at least 8 characters.', 'error');
  if (password !== confirmation) return showMessage('The passwords do not match.', 'error');

  const { error } = await edenSupabase.auth.updateUser({ password });
  if (error) return showMessage('We could not update your password. Request a new reset link and try again.', 'error');

  await edenSupabase.auth.signOut();
  recoveryMode = false;
  setSignedInView(null);
  setActiveTab('signin');
  showMessage('Password updated. Sign in with your new password.', 'success');
});

document.querySelector('#sign-out-button').addEventListener('click', async () => {
  await edenSupabase.auth.signOut();
  setSignedInView(null);
  setActiveTab('signin');
  showMessage('You have been signed out.', 'success');
});

document.querySelector('#start-subscription-button').addEventListener('click', async () => {
  showBillingMessage('Opening secure Stripe checkout…');
  try {
    await callBillingFunction('create-checkout-session');
  } catch (error) {
    showBillingMessage(error.message, 'error');
  }
});

document.querySelector('#manage-billing-button').addEventListener('click', async () => {
  showBillingMessage('Opening secure billing management…');
  try {
    await callBillingFunction('create-portal-session');
  } catch (error) {
    showBillingMessage(error.message, 'error');
  }
});

document.querySelector('#open-workspace-button').addEventListener('click', () => {
  if (!workspaceButton.disabled && window.EDEN_APP_LOGIN_URL) {
    window.location.assign(window.EDEN_APP_LOGIN_URL);
  }
});

document.querySelector('#beta-code-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const code = document.querySelector('#beta-code').value.trim();
  const { data, error } = await edenSupabase.rpc('redeem_eden_beta_code', {
    p_code: code
  });

  if (error) {
    showBillingMessage(error.message || 'That beta code could not be redeemed.', 'error');
    return;
  }

  document.querySelector('#beta-code').value = '';
  setAccessView(data);
  showBillingMessage('Beta access activated. You can now sign in to the Eden app.', 'success');
});

edenSupabase.auth.onAuthStateChange((event, session) => {
  if (event === 'PASSWORD_RECOVERY') {
    recoveryMode = true;
    authPanel.hidden = false;
    showAuthForm('update-password-form');
    showMessage('Choose a new password for your Eden account.', 'success');
    return;
  }

  setSignedInView(session?.user ?? null);
});

if (new URLSearchParams(window.location.search).has('code')) {
  setActiveTab('signup');
  showMessage(
    'Create an Eden account or sign in first. You can redeem your code from your account page.',
    'info'
  );
}

edenSupabase.auth.getUser().then(({ data }) => setSignedInView(data.user ?? null));

const checkoutResult = new URLSearchParams(window.location.search).get('checkout');
if (checkoutResult === 'success') {
  showBillingMessage('Payment received. Activating your Eden workspace…', 'success');
  let attempts = 0;
  const accessTimer = window.setInterval(async () => {
    attempts += 1;
    await refreshAccess();
    if (!workspaceButton.disabled || attempts >= 10) {
      window.clearInterval(accessTimer);
      showBillingMessage(
        workspaceButton.disabled
          ? 'Activation is taking longer than expected. Refresh this page in a moment or contact support.'
          : 'Your Eden subscription is active. You can open your workspace now.',
        workspaceButton.disabled ? 'info' : 'success'
      );
    }
  }, 1500);
} else if (checkoutResult === 'cancelled') {
  showBillingMessage('Checkout was cancelled. Your account was not charged.', 'info');
}
