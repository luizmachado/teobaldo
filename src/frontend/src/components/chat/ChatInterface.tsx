"use client";

import { useState, useCallback } from "react";
import type { Message } from "@/lib/types";
import { useAuth } from "@/hooks/useAuth";
import { MessageList } from "./MessageList";
import { MessageInput } from "./MessageInput";
import { useToast } from "@/hooks/use-toast";
import { LogOut, Bot } from 'lucide-react';
import { Button } from "@/components/ui/button";

const API_BASE_URL = 'http://localhost:8000/api/v1';

export function ChatInterface() {
  const { token, documento, logout } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [threadId, setThreadId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleSendMessage = useCallback(async (content: string) => {
    if (!documento || !token) {
      toast({
        variant: "destructive",
        title: "Erro de Autenticação",
        description: "Você não está autenticado.",
      });
      return;
    }

    const userMessage: Message = { id: crypto.randomUUID(), role: 'user', content };
    const loadingMessage: Message = { id: crypto.randomUUID(), role: 'loading', content: "" };
    
    setMessages((prev) => [...prev, userMessage, loadingMessage]);
    setIsLoading(true);

    const payloadThreadId = threadId ?? undefined;


    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          user_id: documento,
          message: content,
          thread_id: payloadThreadId,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: "Ocorreu um erro na comunicação com o servidor." }));
        throw new Error(errorData.detail || "Resposta de erro inválida do servidor.");
      }
      
      const data = await response.json();
      
      if(data.thread_id && !threadId) {
        setThreadId(data.thread_id);
      }

      const aiMessage: Message = { 
        id: crypto.randomUUID(), 
        role: 'ai', 
        content: data.response,
        embed_map_url: data.embed_map_url,
      };
      
      setMessages((prev) => [...prev.slice(0, -1), aiMessage]);

    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Erro na Conversa",
        description: error.message || "Não foi possível obter uma resposta.",
      });
      setMessages((prev) => prev.slice(0, -1)); // Remove loading indicator on error
    } finally {
      setIsLoading(false);
    }
  }, [documento, token, threadId, toast]);

  return (
    <div className="flex h-screen flex-col bg-background">
      <header className="flex items-center justify-between border-b bg-background p-3 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="relative">
            <Bot className="h-10 w-10 text-primary" />
            <span className="absolute bottom-0 right-0 block h-3 w-3 rounded-full bg-green-500 border-2 border-background ring-2 ring-green-500" />
          </div>
          <div>
            <h1 className="font-headline text-lg font-semibold">Teobaldo</h1>
            <p className="text-sm text-muted-foreground">Online</p>
          </div>
        </div>
        <Button variant="ghost" size="icon" onClick={logout}>
          <LogOut className="h-5 w-5" />
          <span className="sr-only">Sair</span>
        </Button>
      </header>
      <MessageList messages={messages} />
      <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
}
