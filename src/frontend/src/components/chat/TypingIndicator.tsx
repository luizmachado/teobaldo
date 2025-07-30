import { cn } from "@/lib/utils";

export function TypingIndicator() {
  return (
    <div className="flex items-center space-x-1 p-2">
      <span className="sr-only">Teobaldo está digitando...</span>
      <div className={cn("h-2 w-2 animate-[bounce_1s_infinite] rounded-full bg-muted-foreground")} />
      <div className={cn("h-2 w-2 animate-[bounce_1s_infinite_200ms] rounded-full bg-muted-foreground [animation-delay:200ms]")} />
      <div className={cn("h-2 w-2 animate-[bounce_1s_infinite_400ms] rounded-full bg-muted-foreground [animation-delay:400ms]")} />
    </div>
  );
}
