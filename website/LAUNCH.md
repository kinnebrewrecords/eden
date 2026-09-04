# Eden 1.0 launch runbook

The public offer is $199/month with a 14-day Stripe trial. Do not publish the
1.0 purchase buttons until every gate below is complete.

## 1. Stripe

1. Create the Eden 1.0 recurring product and a USD $199/month price.
2. Configure a 14-day trial on the price/checkout policy.
3. Enable the Stripe Customer Portal with payment-method updates and
   cancellation at period end.
4. Keep test mode enabled until the full test journey passes.

## 2. Supabase billing

1. Run `supabase/billing_schema.sql` after the existing beta access schema.
2. Deploy `create-checkout-session`, `create-portal-session`, and
   `stripe-webhook` Edge Functions.
3. Set these Edge Function secrets:
   - `STRIPE_SECRET_KEY`
   - `STRIPE_PRICE_ID`
   - `STRIPE_WEBHOOK_SECRET`
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `EDEN_SITE_ORIGIN` (scheme and hostname only; no trailing slash)
4. Register the Stripe webhook endpoint for:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
5. Do not expose the Stripe secret key, webhook secret, or Supabase
   service-role key in website files.

## 3. Required test journey

- Create and confirm a brand-new account.
- Start checkout and complete the trial subscription with a Stripe test card.
- Confirm Eden access activates automatically.
- Open the Streamlit app and complete onboarding.
- Create a project, build an estimate, add supplier prices and labor, and save.
- Generate and visually inspect the internal cost sheet, proposal, material
  list, and change order.
- Sign out, sign back in, and restore the same cloud workspace.
- Open the billing portal, cancel, and confirm access remains through the paid
  period and becomes inactive on the correct webhook event.
- Verify an account without access can still export recovery data but cannot
  enter the workspace.

## 4. Owner checks

- Replace the Gmail support address with a domain address when available.
- Have a qualified attorney review Terms, Privacy, Refunds, and the estimating
  disclaimer for the operating jurisdiction and legal entity.
- Confirm the policy dates and business identity before publishing.
- Configure uptime/error alerts for the website, app, Edge Functions, Stripe
  webhooks, and Supabase.
- Verify Supabase backups and perform one recovery drill.
- Keep the current site archive as rollback material.

## 5. Release gate

Move Stripe to live mode only after the test journey passes twice with two
different accounts. Repeat once in live mode using a real purchase, issue the
refund if appropriate, then tag the application and archive the exact website
bundle that was published.
