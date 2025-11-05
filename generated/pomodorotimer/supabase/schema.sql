-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- Items table
create table if not exists items (
  id uuid primary key default uuid_generate_v4(),
  content text not null,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Enable Row Level Security
alter table items enable row level security;

-- Policy: Anyone can read items
create policy "Items are viewable by everyone"
  on items for select
  using (true);

-- Policy: Anyone can insert items (adjust for auth later)
create policy "Items are insertable by everyone"
  on items for insert
  with check (true);

-- Policy: Anyone can delete their items (adjust for auth later)
create policy "Items are deletable by everyone"
  on items for delete
  using (true);

-- Indexes
create index if not exists items_created_at_idx on items(created_at desc);
