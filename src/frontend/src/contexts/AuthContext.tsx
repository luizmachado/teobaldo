"use client";

import type { ReactNode } from 'react';
import { createContext, useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { useToast } from "@/hooks/use-toast";

const API_BASE_URL = 'http://localhost:8000/api/v1/auth';

interface AuthContextType {
  token: string | null;
  documento: string | null;
  isLoading: boolean;
  login: (documento: string) => Promise<void>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [documento, setDocumento] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const { toast } = useToast();

  useEffect(() => {
    try {
      const storedToken = localStorage.getItem('token');
      const storedDocumento = localStorage.getItem('documento');
      if (storedToken && storedDocumento) {
        setToken(storedToken);
        setDocumento(storedDocumento);
      }
    } catch (error) {
      console.error("Failed to access localStorage", error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const login = useCallback(async (doc: string) => {
    setIsLoading(true);
    try {
      const params = new URLSearchParams();
      params.append('username', doc);
      params.append('password', doc);

      const response = await fetch(`${API_BASE_URL}/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: params,
      });

      if (!response.ok) {
        throw new Error('Falha na autenticação. Verifique seu documento.');
      }

      const data = await response.json();
      const { access_token } = data;
      console.log('Token recebido:', access_token);


      setToken(access_token);
      setDocumento(doc);
      localStorage.setItem('token', access_token);
      localStorage.setItem('documento', doc);
      router.replace('/chat');
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Erro de Login",
        description: error.message || "Ocorreu um erro desconhecido.",
      });
      setToken(null);
      setDocumento(null);
      localStorage.removeItem('token');
      localStorage.removeItem('documento');
    } finally {
      setIsLoading(false);
    }
  }, [router, toast]);

  const logout = useCallback(() => {
    setToken(null);
    setDocumento(null);
    localStorage.removeItem('token');
    localStorage.removeItem('documento');
    router.replace('/login');
  }, [router]);

  const value = { token, documento, isLoading, login, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

