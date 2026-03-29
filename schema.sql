-- Table: conversations
CREATE TABLE IF NOT EXISTS public.conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title TEXT,
    business_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table: messages
CREATE TABLE IF NOT EXISTS public.messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES public.conversations(id) ON DELETE CASCADE,
    role TEXT NOT NULL, -- 'user', 'assistant'
    content TEXT NOT NULL,
    extras JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Storage bucket 'logos' (must be created manually in Supabase UI or using a policy)
-- Enabling row-level security (optional but recommended)
ALTER TABLE public.conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;

-- Add RLS policies for conversations
CREATE POLICY "Users can only see their own conversations" 
ON public.conversations FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own conversations"
ON public.conversations FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Add RLS policies for messages (requires join with conversations)
CREATE POLICY "Users can only see messages in their conversations"
ON public.messages FOR SELECT
USING (EXISTS (
    SELECT 1 FROM public.conversations 
    WHERE public.conversations.id = public.messages.conversation_id 
    AND public.conversations.user_id = auth.uid()
));

CREATE POLICY "Users can insert messages into their conversations"
ON public.messages FOR INSERT
WITH CHECK (EXISTS (
    SELECT 1 FROM public.conversations 
    WHERE public.conversations.id = public.messages.conversation_id 
    AND public.conversations.user_id = auth.uid()
));
