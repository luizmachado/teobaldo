import type { Message } from "@/lib/types";
import { cn } from "@/lib/utils";
import { Bot, User } from "lucide-react";
import { TypingIndicator } from "./TypingIndicator";
import ReactMarkdown from 'react-markdown';

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';
  const isLoading = message.role === 'loading';

  const bubbleClasses = cn(
    "flex w-fit max-w-xs md:max-w-md lg:max-w-lg flex-col items-start gap-2 rounded-2xl px-4 py-3 text-white animate-slide-in-bottom",
    isUser ? "ml-auto rounded-br-none bg-primary" : "mr-auto rounded-bl-none bg-accent",
    isLoading && "bg-muted p-2"
  );
  
  const iconClasses = "flex h-8 w-8 items-center justify-center rounded-full text-white";

  return (
    <div className={cn("flex items-start gap-3", isUser && "flex-row-reverse")}>
       <div className={cn(iconClasses, isUser ? "bg-accent" : "bg-primary")}>
        {isUser ? <User size={20} /> : <Bot size={20} />}
      </div>
      <div className={bubbleClasses} style={{ animationFillMode: 'backwards' }}>
        {isLoading ? (
          <TypingIndicator />
        ) : (
          <>
            {/* 2. Substitua o <p> pelo componente ReactMarkdown */}
            <div className="prose prose-invert text-primary-foreground max-w-none">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
            
            {message.embed_map_url && (
              <div className="mt-2 w-full overflow-hidden rounded-lg border">
                <iframe
                  src={message.embed_map_url}
                  width="100%"
                  height="300"
                  style={{ border: 0 }}
                  allowFullScreen={false}
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                  title="Mapa da rota"
                ></iframe>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
