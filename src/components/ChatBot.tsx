import { useState } from "react";
import { motion } from "framer-motion";
import { Send, Mic } from "lucide-react";
import { Input } from "../components/ui/input";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";

type Message = {
  text: string;
  sender: "user" | "bot";
};

// Fix for SpeechRecognition TypeScript error
const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

export default function ChatBot() {
  const [messages, setMessages] = useState<Message[]>([
    { text: "Hello! How can I assist you today?", sender: "bot" }
  ]);

  const [input, setInput] = useState<string>("");
  const [isListening, setIsListening] = useState<boolean>(false);

  const handleSend = async (text: string): Promise<void> => {
    if (!text.trim()) return;

    const newMessages: Message[] = [...messages, { text, sender: "user" }];
    setMessages(newMessages);
    setInput("");

    try {
      const response = await fetch("http://localhost:5000/gemini/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });

      const data: { response: string } = await response.json();
      setMessages(prevMessages => [...prevMessages, { text: data.response, sender: "bot" }]);

    } catch (error) {
      console.error("Error fetching Gemini response:", error);
    }
  };

  const startListening = () => {
    if (!SpeechRecognition) {
      alert("Speech recognition not supported in your browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.lang = "en-US";
    recognition.interimResults = false;

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
      handleSend(transcript);
    };
    

    recognition.start();
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100 p-4">
      <Card className="w-full max-w-md bg-white shadow-lg rounded-2xl overflow-hidden">
        <CardContent className="p-4 space-y-2 h-96 overflow-y-auto">
          {messages.map((msg, index) => (
            <motion.div 
              key={index} 
              initial={{ opacity: 0, y: 10 }} 
              animate={{ opacity: 1, y: 0 }} 
              transition={{ duration: 0.3 }}
              className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
            >
              <div className={`p-3 rounded-lg ${msg.sender === "user" ? "bg-blue-500 text-white" : "bg-gray-200 text-black"}`}>
                {msg.text}
              </div>
            </motion.div>
          ))}
        </CardContent>
        <div className="flex items-center p-2 border-t">
          <Input
            value={input}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInput(e.target.value)}
            placeholder="Type a message..."
            className="flex-grow border-none focus:ring-0"
          />
          <Button onClick={() => handleSend(input)} className="ml-2 bg-blue-500 text-white rounded-full p-2">
            <Send size={20} />
          </Button>
          <Button onClick={startListening} className={`ml-2 ${isListening ? "bg-red-500" : "bg-gray-300"} text-black rounded-full p-2`}>
            <Mic size={20} />
          </Button>
        </div>
      </Card>
    </div>
  );
}
