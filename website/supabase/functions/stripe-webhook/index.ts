import Stripe from 'npm:stripe@18.5.0';
import { createClient } from 'jsr:@supabase/supabase-js@2';

const activeStatuses = new Set(['active', 'trialing']);

function periodEnd(subscription: Stripe.Subscription) {
  const seconds = subscription.items.data[0]?.current_period_end
    || subscription.trial_end
    || subscription.billing_cycle_anchor;
  return new Date(seconds * 1000).toISOString();
}

Deno.serve(async (request) => {
  if (request.method !== 'POST') return new Response('Method not allowed', { status: 405 });
  const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY')!);
  const signature = request.headers.get('stripe-signature');
  if (!signature) return new Response('Missing signature', { status: 400 });

  let event: Stripe.Event;
  try {
    event = await stripe.webhooks.constructEventAsync(
      await request.text(), signature, Deno.env.get('STRIPE_WEBHOOK_SECRET')!
    );
  } catch (error) {
    console.error(error);
    return new Response('Invalid signature', { status: 400 });
  }

  const admin = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  );

  try {
    if (event.type === 'checkout.session.completed') {
      const session = event.data.object as Stripe.Checkout.Session;
      const userId = session.client_reference_id;
      if (!userId || !session.subscription || !session.customer) {
        throw new Error('Checkout session is missing Eden account metadata.');
      }
      const subscription = await stripe.subscriptions.retrieve(String(session.subscription));
      const { error } = await admin.from('eden_access_entitlements').upsert({
        user_id: userId,
        access_type: 'subscription',
        status: activeStatuses.has(subscription.status) ? 'active' : 'inactive',
        beta_code_id: null,
        stripe_customer_id: String(session.customer),
        stripe_subscription_id: subscription.id,
        current_period_end: periodEnd(subscription),
        access_expires_at: null,
        updated_at: new Date().toISOString()
      });
      if (error) throw error;
    }

    if (event.type === 'customer.subscription.updated' || event.type === 'customer.subscription.deleted') {
      const subscription = event.data.object as Stripe.Subscription;
      const { error } = await admin.from('eden_access_entitlements').update({
        status: activeStatuses.has(subscription.status) ? 'active' : 'inactive',
        current_period_end: periodEnd(subscription),
        updated_at: new Date().toISOString()
      }).eq('stripe_subscription_id', subscription.id);
      if (error) throw error;
    }
    return new Response('ok', { status: 200 });
  } catch (error) {
    console.error(error);
    return new Response('Webhook processing failed', { status: 500 });
  }
});
