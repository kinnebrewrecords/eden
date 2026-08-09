-- Eden beta access codes
-- Run this once in Supabase: SQL Editor > New query > Run.
-- Then create your private codes with the example INSERT at the bottom.

create table if not exists public.eden_beta_access_codes (
    id bigint generated always as identity primary key,
    code text not null unique,
    label text not null default 'Beta tester',
    active boolean not null default true,
    max_redemptions integer not null default 1 check (max_redemptions > 0),
    redemption_count integer not null default 0 check (redemption_count >= 0),
    expires_at timestamptz,
    created_at timestamptz not null default now()
);

create table if not exists public.eden_access_entitlements (
    user_id uuid primary key references auth.users(id) on delete cascade,
    access_type text not null check (access_type in ('beta', 'subscription')),
    status text not null default 'active' check (status in ('active', 'inactive')),
    beta_code_id bigint references public.eden_beta_access_codes(id),
    access_expires_at timestamptz,
    updated_at timestamptz not null default now()
);

alter table public.eden_beta_access_codes enable row level security;
alter table public.eden_access_entitlements enable row level security;

-- Nobody using the public website key can read the private code list.
drop policy if exists "Users can read their own Eden access" on public.eden_access_entitlements;
create policy "Users can read their own Eden access"
    on public.eden_access_entitlements
    for select to authenticated
    using ((select auth.uid()) = user_id);

create or replace function public.redeem_eden_beta_code(p_code text)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
    beta_code public.eden_beta_access_codes%rowtype;
begin
    if auth.uid() is null then
        raise exception 'Sign in before redeeming a beta code.';
    end if;

    select * into beta_code
    from public.eden_beta_access_codes
    where upper(code) = upper(trim(p_code))
      and active = true
    for update;

    if not found
       or (beta_code.expires_at is not null and beta_code.expires_at <= now())
       or beta_code.redemption_count >= beta_code.max_redemptions then
        raise exception 'This beta code is invalid, expired, or already used.';
    end if;

    insert into public.eden_access_entitlements (
        user_id, access_type, status, beta_code_id, access_expires_at, updated_at
    ) values (
        auth.uid(), 'beta', 'active', beta_code.id, beta_code.expires_at, now()
    )
    on conflict (user_id) do update set
        access_type = 'beta',
        status = 'active',
        beta_code_id = excluded.beta_code_id,
        access_expires_at = excluded.access_expires_at,
        updated_at = now();

    update public.eden_beta_access_codes
    set redemption_count = redemption_count + 1
    where id = beta_code.id;

    return jsonb_build_object(
        'has_access', true,
        'access_type', 'beta',
        'access_expires_at', beta_code.expires_at
    );
end;
$$;

create or replace function public.get_eden_access()
returns jsonb
language sql
stable
security invoker
set search_path = public
as $$
    select coalesce(
        (
            select jsonb_build_object(
                'has_access', true,
                'access_type', access_type,
                'access_expires_at', access_expires_at
            )
            from public.eden_access_entitlements
            where user_id = auth.uid()
              and status = 'active'
              and (access_expires_at is null or access_expires_at > now())
        ),
        jsonb_build_object('has_access', false)
    );
$$;

grant execute on function public.redeem_eden_beta_code(text) to authenticated;
grant execute on function public.get_eden_access() to authenticated;

-- Create one private code at a time. Change the code before running this.
-- Keep this command private; do not put real codes in your website files.
-- insert into public.eden_beta_access_codes (code, label, max_redemptions)
-- values ('CHANGE-THIS-TO-A-LONG-PRIVATE-CODE', 'First beta tester', 1);
