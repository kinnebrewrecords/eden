-- Eden 1.0 cloud workspace storage
-- Run this entire file once in Supabase: SQL Editor > New query > Run.

create table if not exists public.eden_workspaces (
    user_id uuid primary key references auth.users(id) on delete cascade,
    state jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

alter table public.eden_workspaces enable row level security;

drop policy if exists "Users can read their own Eden workspace"
    on public.eden_workspaces;
create policy "Users can read their own Eden workspace"
    on public.eden_workspaces
    for select
    to authenticated
    using ((select auth.uid()) = user_id);

drop policy if exists "Users can create their own Eden workspace"
    on public.eden_workspaces;
create policy "Users can create their own Eden workspace"
    on public.eden_workspaces
    for insert
    to authenticated
    with check ((select auth.uid()) = user_id);

drop policy if exists "Users can update their own Eden workspace"
    on public.eden_workspaces;
create policy "Users can update their own Eden workspace"
    on public.eden_workspaces
    for update
    to authenticated
    using ((select auth.uid()) = user_id)
    with check ((select auth.uid()) = user_id);

-- Keep the last-updated timestamp accurate on each cloud save.
create or replace function public.set_eden_workspace_updated_at()
returns trigger
language plpgsql
as $$
begin
    new.updated_at = now();
    return new;
end;
$$;

drop trigger if exists eden_workspace_updated_at
    on public.eden_workspaces;
create trigger eden_workspace_updated_at
before update on public.eden_workspaces
for each row
execute function public.set_eden_workspace_updated_at();
