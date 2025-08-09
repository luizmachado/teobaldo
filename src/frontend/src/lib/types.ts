export interface Message {
  id: string;
  role: 'user' | 'ai' | 'loading';
  content: string;
  embed_map_url?: string;
}
