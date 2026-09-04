import Stripe from 'npm:stripe@18.5.0';
import { createClient } from 'jsr:@supabase/supabase-js@2';
import { corsHeaders, json } from '../_shared/cors.ts';

Deno.serve(async (request) => {
  if (request.method === 'OPTIONS') return new Response('ok', { headers: corsHeaders });
  if (request.method !== 'POST') return json({ error: 'Method not allowed.' }, 405);

  try {
    const authorization = request.headers.get('Authorization') || '';
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_ANON_KEY')!,
      { global: { headers: { Authorization: authorization } } }
    );
    const { data: { user }, error } = await supabase.auth.getUser();
    if (error || !user?.email) return json({ error: 'Sign in before checkout.' }, 401);

    const { return_url } = await request.json();
    const allowedOrigin = Deno.env.get('EDEN_SITE_ORIGIN')!;
    const safeReturnUrl = new URL(return_url || allowedOrigin);
    if (safeReturnUrl.origin !== allowedOrigin) return json({ error: 'Invalid return URL.' }, 400);

    const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY')!);
    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      customer_email: user.email,
      client_reference_id: user.id,
      line_items: [{ price: Deno.env.get('STRIPE_PRICE_ID')!, quantity: 1 }],
      subscription_data: {
        metadata: { supabase_user_id: user.id },
        trial_period_days: 14
      },
      success_url: `${safeReturnUrl.toString()}?checkout=success`,
      cancel_url: `${safeReturnUrl.toString()}?checkout=cancelled`,
      allow_promotion_codes: true
    });
    return json({ url: session.url });
  } catch (error) {
    console.error(error);
    return json({ error: 'Checkout could not be started.' }, 500);
  }
});
