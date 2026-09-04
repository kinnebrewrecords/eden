-- Eden 1.0 billing fields. Run after beta_access.sql.
alter table public.eden_access_entitlements
    add column if not exists stripe_customer_id text unique,
    add column if not exists stripe_subscription_id text unique,
    add column if not exists current_period_end timestamptz;

create index if not exists eden_access_stripe_customer_idx
    on public.eden_access_entitlements (stripe_customer_id);

-- Billing writes use the service-role key inside verified Edge Functions.
-- Browser clients retain read-only access through the existing RLS policy.
