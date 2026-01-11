
import React, { useState, useRef, useEffect } from 'react';
// Correct import from @google/genai
import { GoogleGenAI } from '@google/genai';
import { X, Send, Bot, User, Loader2, Sparkles } from 'lucide-react';
import { Drill } from '../types';

interface AICoachProps {
  onClose: () => void;
  drills: Drill[];
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const AICoach: React.FC<AICoachProps> = ({ onClose, drills }) => {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: '你好！我是你的 AI 排球教练。我可以帮你制定训练计划，或解答有关技术动作的任何疑问。今天我们重点练什么？' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMsg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setIsLoading(true);

    try {
      // Correct initialization: Always use new GoogleGenAI({apiKey: process.env.API_KEY});
      const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
      // Correct model selection: gemini-3-flash-preview for general text tasks
      const model = 'gemini-3-flash-preview';
      
      const drillTitles = drills.map(d => d.title).join(', ');
      const systemInstruction = `你是一位专业的排球教练。你可以访问以下训练项目数据库：${drillTitles}。
      你的目标是帮助球员和教练提升水平。
      如果用户要求制定计划，请从列表中推荐 2-3 个具体的训练项目。
      回答应简洁、专业且具有鼓励性。
      请始终使用中文回答。
      使用 Markdown 格式化内容。`;

      // Correct usage: Call generateContent with both the model name and prompt/contents.
      const response = await ai.models.generateContent({
        model,
        contents: [...messages, { role: 'user', content: userMsg }].map(m => ({
          role: m.role === 'assistant' ? 'model' : 'user',
          parts: [{ text: m.content }]
        })),
        config: { systemInstruction }
      });

      // Correct usage: Access .text property directly (do not call text()).
      const aiText = response.text || "抱歉，我目前无法生成回复。请稍后再试。";
      setMessages(prev => [...prev, { role: 'assistant', content: aiText }]);
    } catch (error) {
      console.error('Gemini Error:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: "我的“教练大脑”连接出了一点小问题，请检查你的网络连接。" }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4">
      <div className="bg-white w-full max-w-2xl h-[80vh] rounded-3xl shadow-2xl flex flex-col overflow-hidden animate-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="bg-slate-900 p-6 text-white flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="bg-orange-500 p-2 rounded-xl">
              <Bot className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-bold text-lg leading-none">AI 排球教练</h3>
              <span className="text-xs text-slate-400 flex items-center gap-1 mt-1">
                <span className="w-2 h-2 bg-green-500 rounded-full"></span> 在线指导中
              </span>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-full transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Messages */}
        <div 
          ref={scrollRef}
          className="flex-grow overflow-y-auto p-6 space-y-6 bg-slate-50"
        >
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`flex gap-3 max-w-[85%] ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                  msg.role === 'user' ? 'bg-orange-100 text-orange-600' : 'bg-slate-900 text-white'
                }`}>
                  {msg.role === 'user' ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
                </div>
                <div className={`p-4 rounded-2xl text-sm leading-relaxed shadow-sm ${
                  msg.role === 'user' 
                    ? 'bg-orange-600 text-white rounded-tr-none' 
                    : 'bg-white text-slate-700 rounded-tl-none border border-slate-100'
                }`}>
                  <div className="prose prose-sm prose-slate break-words">
                    {msg.content}
                  </div>
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin text-orange-500" />
                <span className="text-sm text-slate-500">教练正在思考中...</span>
              </div>
            </div>
          )}
        </div>

        {/* Suggestions */}
        <div className="px-6 py-2 bg-slate-50 flex gap-2 overflow-x-auto no-scrollbar">
          <button 
            onClick={() => setInput("帮我制定一个30分钟的入门热身和基础训练计划")}
            className="flex-shrink-0 px-4 py-1.5 bg-white border border-slate-200 rounded-full text-xs font-semibold text-slate-600 hover:border-orange-500 hover:text-orange-600 transition-colors"
          >
            30分钟计划
          </button>
          <button 
            onClick={() => setInput("如何提升我的扣球爆发力？")}
            className="flex-shrink-0 px-4 py-1.5 bg-white border border-slate-200 rounded-full text-xs font-semibold text-slate-600 hover:border-orange-500 hover:text-orange-600 transition-colors"
          >
            提升扣球
          </button>
          <button 
            onClick={() => setInput("推荐几个适合在家里练习的控球项目")}
            className="flex-shrink-0 px-4 py-1.5 bg-white border border-slate-200 rounded-full text-xs font-semibold text-slate-600 hover:border-orange-500 hover:text-orange-600 transition-colors"
          >
            居家控球
          </button>
        </div>

        {/* Input */}
        <div className="p-6 bg-white border-t border-slate-100">
          <div className="relative">
            <input 
              type="text"
              placeholder="向 AI 教练提问..."
              className="w-full pl-4 pr-12 py-3 bg-slate-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 transition-all text-sm"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            />
            <button 
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 disabled:opacity-50 disabled:hover:bg-orange-600 transition-colors"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AICoach;
