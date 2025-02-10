// The header provides branding and navigation
export default function Header() {
    return (
      <header className="border-b bg-white">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Stethoscope className="h-6 w-6 text-primary" />
            <h1 className="text-xl font-bold text-primary">Care Connect</h1>
          </div>
          <p className="text-sm text-muted-foreground">
            Your AI Medical Information Guide
          </p>
        </div>
      </header>
    );
  }
  ```
  
  ### 2. Home Page (home.tsx)
  ```tsx
  export default function Home() {
    return (
      <div className="max-w-4xl mx-auto space-y-8">
        <section className="text-center space-y-4">
          <h1 className="text-4xl font-bold text-primary">
            Welcome to Care Connect
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Get reliable medical information and guidance from our AI assistant.
          </p>
        </section>
  
        {/* Feature Cards */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <Card>
            <CardContent className="p-6 space-y-2">
              <h3 className="font-semibold text-lg">Professional Guidance</h3>
              <p className="text-muted-foreground">
                Get clear explanations and understand when to seek professional help.
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6 space-y-2">
              <h3 className="font-semibold text-lg">Medical Information</h3>
              <p className="text-muted-foreground">
                Access reliable medical information and explanations of medical terms.
              </p>
            </CardContent>
          </Card>
        </div>
  
        <ChatInterface />
      </div>
    );
  }
  ```
  
  ### 3. Chat Interface (chat-interface.tsx)
  ```tsx
  export default function ChatInterface() {
    const [input, setInput] = useState("");
    const { toast } = useToast();
  
    // Fetch messages using React Query
    const { data: messages = [], isLoading } = useQuery<Message[]>({
      queryKey: ["/api/messages"],
    });
  
    // Handle message submission
    const mutation = useMutation({
      mutationFn: async (message: string) => {
        const res = await apiRequest("POST", "/api/chat", { message });
        return res.json();
      },
      onSuccess: () => {
        setInput("");
        queryClient.invalidateQueries({ queryKey: ["/api/messages"] });
      },
    });
  
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Chat with Care Connect Assistant</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <ScrollArea className="h-[400px] p-4 border rounded-lg">
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
          </ScrollArea>
  
          <form onSubmit={handleSubmit} className="flex gap-2">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your medical question here..."
              className="flex-1"
            />
            <Button type="submit" disabled={mutation.isPending}>
              Send
            </Button>
          </form>
        </CardContent>
      </Card>
    );
  }
  ```
  
  ### 4. Chat Message Component (chat-message.tsx)
  ```tsx
  export default function ChatMessage({ message }: ChatMessageProps) {
    const isAI = message.role === "assistant";
  
    return (
      <div className={`flex gap-3 ${isAI ? "flex-row" : "flex-row-reverse"}`}>
        <div className="flex-shrink-0">
          {isAI ? (
            <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
              <Bot className="h-5 w-5 text-primary-foreground" />
            </div>
          ) : (
            <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center">
              <User className="h-5 w-5 text-secondary-foreground" />
            </div>
          )}
        </div>
  
        <Card className={`flex-1 ${isAI ? "bg-primary/5" : "bg-secondary/5"}`}>
          <CardContent className="p-4">
            <p className="text-sm">{content}</p>
            {isAI && disclaimer && (
              <p className="text-xs text-muted-foreground mt-2">{disclaimer}</p>
            )}
          </CardContent>
        </Card>
      </div>
    );
  }