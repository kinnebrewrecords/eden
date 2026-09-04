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
    if (error || !user) return json({ error: 'Sign in before managing billing.' }, 401);

    const admin = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    );
    const { data: entitlement } = await admin
      .from('eden_access_entitlements')
      .select('stripe_customer_id')
      .eq('user_id', user.id)
      .maybeSingle();
    if (!entitlement?.stripe_customer_id) {
      return json({ error: 'No Stripe subscription was found for this account.' }, 404);
    }

    const { return_url } = await request.json();
    const allowedOrigin = Deno.env.get('EDEN_SITE_ORIGIN')!;
    const safeReturnUrl = new URL(return_url || allowedOrigin);
    if (safeReturnUrl.origin !== allowedOrigin) return json({ error: 'Invalid return URL.' }, 400);

    const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY')!);
    const session = await stripe.billingPortal.sessions.create({
      customer: entitlement.stripe_customer_id,
      return_url: safeReturnUrl.toString()
    });
    return json({ url: session.url });
  } catch (error) {
    console.error(error);
    return json({ error: 'Billing management is temporarily unavailable.' }, 500);
  }
});
