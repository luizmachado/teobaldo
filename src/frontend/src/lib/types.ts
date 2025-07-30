export interface Message {
  id: string;
  role: 'user' | 'ai' | 'loading';
  content: string;
}
